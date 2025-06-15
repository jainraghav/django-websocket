# Metrics

| Metric                         | Type    | Description                                |
|--------------------------------|---------|--------------------------------------------|
| `chat_total_messages`          | Counter | Total number of chat messages received     |
| `chat_active_connections`      | Gauge   | Current number of active WebSocket sessions|
| `chat_error_count`             | Counter | Total number of errors in the chat consumer|
| `chat_last_shutdown_timestamp` | Gauge   | Unix timestamp of the most recent disconnect|

## Accessing Metrics
```bash
curl -s http://localhost/metrics/ | head -n 20
```
### Sample output
```
# HELP chat_total_messages_total Total number of chat messages received
# TYPE chat_total_messages_total counter
chat_total_messages_total 3.0
# HELP chat_total_messages_created Total number of chat messages received
# TYPE chat_total_messages_created gauge
chat_total_messages_created 1.7498847489962645e+09
# HELP chat_active_connections Current number of active websocket connections
# TYPE chat_active_connections gauge
chat_active_connections 1.0
# HELP chat_error_count_total Total number of errors in ChatConsumer
# TYPE chat_error_count_total counter
chat_error_count_total 0.0
# HELP chat_error_count_created Total number of errors in ChatConsumer
# TYPE chat_error_count_created gauge
chat_error_count_created 1.749884748996285e+09
# HELP chat_last_shutdown_timestamp timestamp of last websocket disconnect
# TYPE chat_last_shutdown_timestamp gauge
chat_last_shutdown_timestamp 0.0
```