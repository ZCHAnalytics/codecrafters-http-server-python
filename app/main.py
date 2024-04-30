import socket

def main():
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f"My while true block starts here and gives the connection from {client_address}")

        try:
            # Read data from the connection        
            client_request_data = client_connection.recv(1024).decode()
            print(f"My try block that decodes the data from the received request: {client_request_data}")

            # Extract path from the request
            _, path, _ = client_request_data.split(" ", 2)
            print(f"This block extractds the path from the multi-line request data which is: {path}")

            if path.startswith("/echo/"):
                random_string = path.split("/")[-1]
                print(f'If the path has echo that the random string in the extracted path is: {random_string}')
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}'
            elif path == "/":
                print(f'If the path only has forward slash and now echom then the random string in the extracted path is: {random_string}')
                http_response = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                print(f'If the path has no echo or string, that it is an ultimate failure and the random string in the extracted path is still is: {random_string}')
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

            # Send the response back
            client_connection.send(http_response.encode())

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the connection socket
            client_connection.close()

    my_serv_socket.close()

if __name__ == "__main__":
    main()
