import socket
import json
from pymongo import MongoClient # my datebase (NoSQL)
from werkzeug.security import check_password_hash, generate_password_hash
from better_profanity import profanity
from datetime import datetime
import re
import uuid



client = MongoClient('mongodb://localhost:27017/') # create a connection to the MongoDB server running on localhost at port 27017

data_base = client['User_Data'] # create a database named 'User_Data'

collection = data_base['Users'] # create a collection named 'Users' in the 'User_Data' database
profanity.load_censor_words() # 
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # this is to check if the email user written is correct 

def User_Request(payload): # func that handles user request
    action = payload.get("Action") # action like register/login
    email = payload.get("Email")
    password = payload.get("Password")
    username = payload.get("Username")
    newpassword = payload.get("Newpassword")
    confirmpassword = payload.get("Confirmpassword")
    newusername = payload.get("Newusername")
    confirmusername = payload.get("Confirmusername")
   

    if action == "Register":
        if not email or not re.match(EMAIL_REGEX, email): # checking if the email is correct based on EMAIL_REGEX
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}} # if not return 400 code

        user_exist = collection.find_one({"Email": email}) # seraching for the email user have puten on register
        if user_exist: # if there is
            return {"status_code": 400, "body": {"Error": "User with email: " + email + " already exists"}} # 

        if username and profanity.contains_profanity(username): # if the username contains bad words it wont let him register
            return {"status_code": 422, "body": {"Error": "Username contains inappropriate language"}}

        username_exist = collection.find_one({"Username": username}) # same as email but username
        if username_exist:
            return {"status_code": 409, "body": {"Error": "User with user name: " + username + " already exists"}}

        try:
            hasing_password = generate_password_hash(password) # hashing the password and than putting it database
            collection.insert_one({
                "Email": email, 
                "Password": hasing_password, 
                "Username": username, 
                "First time registed": datetime.now() # the time that the user have registered
            })
        except Exception as e_r:
            print("Error inserting data into database:", e_r)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}} # if there is any server happened

        print("Register successfully")
        return {"status_code": 201, "body": {"Message": "You have registered successfully"}} # if all is good user have registered successfully

   
    elif action == "Login":

        if not email or not re.match(EMAIL_REGEX, email):
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}}

        try:
            user_data = collection.find_one({"Email": email, "Username": username})
        except Exception as e_l:
            print("Error searching data in database:", e_l)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}

        if not user_data or not check_password_hash(user_data["Password"], password):
            return {"status_code": 401, "body": {"Error": "Email or password or username is incorrect or not registed."}}

        try:
            collection.update_one(
                {"Email": email},
                {"$set": {"Last_Login": datetime.now()}}
            )
        except Exception as e_update:
            print("Error updating last login time:", e_update)

        print("Login successfully")
        return {"status_code": 200, "body": {"Message": "You have logged in successfully"}}

    elif action == "Changepassword":
        if not email or not re.match(EMAIL_REGEX, email): # checking if the email is correct based on EMAIL_REGEX
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}}

        user_exist = collection.find_one({"Email": email})
        if not user_exist:
            return {"status_code": 400, "body": {"Error": "This email does not exist."}}

        if newpassword != confirmpassword:
            return {"status_code": 400, "body": {"Error": "password do not match each other."}}

        try:
            hashingnew_password = generate_password_hash(newpassword)
            collection.update_one(
                {"Email": email},
                {"$set": {"Password": hashingnew_password}}
            )
        except Exception as e:
            print("Error updating new password:", e)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}
        print("Password change successfull")
        return {"status_code": 200, "body": {"Message": "You have changed your password successfully"}}

    elif action == "Changeusername":
        if not email or not re.match(EMAIL_REGEX, email): # checking if the email is correct based on EMAIL_REGEX
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}}

        user_exist = collection.find_one({"Email": email})
        if not user_exist:
            return {"status_code": 400, "body": {"Error": "This email does not exist."}}

        if not check_password_hash(user_exist["Password"], password):
            return {"status_code": 400, "body": {"Error": "Password is incorecct"}}

        if newusername != confirmusername:
            return {"status_code": 400, "body": {"Error": "usernames do not match each other."}}

        if newusername and profanity.contains_profanity(newusername): # if the username contains bad words it wont let him register
            return {"status_code": 422, "body": {"Error": "Username contains inappropriate language"}}

        username_exist = collection.find_one({"Username": newusername}) # same as email but username
        if username_exist:
            return {"status_code": 409, "body": {"Error": "User with user name: " + username + " already exists"}}

        try:

            collection.update_one(
                {"Email": email},
                {"$set": {"Username": newusername}}
            )

        except Exception as e:
            print("Error updating new username:", e)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}
        print("Username change successfull")
        return {"status_code": 200, "body": {"Message": "You have changed your username successfully"}}

    elif action == "Deleteaccount":
        if not email or not re.match(EMAIL_REGEX, email):
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}}

        try:
            user_data = collection.find_one({"Email": email, "Username": username})
        except Exception as e:
            print("Error searching in the data base:", e)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}

        if not user_data or not check_password_hash(user_data["Password"], password):
             return {"status_code": 401, "body": {"Error": "Email or password or username is incorrect or not registed."}}

        try:
            collection.find_one_and_delete({"Email": email})
        except Exception as e:
            print("Error deleting an account:", e)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}
        print("Account have been deleted")
        return {"status_code": 200, "body": {"Message": "You have deleted your account successfully"}}

    elif action == "Loginguest":
        try:
            guest_username = f"Guest_{uuid.uuid4().hex[:6]}"
        except Exception as e:
            print("Error guest login:", e)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}}
        print("User Loged in as a guest successfully")
        return {"status_code": 200, "body": {"Message": "You have logged in successfully your user name is " + guest_username}}
        
        
            


        



            

            


        




            


        
        


        

        

        


   



       
            

        
            

        



def run_socket_server(): # def to run the socket connection
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # start the TCP protocol stream AF_INET IS IPV4
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #  setting the socket settings (not tcp) so error "ALREADY IN USE" wont happen when restarting the server
    server_socket.bind(('127.0.0.1', 12345)) # binding the ip with the port
    server_socket.listen(5) # 5 people wait in line at max
    print("Socket Server is running and listening on port 12345...")
    

    while True: # infinty loop so server will work always
        client_socket, client_address = server_socket.accept() # accepting a new socket to speak with the client and the client ip address
        try:
            
            data_bytes = client_socket.recv(4096) # recving the data from the client in bytes max 4096 bytes
            if not data_bytes: # if client close connection
                client_socket.close() # close the socket
                continue # go back to wait for another client

            
            payload = json.loads(data_bytes.decode('utf-8')) # if client did not disconnect decoding from bytes to json files
            
           
            response_dict = User_Request(payload) # sending users data to func of the request to check for things

            
            client_socket.sendall(json.dumps(response_dict).encode('utf-8')) # sending the response in bytes to client

        except Exception as e:
            print("Error handling client connection:", e)
        finally:
            client_socket.close() # close the socket when done speaking with the client 


if __name__ == '__main__': 
    run_socket_server()
    
