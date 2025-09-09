"""
This main.py module is a way to automate the creation of Roblox accounts,
follow a user, and perform a quick login. It also has management
for a game called "Blox Fruits," where it verifies if 2 hours have passed since
the last use of the account.
"""

import random
import string
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Function to generate random names
def generate_fullname():
    """
    This function generates a random name from a list of first and last names.
    """
    nombres = [
        "Juan", "Carlos", "Luis", "Pedro", "Miguel", "Pablo",
        "Javier", "Francisco", "Jose", "Antonio"
        ]
    apellidos = [
        "Gomez9023", "Tilin9123", "Lopez5411", "Martinez4001", "Gonzalez7982", "Perez321859", "Sanchez7913", "Diaz8923", "Romero7503"
        ]
    return f"{random.choice(nombres)}{random.choice(apellidos)}"

# Function to generate random characters
def generate_caracteres():
    """
    This function generates 3 random characters from a list of letters.
    """
    return ''.join(random.choices(string.ascii_letters, k=3))

# Function to generate random passwords
def generate_password():
    """
    This function generates a random password of 12 random characters.
    """
    length = 12
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def usuario_generado():
    """
    Generates a random username from a full name and random characters.
    """
    return generate_fullname() + generate_caracteres()

def contraseña_generada():
    """
    Requests a random password from the generate_password function.
    """
    return generate_password()

class AccountCreator:
    """
    Responsible for the entire form and automation flow.
    """
    def __init__(self):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=driver_options)

    def create_user(self, user, password):
        """
        This method creates a user on Roblox from a username and password.
        """
        url = "https://www.roblox.com"
        self.driver.get(url)
        time.sleep(3)

        try:
            username_field = self.driver.find_element(By.ID, "signup-username")
            password_field = self.driver.find_element(By.ID, "signup-password")
            day_dropdown = self.driver.find_element(By.ID, "DayDropdown")
            month_dropdown = self.driver.find_element(By.ID, "MonthDropdown")
            year_dropdown = self.driver.find_element(By.ID, "YearDropdown")
            male_button = self.driver.find_element(By.ID, "MaleButton")
            signup_button = self.driver.find_element(By.ID, "signup-button")
        except NoSuchElementException as e:
            print(f"Error finding form elements: {e}")
            return False

        time.sleep(1)

        # Fill out the form
        username_field.send_keys(user)
        password_field.send_keys(password)
        day_dropdown.send_keys(str(random.randint(10, 28)))
        month_dropdown.send_keys("Agosto")
        year_dropdown.send_keys(str(random.randint(2000, 2005)))
        male_button.click()
        time.sleep(1)
        # Verify that the signup button is enabled
        if signup_button.is_enabled():
            signup_button.click()
        else:
            time.sleep(10)
            signup_button.click()

        # Wait for the page to change
        WebDriverWait(self.driver, 120).until(
            EC.url_to_be("https://www.roblox.com/home?nu=true")
        )
        time.sleep(1)
        cookies = self.driver.get_cookies()
        # Create user object with credentials and cookies
        user_data = {
            "username": user,
            "password": password,
            "seUso": "No",
            "nivel": "50-",
            "ultimoUso": f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}",
            "cookies": [
                {"name": cookie["name"],
                 "value": cookie["value"],
                 "domain": cookie["domain"]}
                for cookie in cookies]
        }
        # Read existing data from the file
        try:
            with open("usuarios.json", 'r', encoding='utf-8') as file:
                existing_users = json.load(file)
        except FileNotFoundError:
            existing_users = []

        # Add the new user to the file
        existing_users.append(user_data)
        # Write the updated data to the file
        try:
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(existing_users, file, indent=4)
            print(f"User information for {user} saved to usuarios.json")
        except FileNotFoundError as e:
            print(f"Error saving JSON file: {e}")
        except IOError as e:
            print(f"I/O error saving JSON file: {e}")
        return True
    def login(self, cookies):
        """"
        This method logs into Roblox using a user's cookies.
        """
        # Load the Roblox login page
        self.driver.get('https://www.roblox.com/login')

        # Load the cookies
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)

        # Refresh the page to apply the cookies
        self.driver.refresh()

        # Check if login was successful
        # (Replace this with the appropriate logic for your case)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="right-navigation-header"]/div[2]/ul/div[2]/a'
                ))
        )
        time.sleep(1)

        return True
    def follow_user(self, user_id):
        """
        This method follows a user on Roblox based on their ID.
        """
        # Process to follow a user
        url_user = f"https://www.roblox.com/users/{user_id}/profile"
        self.driver.get(url_user)
        time.sleep(3)

        # Find and follow the user
        try:
            # Find elements
            options_dropdown = self.driver.find_element(
                By.XPATH,
                value="/html/body/div[3]/main/div[2]/div[2]/div/div[1]/div/div/div/div[3]/div/button"
                )
            follow_button = self.driver.find_element(
                By.XPATH, value='//*[@id="profile-header-more rbx-menu-item"]/div/ul/li[1]/a'
                )
        except NoSuchElementException as e:
            print(f"Error finding elements to follow: {e}")
            return False

        # Follow the user
        time.sleep(1)
        options_dropdown.click()
        time.sleep(0.5)
        # Check if the user is already followed
        if follow_button.text == "Dejar de seguir":
            return False
        else:
            follow_button.click()
        time.sleep(0.5)
        return True
    def quick_login(self, code):
        """
        This method logs into Roblox using a login code.
        It also checks if the user is level 50+ or 50- and if they dropped a fruit.
        """
        # Load the Roblox login page
        url = 'https://www.roblox.com/crossdevicelogin/ConfirmCode'
        self.driver.get(url)
        time.sleep(2)

        # Field to enter the code
        code_input = self.driver.find_element(
            By.XPATH, value='//*[@id="confirm-code-container"]/div/div/div/form/div[1]/input'
            )
        submit_button = self.driver.find_element(
            By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/form/div[2]/button"
            )
        # Enter the code
        code_input.send_keys(code)
        time.sleep(1)
        submit_button.click()
        time.sleep(1)
        confirm_button = self.driver.find_element(
            By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/div[3]/button[2]"
            )
        if confirm_button.is_enabled():
            confirm_button.click()
        else:
            time.sleep(1.5)
            confirm_button.click()
        return True

def menu():
    """
    This method is the main menu of the application.
    """
    print("1. Create user")
    print("2. Follow user")
    print("3. Log in quickly")
    print("4. Quick login")
    print("5. Check if 2 hours have passed since the last use")
    print("0. Exit")
    opcion = input("Enter an option: ")
    try:
        # Check if the option is valid
        if opcion not in ["1", "2", "3", "4", "5", "0"]:
            raise ValueError("Invalid option")
        # Create user
        if opcion == "1":
            cantidad = int(input("How many users do you want to create?: "))
            print("Creating users...")
            create = AccountCreator()
            for _ in range(cantidad):  # Create users
                user = usuario_generado()
                passw = contraseña_generada()
                if create.create_user(user, passw):
                    print(f"User {user} created successfully\n")
                    create.driver.delete_all_cookies()
        # Follow a user
        if opcion == "2":
            user_id = input("Enter the ID of the user to follow: ")
            print("Following user...")
            create = AccountCreator()
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    existing_users = json.load(file)
            except FileNotFoundError:
                existing_users = []

            for user in existing_users:
                if create.login(user["cookies"]):
                    if create.follow_user(user_id):
                        print(f"User {user['username']} has followed user {user_id}")
                        create.driver.delete_all_cookies()
                    if not create.follow_user(user_id):
                        print(f"User {user['username']} is already following user {user_id}")
                        create.driver.delete_all_cookies()
        # Quick login with an existing user
        if opcion == "3":
            print("Existing users: ")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    existing_users = json.load(file)
            except FileNotFoundError:
                existing_users = []
            list_num = 1
            for user in existing_users:
                print(f"{list_num}. User: {user['username']} Used: {user['seUso']} Level: {user['nivel']}")
                list_num += 1
            account_index = input("Select an account: ")
            if account_index == "" or not account_index.isdigit() or int(account_index) not in range(1, len(existing_users) + 1):
                print("No valid number entered")
                return
            print("Logging in...")
            create = AccountCreator()
            selected_user = existing_users[int(account_index) - 1]
            if create.login(selected_user["cookies"]):
                print(f"User {selected_user['username']} has logged in")
            else:
                print(f"Error logging in with user {selected_user['username']}")
        # Quick login and check if it's level 50+ or 50- and if a fruit was dropped
        if opcion == "4":
            code = input("Enter the login code: ")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    existing_users = json.load(file)
            except FileNotFoundError:
                existing_users = []
            # Print unused users
            print("\nUnused users:\n")
            unused_users_count = 0
            for user in existing_users:
                if user["seUso"] == "No":
                    unused_users_count += 1
            # Show unused users
            print(f"Unused users: {unused_users_count}")
            selected_user = None
            for user in existing_users:
                if user["seUso"] == "No":
                    print(f"User: {user['username']}")
                    selected_user = user
                    break
            if selected_user is None:
                print("No users available to log in.")
                return
            account_name = selected_user['username']
            if account_name == "":
                print("No account name entered")
                return
            print("Logging in...")
            create = AccountCreator()
            # Start the login process
            if create.login(selected_user["cookies"]):
                if create.quick_login(code):
                    print(f"User {selected_user['username']} has logged in")
                    if selected_user["nivel"] == "50-":
                        ask_level = input("Is it level 50+? (yes/no): ")
                        try:
                            if ask_level not in ["yes", "no"]:
                                raise ValueError("Invalid option")
                            if ask_level == "yes":
                                selected_user["nivel"] = "50+"
                                selected_user["seUso"] = "Si"
                                selected_user["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"User {selected_user['username']} is level 50+")
                            if ask_level == "no":
                                selected_user["nivel"] = "50-"
                                selected_user["seUso"] = "No"
                                print(f"User {selected_user['username']} is level 50-")
                        except ValueError:
                            print("Invalid option")
                    else:
                        dropped_fruit = input("Did it drop a fruit? (yes/no): ")
                        try:
                            if dropped_fruit not in ["yes", "no"]:
                                raise ValueError("Invalid option")
                            if dropped_fruit == "yes":
                                selected_user["seUso"] = "Si"
                                selected_user["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"User {selected_user['username']} has dropped a fruit")
                            if dropped_fruit == "no":
                                selected_user["seUso"] = "No"
                                print(
                                    f"User {selected_user['username']} has not dropped a fruit"
                                    )
                        except ValueError:
                            print("Invalid option")

                else:
                    print(
                        f"Error logging in with user {selected_user['username']}"
                        )
            else:
                print(f"Error logging in with user {selected_user['username']}")
            # Save changes to the JSON file
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(existing_users, file, indent=4, sort_keys=False)
        if opcion == "5":
            print("Checking if 2 hours have passed since the last use...\n")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    existing_users = json.load(file)
            except FileNotFoundError:
                existing_users = []
            for user in existing_users:
                last_use = user["ultimoUso"]
                current_time_last_use = time.mktime(
                    time.strptime(last_use, "%d/%m/%Y %H:%M:%S")
                    )
                current_time = time.time()
                if current_time - current_time_last_use >= 7200:
                    user["seUso"] = "No"
                    print(f"User {user['username']} has had 2 hours pass since the last use")
            # Save changes to the JSON file
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(existing_users, file, indent=4, sort_keys=False)
        if opcion == "0":
            print("Exiting...")
            time.sleep(1)
            exit()
    except ValueError:
        print("Invalid option")
        os.system("clear")
# Start the program
menu()
