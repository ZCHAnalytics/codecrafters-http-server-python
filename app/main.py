import argparse
import os
import socket
import threading

# Function to start the main server loop
def main(directory):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)     # Create a server socket
    while True:
        conn, _ = server_socket.accept() # Accept client connections
        threading.Thread(target=handle_client, args=(conn, directory)).start() # Start a new thread to handle each client connection

# Function to handle client requests
def handle_client(conn, directory):
    try:
        request_data = conn.recv(1024).decode() # Receive request data from the client
        method, path, *_ = request_data.split("\r\n")[0].split(" ", 2) # Split request lines and parse the request method and path

        # Handle different paths and http methods
        if not path:
            response = build_response(400, "Bad Request")
        elif path.startswith("/echo/"):
            _, _, random_string = path.partition("/echo/")
            response = build_response(200, "OK", "text/plain", random_string)
        elif path == "/":
            response = build_response(200, "OK")
        elif path.startswith("/user-agent"):
            # Extract user agent information
            agent = request_data.split("\r\n")[2].split(": ")[1]
            response = build_response(200, "OK", "text/plain", agent)
        elif path.startswith("/files/"):
            file_name = path[7:]
            if method == "GET":
                # Handle GET request for file retrieval
                if os.path.exists(os.path.join(directory, file_name)):
                    with open(os.path.join(directory, file_name), "r") as f:
                        body = f.read()
                    response = build_response(200, "OK", "application/octet-stream", body)
                else:
                    response = build_response(404, "Not Found")
            elif method == "POST" and len(request_data.split("\r\n")) > 6:
                # Handle POST request for file creation/overwriting
                body = request_data.split("\r\n")[-1]
                with open(os.path.join(directory, file_name), "w") as f:
                    f.write(body)
                response = build_response(201, "Created")
            else:
                response = build_response(400, "Bad Request")
        else:
            response = build_response(404, "Not Found")

    except Exception as e:
        print(f"Error handling client request: {e}")
        response = build_response(500, "Internal Server Error")
    finally:
        # Send response back to the client and close connection
        conn.sendall(response.encode())
        conn.close()

# Function to build HTTP response
def build_response(code, phrase, content_type=None, body=None):
    response = f"HTTP/1.1 {code} {phrase}\r\n"
    if content_type:
        response += f"Content-Type: {content_type}\r\n"
    if body:
       response += f"Content-Length: {len(body)}\r\n\r\n{body}\r\n"
    else:
       response += '\r\n'
    return response

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str, default=None)
    args = parser.parse_args()
    # Start the server
    main(args.directory)
