SERVICE="app_blue" # active service name
COMPOSE_FILE="docker/compose.yml"

echo "Tailing ERRORs from ${SERVICE}..."
docker compose -f "${COMPOSE_FILE}" logs -f --no-color "${SERVICE}" \
  | grep --line-buffered "ERROR:" -A 20 &

echo "metrics poll..."
while true; do
  echo -e "\n=== chat_* metrics ==="
  curl -s http://localhost/metrics/ \
    | grep -E '^chat_' \
    | head -n 5
  sleep 10
done
