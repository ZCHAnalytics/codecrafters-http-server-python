import socket
import threading
import os
import sys

http_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"

def main():
    global http_response
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(args=(client_connection,))
        client_thread.start()

def handle_client(client_connection):
    global http_response
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        path = request_lines[0].split(" ")[1]

        if path.startswith("/user-agent"):
            agent = request_lines[2].split(": ")[1] if len(request_lines) >= 3 else "Unknown"
            http_response = extract_agent(agent)
        elif path.startswith("/echo/"):
            _, _, random_string = path.partition("/echo/")
            http_response = extract_path_string(random_string)
        elif path.startswith("/files/"):
            http_response = extract_file(path)
        elif path == "/":
            http_response
        else:
            http_response = default_response
    except Exception as e:
        print(f"Error handling client request: {e}")
        client_connection.sendall(http_response.encode())
    finally:
        client_connection.close()

def extract_agent(agent):
    response_body = f"User-Agent: {agent}"
    return build_response(200, "OK", response_body)

def extract_path_string(random_string):
    return build_response(200, "OK", random_string)

def extract_file(path):
    file_name = path[7:]
    file_path = f"{sys.argv[1]}/{file_name}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            file_content = file.read()
        return build_response(200, "OK", file_content.decode())
    else:
        return build_response(404, "Not Found")

def build_response(status_code, reason_phrase, body=None):
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
    if body:
        response += f"Content-Length: {len(body)}\r\n\r\n{body}"
    else:
        response += "\r\n"
    return response

if __name__ == "__main__":
    main()
