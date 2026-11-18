import sys
from PySide6.QtWidgets import (QApplication, QMessageBox, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QMainWindow, QCheckBox, QHBoxLayout, QFrame, QTextEdit)
from client import Login_request, Register_request, Change_Password_request, Change_Username_request, Delete_Account_request, Login_asGuest_request
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings - Packet Lens")
        self.resize(1200, 700)
        
        # בדיקה מוקדמת של קובץ ההגדרות כדי לקבוע את צבע הרקע הראשוני של החלון
        self.is_dark = False
        try:
            with open("settings.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == "dark":
                    self.is_dark = True
        except FileNotFoundError:
            pass

        if self.is_dark:
            self.setStyleSheet("background-color: #090d16;")
        else:
            self.setStyleSheet("background-color: #0f172a;")  

        self.app_window = None  # משתנה למעבר חזרה לחלון הראשי

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. תפריט צדדי בעיצוב מודרני (Sidebar)
        self.left_screen = QWidget()
        self.left_screen.setStyleSheet("""
            background-color: #1e1b4b;
            border-right: 1px solid #312e81;
        """)
        left_layout = QVBoxLayout(self.left_screen)
        left_layout.setContentsMargins(20, 30, 20, 20)
        left_layout.setSpacing(15)

        menu_label = QLabel("Main Menu")
        menu_label.setStyleSheet("font-size: 24px; color: #ffffff; background: transparent; font-weight: bold;")  
        menu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop) 
        left_layout.addWidget(menu_label)

        separator_menu = QFrame()
        separator_menu.setFrameShape(QFrame.HLine)
        separator_menu.setStyleSheet("background-color: #312e81; max-height: 1px;")
        left_layout.addWidget(separator_menu)

        # כפתור Home שחוזר חזרה לחלון הראשי
        home_button = QPushButton("  Home")
        home_button.setIcon(QIcon("home-icon.png"))
        home_button.setIconSize(QSize(22, 22))
        home_button.setStyleSheet("""
            QPushButton {
                background-color: #3730a3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)
        left_layout.addWidget(home_button)
        home_button.clicked.connect(self.show_app_window)  

        settings_button = QPushButton("  Settings")
        settings_button.setIcon(QIcon("control.png"))
        settings_button.setIconSize(QSize(22, 22))
        settings_button.setStyleSheet("""
            QPushButton {
               background-color: #3730a3;
               color: white;
               font-size: 16px;
               font-weight: bold;
               border-radius: 10px;
               padding: 12px;
               text-align: left;
            }
            QPushButton:hover {
               background-color: #4338ca;
            }
        """)
        left_layout.addWidget(settings_button)

        scan_button = QPushButton("  Capture packets")
        scan_button.setIcon(QIcon("magnifier.png"))
        scan_button.setIconSize(QSize(22, 22))
        scan_button.setStyleSheet("""
            QPushButton {
                 background-color: #3730a3;
                 color: white;
                 font-size: 16px;
                 font-weight: bold;
                 border-radius: 10px;
                 padding: 12px;
                 text-align: left;
              }
              QPushButton:hover {
                 background-color: #4338ca;
              }
        """)
        left_layout.addWidget(scan_button)

        history_button = QPushButton("  Saved captures")
        history_button.setIcon(QIcon("save-instagram.png"))
        history_button.setIconSize(QSize(22, 22))
        history_button.setStyleSheet("""
            QPushButton {
               background-color: #3730a3;
               color: white;
               font-size: 16px;
               font-weight: bold;
               border-radius: 10px;
               padding: 12px;
               text-align: left;
            }
            QPushButton:hover {
               background-color: #4338ca;
            }
        """)
        left_layout.addWidget(history_button)

        graph_button = QPushButton("  Graphs")
        graph_button.setIcon(QIcon("chart.png"))
        graph_button.setIconSize(QSize(22, 22))
        graph_button.setStyleSheet("""
            QPushButton {
               background-color: #3730a3;
               color: white;
               font-size: 16px;
               font-weight: bold;
               border-radius: 10px;
               padding: 12px;
               text-align: left;
            }
            QPushButton:hover {
               background-color: #4338ca;
            }
        """)
        left_layout.addWidget(graph_button)

        Credits_Legal_button = QPushButton("  Credits and Legal")
        Credits_Legal_button.setIcon(QIcon("copyright.png"))
        Credits_Legal_button.setIconSize(QSize(22, 22))
        Credits_Legal_button.setStyleSheet("""
            QPushButton {
               background-color: #3730a3;
               color: white;
               font-size: 16px;
               font-weight: bold;
               border-radius: 10px;
               padding: 12px;
               text-align: left;
            }
            QPushButton:hover {
               background-color: #4338ca;
            }
        """)
        left_layout.addWidget(Credits_Legal_button)   

        left_layout.addStretch(6)

        # 2. המסך המרכזי של ההגדרות
        self.right_screen = QWidget()
        self.right_screen.setStyleSheet("background-color: #090d16;" if self.is_dark else "background-color: #f8fafc;")
        
        self.right_layout = QVBoxLayout(self.right_screen)
        self.right_layout.setContentsMargins(40, 40, 40, 40)
        self.right_layout.setSpacing(20)

        # כותרת ראשית
        self.title_label = QLabel("Settings & Preferences")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.right_layout.addWidget(self.title_label)

        # ---- כרטיס עיצוב וממשק (Theme Settings) ----
        self.theme_card = QFrame()
        theme_layout = QVBoxLayout(self.theme_card)
        theme_layout.setContentsMargins(25, 20, 25, 20)
        theme_layout.setSpacing(10)

        self.theme_title = QLabel("🎨 Appearance Settings")
        theme_layout.addWidget(self.theme_title)

        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode (Dark background for dashboard & windows)")
        self.dark_mode_checkbox.setChecked(self.is_dark) # קביעת מצב הסימון לפי השמירה
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        theme_layout.addWidget(self.dark_mode_checkbox)

        self.right_layout.addWidget(self.theme_card)

        # ---- כרטיס התראות ואבטחה (Security & Alerts) ----
        self.security_card = QFrame()
        security_layout = QVBoxLayout(self.security_card)
        security_layout.setContentsMargins(25, 20, 25, 20)
        security_layout.setSpacing(10)

        self.security_title = QLabel("🛡️ Security & Real-time Alerts")
        security_layout.addWidget(self.security_title)

        self.alert_checkbox = QLabel("Active Threat Detection: Enabled (Monitors unknown IPs and abnormal packets)")
        security_layout.addWidget(self.alert_checkbox)

        self.right_layout.addWidget(self.security_card)

        # ---- כרטיס מידע על המערכת (About) ----
        self.about_card = QFrame()
        about_layout = QVBoxLayout(self.about_card)
        about_layout.setContentsMargins(25, 20, 25, 20)
        about_layout.setSpacing(10)

        self.about_title = QLabel("ℹ️ System Information")
        about_layout.addWidget(self.about_title)

        self.version_label = QLabel("PacketLens Version: 0.2.3 (Final Project Build)\nDatabase: MongoDB (NoSQL)\nFramework: PySide6 (Python)")
        about_layout.addWidget(self.version_label)

        self.right_layout.addWidget(self.about_card)

        self.right_layout.addStretch(1)

        # הפעלת העיצוב הראשוני בהתאם למשתנה
        self.apply_theme_styles(self.is_dark)

        # הוספת התפריט והמסך המרכזי לפריסה הראשית
        main_layout.addWidget(self.left_screen, 2)
        main_layout.addWidget(self.right_screen, 9)

    def toggle_dark_mode(self):
        """מעדכן את העיצוב ושומר את הבחירה בקובץ settings.txt"""
        is_dark = self.dark_mode_checkbox.isChecked()
        
        try:
            with open("settings.txt", "w", encoding="utf-8") as f:
                f.write("dark" if is_dark else "light")
        except Exception as e:
            print(f"Error saving settings: {e}")

        self.apply_theme_styles(is_dark)

    def apply_theme_styles(self, is_dark):
        """פונקציה המרכזת את עיצוב הצבעים והטקסטים לכל מצב"""
        if is_dark:
            self.setStyleSheet("background-color: #090d16;")
            self.right_screen.setStyleSheet("background-color: #090d16;")
            
            card_style = "background-color: #1e1b4b; border-radius: 12px; border: 1px solid #312e81;"
            self.theme_card.setStyleSheet(card_style)
            self.security_card.setStyleSheet(card_style)
            self.about_card.setStyleSheet(card_style)
            
            self.title_label.setStyleSheet("color: #f8fafc; font-size: 36px; font-weight: bold; background: transparent;")
            self.theme_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; background: transparent;")
            self.security_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; background: transparent;")
            self.about_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; background: transparent;")
            
            self.dark_mode_checkbox.setStyleSheet("color: #cbd5e1; font-size: 14px; background: transparent;")
            self.alert_checkbox.setStyleSheet("color: #4ade80; font-size: 14px; font-weight: bold; background: transparent;")
            self.version_label.setStyleSheet("color: #94a3b8; font-size: 14px; background: transparent; line-height: 1.4;")
        else:
            self.setStyleSheet("background-color: #0f172a;")
            self.right_screen.setStyleSheet("background-color: #f8fafc;")
            
            card_style = "background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;"
            self.theme_card.setStyleSheet(card_style)
            self.security_card.setStyleSheet(card_style)
            self.about_card.setStyleSheet(card_style)
            
            self.title_label.setStyleSheet("color: #0f172a; font-size: 36px; font-weight: bold; background: transparent;")
            self.theme_title.setStyleSheet("color: #1e293b; font-size: 18px; font-weight: bold; background: transparent;")
            self.security_title.setStyleSheet("color: #1e293b; font-size: 18px; font-weight: bold; background: transparent;")
            self.about_title.setStyleSheet("color: #1e293b; font-size: 18px; font-weight: bold; background: transparent;")
            
            self.dark_mode_checkbox.setStyleSheet("color: #475569; font-size: 14px; background: transparent;")
            self.alert_checkbox.setStyleSheet("color: #15803d; font-size: 14px; font-weight: bold; background: transparent;")
            self.version_label.setStyleSheet("color: #64748b; font-size: 14px; background: transparent; line-height: 1.4;")

    def show_app_window(self):
        if self.app_window is None:
            self.app_window = AppWindow()
        self.app_window.show()
        self.hide()


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packet Lens")
        self.resize(1200, 700)
        self.settings_window = None
        
        # בדיקה האם מצב Dark Mode פעיל בקובץ ההגדרות
        is_dark = False
        try:
            with open("settings.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == "dark":
                    is_dark = True
        except FileNotFoundError:
            pass

        if is_dark:
            self.setStyleSheet("background-color: #090d16;")
        else:
            self.setStyleSheet("background-color: #0f172a;")  

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. תפריט צדדי בעיצוב מודרני (Sidebar)
        self.left_screen = QWidget()
        self.left_screen.setStyleSheet("""
            background-color: #1e1b4b;
            border-right: 1px solid #312e81;
        """)
        left_layout = QVBoxLayout(self.left_screen)
        left_layout.setContentsMargins(20, 30, 20, 20)
        left_layout.setSpacing(15)

        # כותרת תפריט
        menu_label = QLabel("Main Menu")
        menu_label.setStyleSheet("font-size: 24px; color: #ffffff; background: transparent; font-weight: bold;")  
        menu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop) 
        left_layout.addWidget(menu_label)

        # קו הפרדה קטן מתחת לכותרת התפריט
        separator_menu = QFrame()
        separator_menu.setFrameShape(QFrame.HLine)
        separator_menu.setStyleSheet("background-color: #312e81; max-height: 1px;")
        left_layout.addWidget(separator_menu)

        # כפתור Home
        home_button = QPushButton("  Home")
        home_button.setIcon(QIcon("home-icon.png"))
        home_button.setIconSize(QSize(22, 22))
        home_button.setStyleSheet("""
            QPushButton {
                background-color: #3730a3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)
        left_layout.addWidget(home_button)

        settings_button = QPushButton("  Settings")
        settings_button.setIcon(QIcon("control.png"))
        settings_button.setIconSize(QSize(22, 22))
        settings_button.setStyleSheet("""
               QPushButton {
                  background-color: #3730a3;
                  color: white;
                  font-size: 16px;
                  font-weight: bold;
                  border-radius: 10px;
                  padding: 12px;
                  text-align: left;
               }
               QPushButton:hover {
                  background-color: #4338ca;
               }
            """)
        left_layout.addWidget(settings_button)
        settings_button.clicked.connect(self.show_settings_window)

        scan_button = QPushButton("  Capture packets")
        scan_button.setIcon(QIcon("magnifier.png"))
        scan_button.setIconSize(QSize(22, 22))
        scan_button.setStyleSheet("""
                QPushButton {
                     background-color: #3730a3;
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     border-radius: 10px;
                     padding: 12px;
                     text-align: left;
                  }
                  QPushButton:hover {
                     background-color: #4338ca;
                  }
                  """)
        left_layout.addWidget(scan_button)

        history_button = QPushButton("  Saved captures")
        history_button.setIcon(QIcon("save-instagram.png"))
        history_button.setIconSize(QSize(22, 22))
        history_button.setStyleSheet("""
                  QPushButton {
                     background-color: #3730a3;
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     border-radius: 10px;
                     padding: 12px;
                     text-align: left;
                  }
                  QPushButton:hover {
                     background-color: #4338ca;
                  }
               """)
        left_layout.addWidget(history_button)

        graph_button = QPushButton("  Graphs")
        graph_button.setIcon(QIcon("chart.png"))
        graph_button.setIconSize(QSize(22, 22))
        graph_button.setStyleSheet("""
                  QPushButton {
                     background-color: #3730a3;
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     border-radius: 10px;
                     padding: 12px;
                     text-align: left;
                  }
                  QPushButton:hover {
                     background-color: #4338ca;
                  }
               """)
        left_layout.addWidget(graph_button)

        Credits_Legal_button = QPushButton("  Credits and Legal")
        Credits_Legal_button.setIcon(QIcon("copyright.png"))
        Credits_Legal_button.setIconSize(QSize(22, 22))
        Credits_Legal_button.setStyleSheet("""
                  QPushButton {
                     background-color: #3730a3;
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     border-radius: 10px;
                     padding: 12px;
                     text-align: left;
                  }
                  QPushButton:hover {
                     background-color: #4338ca;
                  }
               """)
        left_layout.addWidget(Credits_Legal_button)

        left_layout.addStretch(6)

        # 2. המסך המרכזי (Dashboard / Content Area)
        self.right_screen = QWidget()
        if is_dark:
            self.right_screen.setStyleSheet("background-color: #090d16;")
        else:
            self.right_screen.setStyleSheet("background-color: #f8fafc;")

        right_layout = QVBoxLayout(self.right_screen)
        right_layout.setContentsMargins(40, 40, 40, 40) 
        right_layout.setSpacing(20)

        # כותרת ראשית לדשבורד
        title_label = QLabel("Welcome to PacketLens")
        if is_dark:
            title_label.setStyleSheet("color: #f8fafc; font-size: 36px; font-weight: bold; background: transparent;")
        else:
            title_label.setStyleSheet("color: #0f172a; font-size: 36px; font-weight: bold; background: transparent;")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        right_layout.addWidget(title_label)

        # קריאת נתונים מ- id.txt והצגת תוכן דינמי מקורי
        try:
            with open("id.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                code = lines[0].strip()
                message = lines[1].strip()

            if code in ["200", "201", "299"]:
                # הודעת ברכה אישית למשתמש
                label2 = QLabel(message)
                if is_dark:
                    label2.setStyleSheet("color: #cbd5e1; font-size: 22px; font-weight: 600; background: transparent;")
                else:
                    label2.setStyleSheet("color: #334155; font-size: 22px; font-weight: 600; background: transparent;")
                right_layout.addWidget(label2)

                # כרטיס מידע (Card style) אודות המערכת
                info_card = QFrame()
                if is_dark:
                    info_card.setStyleSheet("background-color: #1e1b4b; border-radius: 12px; border: 1px solid #312e81;")
                else:
                    info_card.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;")
                
                card_layout = QVBoxLayout(info_card)
                card_layout.setContentsMargins(25, 25, 25, 25)
                card_layout.setSpacing(10)

                labelinfo = QLabel("PacketLens is a powerful network analysis tool that allows you to capture, analyze, and visualize network traffic in real-time. With PacketLens, you can gain deep insights into your network's performance, troubleshoot issues, and ensure the security of your data.")
                if is_dark:
                    labelinfo.setStyleSheet("color: #94a3b8; font-size: 15px; background: transparent; line-height: 1.4;")
                else:
                    labelinfo.setStyleSheet("color: #475569; font-size: 15px; background: transparent; line-height: 1.4;")
                labelinfo.setWordWrap(True)
                card_layout.addWidget(labelinfo)
                
                right_layout.addWidget(info_card)

                # תצוגת סטטוס התחברות (אורח מול רשום)
                status_card = QFrame()
                if is_dark:
                    status_card.setStyleSheet("background-color: #1e1b4b; border-radius: 12px; border: 1px solid #312e81;")
                else:
                    status_card.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;")
                
                status_layout = QVBoxLayout(status_card)
                status_layout.setContentsMargins(25, 20, 25, 20)
                status_layout.setSpacing(8)

                if code == "299":
                    warning_label = QLabel("⚠️ Guest Mode: You are logged in as a guest. Some features may be limited and your data may not be saved. And you will not be able to use the Ai helper.")
                    warning_label.setStyleSheet("color: #f59e0b;" if is_dark else "color: #b45309;")
                    warning_label.setStyleSheet(warning_label.styleSheet() + " font-size: 14px; font-weight: bold; background: transparent;")
                    status_layout.addWidget(warning_label)
                elif code in ["200", "201"]:
                    warning_label = QLabel("✓ Full Access: You are logged in as a registered user. Enjoy full access to all features and your data will be saved.")
                    warning_label.setStyleSheet("color: #4ade80;" if is_dark else "color: #15803d;")
                    warning_label.setStyleSheet(warning_label.styleSheet() + " font-size: 14px; font-weight: bold; background: transparent;")
                    status_layout.addWidget(warning_label)

                labeltips = QLabel("💡 Tip: Use the menu on the left to navigate through the application and access its features.")
                labeltips.setStyleSheet("color: #94a3b8;" if is_dark else "color: #64748b;")
                labeltips.setStyleSheet(labeltips.styleSheet() + " font-size: 14px; background: transparent;")
                status_layout.addWidget(labeltips)

                right_layout.addWidget(status_card)

                cpaturehere_button = QPushButton("Capture from here")
                cpaturehere_button.setStyleSheet("""
                     QPushButton {
                        background-color: #2563eb;
                        color: white;
                        font-size: 16px;
                        padding: 12px;
                        border-radius: 10px;
                     }
                     QPushButton:hover {
                        background-color: #1d4ed8;
                     }
                  """)
                right_layout.addWidget(cpaturehere_button)

                # פרטי מערכת ויוצר בתחתית הדשבורד
                footer_layout = QHBoxLayout()
                labelui = QLabel("PacketLens - Network Packet Analyzer")
                labelui.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")
                
                labeldev = QLabel("Developed by Shon Algazin")
                labeldev.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent; font-weight: bold;")
                
                footer_layout.addWidget(labelui)
                footer_layout.addStretch(1)
                footer_layout.addWidget(labeldev)
                
                right_layout.addLayout(footer_layout)

        except Exception as e:
            print(f"Error reading id.txt: {e}")

        right_layout.addStretch(1)

        # שילוב שני המסכים לפריסה הראשית
        main_layout.addWidget(self.left_screen, 2)
        main_layout.addWidget(self.right_screen, 9)

    def show_settings_window(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.hide()

          
              
         

    
      

      
      
      

      
     
   

      
      
      

      
         
               

      
      



   
      


      
         
        

      
      
         


      
      

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
        self.aw2 = None
        

        
                
                        
        
        
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
          with open("id.txt", "w") as file:
             file.write("201\n")
             data = response.json()
             success_msg = data.get("Message", "You have registered successfully")
             file.write(success_msg)
          self.show_AppWindowReg()

          
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
    def show_AppWindowReg(self): 
       if self.aw2 is None:
          self.aw2 = AppWindow()
          self.aw2.show()
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
        self.aw = None
        self.ap = None
        

        

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
         with open("id.txt", "w") as file:
            file.write("200\n")
            data = response.json()
            success_msg = data.get("Message", "You have logged in successfully")
            file.write(success_msg)
         self.show_AppWindow()
         

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

      elif response.status_code == 299:
         with open("id.txt", "w") as file:
            file.write("299\n")
            data = response.json()
            success_msg = data.get("Message", "You have logged in as a guest")
            file.write(success_msg)
         self.show_AppWindowGuest()
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

    def show_AppWindow(self): 
       if self.aw is None:
          self.aw = AppWindow()
          self.aw.show()
          self.hide()   
    def show_AppWindowGuest(self):
       if self.ap is None:
          self.ap = AppWindow()
          self.ap.show()
          self.hide()


          
            




             
       

     
            


   
   
       
           
       

         

         

       









       
        

    


  



   
        

            
        




        

       

        
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())