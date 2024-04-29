import socket

def main():
    print("Logs from your program will appear here!")
    serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        try:
            client_conn, client_addr = serv_socket.accept()
            print(f"Connection from {client_addr}")

            # Read data from the connection
            client_request_data = client_conn.recv(1024).decode()
            print(f"Received request: {client_request_data}")
            
            # Extract path from the request
            request_lines = client_request_data.split('\r\n')
            start_line = request_lines[0]
            _, path, _ = start_line.split(' ')
            print(f"Requested path: {path}")

            # Check if the path starts with '/echo/'
            if path.startswith('/echo/'):
                # Extract the random string from the path
                _, _, random_string = path.split('/')
                print(f'Random string: {random_string}')

                # Create a response body
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
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
   
            # Send the response
            client_conn.send(response.encode())    
           
            # Close the connection socket
            client_conn.close()

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
