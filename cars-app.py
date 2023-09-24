import pandas as pd
from pandas.api.types import is_numeric_dtype
from tabulate import tabulate 
import logging
import os
import datetime
from datetime import date

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)
 
    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result
 
handler = logging.StreamHandler()
formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

class CarsJSON:

    def __init__(self, path):
        self.path = path
    
    def read_json(self):
        ''' Read json as pandas dataset'''   
        df = pd.read_json(self.path)
        return df

df = CarsJSON("cars.json")

cars_pd_dataset = df.read_json()

class Cars:

    def __init__(self, data):
        '''Define instance attributes'''
        self.data = data
        self.name = data['Name']
        self.weight = data['Weight_in_lbs']
        self.horsepower = data['Horsepower']
        self.year = pd.to_datetime(data['Year'])
    
    def unique_cars(self):
        '''Print the number of unique cars'''
        print("The number of unique cars is", self.name.nunique())

    def mean_horsepower(self):
        '''Print the mean horsepower'''
        try: 
            if not isinstance(self.horsepower, (int, float)):
                          raise ValueError("Horsepower must be float or int") 
        
        except:
            if self.horsepower.lt(0).any():
                 raise ValueError("The cannot be negative values for horsepower")  
             
            
        print("Mean horsepower is", round(self.horsepower.mean(), 2))

    def top5_heaviest_cars(self):
        '''Print a table with the 5 heaviest cars'''
        try: 
            if not isinstance(self.weight, (int, float)):
                          raise ValueError("Car weight must be float or int") 
        
        except:
            if self.weight.lt(0).any():
                 raise ValueError("There cannot be negative values for car weight")  
             
            
        df1 = pd.DataFrame({
              'Weight_in_lbs': self.weight.nlargest(5)
        })

        inner_join = pd.merge(df1, self.data, on = 'Weight_in_lbs', how = 'inner')
        print("Top heaviest cars")
        print(tabulate(inner_join[['Name', 'Weight_in_lbs']], 
                       headers = ['Name', 'Weight_in_lbs'], tablefmt = 'fabcy_grid', showindex = False))
        
    def cars_made_by_manufacturer(self):
        '''Print a table with number of cars by their origin'''
        pivot = pd.pivot_table(self.data, values = 'Name', index = 'Origin', aggfunc='count')
        pivot = pivot.sort_values(by='Origin', ascending=False)
        print("Number of cars by origin")
        print(tabulate(pivot, headers=['Origin', 'N cars made'], tablefmt='fancy_grid'))

    def cars_made_by_year(self):
        '''Print a table with number of cars made each year'''    

        try:
            if  self.year > pd.to_datetime(date.today()):
                raise ValueError("Year must be between 1885 and current year")
        except:
            self.data['Year'] = pd.to_datetime(self.data['Year']).dt.strftime('%Y')
            pivot = pd.pivot_table(self.data, values = 'Name', index = 'Year', aggfunc='count')
            pivot = pivot.sort_values(by='Year', ascending=False)
            print("Number of cars by origin")
            print(tabulate(pivot, headers=['Year', 'N cars made'], tablefmt='fancy_grid'))
            
cars_pd_dataset = Cars(cars_pd_dataset)

cars_pd_dataset.unique_cars()
cars_pd_dataset.mean_horsepower()
cars_pd_dataset.top5_heaviest_cars()
cars_pd_dataset.cars_made_by_manufacturer()
cars_pd_dataset.cars_made_by_year()