import socket
import threading
import signal
import sys

HOST = "10.90.14.24"
PORT = 65432

# Флаг для остановки сервера
running = True
threads = []

def handle_client(conn, addr):
    #Обрабатывает сообщения одного клиента.
    print(f"Connected by {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")

                if message.lower() == "/exit":
                    print(f"Client {addr} requested to disconnect.")
                    conn.sendall(b"Goodbye!")
                    break

                conn.sendall(data)  # эхо-ответ
            except ConnectionError:
                break
    print(f"Connection with {addr} closed.")

def signal_handler(sig, frame):
    #Обработчик Ctrl+C для graceful shutdown.
    global running
    print("\nShutting down server...")
    running = False
    sys.exit(0)

def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while running:
            try:
                # Таймаут для возможности проверки флага running
                s.settimeout(1.0)
                conn, addr = s.accept()
            except socket.timeout:
                continue
            except Exception as e:
                if running:
                    print(f"Accept error: {e}")
                break

            # Создаём поток для нового клиента
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True  # Поток завершится при выходе из главного
            t.start()
            threads.append(t)

        print("Waiting for all clients to disconnect...")
        for t in threads:
            t.join(timeout=2)

if __name__ == "__main__":
    main()
