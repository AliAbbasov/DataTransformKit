import json
import re
import time
import random

class Site:
    def __init__(self):
        self.loops = True
        self.Dataset = self.getdata()
    
    def program(self):
        while self.loops:
            choose = self.menu()
            if choose == "1":
                self.sign_in()
            elif choose == "2":
                self.sign_up()
            elif choose == "3":
                self.quit()

    def menu(self):
        def control(choice):
            if re.search("[^1-3]", choice):
                raise Exception("Please select a choice between 1 and 3")
            elif len(choice) != 1:
                raise Exception("Please select a choice between 1 and 3")
        while True:
            try:
                choice = input("Please select a choice:\n\n [1]- Sign In \n [2]- Sign Up \n [3]- Quit \n")
                control(choice)
                return choice
            except Exception as error:
                print(error)
                time.sleep(3)

    def sign_in(self):
        print("Opening the sign-in menu...")
        time.sleep(2)
        UserName = input("Enter your User Name: ")
        PassWord = input("Enter your password: ")

        result = self.sign_in_check(UserName, PassWord)

        if result:
            self.success_in()
        else:
            self.unsuccess_in()

    def sign_in_check(self, UserName, Password):
        for user in self.Dataset.get("Users", []):
            if user["UserName"] == UserName and user["Password"] == Password:
                return True
        return False

    def success_in(self):
        print("Credential checking...")
        time.sleep(2)
        print("Welcome to the system")
        self.loops = False

    def unsuccess_in(self):
        print("User Name and Password are incorrect")
        time.sleep(2)
        self.back_to_menu()

    def sign_up(self):
        def check_username(username):
            if len(username) < 8:
                raise Exception("Username must be at least 8 characters")
        while True:
            try:
                username = input("Enter your User Name: ")
                check_username(username)
                break
            except Exception as error:
                print(error)
                time.sleep(3)

        def check_password(password):
            if len(password) < 8:
                raise Exception("Password must be at least 8 characters")
            elif not re.search("[0-9]", password):
                raise Exception("Password must contain at least one number")
            elif not re.search("[A-Z]", password):
                raise Exception("Password must contain at least one capital letter")
            elif not re.search("[a-z]", password):
                raise Exception("Password must contain at least one small letter")
        while True:
            try:
                password = input("Enter your Password: ")
                check_password(password)
                break
            except Exception as error:
                print(error)
                time.sleep(3)

        def check_mail(mail):
            if not re.search("@", mail) or not re.search(".com", mail):
                raise Exception("Please enter a valid mail")
        while True:
            try:
                mail = input("Enter your Mail: ")
                check_mail(mail)
                break
            except Exception as error:
                print(error)
                time.sleep(3)

        result = self.sign_up_check(username, mail)
        if result:
            print("This User Name and Mail already exist.")
        else:
            activation_code = self.activation_send()
            status = self.activation_check(activation_code)
            while True:
                if status:
                    self.save_data(username, password, mail)
                    break
                else:
                    print("Invalid activation code received")
                    status = self.activation_check(activation_code)

    def sign_up_check(self, username, mail):
        for user in self.Dataset.get("Users", []):
            if user["UserName"] == username or user["Mail"] == mail:
                return True
        return False

    def activation_send(self):
        activation_code = str(random.randint(100000, 999999))
        with open("Activation.txt", "w", encoding="UTF-8") as file:
            file.write("Activation Code: " + activation_code)
        return activation_code

    def activation_check(self, activation_code):
        entered_code = input("Please write activation code: ")
        if entered_code == activation_code:
            return True
        else:
            return False

    def getdata(self):
        try:
            with open("Users.json", "r", encoding="UTF-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"Users": []}
        except json.JSONDecodeError:
            return {"Users": []}

    def save_data(self, username, password, mail):
        self.Dataset["Users"].append({"UserName": username, "Password": password, "Mail": mail})
        with open("Users.json", "w", encoding="UTF-8") as file:
            json.dump(self.Dataset, file, ensure_ascii=False, indent=4)
            print("Data Saved")
        self.back_to_menu()

    def quit(self):
        print("Exiting program")
        time.sleep(2)
        self.loops = False
        exit(0)

    def back_to_menu(self):
        while True:
            choice = input("Return to main menu press 5, Exit program press 4: ")
            if choice == "5":
                print("Returning to main menu...")
                time.sleep(2)
                self.program()
            elif choice == "4":
                self.quit()
            else:
                print("Please select a choice between 4 and 5")
                time.sleep(3)

System = Site()
while System.loops:
    System.program()
    time.sleep(random.randint(10, 20))
