# Numberly Deploy

Docker_compose deployment including a FastAPI app and its monitoring services.

### Services:
- localhost:8000 => FastAPI app access through Nginx
- localhost:8080(hidden by default) => FastAPI app direct access
- localhost:9090 => Prometheus
- localhost:3000 => Grafana

### API Endpoints:
- localhost:8000/ => root
- localhost:8000/expensive => slow request simulating expensive computation
- localhost:8000/exception => raises an exception
- localhost:8000/crash => induces app crash

### Prometheus rules & alerts:
- job:app_response_latency_seconds:rate1m => API latency for endpoint `/expensive`
- AppLatencyAbove5sec => API latency over 5 secs
- ExceptionOccured => Uncaught exception occured


