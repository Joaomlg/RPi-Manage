from RPi.uci.base_crud_command import uci_base_command

__all__ = ['wireless', 'network', 'firewall', 'dhcp']

class wireless(uci_base_command):
    def __init__(self):
        super().__init__('wireless', 'wifi-iface')

    def create(self, name, **kwargs):
        '''kwargs can be:\n\ndevice, mode, disabled, ssid, bssid, hidden, isolate, wmm, network, encryption, key, maclist, iapp_interface, rsn_preauth, maxassoc, macaddr, wds.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/wireless'''
        super().create(name, **kwargs)

    def update(self, name, **kwargs):
        '''kwargs can be:\n\ndevice, mode, disabled, ssid, bssid, hidden, isolate, wmm, network, encryption, key, maclist, iapp_interface, rsn_preauth, maxassoc, macaddr, wds.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/wireless'''
        super().update(name, **kwargs)

class network(uci_base_command):
    def __init__(self):
        super().__init__('network', 'interface')
        self.static = self.__static()
        self.dhcp = self.__dhcp()
        self.dongle3g = self.__3g()
    
    class __static(uci_base_command):
        def __init__(self):
            super().__init__('network', 'interface')

        def create(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'static\':\n\n ipaddr, netmask, gateway, broadcast, ap6addr, ip6ifaceid, ip6gw, ip6assign, ip6hint, ip6prefix, ip6class, dns, dns_search, metric.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().create(name, proto='static', **kwargs)

        def update(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'static\':\n\n ipaddr, netmask, gateway, broadcast, ap6addr, ip6ifaceid, ip6gw, ip6assign, ip6hint, ip6prefix, ip6class, dns, dns_search, metric.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().update(name, proto='static', **kwargs)

    class __dhcp(uci_base_command):
        def __init__(self):
            super().__init__('network', 'interface')
        
        def create(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'dhcp\':\n\n broadcast, ipaddr, hostname, clientid,, vendorid,dns, peerdns, defaultroute, customroutes, metric, classlessroute, reqopts, sendopts, zone, iface6rd, mtu6rd, zone6rd.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().create(name, proto='dhcp', **kwargs)

        def update(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'dhcp\':\n\n broadcast, ipaddr, hostname, clientid,, vendorid,dns, peerdns, defaultroute, customroutes, metric, classlessroute, reqopts, sendopts, zone, iface6rd, mtu6rd, zone6rd.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().update(name, proto='dhcp', **kwargs)
    
    class __3g(uci_base_command):
        def __init__(self):
            super().__init__('network', 'interface')
        
        def create(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'3g\':\n\n device, service, apn, pincode, dialnumber, maxwait, username, password, keepalive, demand defaultroute, peerdns, dns, ipv6.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().create(name, proto='3g', **kwargs)

        def update(self, name, **kwargs):
            '''kwargs can be:\n\n - Valid for all protocol types:\n\n ifname, type, stp, bridge_empty, igmp_snooping, multicast_to_unicast, macaddr, mtu, auto, ipv6, accept_ra, send_rsforce_link, enabled, ip4table, ip6table.\n\n - Valid for protocol \'3g\':\n\n device, service, apn, pincode, dialnumber, maxwait, username, password, keepalive, demand defaultroute, peerdns, dns, ipv6.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().update(name, proto='3g', **kwargs)

class firewall(uci_base_command):
    def __init__(self):
        super().__init__('firewall', 'forwarding')
        self.defaults = self.__defaults()
        self.zone = self.__zone()
        self.rule = self.__rule()
        self.forwarding = self.__forwarding()
    
    class __defaults(uci_base_command):
        def __init__(self):
            super().__init__('firewall', 'defaults')

        def create(self, name, **kwargs):
            '''kwargs can be:\n\n input, output, forward, drop_invalid, syn_flood, synflood_protect, synflood_rate, synflood_burst, tcp_syncookies, tcp_ecn, tcp_westwood, tcp_window_scaling, accept_redirects, accept_source_route, custom_chains, disable_ipv6.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().create(name, **kwargs)

        def update(self, name, **kwargs):
            '''kwargs can be:\n\n input, output, forward, drop_invalid, syn_flood, synflood_protect, synflood_rate, synflood_burst, tcp_syncookies, tcp_ecn, tcp_westwood, tcp_window_scaling, accept_redirects, accept_source_route, custom_chains, disable_ipv6.\n\n For more informations, access: https://oldwiki.archive.openwrt.org/doc/uci/network'''
            super().update(name, **kwargs)
    
    class __zone(uci_base_command):
        def __init__(self):
            super().__init__('firewall', 'zone')

    class __rule(uci_base_command):
        def __init__(self):
            super().__init__('firewall', 'zone')
    
    class __forwarding(uci_base_command):
        def __init__(self):
            super().__init__('firewall', 'forwarding')

class dhcp(uci_base_command):
    def __init__(self):
        super().__init__('dhcp', 'dhcp')
    
    def create(self, name, **kwargs):
        ''''''
        super().create(name, **kwargs)

    def update(self, name, **kwargs):
        ''''''
        super().update(name, **kwargs)
