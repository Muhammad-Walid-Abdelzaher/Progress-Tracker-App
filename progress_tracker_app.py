"""
This Is An App That Combines OOP With DB
The Idea Of The App Is To Work Like A REAL App
Its Functionality Is To Create An Object From A Class (OOP) And Connect That Object To The Database (DB)
The Object That Is Created Will Also Create An Automatic User ID In The Database

The Fields That Will Be In The DB Are:
-- User ID
-- First Name
-- Last Name
-- Email
-- Password
-- Gender (M or F)
-- Age
-- Skills [Skill Name, Skill Progress]

The Functionalities That The User Will Have Are:
-- Show Skills
-- Add A Skill
-- Update A Skill
-- Delete A Skill
-- Delete Account (Remove The Object)
-- Close The App

Some Conditions:
-- If The User Chose To Add An Existing Skill, The App Will Know That This Is Updating The Skill
-- If The User Chose To Update A Non-Existing Skill, The App Will Know That This Is Adding A Skill
-- There Shall Be Error Handling If The User Chose To Delete A Non-Existing Skill
-- If The User Chose To Delete The Account, There Has To A WARNING That Once The Account Is Deleted, It CANNOT BE BACK
"""

import sqlite3
import re

# Create Database And Connect (You May Put The Database Path That You Want)
db = sqlite3.connect(
    r"c:\Users\Muhammad Walid\Python\ComeBack\ReLearning\progress_tracker_app.db"
)

# Setting Up The Cursor
cr = db.cursor()


def commit_and_close():

    # Commit (Save) Changes
    db.commit()

    # Close The Connection
    db.close()


class Member:

    @classmethod
    def initialize_users_db(cls):

        # Create Table And Fields (user_id => Generated Automatically; name, gender, age => Mandatory; email => Unique)
        # NOTE: User Id Does Not Automatically Reset Or Reorganize The Existing IDs After Deleting A User
        cr.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, gender TEXT NOT NULL, age INTEGER NOT NULL)"
        )

    def __init__(self, first_name, last_name, email, password, gender, age):

        self.fname = first_name
        self.lname = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age

    @staticmethod
    def welcome_message():

        print("-" * 50)
        print("Welcome To Your Progress Tracker App".center(50))
        print("-- A Personal Coach In Your Pocket --".center(50))
        print("-" * 50)

    def sign_up(self):

        # Initialize Database For The First Time (No Longer Needed After Creating The Database For The First Time)
        self.initialize_users_db()

        # Check The Validity Of The Name
        while True:

            try:

                self.fname = input("First Name: ").strip().capitalize()
                self.lname = input("Last Name: ").strip().capitalize()

                if self.fname.isalpha() and self.lname.isalpha():

                    break

                else:

                    print("Enter A Valid Name.")

            except:

                print("Make Sure To Type A Text For The Name")

        # Check The Validity Of The Email
        while True:

            try:

                self.email = input("Email: ").strip().lower()

                email_pattern = r"^[a-z0-9\.\-\_]+@[a-z]+\.[a-z]+\.?[a-z]+?$"

                # Will Return "None" If There Is No Match
                email_valid = re.search(email_pattern, self.email)

                # Check The Validity Of The Email
                if email_valid:

                    break

                else:

                    print("Enter A Valid Email")

            except:

                print("Make Sure To Type A Text For The Email")

        self.password = input("Password: ").strip()

        # Check The Validity Of The Gender
        while True:

            try:

                male_list = ["Male", "Man", "Boy", "M"]
                female_list = ["Female", "Woman", "Girl", "Lady", "F"]

                self.gender = input("Gender: M/F? ").strip().capitalize()

                # Check For "Male", "Man", "Boy"
                if self.gender in male_list:

                    self.gender = "M"
                    break

                # Check For "Female", "Woman", "Girl", "Lady"
                elif self.gender in female_list:

                    self.gender = "F"
                    break

                else:

                    print("There Are ONLY TWO Genders!")

            except:

                print("Make Sure To Type A Text For The Gender")

        # Check The Validity Of The Age
        while True:

            try:

                self.age = int(input("Age: ").strip())

                if self.age < 6 or self.age > 101:

                    print("Please Enter A Valid Age Between 6-101")
                    continue

                break

            except ValueError:

                print("Invalid Input; Make Sure To Type An Integer.")

        # Create The User
        cr.execute(
            "INSERT INTO users (first_name, last_name, email, password, gender, age) values (?, ?, ?, ?, ?, ?)",
            (self.fname, self.lname, self.email, self.password, self.gender, self.age),
        )

        print("User Has Been Created Successfully;", end=" ")
        print(f"We're Glad To Have You Onboard, {self.fname}!")
        commit_and_close()  # Save The Changes And Close Database

    def login(self):

        # Initialize Users Database
        self.initialize_users_db()

        login_username = input("What's Your Username or Email: ").strip().lower()

        cr.execute(
            "SELECT * FROM users WHERE email = ?", (login_username,)
        )  # Check If Email Exists
        user_data = cr.fetchone()  # Return "None" If Email Not Found

        # Check If Email Exists In Database
        if user_data != None:

            self.fname = user_data[1]
            self.lname = user_data[2]
            self.email = user_data[3]

            formatted_welcome_message = f"Welcome Back, {self.fname}!"
            print(
                "#" * len(formatted_welcome_message),
                formatted_welcome_message,
                "#" * len(formatted_welcome_message),
                sep="\n",
            )
            print(
                "What Do You Want To Do?",
                "-- 1 => Show Skills",
                "-- 2 => Add A New Skill",
                "-- 3 => Update A Skill",
                "-- 4 => Delete A Skill",
                sep="\n",
            )

            while True:

                try:

                    user_command = int(input("Your Command: ").strip())
                    break

                except:

                    print("Make Sure To Choose One Of The Commands Number.")

            if user_command == 1:

                self.show_skills()

            elif user_command == 2:

                self.add_skill()

            elif user_command == 3:

                self.update_skill()

            elif user_command == 4:

                self.delete_skill()

            else:

                print("Invalid Command.")

        # If Email Doesn't Exist, The User Will Have The Option To "Sign Up"
        else:

            print("User Not Found.")
            user_answer = (
                input("Do You Want To Add A New Username? Y/N ").strip().capitalize()[0]
            )

            if user_answer == "Y":

                self.sign_up()

            elif user_answer == "N":

                print("Exiting The App...")
                commit_and_close()

            else:

                print("Invalid Option.")

    def delete_account(self):

        # Initialize Users Database
        self.initialize_users_db()

        # WARNING
        print(
            f'{"#" * 50}',
            "Once Your Account Is Deleted, It CANNOT BE BACK!!",
            f'{"#" * 50}',
            sep="\n",
        )

        user_request = (
            input("Do You Still Want To Processed? Y/N ").strip().capitalize()[0]
        )

        if user_request == "Y":

            username_input = (
                input("What's Your Username (Email) That You Want To Delete?: ")
                .strip()
                .lower()
            )

            cr.execute("SELECT email FROM users WHERE email = ?", (username_input,))
            user_check = cr.fetchone()

            # If User (Account) Exists
            if user_check != None:

                cr.execute("DELETE FROM users WHERE email = ?", (username_input,))
                cr.execute("DELETE FROM skills WHERE email = ?", (username_input,))

                print(f"Account: {username_input} Has Been Deleted Successfully.")
                commit_and_close()  # Save The Changes And Close Database

            else:

                print("User Not Found.")

        elif user_request == "N":

            print("Request Has Been Cancelled.")

        else:

            print("Invalid Request.")


class Skills(Member):

    @classmethod
    def initialize_skills_db(cls):

        # Create Table And Fields
        cr.execute(
            "CREATE TABLE IF NOT EXISTS skills (email TEXT NOT NULL, skill_name TEXT NOT NULL, skill_progress FLOAT NOT NULL)"
        )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
        gender,
        age,
        skill_name,
        skill_progress,
    ):

        # Pass All The Parent Class (Member) Parameters To The Child Class (Skills)
        super().__init__(first_name, last_name, email, password, gender, age)

        self.skill_name = skill_name
        self.skill_progress = skill_progress

    def show_skills(self):

        # Initialize Users Database
        self.initialize_skills_db()

        # Retrieve All User Skills In A List
        cr.execute(
            "SELECT skill_name, skill_progress FROM skills WHERE email = ?",
            (self.email,),
        )
        user_skills = cr.fetchall()

        # Check If User Has One Or More Skill
        if len(user_skills) >= 1:

            # Show The Message Based On How Many Skills The User Has (1 OR More)s
            message = (
                f"{self.fname}, You Have {len(user_skills)} Skills:"
                if len(user_skills) > 1
                else f"{self.fname}, You Have One Skill:"
            )
            print("#" * len(message), message, "#" * len(message), sep="\n")

            for skill in user_skills:

                print(f"-- Skill: {skill[0]}, Progress: {skill[1]} %")

        else:

            print(f"{self.fname}, You Have No Skills; Try Add Some.")

    def add_skill(self):

        # Initialize Users Database
        self.initialize_skills_db()

        skill_name = input("What's The New Skill Name? ").strip().capitalize()

        # Check If The Skill Already Exists
        cr.execute(
            "SELECT skill_name FROM skills WHERE skill_name = ? AND email = ?",
            (skill_name, self.email),
        )
        skill_check = cr.fetchone()

        # If The Skill Already Exists
        if skill_check != None:

            print(f"Skill {skill_name} Already Exist!")
            user_answer = (
                input("Do You Want To Update It? Y/N ").strip().capitalize()[0]
            )

            if user_answer == "Y":

                self.update_skill()

            elif user_answer == "N":

                print("App Is Closed.")
                commit_and_close()

            else:

                print("Invalid Choice.")

        # If The Skill Does Not Exist
        else:

            # Check To Ensure That Progress Input Is A Number
            while True:

                try:

                    skill_progress = float(
                        input("What's The New Skill Progress (%)? ").strip()
                    )
                    break

                except:

                    print("Make Sure That Progress Is A Number.")

            # Add The Skill To The SKills Table
            cr.execute(
                "INSERT INTO skills (email, skill_name, skill_progress) values (?, ?, ?)",
                (self.email, skill_name, skill_progress),
            )

            print(f"Skill {skill_name} Has Been Added!")
            commit_and_close()  # Save The Changes And Close Database

    def update_skill(self):

        # Initialize Users Database
        self.initialize_skills_db()

        skill_name = (
            input("What's The Skill That You Want To Update? ").strip().capitalize()
        )

        # Check If The Skill Exists
        cr.execute("SELECT skill_name FROM skills WHERE skill_name = ?", (skill_name,))
        skill_check = cr.fetchone()

        # If The Skill Exists
        if skill_check != None:

            # Check To Ensure That Progress Input Is A Number
            while True:

                try:

                    skill_progress = float(
                        input("What's The New Skill Progress (%)? ").strip()
                    )
                    break

                except:

                    print("Make Sure That Progress Is A Number.")

            # Update Skill Progress
            cr.execute(
                "UPDATE skills SET skill_progress = ? WHERE skill_name = ? AND email = ?",
                (skill_progress, skill_name, self.email),
            )

            print(f"Skill {skill_name} Has Been Updated!")
            commit_and_close()  # Save The Changes And Close Database

        # If The Skill Does Not Exist
        else:

            print(f"Skill {skill_name} Doesn't Exist.")
            user_answer = input("Do You Want To Add It? Y/N ").strip().capitalize()[0]

            if user_answer == "Y":

                self.add_skill()

            elif user_answer == "N":

                print("App Is Closed.")
                commit_and_close()

            else:

                print("Invalid Choice.")

    def delete_skill(self):

        # Initialize Users Database
        self.initialize_skills_db()

        skill_name = (
            input("What's The Skill That You Want To Delete? ").strip().capitalize()
        )

        # Check If The Skill Exists In The DB
        cr.execute("SELECT skill_name FROM skills WHERE skill_name = ?", (skill_name,))
        skill_check = cr.fetchone()

        # If The Skill Exist
        if skill_check != None:

            user_answer = (
                input(f"Are You Sure You Want To Delete {skill_name} Skill? Y/N ")
                .strip()
                .capitalize()[0]
            )

            if user_answer == "Y":

                cr.execute(
                    "DELETE FROM skills WHERE skill_name = ? AND email = ?",
                    (skill_name, self.email),
                )

                print(f"Skill {skill_name} Has Been Deleted.")
                commit_and_close()  # Save The Changes And Close Database

            elif user_answer == "N":

                print("No Changes Made.")

            else:

                print("Invalid Choice.")

        # If The Skill Does Not Exist
        else:

            print(f"Skill {skill_name} Doesn't Exist")
            user_answer = input("Do You Want To Add It? Y/N ").strip().capitalize()[0]

            if user_answer == "Y":

                self.add_skill()

            elif user_answer == "N":

                print("Exiting...")
                commit_and_close()

            else:

                print("Invalid Choice.")


Member.welcome_message()


print(
    "What Do You Want To:",
    "-- 1 => Sign Up",
    "-- 2 => Login",
    "-- 3 => Delete Account",
    sep="\n",
)

while True:

    try:

        user_choice = int(input("Your Choice: "))

    except:

        print("Make Sure To Enter A Number")
        continue

    if user_choice == 1:

        new_member = Skills("", "", "", "", "", 0, "", "")
        new_member.sign_up()
        break

    elif user_choice == 2:

        new_member = Skills("", "", "", "", "", 0, "", "")
        new_member.login()
        break

    elif user_choice == 3:

        new_member = Skills("", "", "", "", "", 0, "", "")
        new_member.delete_account()
        break

    else:

        print("Invalid Option.")
