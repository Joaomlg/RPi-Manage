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
        regex = r'NAME="(.*)"'
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

    def access_point(self, name, radio, encryption='none', network='wlan', firewall_zone='lan'):
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
            if 'name' in info and info['name'] == firewall_zone:
                netwrk = info['network']
                if network not in netwrk:
                    netwrk += ' ' + network
                    uci.firewall.zone.update(zone, network=netwrk)

        # Remove wireless from current radio
        for wireless in uci.wireless.read_all():
            info = uci.wireless.read(wireless)
            if 'device' in info and info['device'] == radio:
                uci.wireless.remove(wireless)

        # Create AccessPoint
        uci.wireless.create('cfg033579', device=radio, encryption=encryption, mode='ap', network=network, ssid=name)

    def scan_wireless(self, interface):
        '''Function to scan wireless'''

        self.update()
        if interface not in self.__interface:
            raise NameError('Interface \'%s\' not found!' % interface)
        
        wireless = []
        
        if self.system == 'OpenWrt':
            command = 'iwinfo %s scan' % interface

            regex = {'ssid': r'ESSID: \"(.*)\"',
            'address': r'Address: ([a-zA-Z0-9:]*)',
            'channel': r'Channel: ([0-9]*)',
            'signal': r'Signal: (-[0-9]*) dBm',
            'encryption': r'Encryption: ([a-zA-Z0-9/\s]*)'}
            
            response = os.popen(command).read()
            if len(response):
                response = response.split('\n\n')
                for item in response:
                    cell = {}
                    for key, regx in regex.items():
                        find = re.search(regx, item)
                        if find is not None:
                            cell[key] = find.group(1)
                        else:
                            break
                    else:
                        wireless.append(wifi_cell(**cell))
        else:
            command = "sudo iwlist %s scan | egrep 'ESSID|Encryption|Address|Channel|Signal'" % interface

            regex = {'ssid': r'ESSID:\"(.*)\"',
            'address': r'Address: ([a-zA-Z:]*)',
            'channel': r'Channel:([0-9]*)',
            'signal': r'Signal level=(-[0-9]*) dBm',
            'encryption': r'Encryption key:([a-zA-Z]*)'}

            response = os.popen(command).read()
            if len(response):
                response = response.split('Cell')
                for item in response:
                    cell = {}
                    for key, regx in regex.items():
                        find = re.search(regx, item)
                        if find is not None:
                            cell[key] = find.group(1)
                        else:
                            break
                    else:
                        wireless.append(wifi_cell(**cell))
        
        # Sort wireless by signal
        if len(wireless):
            for i in range(len(wireless)):
                for j in range(i, len(wireless)):
                    if wireless[i].signal < wireless[j].signal:
                        wireless[i], wireless[j] = wireless[j], wireless[i]
        
        return wireless
    
    def connect_wireless(self, ssid, encryption, password, channel, radio='radio0', network='wwan', firewall_zone='lan'):
        '''Function to connect to a wireless.'''

        if self.system == 'OpenWrt':
            # Creating network if not exist
            if network not in uci.network.read_all():
                uci.network.dhcp.create(network)
            
            # Setting radio channel if necessary
            if uci.wireless.read(radio)['channel'] != channel:
                uci.wireless.update(radio, channel=channel)
            
            # Setting firewall if necessary
            for zone in uci.firewall.zone.read_all():
                info = uci.firewall.zone.read(zone)
                if 'name' in info and info['name'] == firewall_zone:
                    netwrk = info['network']
                    if network not in netwrk:
                        netwrk += ' ' + network
                        uci.firewall.zone.update(zone, network=netwrk)

            # Remove wireless from current radio
            for wireless in uci.wireless.read_all():
                info = uci.wireless.read(wireless)
                if 'device' in info and info['device'] == radio:
                    uci.wireless.remove(wireless)
            
            # Create connection
            uci.wireless.create('cfg033579', ssid=ssid, device=radio, encryption=encryption, key=password, mode='sta', network=network)

        else:
            command = "nmcli d wifi connect '%s' password '%s'" % (ssid, password)
            os.popen(command)

    def wireless_connection(self, interface):
        '''Function to check wireless connection and return True or False.'''

        self.update()
        if interface not in self.__interface:
            raise NameError('Interface \'%s\' not found!' % interface)

        command = 'cat /sys/class/net/%s/operstate' % interface
        response = os.popen(command).read()

        if 'up' in response:
            return True
        return False
    
    @staticmethod
    def internet_connection():
        '''Function to check internet connection and return True or False.'''

        command = 'ping -q -w1 -c1 google.com &>/dev/null && echo True || echo False'
        response = os.popen(command).read()

        return bool(response)
    
    def get_localIp(self, interface):
        '''Function to get and return local ip.'''

        self.update()
        if interface not in self.__interface:
            raise NameError('Interface \'%s\' not found!' % interface)
        
        command = "echo `ifconfig %s 2>/dev/null|awk '/inet (addr:)?/ {{print $2}}'|sed 's/addr://'`" % interface
        response = os.popen(command).read()

        return response.replace('\n', '')
    
    def get_externalIp(self):
        '''Function to get and return external ip.'''
        
        if not self.internet_connection():
            raise OSError('Internet connection error!')
        
        import urllib.request

        try:
            response = urllib.request.urlopen('https://ipinfo.io/ip').read()
            response = response.decode('utf-8').replace('\n', '')
        except Exception as e:
            print(e)
        else:
            return response
        
        return None

# Struct for wifi cell
class wifi_cell:
    def __init__(self, ssid, address, encryption, channel, signal):
        self.ssid = str(ssid)
        self.address = str(address)
        self.encryption = self.__set_encryption(encryption)
        self.security = self.__set_security(encryption)
        self.channel = int(channel)
        self.signal = int(signal)
    
    def get_signal_force(self):
        '''Return signal force in 0-5 range'''
        force = {-49: 5, -66: 4, -75: 3, -85: 2, -91: 1}

        for key in force:
            if int(self.signal) > key:
                return force[key]

        return 0
    
    @staticmethod
    def __set_encryption(encryption):
        types = {'mixed': 'psk-mixed', 'wpa2': 'psk2','wpa': 'psk', 'wep': 'wep'}
        
        for t in types:
            if t in encryption.lower():
                return types[t]

        if 'on' in encryption.lower():
            return 'on'

        return 'none'

    @staticmethod
    def __set_security(encryption):
        if encryption == 'none':
            return False
        return True
