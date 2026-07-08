# link-shortener

start with: `docker compose up --build`

down with : `docker compose down`

just postgres:

```
docker compose up -d postgres
docker compose exec postgres psql -U postgres -d link_shortener
```


## Load Test Results

API Services: 4 vCPU / 2GB MEM \
Postgres: 2 vCPU / 3GB MEM \
Redis: 0.5 vCPU / 512MB MEM

### Baseline (DB w/ 1mil rows and no indexes)

Throughput: 105 RPS \
P95 Latency: 38.51ms
<img width="1640" height="1438" alt="image" src="https://github.com/user-attachments/assets/cce1ab6b-a935-43bf-b002-3676e114d071" />

### Index on short_id

Throughput: 375 RPS \
P95 Latency: 54.74ms
<img width="1616" height="1400" alt="image" src="https://github.com/user-attachments/assets/7cbdf04f-ec1e-483c-ab07-ebd946ec440e" />

### 2 workers

Throughput: 675 RPS \
P95 Latency: 68.52ms
<img width="1630" height="1418" alt="image" src="https://github.com/user-attachments/assets/87b7bcdb-2ea2-4f32-98d3-c2aae589b21e" />

### 4 Workers

Throughput: 1000 RPS \
P95 Latency: 7.01ms
<img width="1634" height="1410" alt="image" src="https://github.com/user-attachments/assets/80066024-5fda-456a-afc2-1873ec0f3322" />


