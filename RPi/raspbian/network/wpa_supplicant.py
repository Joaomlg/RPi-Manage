from string import Template
import os.path

def create(ssid, passwd):
    file_content = ''

    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, 'wpa_supplicant-example.conf')) as file:
        file_content = Template(file.read())
        file_content = str(file_content.safe_substitute(ssid=ssid, passwd=passwd))
    
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
        file.write(file_content)