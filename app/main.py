import socket

def main():
    print("Logs from your program will appear here!")
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        try:
            client_conn, client_addr = my_serv_socket.accept()
            print(f"The connection from {client_addr}")

            # Read data from the connection
            read_client_data = client_conn.recv(1024).decode()
            print(f"The received request: {read_client_data}")
            
            # Extract path from the request
            client_request_lines = read_client_data.split('\r\n')
            start_line = client_request_lines[0]
            _, path, _ = start_line.split(' ')
            print(f"The requested path is: {path}")

            # Check if the path starts with '/'
            if path.startswith('/'):
                # Extract the random string from the path
                _, _, random_string = path.split('/')
                print(f'The random string: {random_string}')

                # Create a response body
                print("this is the outcome of response_body=random_string")
                response_body = random_string

                # Construct the response
                response = (
                    f'HTTP/1.1 200 OK\r\n'
                    f'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(response_body)}\r\n'
                    f'\r\n'
                    f'{response_body}'
                )
            else:
                # Respond with 404 Not Found for other paths
                print("this is the outcome of else operation")
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
   
            # Send the response
            client_conn.send(response.encode())    
            # Close the connection socket
            client_conn.close()

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
