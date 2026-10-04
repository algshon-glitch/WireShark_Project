import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

class SocketResponse:
    def __init__(self, status_code, body): # class that gets response from the server
        self.status_code = status_code # code like: 200 or 400
        self.body = body # data fro server

    def json(self): # func to data to client_ui
        return self.body

def Send_socket_request(action, email="", password="", username="", newpassword="", confirmpassword="", newusername="", confirmusername=""): # func to send request to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP protocol stream to send data to server
        client_socket.connect((SERVER_IP, SERVER_PORT))  # connect to the ip pf the server and the port it works on

        payload = {"Action": action, "Email": email, "Password": password, "Username": username, "Newpassword": newpassword, "Confirmpassword": confirmpassword, "Newusername": newusername, "Confirmusername": confirmusername}  # what data will be sent
        json_data = json.dumps(payload) # put the payload in json files
        client_socket.sendall(json_data.encode('utf-8')) # encoding json data to bytes to stream them in the socket

        response_bytes = client_socket.recv(4096) # get response in bytes untill 4096 bytes
        client_socket.close() # close socket data transfer finished

        if not response_bytes: # if there is no response from the server
            return None

        response_obj = json.loads(response_bytes.decode('utf-8')) # decoding the response from bytes to json
        status_code = response_obj.get("status_code", 500) # searching for key word "status code" if something wrong its error 500
        body = response_obj.get("body", {}) # searching for key word "body" if something wrong put None

        return SocketResponse(status_code, body) # return to class with status code and body to sent to client_ui
    except Exception as e: # catch the error if there is and print it so it wont crush
        print("Socket error:", e)
        return None # 
def Register_request(email, password, username): # this func and the other one are used by client_ui
    return Send_socket_request("Register", email=email, password=password, username=username)

def Login_request(email, password, username):
    return Send_socket_request("Login", email=email, password=password, username=username)

def Change_Password_request(email, newpassword, confirmpassword):
    return Send_socket_request("Changepassword", email=email, newpassword=newpassword, confirmpassword=confirmpassword)

def Change_Username_request(email, password ,newusername, confirmusername):
    return Send_socket_request("Changeusername", email=email ,password=password, newusername=newusername, confirmusername=confirmusername)

def Delete_Account_request(email, password, username):
    return Send_socket_request("Deleteaccount", email=email, password=password, username=username)

def Login_asGuest_request():
    return Send_socket_request("Loginguest")

   
