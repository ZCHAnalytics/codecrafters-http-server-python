import socket # low-level networking interface

def main(): #server logic
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True) #function to create a server socket, listen on localhost, port 4221
    server_socket.accept() # function to wait for client to connect to server before proceeding 
"""
    while True: #loop to keep server running and accepting new connections indefinitely
        try:
            server_socket, client_address = server_socket.accept() # function is called again 
            # # returned value is a tuple with two elements: the first is the socket object and the second is the address of the client
            
            # variable is a string that represents a basic HTTP response indicating a successful request (200 OK). 
            # The \r\n\r\n at the end of the response is required to indicate the end of the HTTP headers according to the HTTP protocol.
            response = "HTTP/1.1 200 OK\r\n\r\n" 
            
            server_socket.send(response.encode())    
            # the server_socket.send function is called to send the response to the client. 
            # The response.encode() function is used to convert the string into bytes, as the send function requires data to be in bytes.
        except Exception as e:
            print(f"An error occurred: {e}")
"""
if __name__ == "__main__":
    main()
