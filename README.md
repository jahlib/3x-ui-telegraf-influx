# 3x-ui-telegraf-influx
3x-ui online users metric collector for grafana (telegraf+influxdb)

## Telegraf configuration

add this input to your telegraf.conf
```
[[inputs.exec]]
  commands = ["/usr/bin/python3 /etc/telegraf/scripts/3xui.py"]
  timeout = "10s"
  data_format = "influx"
```

`sudo systemctl restart telegraf`

`telegraf --config telegraf.conf --test | grep online_users`
