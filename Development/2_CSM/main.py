import socket
import threading
import json
import time
import requests

# Server configuration
HOST = 'localhost'
PORT = 5000

# LLM API configuration
API_ENDPOINT = "https://api.groq.com/v1/generate"  # Replace with actual endpoint
API_KEY = "your_groq_api_key_here"
SOURCE = "Groq"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

clients = []

def handle_client(client_socket):
    while True:
        try:
            prompt = client_socket.recv(1024).decode('utf-8')
            if not prompt:
                break
            print(f"Received prompt from client: {prompt}")

            # Call the LLM API
            time_sent = int(time.time())
            response = requests.post(API_ENDPOINT, headers=HEADERS, json={"prompt": prompt})
            time_recvd = int(time.time())

            if response.status_code == 200:
                message = response.json().get("text", "")
                response_data = {
                    "Prompt": prompt,
                    "Message": message,
                    "TimeSent": time_sent,
                    "TimeRecvd": time_recvd,
                    "Source": SOURCE
                }
                response_json = json.dumps(response_data)

                # Send the response back to all clients
                for client in clients:
                    client.send(response_json.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()


import socket
import json

# Server configuration
HOST = 'localhost'
PORT = 5000

def send_prompt(prompt):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(prompt.encode('utf-8'))

    response = client_socket.recv(4096).decode('utf-8')
    response_data = json.loads(response)
    print(f"Received response: {response_data}")

    # Save response to JSON file
    with open('client_responses.json', 'a') as f:
        json.dump(response_data, f, indent=4)
        f.write(",\n")

    client_socket.close()

if __name__ == "__main__":
    # Example prompt
    prompt = "What is the capital of France?"
    send_prompt(prompt)
