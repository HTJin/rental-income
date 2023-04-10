import json
from rental_property_calculator import User, Income, Expenses, CashFlow, CashReturn

class PropertyInvestmentCalculator:
    def __init__(self):
        self.user = None
        self.users = {}
        self.states = User("", 0).get_states()

    def validate_inputs(self, prompt, var_type=float, default=None):
        while True:
            try:
                value = input(prompt)
                if not value and default is not None:
                    return default
                return var_type(value)
            except ValueError:
                print(f"Invalid input: {prompt} must be a {var_type.__name__}.")
    
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
        state, year = None, None
        while True:
            state = input("1. State: ").capitalize()
            if state not in self.states:
                print("Invalid input: State not found. Please enter a valid state.")
                continue
            year = self.validate_inputs("2. Year (between 1940 and 2000): ", int)
            if year < 1940 or year > 2000:
                print("Invalid input: year must be an integer and between 1940 and 2000.")
                continue
            break

        self.user = User(state, year)
        self.user.access_rent_data()
        self.user.get_rates()

        insurance = self.validate_inputs("3. Insurance amount: ")
        yard = self.validate_inputs("4. Yard amount: ")
        vacancy = self.validate_inputs("5. Vacancy amount: ")
        repairs = self.validate_inputs("6. Repairs amount: ")
        capex = self.validate_inputs("7. Capital Expenditure amount: ")
        mortgage = self.validate_inputs("8. Mortgage amount: ")
        down = self.validate_inputs("9. Down payment amount: ")
        closing = self.validate_inputs("10. Closing cost amount: ")
        rehab = self.validate_inputs("11. Rehab cost amount: ")
        laundry = self.validate_inputs("12. Laundry income (default: 0): ", default=0)
        storage = self.validate_inputs("13. Storage income (default: 0): ", default=0)
        misc = self.validate_inputs("14. Miscellaneous income (default: 0): ", default=0)
                
        self.user = User(state, year, insurance, yard, vacancy, repairs, capex, mortgage, down, closing, rehab, laundry, storage, misc)
    
    def calculate(self):
        income = Income(self.user)
        expenses = Expenses(self.user, self.user.insurance, self.user.yard, self.user.vacancy, self.user.repairs, self.user.capex, self.user.mortgage)
        cash_flow = CashFlow(income, expenses)
        cash_return = CashReturn(cash_flow, self.user.down, self.user.closing, self.user.rehab)
        print(cash_return)
       
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
                print("Good bye.")
                break
            else:
                print("Invalid input. Please enter 'register', 'login', or 'exit'.")

calculator = PropertyInvestmentCalculator()
print(calculator.run())