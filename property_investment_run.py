import json
from rental_property_calculator import User

class PropertyInvestmentCalculator:
    def __init__(self):
        self.user = None
        self.users = {}
        self.states = User("", 0).get_states()

    def validate_inputs(self, state, year):
        if state not in self.states:
            return False, f"Invalid state: {state}. Please enter a valid state."
        if year < 1940 or year > 2000:
            return False, f"Invalid year: {year}. Please enter a valid year between 1940 and 2023."
        return True, ""
    
    def register(self):
        while True:
            print("[<-- New User Registration -->]")
            username = input("Enter a new username: ")
            if username in self.users:
                print("Username already exists. Please choose another one.")
            else:
                break
        password = input("Enter a new password: ")
        self.users[username] = password
        print("Registration successful.")
        return username

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in self.users and self.users[username] == password:
            print("Logged in as " + username)
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout(self):
        self.user = None
        print("Logged out successfully.")
        
    def get_user_inputs(self):
        while True:
            state = input("1. State: ").capitalize()
            try:
                year = int(input("2. Year (between 1940 and 2000): "))
                if year < 1940 or year > 2000:
                    raise ValueError("Invalid input: year must be an integer and between 1940 and 2000.")
            except ValueError as e:
                print(e)
                continue
            self.user = User(state, year)
            is_valid, error_message = self.validate_inputs(state, year)
            if not is_valid:
                print(error_message)
                continue
            break

        self.user.access_rent_data()
        self.user.get_rates()

        while True:
            try:
                insurance = float(input("3. Insurance amount: "))
                break
            except ValueError:
                print("Invalid input: Insurance amount must be a number.")
        while True:
            try:
                yard = float(input("4. Yard amount: "))
                break
            except ValueError:
                print("Invalid input: Yard amount must be a number.")
        while True:
            try:
                vacancy = float(input("5. Vacancy amount: "))
                break
            except ValueError:
                print("Invalid input: Vacancy amount must be a number.")
        while True:
            try:
                repairs = float(input("6. Repairs amount: "))
                break
            except ValueError:
                print("Invalid input: Repairs amount must be a number.")
        while True:
            try:
                capex = float(input("7. Capital Expenditure amount: "))
                break
            except ValueError:
                print("Invalid input: CapEx amount must be a number.")
        while True:
            try:
                mortgage = float(input("8. Mortgage amount: "))
                break
            except ValueError:
                print("Invalid input: Mortgage amount must be a number.")
        while True:
            try:
                down = float(input("9. Down payment amount: "))
                break
            except ValueError:
                print("Invalid input: Down payment amount must be a number.")
        while True:
            try:
                closing = float(input("10. Closing cost amount: "))
                break
            except ValueError:
                print("Invalid input: Closing cost amount must be a number.")
        while True:
            try:
                rehab = float(input("11. Rehab cost amount: "))
                break
            except ValueError:
                print("Invalid input: Rehab cost amount must be a number.")
        while True:
            try:
                laundry = float(input("12. Laundry income (default: 0): ") or 0)
                break
            except ValueError:
                print("Invalid input: Laundry income must be a number.")
        while True:
            try:
                storage = float(input("13. Storage income (default: 0): ") or 0)
                break
            except ValueError:
                print("Invalid input: Storage income must be a number.")
        while True:
            try:
                misc = float(input("14. Miscellaneous income (default: 0): ") or 0)
                break
            except ValueError:
                print("Invalid input: Misc income must be a number.")
                
        self.user = User(state, year, insurance, yard, vacancy, repairs, capex, mortgage, down, closing, rehab, laundry, storage, misc)
    
    def calculate(self):
        self.user.calculate()
       
    def run(self):
        while True:
            action = input("Enter 'register', 'login', or 'exit': ").lower()
            if action == "register":
                username = self.register()
                if username:
                    print("Please log in with your newly registered account.")
            elif action == "login":
                is_logged_in = self.login()
                if is_logged_in:
                    self.get_user_inputs()
                    self.calculate()
                    self.logout()
                elif not self.users:
                    print("No users found. Please register.")
                    username = self.register()
                    if username:
                        print("Please log in with your newly registered account.")
            elif action == "exit":
                print("Exiting.")
                break
            else:
                print("Invalid input. Please enter 'register', 'login', or 'exit'.")

calculator = PropertyInvestmentCalculator()
print(calculator.run())