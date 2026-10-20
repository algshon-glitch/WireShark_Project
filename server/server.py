import ctypes
import json
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from better_profanity import profanity
from datetime import datetime
import re 
import uuid 

# 
ws2_32 = ctypes.windll.ws2_32


class WSADATA(ctypes.Structure):
    _fields_ = [
        ("wVersion", ctypes.c_ushort),
        ("wHighVersion", ctypes.c_ushort),
        ("szDescription", ctypes.c_char * 257),
        ("szSystemStatus", ctypes.c_char * 129),
        ("iMaxSockets", ctypes.c_ushort),
        ("iMaxUDPDSeg", ctypes.c_ushort),
        ("lpVendorInfo", ctypes.c_void_p),
    ]

#
class sockaddr_in(ctypes.Structure):
    _fields_ = [
        ("sin_family", ctypes.c_short),
        ("sin_port", ctypes.c_ushort),
        ("sin_addr", ctypes.c_ulong),
        ("sin_zero", ctypes.c_char * 8),
    ]


def _init_winsock():
    wsa_data = WSADATA()
    res = ws2_32.WSAStartup(0x0202, ctypes.byref(wsa_data)) # גרסה 2.2
    if res != 0:
        raise Exception(f"WSAStartup failed with error: {res}")

_init_winsock()

client = MongoClient('mongodb://localhost:27017/') 
data_base = client['User_Data'] 
collection = data_base['Users'] 
profanity.load_censor_words() 
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 

def User_Request(payload): 
    action = payload.get("Action") 
    email = payload.get("Email")
    password = payload.get("Password")
    username = payload.get("Username")
    newpassword = payload.get("Newpassword")
    confirmpassword = payload.get("Confirmpassword")
    newusername = payload.get("Newusername")
    confirmusername = payload.get("Confirmusername")
   
    if action == "Register":
        if not email or not re.match(EMAIL_REGEX, email): 
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}} 

        user_exist = collection.find_one({"Email": email}) 
        if user_exist: 
            return {"status_code": 400, "body": {"Error": "User with email: " + email + " already exists"}} 

        if username and profanity.contains_profanity(username): 
            return {"status_code": 422, "body": {"Error": "Username contains inappropriate language"}}

        username_exist = collection.find_one({"Username": username}) 
        if username_exist:
            return {"status_code": 409, "body": {"Error": "User with user name: " + username + " already exists"}}

        try:
            hasing_password = generate_password_hash(password) 
            collection.insert_one({
                "Email": email, 
                "Password": hasing_password, 
                "Username": username, 
                "First time registed": datetime.now() 
            })
        except Exception as e_r:
            print("Error inserting data into database:", e_r)
            return {"status_code": 500, "body": {"Error": "Server error. please try again later."}} 

        print("Register successfully")
        return {"status_code": 201, "body": {"Message": "Hello " + username + ", it's nice to meet you!"}} 
   
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
        return {"status_code": 200, "body": {"Message": "Welcome back " + username + ", it's nice to see you again!"}}

    elif action == "Changepassword":
        if not email or not re.match(EMAIL_REGEX, email): 
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
        if not email or not re.match(EMAIL_REGEX, email): 
            return {"status_code": 400, "body": {"Error": "Invalid email address format"}}

        user_exist = collection.find_one({"Email": email})
        if not user_exist:
            return {"status_code": 400, "body": {"Error": "This email does not exist."}}

        if not check_password_hash(user_exist["Password"], password):
            return {"status_code": 400, "body": {"Error": "Password is incorecct"}}

        if newusername != confirmusername:
            return {"status_code": 400, "body": {"Error": "usernames do not match each other."}}

        if newusername and profanity.contains_profanity(newusername): 
            return {"status_code": 422, "body": {"Error": "Username contains inappropriate language"}}

        username_exist = collection.find_one({"Username": newusername}) 
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
        return {"status_code": 299, "body": {"Message": "Hello " + guest_username}}


def run_socket_server():
    server_socket = -1
    try:
        # 1. יצירת סוקט שרת דרך ה-Windows API
        server_socket = ws2_32.socket(2, 1, 0) # AF_INET = 2, SOCK_STREAM = 1
        if server_socket == -1 or server_socket == 0xFFFFFFFF:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Failed to create server socket. Error: {err}")

        # 2. הגדרת SO_REUSEADDR למניעת שגיאת Address already in use
        optval = ctypes.c_int(1)
        ws2_32.setsockopt(server_socket, 0xFFFF, 0x0004, ctypes.byref(optval), ctypes.sizeof(optval))

        # 3. Bind לכתובת ולפורט
        server_addr = sockaddr_in()
        server_addr.sin_family = 2  # AF_INET
        server_addr.sin_port = ws2_32.htons(12345)
        server_addr.sin_addr = ws2_32.inet_addr("127.0.0.1".encode('utf-8'))

        bind_res = ws2_32.bind(server_socket, ctypes.byref(server_addr), ctypes.sizeof(server_addr))
        if bind_res == -1:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Bind failed. Error: {err}")

        # 4. Listen (האזנה לחיבורים נכנסים עם תור של עד 5 לקוחות)
        listen_res = ws2_32.listen(server_socket, 5)
        if listen_res == -1:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Listen failed. Error: {err}")

        print("Winsock Socket Server is running and listening on port 12345...")

        while True:
            # 5. Accept (קבלת חיבור מלקוח חדש)
            client_socket = ws2_32.accept(server_socket, None, None)
            if client_socket == -1 or client_socket == 0xFFFFFFFF:
                continue

            try:
                # קבלת הנתונים לתוך באפר של C
                buf_size = 4096
                buf = ctypes.create_string_buffer(buf_size)
                received_bytes = ws2_32.recv(client_socket, buf, buf_size, 0)

                if received_bytes <= 0:
                    ws2_32.closesocket(client_socket)
                    continue

                data_bytes = buf.raw[:received_bytes]
                payload = json.loads(data_bytes.decode('utf-8'))
                
               
                response_dict = User_Request(payload) 

                response_json = json.dumps(response_dict).encode('utf-8')
                ws2_32.send(client_socket, response_json, len(response_json), 0)

            except Exception as e:
                print("Error handling client connection:", e)
            finally:
                ws2_32.closesocket(client_socket)

    except Exception as e:
        print("Server error:", e)
    finally:
        if server_socket != -1 and server_socket != 0xFFFFFFFF:
            ws2_32.closesocket(server_socket)


if __name__ == '__main__': 
    run_socket_server()

    


    


    


    
    
    
    




     



    



          
    
          
