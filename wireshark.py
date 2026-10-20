 with open("id.txt", "r", encoding="utf-8") as file:
         lines = file.readlines()
      code = lines[0].strip()
      message = lines[1].strip()

      if code == "200":
         label2 = QLabel(message)
         label2.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
         layout.addWidget(label2)
         layout.setAlignment(Qt.AlignCenter)
         layout.addStretch()
         

      elif code == "201":
         label2 = QLabel(message)
         label2.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
         layout.addWidget(label2, alignment=Qt.AlignCenter)
         layout.setAlignment(Qt.AlignCenter)
         layout.addStretch()
        

      elif code == "299":
         label2 = QLabel(message)
         label2.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
         layout.addWidget(label2, alignment=Qt.AlignCenter)  
         layout.setAlignment(Qt.AlignCenter) 
         layout.addStretch()

         label = QLabel("Welcome to PacketLens")
               label.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")
               font = label.font()
               font.setUnderline(True)
               label.setFont(font)
               label.setAlignment(Qt.AlignCenter)
               layout.addWidget(label, alignment=Qt.AlignTop)