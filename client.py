import socket

HOST = "127.0.0.3"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    print("Type '/exit' to disconnect.\n")
    
    while True:
        # Ввод сообщения
        message = input("You: ")
        
        # Отправка сообщения
        s.sendall(message.encode('utf-8'))
        
        # Если пользователь ввел exit - завершаем
        if message.lower() == "/exit":
            print("Disconnecting...")
            break
        
        # Получение ответа от сервера
        data = s.recv(1024)
        print(f"Server: {data.decode('utf-8')}")
    
    # Получаем прощальное сообщение от сервера
    try:
        data = s.recv(1024)
        if data:
            print(f"Server: {data.decode('utf-8')}")
    except:
        pass
    
print("Connection closed.")