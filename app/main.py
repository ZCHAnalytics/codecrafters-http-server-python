import socket
import threading
import os
import sys

# 1. The main function that delegates to the handle_client function
def main():
    http_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, http_response))
        client_thread.start()
# 1.1. Function that takes over from the main function and delegates to the helper functions
# it receives client_connection as an argument from the  main function
# Depending on the requested path, it calls different helper functions - string, agent, file
def handle_client(client_connection):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        path = request_lines[0].split(" ")[1]
        print(path)
        if path.startswith("/user-agent"):
            agent = request_lines[2].split(": ")[1] if len(request_lines) >= 3 else "Unknown"
            response_content = extract_agent(agent) # calling helper function
            print(response_content)
        elif path.startswith("/echo/"):
            _, _, random_string = path.partition("/echo/")
            response_content = extract_string(random_string) # calling helper function
            print(response_content)
        elif path.startswith("/files/"):
            response_content = extract_file(path) # calling helper function
            print(response_content)
        elif path == "/":
            response_content = build_response() # calling http helper function
            print(f" The outcome of handle_clinet function with only path of slash: {response_content}")
        else:
           return build_response(404, "Not Found")

    except Exception as e:
        print(f"Error handling client request: {e}")
        return build_response(404, "Not Found")
    finally:
        client_connection.sendall(response_content.encode())
        client_connection.close()

# 1.1.1. string helper function called by handle_client function
def extract_string(random_string):
    return build_response(200, "OK", random_string)

# 1.1.2. agent helper function called by handle_client function
def extract_agent(agent):
    response_body = f"User-Agent: {agent}"
    return build_response(200, "OK", response_body)

# 1.1.3. file helper function called by handle_client function that has additional subfunction
def extract_file(file_content):
    if file_content():
        return build_response(200, "OK", file_content.decode())
    else:
        return build_response(404, "Not Found when trying to get file content")

# 1.1.3.1 Content retrieval by 1.1.3. helper function
def get_file_content(path):
    file_name = path[7:]
    file_path = f"{sys.argv[2]}/{file_name}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()
        return file_content
    else:
        return None

# 1.2. Function called by any of the three helper functions if ....
def build_response(status_code, reason_phrase, body=None):
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
    if body:
        response += f"Content-Length: {len(body)}\r\n\r\n{body}"
    else:
        response += "\r\n"
    return response

if __name__ == "__main__":
    main()