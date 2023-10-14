import socket
import threading
from Crypto.Cipher import AES
import base64

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('server_ip_address', 12345))

# Ask the user to enter a username
username = input("Enter your username: ")
client_socket.send(username.encode('utf-8')

# Set up AES encryption
key = get_random_bytes(32)  # AES-256 key
cipher = AES.new(key, AES.MODE_EAX)

# Function to send messages
def send_message():
    while True:
        message = input(f"{username}: ")
        # Encrypt the message with AES
        ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))

        # Send the encrypted message to the server
        encrypted_message = base64.b64encode(ciphertext + tag)
        client_socket.send(encrypted_message)

# Function to receive and display messages
def receive_messages():
    while True:
        encrypted_message = client_socket.recv(1024)
        if encrypted_message:
            # Decrypt the message with AES
            encrypted_message = base64.b64decode(encrypted_message)
            ciphertext, tag = encrypted_message[:16], encrypted_message[16:]
            decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
            print(decrypted_message.decode('utf-8'))

# Start separate threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_messages)

send_thread.start()
receive_thread.start()
