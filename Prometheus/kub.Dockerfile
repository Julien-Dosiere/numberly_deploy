FROM prom/prometheus
ADD kub-prometheus.yml /etc/prometheus/prometheus.yml
ADD rules.yml /etc/prometheus/


