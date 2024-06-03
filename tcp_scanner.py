import argparse
import socket
import ipaddress
import logging
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def scan_port(ip, port, timeout):
    """Scan a single port on a single IP"""
    debug_msg = f"Attempting to scan IP {ip} on port {port}"
    print(debug_msg)
    logging.debug(debug_msg)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
            success_msg = f"Open port {port} on {ip}"
            print(success_msg)
            logging.info(success_msg)
            return True
        except socket.timeout:
            timeout_msg = f"Timeout occurred while scanning IP {ip} on port {port}"
            print(timeout_msg)
            logging.debug(timeout_msg)
            return False
        except ConnectionRefusedError:
            refused_msg = f"Connection refused while scanning IP {ip} on port {port}"
            print(refused_msg)
            logging.debug(refused_msg)
            return False
        except Exception as e:
            error_msg = f"Error {e} occurred while scanning IP {ip} on port {port}"
            print(error_msg)
            logging.debug(error_msg)
            return False

def scan_ip(ip, tcp_ports, timeout):
    """Scan all ports on a single IP"""
    results = []
    for port in tcp_ports:
        if scan_port(ip, port, timeout):
            results.append(port)
    return ip, results

def generate_ips(ip_ranges):
    """Generate all IP addresses from the given CIDR ranges and individual IP addresses"""
    ips = []
    for ip_range in ip_ranges:
        try:
            if '/' in ip_range:
                # Handle CIDR notation
                network = ipaddress.ip_network(ip_range, strict=False)
                for ip in network.hosts():
                    ips.append((str(ip), ip_range))
            else:
                # Handle individual IP address
                ip = ipaddress.ip_address(ip_range)
                ips.append((str(ip), ip_range))
        except ValueError as e:
            logging.error(f"Invalid IP address or CIDR block: {ip_range} - {e}")
    return ips

def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner.")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads")
    parser.add_argument('--timeout', type=float, default=0.5, help="TCP timeout in seconds")
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help="Path to the config file")
    parser.add_argument('-l', '--logfile', type=str, default='tcp_scan.log', help="Path to the log file")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(filename=args.logfile, level=logging.DEBUG, 
                        format='%(asctime)s %(message)s')

    # Start timestamp
    start_time = datetime.now()
    start_msg = f"Program started at {start_time}"
    print(start_msg)
    logging.info(start_msg)

    # Load configuration from YAML file
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    tcp_ports = config['tcp_ports']
    ip_ranges = config['ip_ranges']
    ips = generate_ips(ip_ranges)

    # Debug: Print the IPs to be scanned
    print(f"IPs to scan: {ips}")
    logging.debug(f"IPs to scan: {ips}")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_ip, ip[0], tcp_ports, args.timeout): ip for ip in ips}
        current_range = None
        for future in as_completed(futures):
            ip, ip_range = futures[future]
            if ip_range != current_range:
                current_range = ip_range
                if '/' in current_range:
                    network = ipaddress.ip_network(current_range, strict=False)
                    first_ip = str(network[0])
                    last_ip = str(network[-1])
                    total_ips = network.num_addresses - 2  # Excluding network and broadcast addresses
                else:
                    first_ip = last_ip = current_range
                    total_ips = 1
                timestamp = datetime.now()
                range_msg = (f"Starting scan for IP range: {current_range} "
                             f"({first_ip} - {last_ip}, total {total_ips} IPs) at {timestamp}")
                print(range_msg)
                logging.info(range_msg)
            try:
                ip, open_ports = future.result()
                if open_ports:
                    logging.info(f"IP {ip} has open ports: {open_ports}")
                complete_msg = f"Completed scan for IP {ip}"
                print(complete_msg)
                logging.info(complete_msg)
            except Exception as exc:
                logging.error(f"IP {ip} generated an exception: {exc}")

    # End timestamp
    end_time = datetime.now()
    end_msg = f"Program finished at {end_time}, total duration: {end_time - start_time}"
    print(end_msg)
    logging.info(end_msg)

if __name__ == "__main__":
    main()
