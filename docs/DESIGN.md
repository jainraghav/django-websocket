# DESIGN

## 1. ASGI Event Loop
- **One loop per worker**: each Uvicorn process runs a single async loop.  
- **Heartbeat task**: scheduled via `asyncio.create_task()`, runs on the same loop.  

---

## 2. Workers vs Thread Pool
- **Workers**: we start Uvicorn with `--workers`. Each worker is a separate OS process and has its own loop.  
- **Thread pool**: inside each worker, Django Channels uses ~100 threads to run any sync code (ORM, etc.) without pausing the async loop.

---

## 3. No Shared Mutable State
- **Per-connection state**: every `AsyncWebsocketConsumer` has its own `self.counter`, so counts stay isolated.  
- **Broadcasts** (like heartbeat) go through the channel layer (Redis), not via in-process globals.

---

## 4. Concurrency Tuning
- **Uvicorn backlog**: start with `--backlog 1024` so the OS can queue up more pending connections.  
- **OS limits**: bump file-descriptor limits (`ulimit -n 65536`) and kernel queue size (`somaxconn`).  
- **Nginx tuning** (`docker/nginx.conf`): without this tuning, not more than only 100 concurrent workers were concurrently handling the load. With this, more than 5000 workers were concurrently able to handle the load. Although I have made the load test script to be in batches but we can mimic removing batching by making BATCH_SIZE = CONCURRENCY.
  ```nginx
  worker_processes auto;
  worker_rlimit_nofile 65535;

  events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
  }
  ```
