# Prometheus + Splunk Observability Example

This is a very, very simple example of configuraing an OpenTelemetry Collector to collect metrics from Promotheus and send them to Splunk Observability. For this example, I started with a fresh EC2 instance which already had the Splunk OpenTelemetry Collector for linux installed via the Data Setup page.

## Install Prometheus

First, generally follow the [Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/) page for Prometheus. On the command line, this looks like below. Your version number may vary.

```
wget https://github.com/prometheus/prometheus/releases/download/v2.30.0/prometheus-2.30.0.linux-amd64.tar.gz
tar xvzf prometheus-2.30.0.linux-amd64.tar.gz
cd prometheus-2.30.0.linux-amd64
```

In the `prometheus` directory, edit the config file to below, this will have prometheus monitor itself and give us some simple metrics to work with.

```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']
```

Start Prometheus with the config file that was just created.

```
./prometheus --config.file=prometheus.yml
```

Verify that you can see metrics at

```
curl localhost:9090/metrics
```

## Configure the OpenTelemetry Collector to Receive Promtheus metrics.

If not already done, install the Splunk OpenTelemetry Collector (fluentd/logging not required).

Edit the config file at `/etc/otel/collector/agent_config.yaml`, add the `prometheus_simple` receiver and include it within the metrics pipeline.

```
...
receivers:
  ...
  prometheus_simple:
    collection_interval: 10s
    endpoint: localhost:9090
    metrics_path: /metrics
...
pipelines
  ...
  metrics:
    receivers: [..., prometheus_simple, ...]
    ...
```

Restart the collector to re-load config, tail the logs to make sure things are working.

```
sudo systemctl restart splunk-otel-collector; journalctl -u splunk-otel-collector -f
```

## Verify metrics in Splunk Observability

In Splunk Observability, navigate to the _Metric Finder_ and search for "prometheus", you should see several prometheus metrics. Clicking one of the metric names will load a chart of this metric where you should see where it started reporting when the collector config was updated.