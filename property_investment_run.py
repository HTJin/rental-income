import re
import json
from rental_property_calculator import User, Income, Expenses, CashFlow, CashReturn

class PropertyInvestmentCalculator:
    def __init__(self):
        self.states = []
        with open("rates.json", "r") as f:
            self.rates_data = json.load(f)
        self.load_states()

    def load_states(self):
        self.states = list(self.rates_data.keys())

    def validate_inputs(self, state, year):
        if state not in self.states:
            return False, f"Invalid state: {state}. Please enter a valid state."
        if year < 1940 or year > 2023:
            return False, f"Invalid year: {year}. Please enter a valid year between 1940 and 2023."
        return True, ""

    def run(self, state, year, insurance, yard, vacancy, repairs, capex, mortgage, down, closing, rehab, laundry=0, storage=0, misc=0):
        is_valid, error_message = self.validate_inputs(state, year)
        if not is_valid:
            return error_message

        user = User(state, year)
        income = Income(user, laundry, storage, misc)
        expenses = Expenses(user, insurance, yard, vacancy, repairs, capex, mortgage)
        cash_flow = CashFlow(income, expenses)
        cash_return = CashReturn(cash_flow, down, closing, rehab, misc)

        return f"{income}\n{expenses}\n{cash_flow}\n{cash_return}"

# Example usage:
calculator = PropertyInvestmentCalculator()
result = calculator.run("Alabama", 2000, 50, 100, 10, 50, 100, 800, 10000, 3000, 5000)
print(result)