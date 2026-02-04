import socket

HOST = "127.0.0.3"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Received: {message}")
            
            # Проверяем, не хочет ли клиент выйти
            if message.lower() == "/exit":
                print(f"Client {addr} requested to disconnect.")
                conn.sendall(b"Goodbye!")
                break
            
            # Отправляем обратно (эхо)
            conn.sendall(data)
        
        print("Connection closed.")