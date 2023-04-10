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
        self.rent = 0
        self.data = self.access_rent_data()
        if self.state:
            self.tax_rate, self.hoa_rate, self.propman_rate, self.utilities = self.get_rates()
        else:
            self.tax_rate, self.hoa_rate, self.propman_rate, self.utilities = None, None, None, None

    def access_rent_data(self):
        with open('grossrents.txt') as f:
            rents = f.readlines()
        pattern = re.compile(r'^([A-Z][a-z]*)\W+([0-9]*)\W+([0-9]*)\W+([0-9]*)\W+([0-9]*)\W+([0-9]*)\W+([0-9]*)\W+([0-9]*)')
        for line in rents:
            match = pattern.search(line)
            if match:
                state, rent2000, rent1990, rent1980, rent1970, rent1960, rent1950, rent1940 = match.groups()
                if state == self.state:
                    rents_by_decade = [int(rent2000), int(rent1990), int(rent1980), int(rent1970), int(rent1960), int(rent1950), int(rent1940)]
                    start_year = 2000
                    end_year = 1940
                    increment = (rents_by_decade[0] - rents_by_decade[-1]) / (start_year - end_year)
                    for year in range(start_year, end_year - 1, -1):
                        if self.year == year:
                            self.rent = rents_by_decade[(start_year - year) // 10] - increment * (start_year - year) % 10
                            break
                        elif year > self.year > year - 10:
                            self.rent = rents_by_decade[(start_year - year) // 10] - increment * (start_year - self.year) % 10
                            break
                        
    def get_rates(self):
        with open('rates.json', 'r') as f:
            rates = json.load(f)
        return rates[self.state]
    
    def get_states(self):
        with open('rates.json', 'r') as f:
            rates = json.load(f)
        return list(rates.keys())
                
class Income():
    def __init__(self, user, laundry=0, storage=0, misc=0):
        self.state = user.state
        self.year = user.year
        self.rental = user.rent
        self.laundry = laundry
        self.storage = storage
        self.misc = misc
        self.total = self.calculate_income()

    def calculate_income(self):
        self.total = self.rental + self.laundry + self.storage + self.misc
        print(self.__repr__())
        return self.total

    def __repr__(self):
        return f'Your total income is ${self.total:,.2f}'
       
class Expenses():
    def __init__(self, user, insurance, yard, vacancy, repairs, capex, mortgage):
        self.tax = user.rent * user.tax_rate
        self.hoa = user.rent * user.hoa_rate
        self.propman = user.rent * user.propman_rate
        self.insurance = insurance
        self.yard = yard
        self.vacancy = vacancy
        self.repairs = repairs
        self.capex = capex
        self.mortgage = mortgage
        self.utilities = user.utilities
        self.total = self.calculate_expense()
        
    def calculate_expense(self):
        self.total = self.tax + self.insurance + sum(self.utilities.values()) + self.hoa + self.yard + self.vacancy + self.repairs + self.capex + self.propman + self.mortgage
        print(self.__repr__())
        return self.total
        
    def __repr__(self):
        return f'Your total expenses are ${self.total:,.2f}'

        
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
        return f'Your total cash flow is ${self.total:,.2f}'

class CashReturn():
    def __init__(self, cash_flow, down, closing, rehab, misc=0):
        self.down = down
        self.closing = closing
        self.rehab = rehab
        self.misc = misc
        self.total_investment = self.calculate_investment()
        self.cash_flow = cash_flow.total
        self.return_rate = self.calculate_return()

    def calculate_investment(self):
        return self.down + self.closing + self.rehab + self.misc

    def calculate_return(self):
        return (self.cash_flow / self.total_investment) * 100

    def __repr__(self):
        return f'Your cash-on-cash return is {self.return_rate:.2f}%'