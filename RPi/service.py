import os
import re

def get_status(service_name):
    command = '/etc/init.d/%s status | grep Active' % (str(service_name))
    regex = r'Active: ([a-zA-Z]*)'
    response = os.popen(command).read()
    if response:
        status = re.search(regex, response)
        if status:
            return str(status.group(1))
    return None

def is_loaded(service_name):
    command = '/etc/init.d/%s status | grep Loaded' % (str(service_name))
    regex = r'Loaded: ([a-zA-Z]*)'
    response = os.popen(command).read()
    if response:
        status = re.search(regex, response)
        if status:
            if 'loaded' in status.group(1):
                return True
            return False
    return None

def unmask_service(service_name):
    command = 'sudo systemctl unmask %s' % (str(service_name))
    os.popen(command)