#Josh
import random
num = int(input("How many images do you want to see? "))

def apple():
    print("""  ,--./,-.
 / #      \\
|          |
 \        /    
  `._,._,'""")

def banana():
    print("""         _   
       _ \\'-_,#
      _\\'--','`|
      \`---`  /
       `----'`""")

def cherry():
    print("""                d888P
      d8b d8888P:::P
    d:::888b::::::P
   d:::dP8888b:d8P
  d:::dP 88b  Yb   .d8888b.
 d::::P  88Yb  Yb .P::::::Y8b
 8:::8   88`Yb  YbP::::   :::b
 8:::P   88 `8   8!:::::::::::b
 8:dP    88  Yb d!!!::::::::::8
 8P    ..88   Yb8!!!::::::::::P
  .d8:::::Yb  d888VKb:!:!::!:8
 d::::::  ::dP:::::::::b!!!!8
8!!::::::::P::::::::::::b!8P
8:!!::::::d::::::: ::::::b
8:!:::::::8!:::::::  ::::8
8:!!!:::::8!:::::::::::::8
Yb:!!:::::8!!::::::::::::8
 8b:!!!:!!8!!!:!:::::!!:dP
  `8b:!!!:Yb!!!!:::::!d88
      \"""  Y88!!!!!!!d8P
              \""\"""\"" """)

def pineapple():
    print("""          \||/
          \||/
        .<><><>.
       .<><><><>.
       '<><><><>'
        '<><><>'""")
def watermelon():
    print("""            ______
        .-'' ____ ''-.
       /.-=""    ""=-.\\
       |-===wwwwww===-|
       \\'-=,,____,,=-'/
   jgs  '-..______..-'""")

def randomfruit():
    fruit = random.randint(1,5)
    if fruit == 1:
        apple()
    elif fruit == 2:
        banana()
    elif fruit == 3:
        cherry()
    elif fruit == 4:
        pineapple()
    elif fruit == 5:
        watermelon()

for i in range(num):
    randomfruit()
    print()