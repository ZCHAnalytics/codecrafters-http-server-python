import socket

def main():
    print("Logs from your program will appear here!")
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f"The connection from {client_address}")

        try:
            # Read data from the connection        
            client_request_data = client_connection.recv(1024).decode()
            print(f"Received request: {client_request_data}")

            # Extract path from the request
            _, path, _ = client_request_data.split(" ", 2)
            print(f"The extracted path is: {path}")

            # Conditional
            if path.startswith("/echo/"):
                random_string = path.split("/")[-1]
                print(f'The random string in the extracted path is: {random_string}')
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}'
            elif path == "/":
                http_response = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                print("this is the outcome of else operation")
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

            # Send the response
            client_connection.send(http_response.encode())

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the connection socket
            client_connection.close()

    my_serv_socket.close()

if __name__ == "__main__":
    main()
