
import socket
import threading

HOST = '0.0.0.0'
PORT = 21002

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    with conn:
        while True:
            try:
                message_received = ""
                while True:
                    data = conn.recv(32)
                    if data:
                        message_received += data.decode()
                        if message_received.endswith("\n"):
                            break
                    else:
                        print(f"Connection lost with {addr}")
                        return

                if message_received:
                    print(f"Message from {addr}: {message_received.strip()}")
                    response = f"Echo: {message_received.strip()}\n"
                    conn.send(response.encode())
                else:
                    break
            except ConnectionResetError:
                print(f"Connection reset by {addr}")
                break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
except Exception as e:
    print(f"Server error: {e}")
finally:
    server.close()
    print("Server shutdown")
