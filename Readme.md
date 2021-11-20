# Numberly Deploy

Docker-compose deployment including a FastAPI app and its monitoring services.

### Services:
- localhost:8000 => Nginx server
- localhost:9090 => Prometheus
- localhost:3000 => Grafana
- hidden => FastAPI app instance 1
- hidden => FastAPI app instance 2
- hidden => PostgresQL DB
- localhost:9187 => PostgresQL->Prometheus exporter
- localhost:9113 => Nginx->Prometheus exporter



### API Endpoints:
- localhost:8000/ => root
- localhost:8000/expensive => slow request simulating expensive computation
- localhost:8000/exception => raises an exception
- localhost:8000/crash => induces app crash
- GET localhost:8000/posts => get all posts
- GET localhost:8000/posts/{id} => get specified post
- POST localhost:8000/posts => create specified post in body
- DEL localhost:8000/posts/{id} => delete specified post

### Prometheus rules & alerts:
- job:app_response_latency_seconds:rate1m => API latency for endpoint `/expensive`
- AppLatencyAbove5sec => API latency over 5 secs
- ExceptionOccured => Uncaught exception occured


