import ctypes
import json


ws2_32 = ctypes.windll.ws2_32

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345


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

class SocketResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def json(self):
        return self.body

def Send_socket_request(action, email="", password="", username="", newpassword="", confirmpassword="", newusername="", confirmusername=""):
    sock_handle = -1
    try:
        # 1. יצירת סוקט עצמאי דרך ה-Windows API (AF_INET = 2, SOCK_STREAM = 1)
        sock_handle = ws2_32.socket(2, 1, 0)
        if sock_handle == -1 or sock_handle == 0xFFFFFFFF:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Failed to create socket. Error code: {err}")

        # 2. הגדרת כתובת השרת ויציאה לחיבור (connect)
        server_addr = sockaddr_in()
        server_addr.sin_family = 2  # AF_INET
        server_addr.sin_port = ws2_32.htons(SERVER_PORT)
        server_addr.sin_addr = ws2_32.inet_addr(SERVER_IP.encode('utf-8'))

        connect_res = ws2_32.connect(sock_handle, ctypes.byref(server_addr), ctypes.sizeof(server_addr))
        if connect_res == -1:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Connect failed. Error code: {err}")

        
        payload = {
            "Action": action, "Email": email, "Password": password, 
            "Username": username, "Newpassword": newpassword, 
            "Confirmpassword": confirmpassword, "Newusername": newusername, 
            "Confirmusername": confirmusername
        }
        json_data = json.dumps(payload).encode('utf-8')
        
        sent = ws2_32.send(sock_handle, json_data, len(json_data), 0)
        if sent == -1:
            err = ws2_32.WSAGetLastError()
            raise Exception(f"Send failed. Error code: {err}")

        
        buf_size = 4096
        buf = ctypes.create_string_buffer(buf_size)
        received_bytes = ws2_32.recv(sock_handle, buf, buf_size, 0)

        if received_bytes <= 0:
            return None

       
        response_bytes = buf.raw[:received_bytes]

        response_obj = json.loads(response_bytes.decode('utf-8'))
        status_code = response_obj.get("status_code", 500)
        body = response_obj.get("body", {})

        return SocketResponse(status_code, body)

    except Exception as e:
        print("Winsock / Socket error:", e)
        return None
    finally:
        
        if sock_handle != -1 and sock_handle != 0xFFFFFFFF:
            ws2_32.closesocket(sock_handle)


def Register_request(email, password, username):
    return Send_socket_request("Register", email=email, password=password, username=username)

def Login_request(email, password, username):
    return Send_socket_request("Login", email=email, password=password, username=username)

def Change_Password_request(email, newpassword, confirmpassword):
    return Send_socket_request("Changepassword", email=email, newpassword=newpassword, confirmpassword=confirmpassword)

def Change_Username_request(email, password, newusername, confirmusername):
    return Send_socket_request("Changeusername", email=email, password=password, newusername=newusername, confirmusername=confirmusername)

def Delete_Account_request(email, password, username):
    return Send_socket_request("Deleteaccount", email=email, password=password, username=username)

def Login_asGuest_request():
    return Send_socket_request("Loginguest")
