import socket
import threading
import os
import argparse

def main(directory):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, directory))
        client_thread.start()
        
def handle_client(client_connection, directory):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")

        if len(request_lines) < 1:
            response = build_response(400, "Bad Request")
        else:
            method, path, _ = request_lines[0].split(" ", 2)

            if path.startswith("/echo/"):
                _, _, random_string = path.partition("/echo/")
                response = extract_info(random_string, 'text/plain', random_string)

            elif path == "/":
                response = build_response(200, "OK", content_type="text/html", body="<h1>Welcome to the server!</h1>")

            elif path.startswith("/user-agent") and len(request_lines) >= 3:
                agent_line = request_lines[2]
                response = extract_info(agent_line.split(": ")[1], 'text/plain', agent_line.split(": ")[1])

            elif path.startswith("/files/"):
                file_name = path[7:]
                
                if method == "GET":
                    if os.path.exists(os.path.join(directory, file_name)):
                        with open(os.path.join(directory, file_name), "rb") as f:
                            body = f.read()
                        response = build_response(200, "OK", "application/octet-stream", body)
                    else:
                        response = build_response(404, "Not Found")
                
                elif method == "POST":
                    if len(request_lines) > 6:
                        body = request_lines[-1]
                        with open(os.path.join(directory, file_name), "wb") as f:
                            f.write(body.encode())
                        response = build_response(201, "Created")
                    else:
                        response = build_response(400, "Bad Request")

                else:
                    response = build_response(405, "Method Not Allowed")

            else:
                response = build_response(404, "Not Found")

    except Exception as e:
        print(f"Error handling client request: {e}")
        response = build_response(500, "Internal Server Error")
    finally:
        client_connection.sendall(response.encode())
        client_connection.close()

def extract_info(info, content_type, response_body):
    return build_response(200, 'OK', content_type, response_body)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str, default=None)
    args = parser.parse_args()
    main(args.directory)
