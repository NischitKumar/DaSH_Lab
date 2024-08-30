#!/bin/bash

# Start the server in the background
python3 server.py &

# Allow the server to initialize
sleep 2

# Start multiple clients in parallel
for i in {1..5}; do
    python3 client.py &
done

# Wait for all background processes to finish
wait
