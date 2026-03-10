cd ..
docker build . -t video-flow:latest

docker run -d \
    --name video-flow \
    -p 7755:4411 \
    -e "SECURITY_API_KEY=key-test-dev" \
    -e "OUTPUT_FOLDER=/app/data" \
    -e "SOS_BUCKET=test-delete-me" \
    -e "SOS_API_KEY=outra_key_xxxyyyzzz" \
    -v $(pwd)/data:/app/data \
    video-flow:latest