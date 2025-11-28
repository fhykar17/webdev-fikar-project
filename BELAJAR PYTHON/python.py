import turtle
import time

# Setup turtle
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
turtle.bgcolor("black")
turtle.tracer(0, 0)  # Turn off animation for smoother control

# Function to draw a petal
def draw_petal():
    t.begin_fill()
    t.circle(100, 60)
    t.left(120)
    t.circle(100, 60)
    t.left(120)
    t.end_fill()

# Function to draw the rose blooming smoothly
def bloom_rose():
    t.penup()
    t.goto(0, -100)
    t.pendown()
    t.color("red")
    for i in range(12):  # 12 petals for a full bloom
        draw_petal()
        t.right(30)
        turtle.update()  # Update the screen after each petal
        time.sleep(0.2)  # Shorter delay for smoother animation

# Function to write text
def write_text():
    t.penup()
    t.goto(0, 100)
    t.color("white")
    t.write("For You Baby", align="center", font=("Arial", 24, "bold"))
    t.hideturtle()
    turtle.update()  # Ensure text is displayed

# Main execution
bloom_rose()
write_text()

turtle.done()
