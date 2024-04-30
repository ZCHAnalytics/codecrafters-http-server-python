import socket

def main():
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print('...  Starting the "while True" block...\n')
    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f'Accepting the connection from client at this address {client_address}\n')

        print('...  ... Starting the "try" block inside the "while" block\n')    
        try:
            # Read data from the connection
            client_request_data = client_connection.recv(1024).decode()
            print(f'Decoded request received from client: {client_request_data}')

            # Split http request into separate lines 
            print(f'Let us splitting http request lines into separate lines!')
            request_lines = client_request_data.split("\r\n")
            print(f'    Http request lines split as: {request_lines}')
            
            # Extract user-agent line
            print('    Let us extract the User-Agent line from the http request')
            user_agent_line = request_lines[2] if len(request_lines) >= 3 else None
            print('      Hurray! There is a user agent line!')
           
            print('...  ... ... Starting the "If" block inside the "Try" block\n') 
            if user_agent_line:
                content = user_agent_line.split(": ")[1]
                print(f'Value of User-Agent extracted and is: {content}\n')
                print(f'Value of User-Agent in length is: {len(content)}\n')
            else:
                print("User-Agent header not found in the request\n")

            http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(content)}\r\n\r\n{content}'.encode()
            # Send the response back
            print('Sending the response back and putting the kettle on')
            client_connection.send(http_response.encode('utf-8'))

        except Exception as e:
            print(f'Throwing my hands in the air - an error occurred: {e}')

        finally:
            # Close the connection socket
            print("Closing the client connection and going to bed")
            client_connection.close()

if __name__ == "__main__":
    main()
