# 3x-ui-telegraf-influx
3x-ui online users and traffic metric collector for grafana (telegraf+influxdb)

## Telegraf configuration

`cd /etc/telegraf/`

`sudo mkdir scripts && cd scripts`

`sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/online.py`
`sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/traffic.py`

`sudo chmod a+x online.py traffic.py`

Dont forget to change {PORT} {WEBPATH} {USERNAME} and {PASSWORD} in both .py scripts
```
>>>
BASE_URL = "http://localhost:{PORT}"
LOGIN_ENDPOINT = "/{WEBPATH}/login"
ONLINE_ENDPOINT = "/{WEBPATH}/panel/inbound/onlines"
USERNAME = "{USERNAME}"
PASSWORD = "{PASSWORD}"
<<<
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

`sudo systemctl restart telegraf`

make sure your new metrics are showing up

`telegraf --config telegraf.conf --test`

