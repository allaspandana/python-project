import random

from streamlit import user
user_choice=int(input("Enter your Choice:0-rock,1-paper,2-scissors:"))
if user_choice>=3 or user_choice<0:
    print("You enterd invalid number,you lose.")
else:
    computer_choice=random.randint(0,2)
    print("Computer chose:")
    print(computer_choice)
    if computer_choice==user_choice:
        print("It's a draw")
    elif computer_choice>user_choice:
        print("Computer Win's And You Lose")
    elif user_choice>computer_choice:
        print("Computer lose And you Win")
    elif computer_choice==0 and user_choice==2:
        print("You lose and Computer Win's")
    elif user_choice==0 and computer_choice==2:
        print("You win's and computer lose")