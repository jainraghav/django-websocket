COMPOSE_FILE="docker/compose.yml"
# SMOKE_CMD="pytest tests/smoke --maxfail=1 -q"
HEALTH_URL="http://localhost/healthz/"
NGINX_CONF="docker/nginx.conf"

get_color() {
  curl -s "$HEALTH_URL" | sed -n 's/.*"color"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
}

current="$(get_color)"
if [[ "$current" != "blue" && "$current" != "green" ]]; then
  echo "Unexpected current color: $current"; exit 1
fi

if [[ "$current" == "blue" ]]; then
  next="green"
else
  next="blue"
fi

echo "Promoting traffic from $current → $next"

echo "Building image for app_$next"
docker compose -f "$COMPOSE_FILE" build "app_$next"

echo "Starting app_$next"
docker compose -f "$COMPOSE_FILE" up -d "app_$next"


echo "Copying nginx.${next}.conf → docker/nginx.conf …"
cp "docker/nginx.${next}.conf" "docker/nginx.conf"

echo "Reloading proxy…"
docker compose -f "$COMPOSE_FILE" exec proxy nginx -s reload


echo -n "Waiting for app_$next to respond on /healthz/ … "
for i in {1..15}; do
  col="$(get_color)"
  if [[ "$col" == "$next" ]]; then
    echo "OK"
    break
  fi
  echo -n "."
  sleep 2
done

# echo "Running smoke tests"
# eval "$SMOKE_CMD"

echo "Reloading proxy to send traffic to $next"
docker compose -f "$COMPOSE_FILE" exec proxy nginx -s reload

echo "Stopping & removing app_$current"
docker compose -f "$COMPOSE_FILE" rm -sf "app_$current"

echo "Promotion complete: live = $next"