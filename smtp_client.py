import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 2525))
    
    print(client_socket.recv(1024).decode())
    
    client_socket.send(b"HELO localhost\r\n")
    print(client_socket.recv(1024).decode())
    
    client_socket.send(b"MAIL FROM: student@kvkedu.lt\r\n")
    print(client_socket.recv(1024).decode())
    
    client_socket.send(b"RCPT TO: teacher@kvkedu.lt\r\n")
    print(client_socket.recv(1024).decode())
    
    client_socket.send(b"DATA\r\n")
    print(client_socket.recv(1024).decode())
    
    message = "Subject: Computer Networks Project Milestone 1\r\n\r\nHello, this is a test email from mini SMTP client!\r\n.\r\n"
    client_socket.send(message.encode())
    print(client_socket.recv(1024).decode())
    
    client_socket.send(b"QUIT\r\n")
    print(client_socket.recv(1024).decode())
    
    client_socket.close()

if __name__ == "__main__":
    run_client()