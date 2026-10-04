import sys
from PySide6.QtWidgets import (QApplication, QMessageBox, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QMainWindow, QCheckBox, QHBoxLayout)
from client import Login_request, Register_request, Change_Password_request, Change_Username_request, Delete_Account_request, Login_asGuest_request
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon


class DeleteAccount_Window(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Delete Account page")
      self.resize(600, 400)
      central_widget = QWidget()
      self.setCentralWidget(central_widget)

      layout = QVBoxLayout(central_widget)
      label = QLabel("DELETE ACCOUNT")
      label.setStyleSheet("color: blue; font-size: 34px; font-weight: bold;")
      label.setAlignment(Qt.AlignCenter)
      layout.addWidget(label, alignment=Qt.AlignTop)

      self.email_input = QLineEdit()
      self.email_input.setMaxLength(254)
      self.email_input.setPlaceholderText("Enter your email")
      layout.addWidget(self.email_input, alignment=Qt.AlignTop)

      self.password_input = QLineEdit()
      self.password_input.setMaxLength(50)
      self.password_input.setPlaceholderText("Enter your password")
      self.password_input.setEchoMode(QLineEdit.Password)
      layout.addWidget(self.password_input, alignment=Qt.AlignTop)

      

      self.eye_action = QAction(QIcon("eye.png"), "", self)
      self.eye_action.triggered.connect(self.password_view)
      self.password_input.addAction(self.eye_action, QLineEdit.TrailingPosition)

      self.username_input = QLineEdit()
      self.username_input.setMaxLength(20)
      self.username_input.setPlaceholderText("Enter your Username")
      layout.addWidget(self.username_input, alignment=Qt.AlignTop)

      self.rt = None

      self.submit_btn = QPushButton("Delete")
      self.submit_btn.setStyleSheet("background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.submit_btn)
      self.submit_btn.clicked.connect(self.Outputs_deleteaccount)

      self.BaCk_btn = QPushButton("Back to login page")
      self.BaCk_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.BaCk_btn)
      self.BaCk_btn.clicked.connect(self.BACK_W)
      layout.addStretch()
   def password_view(self):
      if self.password_input.echoMode() == QLineEdit.Password:
         self.password_input.setEchoMode(QLineEdit.Normal)
         self.eye_action.setIcon(QIcon("hidden.png"))

      else:
         self.password_input.setEchoMode(QLineEdit.Password)
         self.eye_action.setIcon(QIcon("eye.png"))

   def Outputs_deleteaccount(self):
      email = self.email_input.text()
      password = self.password_input.text() 
      username = self.username_input.text()
      response = Delete_Account_request(email, password, username)

      if not email or not password or not username:
         QMessageBox.warning(self, "Error", "Please fiil all the fields")
         return

      elif response.status_code == 400:
         data = response.json()
         error_msg = data.get("Error", "Account delte failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 500:
          data = response.json()
          error_msg = data.get("Error", "Account delte failed")
          QMessageBox.warning(self, "Error", error_msg)
          return

      elif response.status_code == 401:
         data = response.json()
         error_msg = data.get("Error", "Account delte failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 200:
         data = response.json()
         success_msg = data.get("Message", "You have deleted your account")
         QMessageBox.information(self, "Message", success_msg)

      else:
         data = response.json()
         error_msg = data.get("Error", "deleting account failed")   
         QMessageBox.warning(self, "Error", error_msg)
         return
   def BACK_W(self):
      if self.rt is None:
         self.rt = MainWindow()
         self.rt.show()
         self.hide()














class ForgotUsername_Window(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Forgot username page")
      self.resize(600, 400)
      central_widget = QWidget()
      self.setCentralWidget(central_widget)

      layout = QVBoxLayout(central_widget)
      label = QLabel("USER SET NEW USERNAME")
      label.setStyleSheet("color: blue; font-size: 34px; font-weight: bold;")
      label.setAlignment(Qt.AlignCenter)
      layout.addWidget(label, alignment=Qt.AlignTop)

      self.email_input = QLineEdit()
      self.email_input.setMaxLength(254)
      self.email_input.setPlaceholderText("Enter your email")
      layout.addWidget(self.email_input, alignment=Qt.AlignTop)

      self.password_input = QLineEdit()
      self.password_input.setMaxLength(50)
      self.password_input.setPlaceholderText("Enter your password")
      self.password_input.setEchoMode(QLineEdit.Password)
      layout.addWidget(self.password_input, alignment=Qt.AlignTop)

      self.eye_action = QAction(QIcon("eye.png"), "", self)
      self.eye_action.triggered.connect(self.password_view)
      self.password_input.addAction(self.eye_action, QLineEdit.TrailingPosition)

      self.qa = None



      self.newusername_input = QLineEdit()
      self.newusername_input.setMaxLength(20)
      self.newusername_input.setPlaceholderText("Enter your new Username")
      
      layout.addWidget(self.newusername_input, alignment=Qt.AlignTop)

      self.confirm_newusername_input = QLineEdit()
      self.confirm_newusername_input.setMaxLength(20)
      self.confirm_newusername_input.setPlaceholderText("Enter your new Username again to confirm")
     
      layout.addWidget(self.confirm_newusername_input, alignment=Qt.AlignTop)

      self.submit_btn = QPushButton("Confirm")
      self.submit_btn.setStyleSheet("background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.submit_btn)
      self.submit_btn.clicked.connect(self.Outputs_forgotusername)

      self.BACK_btn = QPushButton("Back to login page")
      self.BACK_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.BACK_btn)
      self.BACK_btn.clicked.connect(self.Show_Wm)
      
      layout.addStretch()
   def password_view(self):
     if self.password_input.echoMode() == QLineEdit.Password:
        self.password_input.setEchoMode(QLineEdit.Normal)
        self.eye_action.setIcon(QIcon("hidden.png"))

     else:
        self.password_input.setEchoMode(QLineEdit.Password)
        self.eye_action.setIcon(QIcon("eye.png"))





   def Outputs_forgotusername(self):
      email = self.email_input.text()
      password = self.password_input.text()
      newusername = self.newusername_input.text()
      confirmusername = self.confirm_newusername_input.text()
      response = Change_Username_request(email, password ,newusername, confirmusername)

      if not email or not password or not newusername or not confirmusername:
         QMessageBox.warning(self, "Error", "please fill all the fields!")
         return

      elif response.status_code == 400:
         data = response.json()
         error_msg = data.get("Error", "Username change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 422:
         data = response.json()
         error_msg = data.get("Error", "Username change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 409:
         data = response.json()
         error_msg = data.get("Error", "Username change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 500:
         data = response.json()
         error_msg = data.get("Error", "Username change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 200:
         data = response.json()
         success_msg = data.get("Message", "You have changed your username successfully")
         QMessageBox.information(self, "Message", success_msg)

      else:
         data = response.json()
         error_msg = data.get("Error", "Username change failed")   
         QMessageBox.warning(self, "Error", error_msg)
         return
   def Show_Wm(self):
      if self.qa is None:
         self.qa = MainWindow()
         self.qa.show()
         self.hide()


      


      








class ForgotPassword_Window(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Forgot password page")
      self.resize(600, 400)
      central_widget = QWidget()
      self.setCentralWidget(central_widget)

      layout = QVBoxLayout(central_widget)
      label = QLabel("USER SET NEW PASSWORD")
      label.setStyleSheet("color: blue; font-size: 34px; font-weight: bold;")
      label.setAlignment(Qt.AlignCenter)
      layout.addWidget(label, alignment=Qt.AlignTop)

      self.email_input = QLineEdit()
      self.email_input.setMaxLength(254)
      self.email_input.setPlaceholderText("Enter your email")
      layout.addWidget(self.email_input, alignment=Qt.AlignTop)

      self.newpassword_input = QLineEdit()
      self.newpassword_input.setMaxLength(50)
      self.newpassword_input.setPlaceholderText("Enter your new Password")
      self.newpassword_input.setEchoMode(QLineEdit.Password)
      layout.addWidget(self.newpassword_input, alignment=Qt.AlignTop)

      self.eye_action = QAction(QIcon("eye.png"), "", self)
      self.eye_action.triggered.connect(self.password_view)
      self.newpassword_input.addAction(self.eye_action, QLineEdit.TrailingPosition)
              

      self.confirm_newpassword_input = QLineEdit()
      self.confirm_newpassword_input.setMaxLength(50)
      self.confirm_newpassword_input.setPlaceholderText("Enter your new Password again to confirm")
      self.confirm_newpassword_input.setEchoMode(QLineEdit.Password)
      layout.addWidget(self.confirm_newpassword_input, alignment=Qt.AlignTop)

      self.eye_action2 = QAction(QIcon("eye.png"), "", self)
      self.eye_action2.triggered.connect(self.password_view2)
      self.confirm_newpassword_input.addAction(self.eye_action2, QLineEdit.TrailingPosition)
              

      self.mwq = None

      self.submit_btn = QPushButton("Confirm")
      self.submit_btn.setStyleSheet("background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.submit_btn)
      self.submit_btn.clicked.connect(self.Outputs_forgotpassword)

      self.back1_btn = QPushButton("Back to login page")
      self.back1_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
      layout.addWidget(self.back1_btn)
      self.back1_btn.clicked.connect(self.BacK_W)

      layout.addStretch()

   def password_view(self):
      if self.newpassword_input.echoMode() == QLineEdit.Password:
         self.newpassword_input.setEchoMode(QLineEdit.Normal)
         self.eye_action.setIcon(QIcon("hidden.png"))
      else:
         self.newpassword_input.setEchoMode(QLineEdit.Password)
         self.eye_action.setIcon(QIcon("eye.png"))

   def password_view2(self):
      if self.confirm_newpassword_input.echoMode() == QLineEdit.Password:
         self.confirm_newpassword_input.setEchoMode(QLineEdit.Normal)
         self.eye_action2.setIcon(QIcon("hidden.png"))
      else:
         self.confirm_newpassword_input.setEchoMode(QLineEdit.Password)
         self.eye_action2.setIcon(QIcon("eye.png"))




   def Outputs_forgotpassword(self):
      email = self.email_input.text()
      newpassword = self.newpassword_input.text()
      confirmpassword = self.confirm_newpassword_input.text()
      response = Change_Password_request(email, newpassword, confirmpassword)  

      if not email or not newpassword or not confirmpassword:
         QMessageBox.warning(self, "Error", "please fill all the fields!")
         return
      
      

      elif response.status_code == 400:
         data = response.json()
         error_msg = data.get("Error", "Password change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 500:
         data = response.json()
         error_msg = data.get("Error", "Password change failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 200:
         data = response.json()
         success_msg = data.get("Message", "You have changed your password successfully")
         QMessageBox.information(self, "Message", success_msg)
         

      else:
         data = response.json()
         error_msg = data.get("Error", "Password change failed")
         QMessageBox.warning(self, "Error", "Something wrong happened try again later")
         return
   def BacK_W(self):
      if self.mwq is None:
         self.mwq = MainWindow()
         self.mwq.show()
         self.hide()



      
      






     



         

      
     

      
                       

      
      
                           
      
      
      
      



class RegisterWindow(QMainWindow): # Registerwindow class
    def __init__(self):
        super().__init__() # # inheriting form the built in QMainWindow class
        self.setWindowTitle("Register page") # Wndow title
        self.resize(600, 400) # window size
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
                
            
        
        layout = QVBoxLayout(central_widget)
        label = QLabel("USER REGISTER")
        label.setStyleSheet("color: blue; font-size: 34px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignTop)
        
                
       

        
        
        self.email_input = QLineEdit()
        self.email_input.setMaxLength(254)
        self.email_input.setPlaceholderText("Enter your Email")
        layout.addWidget(self.email_input, alignment=Qt.AlignTop)

                     
        self.password_input = QLineEdit()
        self.password_input.setMaxLength(50)
        self.password_input.setPlaceholderText("Enter your Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignTop)

        self.eye_action = QAction(QIcon("eye.png"), "", self)
        self.eye_action.triggered.connect(self.password_view)
        self.password_input.addAction(self.eye_action, QLineEdit.TrailingPosition)
        


        self.username_input = QLineEdit()
        self.username_input.setMaxLength(20)
        self.username_input.setPlaceholderText("Enter your Username")
        layout.addWidget(self.username_input, alignment=Qt.AlignTop)
       

        
        
        self.mw = None

        
                
                        
        
        
        self.submit_btn = QPushButton("Register")
        self.submit_btn.setStyleSheet("background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
        layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.Outputs_register)

        self.back_btn = QPushButton("Back to login page")
        self.back_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")
        layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.Show_MAinWindow)

       
        layout.addStretch()

    def password_view(self):
       if self.password_input.echoMode() == QLineEdit.Password:
          self.password_input.setEchoMode(QLineEdit.Normal)
          self.eye_action.setIcon(QIcon("hidden.png"))
       else:
          self.password_input.setEchoMode(QLineEdit.Password)
          self.eye_action.setIcon(QIcon("eye.png"))   

    def Outputs_register(self):
       email = self.email_input.text()
       password = self.password_input.text()
       username = self.username_input.text()
       response = Register_request(email, password, username)

       if not email or not password or not username:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

       elif response.status_code == 400:
          data = response.json()
          error_msg = data.get("Error", "Registration failed")
          QMessageBox.warning(self, "Error", error_msg)
          return

       elif response.status_code == 422:
          data = response.json()
          error_msg = data.get("Error", "Registration failed")
          QMessageBox.warning(self, "Error", error_msg)
          return

       elif response.status_code == 409:
          data = response.json()
          error_msg = data.get("Error", "Registration failed")
          QMessageBox.warning(self, "Error", error_msg)
          return

       
       
       

        
       elif response.status_code == 500:
          data = response.json()
          error_msg = data.get("Error", "Registration failed try again later")
          QMessageBox.warning(self, "Error", error_msg)
          return
       
            
            

       elif response.status_code == 201:
          data = response.json()
          success_msg = data.get("Message", "You have registered successfully")
          QMessageBox.information(self, "Message", success_msg)

          
       else:
          data = response.json()
          error_msg = data.get("Error", "Registration failed")
          QMessageBox.warning(self, "Error", "Something wrong happened try again later")
          return

    def Show_MAinWindow(self):
       if self.mw is None:
          self.mw = MainWindow()
          self.mw.show()
          self.hide()
          

          
            
             
        

        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login page")
        self.resize(600, 420)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
    

        layout = QVBoxLayout(central_widget)
        label = QLabel("USER LOGIN")
        label.setStyleSheet("color: blue; font-size: 34px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignTop)

        
        
        self.email_input = QLineEdit()
        self.email_input.setMaxLength(254)
        self.email_input.setPlaceholderText("Enter your Email")
        layout.addWidget(self.email_input, alignment=Qt.AlignTop)
                
        self.password_input = QLineEdit()
        self.password_input.setMaxLength(50)
        self.password_input.setPlaceholderText("Enter your Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignTop)

        self.eye_action = QAction(QIcon("eye.png"), "", self)
        self.eye_action.triggered.connect(self.password_view)
        self.password_input.addAction(self.eye_action, QLineEdit.TrailingPosition)

        

        self.username_input = QLineEdit()
        self.username_input.setMaxLength(20)
        self.username_input.setPlaceholderText("Enter your Username")
        layout.addWidget(self.username_input, alignment=Qt.AlignTop)

       
        

        
                
        

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet("background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
        layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.Outputs_login)

        self.guest_btn = QPushButton("Login as a guest")
        self.guest_btn.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")   
        layout.addWidget(self.guest_btn)
        self.guest_btn.clicked.connect(self.Outputs_guest)

       

        
        self.w = None
        self.ow = None
        self.ww = None
        self.zw = None
        

        

        self.register_btn = QPushButton("New here? Click to register") 
        
        self.register_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 20px;")  
        layout.addWidget(self.register_btn)  
        self.register_btn.clicked.connect(self.Show_registerWindow)


      
    
    
        h_layout = QHBoxLayout()
       
        self.remember = QCheckBox(text="Remember me")
        
        self.remember.stateChanged.connect(self.Remember_me)
        h_layout.addWidget(self.remember)
        h_layout.addStretch()
        layout.addLayout(h_layout)

        self.deleteaccount_btn = QPushButton("Delete Account")
        h_layout.addWidget(self.deleteaccount_btn)
        self.deleteaccount_btn.clicked.connect(self.show_deleteaccountwindow)
        

       
        
      
       
        
        
        


        self.forgotpassword_btn = QPushButton("Forgot password? Click here")
        layout.addWidget(self.forgotpassword_btn)
        self.forgotpassword_btn.clicked.connect(self.Show_forgotpasswordWindow)

        self.forgotusername_btn = QPushButton("Forgot username? Click here")
        layout.addWidget(self.forgotusername_btn)
        self.forgotusername_btn.clicked.connect(self.Show_forgotusernamedWindow)

       # self.deleteaccount_btn = QPushButton("Delete Account")
       # layout.addWidget(self.deleteaccount_btn)
       # self.deleteaccount_btn.clicked.connect(self.show_deleteaccountwindow)
        

        layout.addStretch()


        
        
           
    def Remember_me(self):
       if self.remember.isChecked():
          self.remember.setText("Remembered")
       else:
          self.remember.setText("Remember me")

         



    def password_view(self):
       if self.password_input.echoMode() == QLineEdit.Password:
          self.password_input.setEchoMode(QLineEdit.Normal)
          self.eye_action.setIcon(QIcon("hidden.png"))

       else:
          self.password_input.setEchoMode(QLineEdit.Password)
          self.eye_action.setIcon(QIcon("eye.png"))


           

    def Outputs_login(self):
      email = self.email_input.text()
      password = self.password_input.text()
      username = self.username_input.text()
      response = Login_request(email, password, username)

      if not email or not password or not username:
         QMessageBox.warning(self, "Error", "Please fill in all fields!")
         return

      elif response.status_code == 400:
        data = response.json()
        error_msg = data.get("Error", "Login failed")
        QMessageBox.warning(self, "Error", error_msg)
        return

      elif response.status_code == 500:
        data = response.json()
        error_msg = data.get("Error", "Login failed")
        QMessageBox.warning(self, "Error", error_msg)
        return

      elif response.status_code == 401:
         data = response.json()
         error_msg = data.get("Error", "Login failed")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 200:
         data = response.json()
         success_msg = data.get("Message", "Login success")
         QMessageBox.information(self, "Message", success_msg)

      else:
         data = response.json()
         error_msg = data.get("Error", "Login failed")
         QMessageBox.warning(self, "Error", "Something wrong happened try again later")
         return

    def Outputs_guest(self):
      response = Login_asGuest_request()

      if response.status_code == 500:
         data = response.json()
         error_msg = data.get("Error", "Something went wrong")
         QMessageBox.warning(self, "Error", error_msg)
         return

      elif response.status_code == 200:
         data = response.json()
         success_msg = data.get("Message", "You have logged in as a guest successfully")
         QMessageBox.information(self, "Message", success_msg)

      else:
         data = response.json()
         error_msg = data.get("Error", "Something went wrong")
         QMessageBox.warning(self, "Error", error_msg)
         return
         

      

      


         




            



      

      


        

      

       
     

      
       

       
      
            
      

    
            

   



    
        

    def Show_registerWindow(self):
        if self.w is None:
         self.w = RegisterWindow()
         self.w.show()
         self.hide()

    def Show_forgotpasswordWindow(self):   
       if self.ow is None:
          self.ow = ForgotPassword_Window()
          self.ow.show()
          self.hide()

    def Show_forgotusernamedWindow(self):   
        if self.ww is None:
          self.ww = ForgotUsername_Window()
          self.ww.show()
          self.hide()  

    def show_deleteaccountwindow(self):
       if self.zw is None:
          self.zw = DeleteAccount_Window()
          self.zw.show()
          self.hide()

    def show_MainWindow(self):
       if self.mw is None:
          self.mw = MainWindow()
          self.mw.show()
          self.hide()      




             
       

     
            


   
   
       
           
       

         

         

       









       
        

    


  



   
        

            
        




        

       

        
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
