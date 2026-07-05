# link-shortener

start with: `docker compose up --build`

down with : `docker compose down`

just postgres:

```
docker compose up -d postgres
docker compose exec postgres psql -U postgres -d link_shortener
```


## Load Test Results
### Baseline (DB w/ 1mil rows and no indexes)

Throughput: 105 RPS \
P95 Latency: 38.51ms
<img width="1640" height="1438" alt="image" src="https://github.com/user-attachments/assets/cce1ab6b-a935-43bf-b002-3676e114d071" />

### Index on short_id

Throughput: 375 RPS \
P95 Latency: 54.74ms
<img width="1616" height="1400" alt="image" src="https://github.com/user-attachments/assets/7cbdf04f-ec1e-483c-ab07-ebd946ec440e" />

### 2 workers

Throughput: 650 RPS \
P95 Latency: 50.01ms
<img width="1654" height="1434" alt="image" src="https://github.com/user-attachments/assets/f63c5365-2279-4b44-b8bd-f0f0bebb811c" />

### 4 Workers

Throughput: 1100 RPS \
P95 Latency: 18.87ms
<img width="1630" height="1408" alt="image" src="https://github.com/user-attachments/assets/f81993e9-c298-45d0-afd3-f144b8f9fbc9" />

