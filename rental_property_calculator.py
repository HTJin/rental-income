import re
import json

class User():
    def __init__(self, state, year, insurance=0, yard=0, vacancy=0, repairs=0, capex=0, mortgage=0, down=0, closing=0, rehab=0, laundry=0, storage=0, misc=0):
        self.state = state
        self.year = year
        self.insurance = insurance
        self.yard = yard
        self.vacancy = vacancy
        self.repairs = repairs
        self.capex = capex
        self.mortgage = mortgage
        self.down = down
        self.closing = closing
        self.rehab = rehab
        self.laundry = laundry
        self.storage = storage
        self.misc = misc
        self.rent = self.access_rent_data()
        if self.state:
            self.tax_rate, self.hoa_rate, self.propman_rate, self.utilities = self.get_rates()
        else:
            self.tax_rate, self.hoa_rate, self.propman_rate, self.utilities = None, None, None, None

    def access_rent_data(self):
        with open('grossrents.txt') as f:
            rents = f.readlines()
        pattern = re.compile(r'^([A-Za-z\s\.]+)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)\s+\$?(\d+|\bNA\b)$')
        for line in rents:
            match = pattern.search(line)
            if match:
                state, rent2000, rent1990, rent1980, rent1970, rent1960, rent1950, rent1940 = match.groups()
                state = ' '.join(state.split()).lower()
                if state == self.state:
                    rent_values = [rent2000, rent1990, rent1980, rent1970, rent1960, rent1950, rent1940]
                    rents_by_decade = [int(rent) if rent != 'NA' else None for rent in rent_values]
                    start_year = 2000
                    end_year = 1940
                    valid_rents = [(index * 10, rent) for index, rent in enumerate(rents_by_decade) if rent is not None]
                    increment = (valid_rents[0][1] - valid_rents[-1][1]) / (valid_rents[0][0] - valid_rents[-1][0])
                    for year in range(start_year, end_year - 1, -1):
                        if self.year == year:
                            rent = rents_by_decade[(start_year - year) // 10] - increment * (start_year - year) % 10
                            return rent
                        elif year > self.year > year - 10:
                            rent = rents_by_decade[(start_year - year) // 10] - increment * (start_year - self.year) % 10
                            return rent
                        
    def get_rates(self):
        with open('rates.json', 'r') as f:
            rates = json.load(f)
        formatted_rates = {key.lower(): value for key, value in rates.items()}
        return formatted_rates[self.state]
    
    def get_states(self):
        with open('rates.json', 'r') as f:
            rates = json.load(f)
        return [state.lower() for state in rates.keys()]
                
class Income():
    def __init__(self, user):
        self.rental = user.rent
        self.laundry = user.laundry
        self.storage = user.storage
        self.misc = user.misc
        self.total = self.calculate_income()

    def calculate_income(self):
        self.total = self.rental + self.laundry + self.storage + self.misc
        print(self.__repr__())
        return self.total

    def __repr__(self):
        return f'\nYour total monthly income is ${self.total:,.2f}\n'
       
class Expenses():
    def __init__(self, user):
        self.tax = user.rent * user.tax_rate
        self.hoa = user.rent * user.hoa_rate
        self.propman = user.rent * user.propman_rate
        self.insurance = user.insurance
        self.yard = user.yard
        self.vacancy = user.vacancy
        self.repairs = user.repairs
        self.capex = user.capex
        self.mortgage = user.mortgage
        self.utilities = user.utilities
        self.total = self.calculate_expense()
        
    def calculate_expense(self):
        self.total = self.tax + self.insurance + sum(self.utilities.values()) + self.hoa + self.yard + self.vacancy + self.repairs + self.capex + self.propman + self.mortgage
        print(self.__repr__())
        return self.total
        
    def __repr__(self):
        return f'Your total monthly expenses are ${self.total:,.2f}\n'

        
class CashFlow:
    def __init__(self, income, expenses):
        self.income = income.total
        self.expenses = expenses.total
        self.total = self.calculate_cashflow()

    def calculate_cashflow(self):
        self.total = (self.income - self.expenses) * 12
        print(self.__repr__())
        return self.total

    def __repr__(self):
        return f'Your total annual cash flow is ${self.total:,.2f}\n'

class CashReturn():
    def __init__(self, cash_flow, user):
        self.down = user.down
        self.closing = user.closing
        self.rehab = user.rehab
        self.misc = user.misc
        self.total_investment = self.calculate_investment()
        self.cash_flow = cash_flow.total
        self.return_rate = self.calculate_return()

    def calculate_investment(self):
        return self.down + self.closing + self.rehab + self.misc

    def calculate_return(self):
        return (self.cash_flow / self.total_investment) * 100

    def __repr__(self):
        return f'Your annual cash-on-cash return is {self.return_rate:.2f}%\n'