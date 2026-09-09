import turtle # שם מחלקה של לצבוע
screen = turtle.Screen() # הגדרת מסך
screen.setup(800, 500) # הגדרת גודל המסך
screen.title("Log in page") # הגדרת כותרת המסך
screen.bgcolor("white") # הגדרת צבע רקע
t1 = turtle.Turtle() # הגדרה של פקודות צב לציור ויצור

 

t1.color("blue")  # צבע המסגרת
t1.goto(0, 210) # מיקום הטקסט
t1.write("Hawk" , font=("Arial", 25, "normal"), align="center") # הגדרת טקסט

t1.goto(0, 150) # מיקום הטקסט
t1.write("USER LOGIN" , font=("Arial", 20, "normal"), align="center") # הגדרת טקסט

t2 = turtle.Turtle() # הגדרה של פקודות צב לציור ויצור

t2.hideturtle()  # הסתרת החץ של הצב
t2.speed(0)

# מיקום התחלתי לפינת המלבן (כדי שהמלבן יהיה ממוקכז באמצע המסך)
# רוחב המלבן: 300, גובה: 45
t2.penup()
t2.goto(-193, -125)
t2.pendown()

t2.color("gray")  # צבע המסגרת
t2.fillcolor("blue")  # צבע הרקע של המלבן (אפור בהיר)
t2.begin_fill()

for _ in range(2):
  t2.forward(400)  # רוחב
  t2.left(90)
  t2.forward(250)  # גובה
  t2.left(90)

t2.end_fill()

t2.color("gray")  # צבע המסגרת
t2.goto(-180, 80) # מיקום הטקסט
t2.write("Email: ", font=("Arial", 15, "normal"), align="left") # הגדרת טקסט

t2.color("gray")  # צבע המסגרת
t2.goto(-180, 30) # מיקום הטקסט
t2.write("Password: ", font=("Arial", 15, "normal"), align="left") # הגדרת טקסט

t2.color("black")  # צבע המסגרת
t2.goto(-180, -20) # מיקום הטקסט
t2.write("Remember me", font=("Arial", 12, "normal"), align="left") # הגדרת טקסט

t2.color("black")  # צבע המסגרת
t2.goto(200, -20) # מיקום הטקסט
t2.write("Forgot password?", font=("Arial", 12, "normal"), align="right") # הגדרת טקסט

t2.color("gray")  # צבע המסגרת
t2.goto(10, -100) # מיקום הטקסט
t2.write("LOGIN", font=("Arial", 18, "normal"), align="center") # הגדרת טקסט
turtle.exitonclick() # סוף


