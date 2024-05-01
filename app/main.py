import socket
import threading
import os
import sys

# 1. The main function that delegates to the handle_client function
def main(directory):
    #http_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, directory))
        client_thread.start()
        
# 1.1. Function that takes over from the main function and delegates to the helper functions
def handle_client(client_connection):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        method, path, _ = request_lines[0].split(" ", 2)

        if path.startswith("/echo/"):
            _, _, random_string = path.partition("/echo/")
            response = extract_string(random_string) # calling string helper function

        elif path == "/":
            response = build_response(200, "OK", None, None)
        
        elif path.startswith("/user-agent") and len(request_lines) >= 3:
            agent_line = request_lines[2]
            response = extract_agent(agent_line) # calling agent helper function

        elif path.startswith("/files/"):
            file_name = path[7: ]
                      
            if method == "GET":
                if os.path.exists(os.path.join(directory, file_name)):
                    body = read_file_content(os.path.join(directory, file_name))
                    response = build_response(200, "OK", "application/octet-stream", body)
                else:
                    response = build_response(404, "Not Found", None, None)
            if method == "POST":
                request_lines = request_data.split("\r\n")[6]
                body = write_file_contents(os.path.join(directory, file_name), request_lines)    
                response = build_response(201, "Created", None, request_lines)
                    
        elif 'response' not in locals():
            response = build_response(500, "Internal Server Error", None, None)
        else:
            print("there is not path")
            response = build_response(404, 'Not Found', None, None)

    except Exception as e:
        print(f"Error handling client request: {e}")
        response = build_response(500, "Internal Server Error", None, None)
    finally:
        print("Sending response")
        client_connection.sendall(response.encode())
        print("Closing the connection")
        client_connection.close()

# 1.1.1. string helper function called by handle_client function
def extract_string(random_string):
    print("Running extract_string function")
    response_body = random_string
    return build_response(200, 'OK', 'text/plain', response_body)

# 1.1.2. agent helper function called by handle_client function
def extract_agent(agent_line):
    print("Running extract_agent function")
    agent = agent_line.split(": ")[1]
    response_body = agent
    return build_response(200, 'OK', 'text/plain', response_body)

# 1.1.3. Content retrieval helper function
def read_file_content(path):
    print("Running get_file_content function")
    file_name = path[7:]
    print(file_name)
    with open(file_name, "r") as f:
        file_content = f.read()
    return build_response(200, "OK", "application/octet-stream", file_content)

# 1.1.4/ Write file content
def write_file_contents(path, content):
    file_name = path[7:]
    with open(file_name, "w") as file:
        file.write(content)

# 1.2. Function called by any of the three helper functions
def build_response(status_code, reason_phrase, content_type=None, body=None):
    print("Running build_response function")
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
    if content_type:
        print("There is content-type parameter available")
        response += f"Content-Type: {content_type}\r\n"
    if body:
       print("There is body parameter available")
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
