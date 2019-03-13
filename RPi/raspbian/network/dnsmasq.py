import re

def create(iface_name, dhcp_init, dhcp_end, subnet_mask, lease_time):
    with open('/etc/dnsmasq.conf', 'a') as file:
        file.write('\n# Start interface ' + str(iface_name) + ' (required for RPi-Manage python\'s lib)\n')
        file.write('interface=' + str(iface_name) + '\n')
        dhcp_range = '{},{},{},{}'.format(dhcp_init, dhcp_end, subnet_mask, lease_time)
        file.write('dhcp-range=' + dhcp_range + '\n')
        file.write('# End interface\n')

def read():
    interfaces = []
    with open('/etc/dnsmasq.conf') as file:
        for line in file:
            if 'Start interface' in line:
                regex = r'interface=([a-zA-Z0-9]*)'
                result = re.search(regex, file.readline())
                if result:
                    new_interface = {'iface': result.group(1)}
                    regex = r'dhcp-range=(.*)\n'
                    for i_line in file:
                        if 'End interface' in i_line:
                            break
                        result = re.search(regex, i_line)
                        if result:
                            result = result.group(1).replace('\n', '')
                            new_interface['dhcp_init'], new_interface['dhcp_end'], new_interface['subnet_mask'], new_interface['lease_time'] = result.split(',')
                    interfaces.append(new_interface)
    return interfaces

def read_by_name(iface_name):
    interfaces = read()

    for iface in interfaces:
        if iface['iface'] == iface_name:
            return iface
    
    return None

def delete_interface(iface_name):
    file_text = ''
    with open('/etc/dnsmasq.conf') as file:
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
    
    with open('/etc/dnsmasq.conf', 'w') as file:
        file.write(file_text)
                