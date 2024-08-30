import socket
import threading
import json
from main import call_llm_api as cla # type: ignore


# Server configuration
HOST = 'localhost'
PORT = 5050

clients = []

def handle_client(client_socket):
    while True:
        try:
            prompt = client_socket.recv(1024).decode('utf-8')
            if not prompt:
                break
            print(f"Received prompt from client: {prompt}")

            # Call the LLM API

            response_data = cla(prompt)
            response_json = json.dumps(response_data)

            # Send the response back to all clients
            for client in clients:
                client.send(response_json.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()


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