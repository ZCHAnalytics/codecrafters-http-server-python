import socket
import threading
import os

def parsing_requests(client_connection, directory):
    try:
        request_data = client_connection.recv(1024).decode()
        request_lines = request_data.split("\r\n")
        path = request_lines[0].split(" ")[1]
        print(path)
    
        if len(request_lines) >= 3:
            agent = request_lines[2].split(": ")[1]
            print(agent)
        else:
            print("Request data does not contain enough lines")
    
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
            # extract file name
            file_name = path.split("/")[-1]
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                print(f' the content of the file:{file_name}')
                with open(file_path, "rb") as file:
                    file_content = file.read()
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content.decode()}'
        else:
            print(f"Requsted path not found, returning 404 error")
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        
        # Send the response back
        client_connection.sendall(http_response.encode())
 
    except Exception as e:
        print(f"Throwing my hands in the air - an error occurred: {e}")
    finally:
        # Close the connection socket
        print("Closing the client connection and going to bed")
        client_connection.close()

def main(directory):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=parsing_requests, args=(client_connection, directory))
        client_thread.start()
        
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="My HTTP Server")
    parser.add_argument("--directory", required=True, help="Directory with files")
    args = parser.parse_args()

    main(args.directory)