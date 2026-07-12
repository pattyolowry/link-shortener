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

Throughput: 40 RPS \
P95 Latency: 19.57ms
<img width="1654" height="1416" alt="image" src="https://github.com/user-attachments/assets/690aebad-5f66-42bb-a5a1-dd2322a6776b" />

### Index on short_id

Throughput: 400 RPS \
P95 Latency: 4.02ms
<img width="1642" height="1400" alt="image" src="https://github.com/user-attachments/assets/2c9b0812-cc68-44bb-9c70-38b17a9f9ec5" />

### 2 workers

Throughput: 675 RPS \
P95 Latency: 68.52ms
<img width="1630" height="1418" alt="image" src="https://github.com/user-attachments/assets/87b7bcdb-2ea2-4f32-98d3-c2aae589b21e" />

### 4 Workers

Throughput: 1000 RPS \
P95 Latency: 7.01ms
<img width="1634" height="1410" alt="image" src="https://github.com/user-attachments/assets/80066024-5fda-456a-afc2-1873ec0f3322" />

### 8 Workers

*Note:* at this point the app started exceeding default Postgres connection limits, so I limited each worker to 8 connections, for a maximum of 64 connections:
- `pool_size = 4`
- `max_overflow = 4`

Before adding more API instances, PgBouncer should be introduced between the app and Postgres, so that PgBouncer can manage a shared connection pool instead of each instance managing its own connection pool.

Throughput: 1600 RPS \
P95 Latency: 27.88ms
<img width="1676" height="1422" alt="image" src="https://github.com/user-attachments/assets/e1443993-b2f0-4ba0-9f23-06d1a3a4edef" />

### Add PgBouncer

No expected performance improvement, just easier to manage the connection pool for Postgres

Throughput: 1450 RPS \
P95 Latency: 5.29ms
<img width="1678" height="1542" alt="image" src="https://github.com/user-attachments/assets/42eec88d-9809-4c11-9454-9fb0ea258616" />

## Bottlenecks Encountered

- CPU exhaustion on Postgres server when not using index on short_id
- CPU exhaustion on API server (can reduce this bottleneck up to a point by increasing number of workers)
- Exhausted Postgres client connections upon increasing to 8 workers (default max connections is 100)
