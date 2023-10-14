import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pickle
import base64

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up AES encryption
key = get_random_bytes(32)  # AES-256 key
cipher = AES.new(key, AES.MODE_EAX)

# Bind the socket to a specific address and port
server_socket.bind(('0.0.0.0', 12345))

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening...")

# Dictionary to store connected clients and their usernames
connected_clients = {}

# Function to handle client connections
def handle_client(client_socket):
    # Ask the client for their username
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    connected_clients[username] = client_socket
    print(f"{username} connected")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data}")

        # Encrypt the message with AES
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Broadcast the encrypted message to all connected clients
        for client in connected_clients.values():
            encrypted_message = base64.b64encode(nonce + ciphertext + tag)
            client.send(encrypted_message)

    # Remove the disconnected client
    del connected_clients[username]
    client_socket.close()

# Accept and handle client connections
while True:
    client, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
  
