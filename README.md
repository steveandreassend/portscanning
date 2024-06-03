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



