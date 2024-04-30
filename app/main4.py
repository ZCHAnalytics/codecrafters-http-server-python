import socket

def main():
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print('...  Starting the "while True" block...')
    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f'Accepting the connection from client at this address {client_address}')

        print('...  ... Starting the "try" block inside the "while" block')    
        try:
            # Read data from the connection
            client_request_data = client_connection.recv(1024).decode()
            print(f'Decoded request received from client: {client_request_data}')

            # Extract path from the request
            _, path, _ = client_request_data.split(" ", 2)
            print(f'Extracted path from the request: {path}')

            print('...  ... ... Starting "If" block')
            if path.startswith("/echo/"):
                random_string = path.split("/")[-1]
                print(f'Extracted random string from path: {random_string}')
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}'
            elif path == "/":
                print(f'No specific path provided, so returning the default respose')
                http_response = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                print(f'Requsted path not found, returning 404 error')
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

            # Send the response back
            print("Sending the response back and putting the kettle on")
            client_connection.send(http_response.encode())

        except Exception as e:
            print(f'Throwing my hands in the air - an error occurred: {e}')

        finally:
            # Close the connection socket
            print("Closing the client connection and going to bed")
            client_connection.close()

if __name__ == "__main__":
    main()
