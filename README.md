# 3x-ui-telegraf-influx
3x-ui online users and traffic metric collector for grafana (telegraf+influxdb)

First of all you need Python3 and "requests" lib.
```
sudo apt install python3 python3-pip
```
```
sudo pip3 install requests
```

## Telegraf configuration
```
cd /etc/telegraf/ && sudo mkdir scripts
```
## Get scripts
```
sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/online.py -O /etc/telegraf/scripts/online.py
```
```
sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/traffic.py -O /etc/telegraf/scripts/traffic.py
```
```
sudo chmod a+x online.py traffic.py
```

Run that one-shot command to enter&replace placeholders in both files:
```
sudo bash -c '
read -p "Enter port (PORT): " PORT && \
read -p "Enter web path (WEBPATH): " WEBPATH && \
read -p "Enter username (USERNAME): " USERNAME && \
read -sp "Enter password (PASSWORD): " PASSWORD && echo && \
for FILE in /etc/telegraf/scripts/online.py /etc/telegraf/scripts/traffic.py; do \
  sed -i "s|{PORT}|${PORT}|g; s|{WEBPATH}|${WEBPATH}|g; s|{USERNAME}|${USERNAME}|g; s|{PASSWORD}|${PASSWORD}|g" "$FILE"; \
done
'
```

add this input to your telegraf.conf
```
sudo nano /etc/telegraf/telegraf.conf
```
```
[[inputs.exec]]
  commands = ["/usr/bin/python3 /etc/telegraf/scripts/online.py"]
  timeout = "10s"
  data_format = "influx"

[[inputs.exec]]
  interval = "15m"
  commands = ["/usr/bin/python3 /etc/telegraf/scripts/traffic.py"]
  timeout = "30s"
  data_format = "influx"
```
```
sudo systemctl restart telegraf
```

make sure your new metrics are showing up

```
telegraf --config telegraf.conf --test
```

#### To update to the latest version of the scripts when new commits are available in this repository, simply execute the wget commands provided in the Get Scripts section and re-run one-shot command.
