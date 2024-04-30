import socket

def main():
    print("Logs from your program will appear here!")
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        try:
            client_conn, client_addr = my_serv_socket.accept()
            print(f"The connection from {client_addr}")
            # Read data from the connection        
            client_request_data = client_conn.recv(1024).decode()
            print(f"Received request: {client_request_data}")

            # Extract path from the request
            http_request_data = client_request_data.split("\r\n")
            first_line = http_request_data[0]
            method, path, version = first_line.split(" ")
            
            print(f"The extracted path is: {path}")
            random_string = ""

            # Conditional
            # Conditional
            if path.startswith("/echo/"):
                # Extract the random string from the path
                _, _, random_string = path.partition('/echo/')
                print(f'The random string in the extracted path is: {random_string}')

                # Create a response body
                print("this is the outcome of response_body=random_string")
                response_body = random_string

                # Construct the response
                http_response = (
                    f'HTTP/1.1 200 OK\r\n'
                    f'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(response_body)}\r\n'
                    f'\r\n'
                    f'{response_body}'
                )
            elif path == "/":
                # The \r\n\r\n at the end of the response is required to indicate the end of the HTTP headers according to the HTTP protocol.
                http_response = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                # Respond with 404 Not Found for other paths
                print("this is the outcome of else operation")
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

            # Send the response
            client_conn.send(http_response.encode())    
            # Close the connection socket
            client_conn.close()

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
