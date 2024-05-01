import socket
import threading
import os
import sys

# 1. The main function that delegates to the handle_client function
def main(directory):
    http_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, directory))
        client_thread.start()
# 1.1. Function that takes over from the main function and delegates to the helper functions
def handle_client(client_connection, directory):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        path = request_lines[0].split(" ")[1]
        method = request_lines[0].split(" ")[0]
        print(method, path)
        if path.startswith("/files/"):
            if method == "POST":
                filename = os.path.basename(path)
                file_path = os.path.join(directory, filename)
                #  Read the request body to obtain file contents
                content_length = int(next(line.split(": ")[1] for line in request_lines if line.startswith("Content-Length")))
                request_body = "".join(request_lines[-1])
                file_content = request_body.encode()[:content_length]
                # Write file contents to the specified directory
                with open(file_path, "wb") as file:
                    file.write(file_content)
                # Respond to the client with status code 201
                response = build_response(201, "Created", None, None)
            elif method == "GET":
                response_content = get_file_content(path) # calling file helper function
                print(response_content)
            else:
                response = build_response(404, "Not Found", None, None)
        
        elif path.startswith("/user-agent") and len(request_lines) >= 3:
            agent_line = request_lines[2]
            response_content = extract_agent(agent_line) # calling agent helper function
            print(response_content)
        elif path.startswith("/echo/"):
            _, _, random_string = path.partition("/echo/")
            response_content = extract_string(random_string) # calling string helper function
            print(response_content)
        elif path == "/":
            print("The outcome of handle_client function is an empty path")
            response_content = build_response(200, "OK", None, None)
        else:
            response_content = build_response(404, 'Not Found', None, None)

    except Exception as e:
        print(f"Error handling client request: {e}")
        response = build_response(500, "Internal Server Error", None, None)
    finally:
        client_connection.sendall(response.encode())
        client_connection.close()
# 1.1.1. string helper function called by handle_client function
def extract_string(random_string):
    response_body = random_string
    return build_response(200, 'OK', 'text/plain', response_body)

# 1.1.2. agent helper function called by handle_client function
def extract_agent(agent_line):
    agent = agent_line.split(": ")[1]
    response_body = agent
    return build_response(200, 'OK', 'text/plain', response_body)

# 1.1.3. Content retrieval helper function
def get_file_content(path):
    file_name = path[7:]
    print(file_name)
    file_path = f"{sys.argv[2]}/{file_name}"
    print(file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()
        return build_response(200, "OK", 'application/octet-stream', file_content)
    else:
        return build_response(404, "Not Found when trying to get file content", None, None)

# 1.2. Function called by any of the three helper functions if ....
def build_response(status_code, reason_phrase, content_type=None, body=None):
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
    if content_type:
        response += f"Content-Type: {content_type}\r\n"
    if body:
       response += f"Content-Length: {len(body)}\r\n\r\n{body}\r\n"
    else:
       response += '\r\n'
    return response

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--directory":
        print("Usage: python server.py --directory <directory>")
        sys.exit(1)

    directory = sys.argv[2]
    main(directory)
