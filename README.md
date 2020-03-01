# Indoor Weather Station

## Installation

```shell
$ curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
$ curl -sL https://packages.grafana.com/gpg.key | sudo apt-key add -
$ echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
$ echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
$ sudo apt-get update && sudo apt-get install -y libgpiod2 influxdb grafana
```

InfluxDB setup
```
CREATE DATABASE weather
CREATE RETENTION POLICY cleanup ON weather DURATION 2w REPLICATION 1
```

`pip3 install requirements.txt`