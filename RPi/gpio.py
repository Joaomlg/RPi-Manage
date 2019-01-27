#!/usr/bin/python3

import os
import threading

__interrupt_list = {}
__interrupt_run = {}

OUT = 'out'
IN = 'in'

CHANGE = 0
RISING = 1
FALLING = 2

def pinMode(pin, mode):
    '''Set up single or pin list with the mode...\n - pin: int, list or tuple;\n - mode: gpio.OUT or gpio.IN;\n\nEx.: pinMode(17, gpio.OUT)'''

    # Configure mode
    if mode not in (OUT, IN):
        raise TypeError('Mode should be gpio.OUT or gpio.IN!')
    
    # Set pin/pins
    if type(pin) is int:
        os.popen("echo \"{pin}\" > /sys/class/gpio/export".format(pin=pin))
        os.popen("echo \"{mode}\" > /sys/class/gpio/gpio{pin}/direction".format(mode=mode, pin=pin))
    elif (type(pin) is list) or (type(pin) is tuple):
        for p in pin:
            # Check if arg is a number
            if not str(p).isnumeric:
                raise('List values need be a number!')
        
            os.popen("echo \"{pin}\" > /sys/class/gpio/export".format(pin=p))
            os.popen("echo \"{mode}\" > /sys/class/gpio/gpio{pin}/direction".format(mode=mode, pin=p))
    else:
        raise TypeError('Pin should be an int, list or tuple!')
        

def digitalWrite(pin, value):
    '''Set pin status...\n - pin: int, list or tuple;\n - value: 1 or 0;\n\nEx.: digitalWrite(10, 1)'''

    # Configure value
    if value not in (1, 0):
        raise TypeError('Value should be [\'HIGH\', True, 1] or [\'LOW\', False, 0]!')

    # Setting pin state
    if type(pin) is int:
        os.popen("echo \"{value}\" > /sys/class/gpio/gpio{pin}/value".format(pin=pin, value=value))
    elif (type(pin) is list) or (type(pin) is tuple):
        for p in pin:
            # Check if arg is a number
            if not str(p).isnumeric:
                raise('List values need be a number!')

            os.popen("echo \"{value}\" > /sys/class/gpio/gpio{pin}/value".format(pin=p, value=value))
    else:
        raise TypeError('Pin should be an int, list or tuple!')


def digitalRead(pin):
    '''Read pin status...\n - pin: int;\n\nEx.: digitalRead(14)'''

    response = None

    # Check if arg is a number
    if str(pin).isnumeric():
        response = os.popen("cat /sys/class/gpio/gpio{pin}/value".format(pin=pin)).read()
    else:
        raise TypeError('Pin should be an int!')

    # Return response
    if '1' in response:
        return 1
    elif '0' in response:
        return 0
    else:
        raise OSError('Please set pin before!')


def __interrupt(pin, edge, func, kwargs):
    # Call func with args (if exist)
    def execute_func():
        if len(kwargs) > 0:
            func(**kwargs)
        else:
            func()
    
    # Config interrupt running flag as last pin state
    __interrupt_run[pin] = True
    last_state = digitalRead(pin)

    # While interrupt is running...
    while (__interrupt_run[pin]):
        current_state = digitalRead(pin)

        # When pin state change, verify edge and call function if necessary
        if current_state != last_state:
            if edge == 'FALLING':
                if last_state == 1 and current_state == 0:
                    execute_func()
            elif edge == 'RISING':
                if last_state == 0 and current_state == 1:
                    execute_func()
            else:
                execute_func()
        
        # Update last pin state
        last_state = current_state
    
    # When interrupt is done, delete variables
    del(__interrupt_list[pin])
    del(__interrupt_run[pin])


def attachInterrupt(pin, edge, func, **kwargs):
    '''Configure pin interrupt...\n - pin: int;\n - edge: gpio.CHANGE, gpio.RISING or gpio.FALLING;\n - func: func that will be call when interrupt occurs (can be pass kwargs);\n\nEx.: attachInterrupt(6, gpio.RISING, foo)'''

    # Check interrupt edge arg
    if edge not in (CHANGE, RISING, FALLING):
        raise TypeError('Edge should be gpio.CHANGE, gpio.RISING or gpio.FALLING!')
    
    # Check pin arg
    if not str(pin).isnumeric():
        raise TypeError('Pin should be an int!')

    # If pin not has an interrupt setted
    if pin not in __interrupt_list:
        __interrupt_list[pin] = threading.Thread(target=__interrupt, args=(pin, edge, func, kwargs))
        __interrupt_list[pin].start()
    else:
        raise OverflowError('This pin already has an interrupt method!')


def detachInterrupt(pin):   
    '''Cancel pin interrupt...\n - pin: int;\n\nEx.: detachInterrupt(14)'''

    # Check if pin has interrupt
    if pin in __interrupt_list:
        __interrupt_run[pin] = False
    else:
        raise KeyError('This pin not has an interrupt method!')
