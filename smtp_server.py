import socket
import os

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 2525))
    server_socket.listen(1)
    
    print("SMTP Server is running on port 2525...")
    
    if not os.path.exists("mailbox"):
        os.makedirs("mailbox")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        client_socket.send(b"220 localhost SMTP Server Ready\r\n")
        
        email_data = ""
        recipient = "unknown"
        
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
                
            print(f"Received: {data.strip()}")
            
            if data.startswith("HELO"):
                client_socket.send(b"250 Hello\r\n")
            elif data.startswith("MAIL FROM:"):
                client_socket.send(b"250 Sender OK\r\n")
            elif data.startswith("RCPT TO:"):
                recipient = data.split(":")[-1].strip()
                client_socket.send(b"250 Recipient OK\r\n")
            elif data.startswith("DATA"):
                client_socket.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                email_data = ""
                while True:
                    line = client_socket.recv(1024).decode()
                    if line.strip() == ".":
                        break
                    email_data += line
                
                filename = os.path.join("mailbox", "email_" + recipient.replace("@", "_") + ".txt")
                with open(filename, "w") as f:
                    f.write(email_data)
                
                client_socket.send(b"250 Message accepted for delivery\r\n")
            elif data.startswith("QUIT"):
                client_socket.send(b"221 Bye\r\n")
                break
                
        client_socket.close()

if __name__ == "__main__":
    run_server()