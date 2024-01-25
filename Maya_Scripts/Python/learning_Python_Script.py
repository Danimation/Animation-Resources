print("Hello, welcome to my Coffee Shop")

name = input("What is your name? \n")

if name == "Ben":
  evil_status = input("Are you evil?\n")
  if evil_status == "Yes":
    print("You are not welcome here Evil Ben!! Get Out!!")
    exit()
  else:
    print("Oh, so you're one of those good Bens. Come on in!!")
else:
  print("Hello " + name + ", thank you for coming in today!! \n\n")
  
menu = "Black Coffee, Espresso, Latte, Cuppucino, Frappuccino \n\n"

order = input(name + ", what would you like from our menu today? We have the following options. \n\n" + menu)

if order == "Frappuccino":
  price = 13
elif order == "Black Coffee":
  price = 3
elif order == "Espresso":
  price = 5
elif order == "Latte":
  price = 7
elif order == "Cappucino":
  price = 10
else:
  print("Sorry, we don't have that here")
  price = 0

print(price)

wipped_cream = input("Would you like some whipped cream with that? \n")

if wipped_cream == "Yes":
  print("that will be an extra 4 dollars \n")
  print("That will be ready for a you in couple of minutes! Have a good day!")
else:
  print("Enjoy your " + order)
