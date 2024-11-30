# 3x-ui-telegraf-influx
3x-ui online users metric collector for grafana (telegraf+influxdb)

## Telegraf configuration

`cd /etc/telegraf/`

`sudo mkdir scripts && cd scripts`

`sudo wget https://raw.githubusercontent.com/jahlib/3x-ui-telegraf-influx/refs/heads/main/telegraf/scripts/3xui.py`

`sudo chmod a+x 3xui.py`

Dont forget to change {PORT} {WEBPATH} {USERNAME} and {PASSWORD} in 3xui.py
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
  commands = ["/usr/bin/python3 /etc/telegraf/scripts/3xui.py"]
  timeout = "10s"
  data_format = "influx"
```

`sudo systemctl restart telegraf`

`telegraf --config telegraf.conf --test | grep online_users`
