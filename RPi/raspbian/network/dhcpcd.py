import os
import re

def create_interface(iface_name, *args, **kwargs):
    configs = ('ip_address', 'ip6_address', 'routers', 'domain_name_servers')
    with open('/etc/dhcpcd.conf', 'a') as file:
        file.write('\n# Start interface ' + str(iface_name) + ' (required for RPi-Manage python\'s lib)\n')
        file.write('interface ' + str(iface_name) + '\n')
        for key, value in kwargs.items():
            if key in configs:
                file.write('static ' + str(key) + '=' + str(value) + '\n')
        for extra_config in args:
            file.write(str(extra_config) + '\n')
        file.write('# End interface\n')

def read_interface():
    interfaces = []
    with open('/etc/dhcpcd.conf') as file:
        for line in file:
            if 'Start interface' in line:
                regex = r'interface ([a-zA-Z0-9]*)'
                result = re.search(regex, file.readline())
                if result:
                    new_interface = {'iface': result.group(1)}
                    regex = r'(ip_address|ip6_address|routers|domain_name_servers)=(.*)\n'
                    for i_line in file:
                        if 'End interface' in i_line:
                            break
                        result = re.search(regex, i_line)
                        if result and len(result.groups()) == 2:
                            new_interface[result.group(1)] = result.group(2)
                    interfaces.append(new_interface)
    return interfaces

def read_interface_by_name(iface_name):
    interfaces = read_interface()

    for iface in interfaces:
        if iface['iface'] == iface_name:
            return iface
    
    return None

def delete_interface(iface_name):
    file_text = ''
    with open('/etc/dhcpcd.conf') as file:
        for line in file:
            if 'Start interface' in line:
                regex = r'interface ([a-zA-Z0-9]*)'
                iface = re.search(regex, line)
                if iface:
                    if iface_name == iface.group(1):
                        while 'End interface' not in file.readline():
                            pass
                        continue
            file_text += line
    
    with open('/etc/dhcpcd.conf', 'w') as file:
        file.write(file_text)
                