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
def handle_client(client_connection, directory):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        method, path, _ = request_lines[0].split(" ", 2)
        print(f"Method is {method} and path is {path}")

        if path.startswith("/files/"):
            if method == "POST":
                filename = os.path.basename(path)
                file_path = os.path.join(directory, filename)
                print(f"File name is {filename} and file path is {file_path}")
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
                print("Method is GET")
                response_content = get_file_content(path, directory) # calling file helper function
                print(response_content)
            else:
                print("Method is not provided")
                response = build_response(404, "Not Found", None, None)
        
        elif path.startswith("/user-agent") and len(request_lines) >= 3:
            print("Path starts with user-agent")
            agent_line = request_lines[2]
            print("agent_line requested")
            response_content = extract_agent(agent_line) # calling agent helper function
            print(response_content)

        elif path.startswith("/echo/"):
            print("Path starts with echo")
            _, _, random_string = path.partition("/echo/")
            print(random_string)
            response_content = extract_string(random_string) # calling string helper function
            print(response_content)

        elif path == "/":
            print("The outcome of handle_client function is an empty path")
            response_content = build_response(200, "OK", None, None)
        
        else:
            print("there is not path")
            response_content = build_response(404, 'Not Found', None, None)

    except Exception as e:
        print(f"Error handling client request: {e}")
        response = build_response(500, "Internal Server Error", None, None)
    
    finally:
        print("Sending response")
        client_connection.sendall(response)
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
def get_file_content(path, directory):
    print("Running get_file_content function")
    file_name = path[7:]
    print(file_name)
    
    path = os.path.join(directory, file_name)   
    if os.path.exists(path) and os.path.isfile(path):
        print("Both path and file exist")
        with open(path, "r") as file:
            file_content = file.read()
        return build_response(200, "OK", "application/octet-stream", file_content)
    else:
        print("Both path and file do not exist")
        return build_response(404, "Not Found", None, None)

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
