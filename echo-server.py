import socket
import hashlib

def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

def verify_checksum(received_checksum, data):
    return received_checksum == calculate_checksum(data)

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server started, waiting for connection...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        expected_sequence = 0  # Esperando a sequência inicial
        while True:
            data = conn.recv(1024)
            if not data:
                break
            sequence, received_checksum, message = data.decode().split(',', 2)
            sequence = int(sequence)  # Converter o número de sequência para int
            if sequence == expected_sequence:
                if verify_checksum(received_checksum, message.encode()):
                    response = f"Echo: {message} - Checksum OK - Seq: {sequence}"
                    expected_sequence += 1  # Incrementa para esperar o próximo número de sequência
                else:
                    response = "Checksum Error"
            else:
                response = "Sequence Error"
            conn.sendall(response.encode())
            print(f"\nData received: {message} \nChecksum: {received_checksum}\n{response}\n")
