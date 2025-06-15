## Quick Start
#### This starts up nginx and both the containers along with the proxy
```bash
docker-compose -f docker/compose.yml up --build
```
### flip color (blue→green or green→blue)
```bash
chmod +x app/scripts/promote.sh
./app/scripts/promote.sh
```

### Load test (configurable concurrency and messages)
```bash
python3 load/load_test.py
```