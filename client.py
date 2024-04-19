import socket
from header import pack_header, calculate_checksum


def create_client(host=socket.gethostname(), port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        try:
            seq_num = 1
            while True:
                message = input("Digite a mensagem para enviar ou:\nDigite 1 para simular pacote perdido\nDigite 2 para simular o timeout no cliente\nEscreva: ")
                if message.lower() == 'exit':
                    break
                payload = message.encode('utf-8')  # criptografa
                checksum = calculate_checksum(payload)
                # payload = sock.sendall(message.encode())
                header = pack_header(seq_num, 0, 0b00000001, checksum, len(payload))
                packet = header + payload
                sock.sendall(packet)
                response = sock.recv(1024)  # maximum amount of data to be received at once
                seq_num += 1
                if response == b'ACK':
                    print(f"ACK received!, {seq_num}")
                else:
                    print("No ACK, resending...")
        finally:
            print("Closing connection")
            sock.close()


if __name__ == '__main__':
    create_client()
