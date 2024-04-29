import socket # low-level networking interface

def main(): # server logic
    print("Logs from your program will appear here!")
    serv_socket = socket.create_server(("localhost", 4221), reuse_port=True) #function to create a server socket, listen on localhost, port 4221

    while True: #loop to keep server running and accepting new connections indefinitely
        try:
            client_conn, client_addr = serv_socket.accept() # function is called again 
            # # returned value is a tuple with two elements: the first is the socket object and the second is the address of the client
            print(f"Connection from {client_addr}")

            # Read data from the connection
            client_request_data = client_conn.recv(1024).decode()
            print(f"Received request: {client_request_data}")
            
            # Extract path from the request
            request_lines = client_request_data.split('\r\n')
            start_line = request_lines[0]
            _, path, _ = start_line.split(' ')
            print(f"Requested path: {path}")
   
            # Extract a random string from the path
            path_parts = path.split('/')
            if len(path_parts) >= 3:
                _, _, random_string = path_parts
                print(f'Random string: {random_string}')
            else:
                random_string = ''
                print('No random string present')

            # Create a reponse body
            response_body = random_string
            
            # Construct the response
            response = (
                f'HTTP/1.1 200 OK\r\n'
                f'Content-Type: text/plain\r\n'
                f'Content-Length: {len(response_body)}\r\n'
                f'\r\n'
                f'{response_body}'
            )
            # Conditional
#            if path == '/':
                 # The \r\n\r\n at the end of the response is required to indicate the end of the HTTP headers according to the HTTP protocol.
 #               http_response = "HTTP/1.1 200 OK\r\n\r\n"
  #          else:
   #             http_response = "HTTP/1.1 404 Not Found\r\n\r\n"  
            # The response.encode() function is used to convert the string into bytes, as the send function requires data to be in bytes.
            client_conn.send(response.encode())    
           
            # Close the connection socket
            client_conn.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
