import os
import re

class _uci_command:
    def __init__(self, _config, _type):
        self.__config = _config
        self.__type = _type

    def create(self, name, **args):
        os.popen('uci set ' + self.__config + '.' + name + '=' + self.__type)
        for key, arg in args.items():
            if ' ' in arg:
                arg = '"%s"' % (arg)
            os.popen('uci set ' + self.__config + '.' + name  + '.' + key + '=' + arg)
        os.popen('uci commit ' + self.__config)
        os.popen('wifi')

    def read_all(self):
        ls = []
        resp = os.popen('uci show ' + self.__config).read().split('\n')
        for line in resp:
            regex = re.match(self.__config + r'\.([^\.=]*)', line)
            if regex is not None:
                if regex.group(1) not in ls:
                    ls.append(regex.group(1))
        return ls

    def read(self, name):
        dic = {}
        resp = os.popen('uci show ' + self.__config).read().split('\n')
        for line in resp:
            regex = re.match(self.__config + r'\.([^\.=]*)\.([^\.=]*)=([^\0]*)', line)
            if regex is not None:
                if regex.group(1) == name:
                    dic[regex.group(2)] = regex.group(3).replace('\'', '')
        return dic

    def update(self, name, **args):
        for key, arg in args.items():
            if ' ' in arg:
                arg = '"%s"' % (arg)
            os.popen('uci set ' + self.__config + '.' + name  + '.' + key + '=' + arg)
        os.popen('uci commit ' + self.__config)
        os.popen('wifi')

    def remove(self, args):
        if type(args) is str:
            args = [args]
        elif type(args) is list or type(args) is tuple:
            pass
        else:
            raise TypeError('args deve ser str, list ou tuple')
        
        for arg in args:
            os.popen('uci delete ' + self.__config + '.' + arg)
        
        os.popen('uci commit ' + self.__config)
        os.popen('wifi')

    def remove_all(self):
        all_elements = self.read_all()

        for element in all_elements:
            if 'radio' in element:
                all_elements.remove(element)  # Don't remove radios!
                
        self.remove(all_elements)

class __wireless(_uci_command):
    def __init__(self):
        super().__init__('wireless', 'wifi-iface')  

class __network(_uci_command):
    def __init__(self):
        super().__init__('network', 'interface')

class __firewall():
    def __init__(self):
        '''Type can: dafaults, zone, rule, forwarding'''
        self.defaults = _uci_command('firewall', 'defaults')
        self.zone = _uci_command('firewall', 'zone')
        self.rule = _uci_command('firewall', 'rule')
        self.forwarding = _uci_command('firewall', 'forwarding')

class __dhcp(_uci_command):
    def __init__(self):
        super().__init__('dhcp', 'dhcp')


wireless = __wireless()
network = __network()
firewall = __firewall()
dhcp = __dhcp()
