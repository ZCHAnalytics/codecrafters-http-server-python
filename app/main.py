import socket
import threading
import os
import sys

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=parsing_requests, args=(client_connection,))
        client_thread.start()
    print("main function completed")

def parse_lines(client_connection):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        path = request_lines[0].split(" ")[1]
        print(path)
        try: 
            if len(request_lines) >= 3:
                agent = request_lines[2].split(": ")[1]
                print(agent)
            else:
                print("Request data does not contain enough lines")
        except Exception as e:
            print(f"Number of lines is less than 3: {e}")

    except Exception as e:
        print(f"Error in parsing-lines: {e}")
        http_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"

def extract_content(path, client_connection, agent):
    if path.startswith("/echo/"):
        _, _, random_string = path.partition("/echo/")
        print(f"Extracted random string from path: {random_string}")
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
    elif path == "/":
        print(f"No specific path provided, so returning the default respose")
        http_response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/user-agent"):
        print(f"Value of User-Agent extracted and is: {agent}\n")
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(agent)}\r\n\r\n{agent}"
    elif path.startswith("/files/"):
        file_name = path[7:]
        file_path = f"{sys.argv[2]}/{file_name}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                file_content = file.read()
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content.decode()}"
            client_connection.sendall(http_response.encode())
        else:
            print(f"Requested file not found: {file_name}")
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
            client_connection.sendall(http_response.encode())
    else:
        print(f"Requsted path not found, returning 404 error")
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_connection.sendall(http_response.encode())
    
        print("Closing the client connection and going to bed")
        client_connection.close()

if __name__ == "__main__":
    main()