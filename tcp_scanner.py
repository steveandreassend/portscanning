import argparse
import socket
import ipaddress
import logging
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(ip, port, timeout):
    """Scan a single port on a single IP"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
            logging.info(f"Open port {port} on {ip}")
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def scan_ip(ip, tcp_ports, timeout):
    """Scan all ports on a single IP"""
    results = []
    for port in tcp_ports:
        if scan_port(ip, port, timeout):
            results.append(port)
    return ip, results

def generate_ips(ip_ranges):
    """Generate all IP addresses from the given CIDR ranges"""
    ips = []
    for ip_range in ip_ranges:
        network = ipaddress.ip_network(ip_range, strict=False)
        ips.extend(str(ip) for ip in network.hosts())
    return ips

def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner.")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads")
    parser.add_argument('--timeout', type=float, default=0.5, help="TCP timeout in seconds")
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help="Path to the config file")
    parser.add_argument('-l', '--logfile', type=str, default='tcp_scan.log', help="Path to the log file")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(filename=args.logfile, level=logging.INFO, 
                        format='%(asctime)s %(message)s')

    # Load configuration from YAML file
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    tcp_ports = config['tcp_ports']
    ip_ranges = config['ip_ranges']
    ips = generate_ips(ip_ranges)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_ip, ip, tcp_ports, args.timeout): ip for ip in ips}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                ip, open_ports = future.result()
                if open_ports:
                    logging.info(f"IP {ip} has open ports: {open_ports}")
            except Exception as exc:
                logging.error(f"IP {ip} generated an exception: {exc}")

if __name__ == "__main__":
    main()
