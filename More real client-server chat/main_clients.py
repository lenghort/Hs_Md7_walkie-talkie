import socket
import threading

HOST = '0.0.0.0'
PORT = 21002

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message:
                print(message)
            else:
                print("Server closed the connection.")
                client.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

def write():
    while True:
        try:
            message = input('')
            if message:
                formatted_message = f"{nickname}: {message}\n"
                client.send(formatted_message.encode('ascii'))
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive, daemon=True)
write_thread = threading.Thread(target=write, daemon=True)

receive_thread.start()
write_thread.start()

receive_thread.join()
write_thread.join()
