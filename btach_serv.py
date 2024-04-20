import socket

def send_message(sock, message):
    sock.sendall(message.encode('utf-8'))

def send_batch(sock, messages):
    batch = "\n".join(messages)  # Combina todas as mensagens em um único lote
    sock.sendall(batch.encode('utf-8'))

def main_client(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        # Enviar uma única mensagem
        send_message(sock, "Hello, Server!")
        # Enviar um lote de mensagens
        send_batch(sock, ["Message 1", "Message 2", "Message 3"])