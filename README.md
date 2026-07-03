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

### DB w/ 1mil rows and index on short_id

Throughput: 375 RPS \
P95 Latency: 54.74ms
<img width="1616" height="1400" alt="image" src="https://github.com/user-attachments/assets/7cbdf04f-ec1e-483c-ab07-ebd946ec440e" />
