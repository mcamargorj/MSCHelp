import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import ARP, Ether, srp

def scan(ip):
    arp_request = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout=3, verbose=False)[0]

    # Lista para armazenar os hosts ativos
    active_hosts = []

    for sent, received in result:
        active_hosts.append({'ip': received.psrc, 'mac': received.hwsrc})

    return active_hosts

if __name__ == "__main__":
    ip_range = "192.168.114.0/24"  # Substitua pelo intervalo de IPs da sua rede
    active_hosts = scan(ip_range)
    print("Hosts ativos na rede:")
    for host in active_hosts:
        print("IP:", host['ip'], "- MAC:", host['mac'])


