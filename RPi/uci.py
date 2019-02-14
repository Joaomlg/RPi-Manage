import os
import re

class uci_command:
    def __init__(self):
        self.__config = None
        self.__type = None

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
        length = None

        if type(args) is str:
            length = 1
            args = [args]
        elif type(args) is list or type(args) is tuple:
            length = len(args)
        else:
            raise TypeError('args deve ser str, list ou tuple')
        
        for i in range(length):
            os.popen('uci delete ' + self.__config + '.' + args[i])
        
        os.popen('uci commit ' + self.__config)
        os.popen('wifi')

    def remove_all(self):
        ls = self.read_all()
        ls.remove('radio0')  # Don't remove radio0 !
        for i in ls:
            self.remove(i)

class Wireless(uci_command):
    def __init__(self):
        super().__init__()
        self.__config = 'wireless'
        self.__type = 'wifi-iface'

class Network(uci_command):
    def __init__(self):
        super().__init__()
        self.__config = 'network'
        self.__type = 'interface'

class Firewall(uci_command):
    def __init__(self, _type):
        '''Type can: dafaults, zone, rule, forwarding'''
        super().__init__()
        self.__config = 'firewall'
        self.__type = _type

class Dhcp(uci_command):
    def __init__(self):
        super().__init__()
        self.__config = 'dhcp'
        self.__type = 'dhcp'