# portscanning
A simple python tool that will scan a defined range of IPs for open TCP ports using a defined port list

Example Usage
=============
```
python tcp_scanner.py --threads 20 --timeout 1 --config config.yaml --logfile custom_log.log
```

Where
--threads is the number of concrrent tcp threads
--timeout is the amount of seconds to wait on receiving a response
--config specifies the input for the scan
--logfile specifies where to write the output of the scan

Sample input for config.yaml:

```
tcp_ports:
  - 22
  - 111
  - 44321
  - 4330
ip_ranges:
  - '10.0.0.78'
  - '127.0.0.1'
  - '10.0.0.0/24'
```

Setup
=====
pyyaml is required for procesing the config.yaml file.

On Oracle Linux:
```
sudo dnf install -y python3-pip && pip3 install pyyaml
```

Sample Output
=============
```
Program started at 2024-06-03 16:43:14.770331
IPs to scan: [('10.0.0.78', '10.0.0.78'), ('127.0.0.1', '127.0.0.1')]
Attempting to scan IP 10.0.0.78 on port 22
Open port 22 on 10.0.0.78
Attempting to scan IP 10.0.0.78 on port 111
Open port 111 on 10.0.0.78
Attempting to scan IP 10.0.0.78 on port 44321
Connection refused while scanning IP 10.0.0.78 on port 44321
Attempting to scan IP 10.0.0.78 on port 4330
Connection refused while scanning IP 10.0.0.78 on port 4330
Attempting to scan IP 127.0.0.1 on port 22
Starting scan for IP range: 10.0.0.78 (10.0.0.78 - 10.0.0.78, total 1 IPs) at 2024-06-03 16:43:14.830647
Completed scan for IP 10.0.0.78
Open port 22 on 127.0.0.1
Attempting to scan IP 127.0.0.1 on port 111
Open port 111 on 127.0.0.1
Attempting to scan IP 127.0.0.1 on port 44321
Open port 44321 on 127.0.0.1
Attempting to scan IP 127.0.0.1 on port 4330
Open port 4330 on 127.0.0.1
Starting scan for IP range: 127.0.0.1 (127.0.0.1 - 127.0.0.1, total 1 IPs) at 2024-06-03 16:43:14.832849
Completed scan for IP 127.0.0.1
Program finished at 2024-06-03 16:43:14.833484, total duration: 0:00:00.063153
```
