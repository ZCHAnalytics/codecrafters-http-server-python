import socket

def main():
    my_serv_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print('...  Starting the "while True" block...\n')
    while True:
        client_connection, client_address = my_serv_socket.accept()
        print(f'Accepting the connection from client at this address {client_address}\n') ##

        print('...  ... Starting the "try" block inside the "while" block\n')    ##
        try:
            # Read data from the connection
            client_request_data = client_connection.recv(1024).decode()
            print(f'Decoded request received from client: {client_request_data}\n\n') ##

            # Split http request into separate lines 
            print('Let us splitting http request lines into separate lines!\n')
            request_lines = client_request_data.split("\r\n")
            print(f'    Http request lines split as: {request_lines}\n')      
            
            # Extract the path from the request
            first_line = request_lines[0]
            _, path, _ = first_line.split(" ")

            # Select 3rd line 

            print('...  ... ... Starting "If" block')
            if 'echo' in path:
                random_string = path.split("/")[-1]
                print(f'Extracted random string from path: {random_string}')
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}'
            elif 'User-Agent' in request_lines[2]:
                content = request_lines[2].split(": ")[1]
                print(f'Value of User-Agent extracted and is: {content}\n')
                # Exclude the version number from the User-Agent value
                #content_lengthhout_version = content_with_version.split('/')[0]
                # Calculate the length of the extracted User-Agent substring
                #content_length = len(content_without_version.encode('utf-8'))   
                # print(f'Value of User-Agent extracted and is: {content_with_version}\n')
                #print(f'Value of User-Agent in length is: {len(content_without_version)}\n')
                http_response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}'
            elif path == '/':
                print(f'No specific path provided, so returning the default respose')
                http_response = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                print(f'Requsted path not found, returning 404 error')
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

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
