curl -X POST \
  http://localhost:8080/api/v1/download \
  -H "Content-Type: application/json" \
  -H "x-api-key: key-test-dev" \
  -d '{
    "url": "https://www.youtube.com/watch?v=mBenb7O8Hnc",
    "id": "essa-string-aqui-vai-ser-um-uuid",
    "url_callback": "https://webhook.site/ec13a642-72d1-4b00-bf19-fd84d619241f"
  }'