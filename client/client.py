import requests

email = input("Enter your email: ") # User email input
password = input("Enter your password: ") # User password input

Server_Url = "http://localhost:5000" # The URL of the server to which the request will be sent

payload = {"email": email, "password": password} # what will be sent to the server in the request

r = requests.post(Server_Url, json=payload) # Send a POST request to the server 

def Check_Response(): # func tion to check the response from the server
    if r.status_code == 200: # login successful
        print("Login successful.")
        print(r.json())  # Print the response from the server
       

    elif r.status_code == 401: # server does not recognize the user
        print("Email or password is incorrect.")

    elif r.status_code == 500: # server error
        print("Server error. Please try again later.") 

    else: # other unexpected status codes
        print("Unexpected error. Status code: " + str(r.status_code))     

Check_Response()  

