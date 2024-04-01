import socket

#creating echo server

HOST = "127.0.0.1" #endereço de loopback ou local host, estabelece conexão com o proprio pc
PORT = 65432

#AF_INET = a familia de endereços de internet IPv4
#SOCK_stream = socket do tipo TCP ( protocolo de transporte de mensagens)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind ((HOST, PORT)) # função que prepara um socket para aceitar conexões entrantes, onde o socket deve ouvir 
    s.listen() # backlog parameter
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)