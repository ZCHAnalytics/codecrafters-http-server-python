import socket

def main():
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print('...  Starting the "while True" block...\n')
    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f'Accepting the connection from client at this address {client_address}')

        print('...  ... Starting the "try" block inside the "while" block\n')    
        try:
            # Read data from the connection
            client_request_data = client_connection.recv(1024).decode()
            print(f'Decoded request received from client: {client_request_data}')

            # Extract path from the request
            _, _, user_agent = client_request_data.split(" ")
            print(f'Extracted User Agent from the request: {user_agent}')

            print('...  ... ... Starting "If" block\n')
            if  user_agent == '*curl*':
                curl_string = user_agent.split(" ")
                print(f'           Preparing curl http response')
                http_response = (f'HTTP/1.1 200 OK\r\nContent_type: text/plain\r\nContent-Length: len({curl_string})\r\n\r\n{curl_string}')
            else:
                print(f'Requsted path not found, returning 404 error')
                http_response = 'HTTP/1.1 404 Not Found\r\n\r\n'

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
