
import socket
import hashlib
import time

def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

HOST = "127.0.0.1"
PORT = 65432
TIMEOUT = 5  # Tempo em segundos para retransmissão da mensagem
MAX_ATTEMPTS = 3  # Número máximo de tentativas de reenvio

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.settimeout(TIMEOUT)  # Definindo o timeout do socket
    message = "Hello, world"
    sequence_number = 0  # Número de sequência inicial
    checksum = calculate_checksum(message.encode())
    message_with_checksum = f"{sequence_number},{checksum},{message}"
    
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            s.sendall(message_with_checksum.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
            break  # Sair do loop se a resposta for recebida
        except socket.timeout:
            print(f"Timeout occurred, retransmitting... (Attempt {attempt+1})")
            attempt += 1
    
    if attempt == MAX_ATTEMPTS:
        print("Failed to receive response after maximum attempts.")

    s.close()
