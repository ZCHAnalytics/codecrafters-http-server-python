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

            # Split request into lines 
            print(f'Splitting http request lines into lines')
            request_lines = client_request_data.split("\r\n")
            print(f'    Http request lines split as: {request_lines}')
            
            # Extract user-agent line
            print('    extracting the last line of http request')
            user_agent_line = request_lines[2] if len(request_lines) >= 3 else None
            print('     last line with user agent extracted')
           
            print('...  ... ... Starting "If" block\n') 
            if user_agent_line:
                print(f'Value of User-Agent extracted and is: {user_agent_line.split(": ")[1]}\n')
            else:
                print("User-Agent header not found in the request\n")

            http_response = (f'HTTP/1.1 200 OK\r\n\r\n')
            
            # Extracting value of User-Agent and including it in the response
            print('     Extracting value of User-Agent\n')
            user_agent_value = user_agent_line.split(": ")[1] if user_agent_line else "Unknown"

            http_response += f"Content-Length: {len(user_agent_value)}\r\n\r\n{user_agent_value}"
                     
            # Send the response back
            print('Sending the response back and putting the kettle on')
            client_connection.send(http_response.encode())

        except Exception as e:
            print(f'Throwing my hands in the air - an error occurred: {e}')

        finally:
            # Close the connection socket
            print("Closing the client connection and going to bed")
            client_connection.close()

if __name__ == "__main__":
    main()
