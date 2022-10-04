import socket
import threading
import argparse

def scan_host(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open on {ip}")
        sock.close()
    except socket.error:
        pass

def scan_ports(ip, port_range):
    print(f"Scanning ports for {ip}...")
    for port in range(*port_range):
        thread = threading.Thread(target=scan_host, args=(ip, port))
        thread.start()

def scan_network(ip_range, port_range):
    print(f"Scanning network {ip_range}...")
    for host in ip_range:
        thread = threading.Thread(target=scan_ports, args=(str(host), port_range))
        thread.start()

def main():
    parser = argparse.ArgumentParser(description='Network and Port Scanner')
    parser.add_argument('-i', '--ip', help='IP address or IP range to scan', required=True)
    parser.add_argument('-p', '--port', help='Port range to scan (e.g., 1-100)', required=True)
    args = parser.parse_args()

    ip_range = args.ip.split('-')
    start_ip = ip_range[0]
    end_ip = ip_range[1] if len(ip_range) > 1 else start_ip

    start_port, end_port = map(int, args.port.split('-'))
    port_range = (start_port, end_port + 1) 

    scan_network(range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1), port_range)

if __name__ == '__main__':
    main()
