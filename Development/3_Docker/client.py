import socket
import json

# Server configuration
HOST = 'localhost'
PORT = 5050

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


# Example prompt
prompt = "What is the capital of France?"
send_prompt(prompt)