# 3x-ui-telegraf-influx
3x-ui online users and traffic metric collector for grafana (telegraf+influxdb)

## Telegraf configuration
```
cd /etc/telegraf/ && sudo mkdir scripts && cd scripts
```
```
sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/online.py
```
```
sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/traffic.py
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
for FILE in /etc/telegraf/scripts/file1.txt /etc/telegraf/scripts/file2.txt; do \
  sed -i "s|{PORT}|${PORT}|g; s|{WEBPATH}|${WEBPATH}|g; s|{USERNAME}|${USERNAME}|g; s|{PASSWORD}|${PASSWORD}|g" "$FILE"; \
done
'
```

add this input to your telegraf.conf
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

