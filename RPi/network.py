import RPi.uci as uci
import os
import re

class Network:
    def __init__(self):
        self.__system = self.__set_system()
        self.__interface = self.__set_interface()
        self.__mode = self.__set_mode()
    
    @property
    def system(self):
        return self.__system
    
    @staticmethod
    def __set_system():
        command = 'cat /etc/os-release | grep \'NAME\''
        regex = r'NAME="([a-zA-Z\d]*)"'
        response = os.popen(command)
        try:
            system = re.search(regex, response.read())
            if system is not None:
                return system.group(1)
        except Exception as e:
            print(e)
        return None

    @property
    def interface(self):
        return self.__interface
    
    @staticmethod
    def __set_interface():
        command = 'iw dev | grep \'Interface\''
        regex = r'Interface ([a-zA-Z\d]*)'
        response = os.popen(command)
        interfaces = []
        try:
            for r in list(response):
                iface = re.search(regex, r)
                if iface is not None:
                    interfaces.append(iface.group(1))
        except Exception as e:
            print(e)
        return interfaces if len(interfaces) else None
    
    @property
    def mode(self):
        return self.__mode

    def __set_mode(self):
        command = 'iwinfo %s info | grep \'Mode\''
        regex = r'Mode: ([a-zA-Z]*)'
        mode = {}
        try:
            if self.interface is not None:
                for iface in self.interface:
                    response = os.popen(command % iface).read()
                    _mode = re.search(regex, response)
                    if _mode is not None:
                        mode[iface] = _mode.group(1)
        except Exception as e:
            print(e)
        return mode if len(mode) else None
    
    def update(self):
        self.__interface = self.__set_interface()
        self.__mode = self.__set_mode()
    
    def access_point(self, name, radio, network='wlan', encryption='none'):
        '''Function to create and start an access point'''

        # Creating network if not exist
        if 'wlan' not in uci.network.read_all():
            uci.network.create('wlan', ifname='wlan0', proto='static', ipaddr='192.168.22.1', netmask='255.255.255.0', type='bridge')

        # Setting dhcp for network if not exist
        if 'wlan' not in uci.dhcp.read_all():
            uci.dhcp.create('wlan', interface='wlan', leasetime='12h', limit='150', start='100')
        
        # Setting firewall if necessary
        for zone in uci.firewall.zone.read_all():
            info = uci.firewall.zone.read(zone)
            if 'name' in info and info['name'] == 'lan':
                network = info['network']
                if 'wlan' not in network:
                    network += ' wlan'
                    uci.firewall.zone.update(zone, network=network)
        
        # Remove wireless from current radio
        for wireless in uci.wireless.read_all():
            info = uci.wireless.read(wireless)
            if 'device' in info and info['device'] == radio:
                uci.wireless.remove(wireless)

        # Create AccessPoint
        uci.wireless.create('cfg033579', device=radio, encryption=encryption, mode='ap', network=network, ssid=name)

    def __check_interface(self, interface):
        self.__interface = self.__set_interface()
        if interface in self.__interface:
            return True
        return False

    def wireless_connection(self, interface):
        '''Function to check wireless connection'''

        command = 'cat /sys/class/net/%s/operstate' % interface
        response = os.popen(command).read()

        if 'up' in response:
            return True
        return False
    
    def internet_connection(self, interface):
        pass

# Testes
if __name__ == '__main__':
    n = Network()
    print(n.system)
    print(n.interface)
    print(n.mode)
    print(n.wireless_connection('wlp6s0'))