import socket

def create_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        try:
            while True:
                message = input("Digite a mensagem para enviar ou:\nDigite 1 para simular pacote perdido\nDigite 2 para simular o timeout no cliente")
                if message.lower() == 'exit':
                    break
                sock.sendall(message.encode())
                response = sock.recv(1024)
                if response == b'ACK':
                    print("ACK received!")
                else:
                    print("No ACK, resending...")
        finally:
            print("Closing connection")
            sock.close()

if __name__ == '__main__':
    create_client()
