from string import Template
import os.path

def create(iface_name, ssid, password=None, channel=6, driver='nl80211'):
    file_content = ''

    current_path = os.path.dirname(__file__)
    with open(os.path.join(current_path, 'hostapd-example.conf')) as file:
        file_content = Template(file.read())
        file_content = str(file_content.safe_substitute(iface=iface_name, ssid=ssid, channel=channel, driver=driver))

        if password:
            file_content += '\nwpa_key_mgmt=WPA-PSK'
            file_content += '\nwpa=2'
            file_content += '\nwpa_pairwise=TKIP'
            file_content += '\nwpa_passphrase=' + str(password)
    
    with open('/etc/hostapd/hostapd.conf', 'w') as file:
        file.write(file_content)

    with open('/etc/default/hostapd', 'w') as file:
        file.write('DAEMON_CONF=/etc/hostapd/hostapd.conf')

def remove():
    with open('/etc/hostapd/hostapd.conf', 'w') as file:
        file.write('')
