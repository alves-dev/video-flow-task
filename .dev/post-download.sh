curl -X POST http://localhost:8080/api/v1/download \
  -H "Content-Type: application/json" \
  -H "x-api-key: key-test-dev" \
  -d '{"url":"https://www.youtube.com/watch?v=mBenb7O8Hnc"}'