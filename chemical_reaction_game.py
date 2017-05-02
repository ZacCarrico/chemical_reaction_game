### Author: Zac Carrico
### This script creates a game-like scenario to
### explore chemical reaction conditions.
### It can be adapted to other chemical reactions by
### replacing the constants.

import numpy as np
from math import e
from math import exp
import textwrap
import pandas as pd
import os
import sys

class molecule():
    """a class for molecular information for molecule objects"""
    def __init__(self, molecular_weight, dollars_per_gram):
        self.molecular_weight = molecular_weight
        self.dollars_per_gram = dollars_per_gram # dollar/gram

    def molarity_calculator(self, grams, volume):
        self.molarity = grams / (volume * self.molecular_weight)
        return self.molarity

# reagents and product ------------
glucose = molecule(molecular_weight = 180.16, dollars_per_gram = 0.22)
glycine = molecule(molecular_weight = 75.07, dollars_per_gram = 0.65)
dimethylpyrazine = molecule(molecular_weight = 174, dollars_per_gram = 5)
# --------------------
class reaction(): #reagent1, reagent2, product, activation_energy = 120, collision_frequency = 2.482473416371322e+16, reagent1_grams, reagent2_grams, volume, temperature, pH, duration
    """attributes reaction and provides functions for calculating the molarity of molecules after specified durations of time"""
    def __init__(self,
    reagent1 = glucose,
    reagent2 = glycine,
    product = dimethylpyrazine,
    activation_energy = 120, # activation energy, kJ/mol
    collision_frequency = 2.482473416371322e+16, # calculated from imine formation rate constant 1.4e-5 at 293 K
    reagent1_grams = 1,
    reagent2_grams = 1,
    volume = 0.001,
    temperature = 25,
    pH = 7,
    duration = 60):
        self.reagent1 = reagent1
        self.reagent2 = reagent2
        self.product = dimethylpyrazine
        self.reagent1_grams = reagent1_grams # assuming a solubility of limit of 1 g/ml
        self.reagent2_grams = reagent2_grams # assuming a solubility of limit of 1 g/ml
        self.volume = volume
        if temperature > 100:
            temperature = 100
        self.celcius = temperature
        self.pH = pH
        self.Ea = activation_energy
        self.collision_frequency = collision_frequency
        self.duration = duration
        self.reagent1_molarity = self.reagent1.molarity_calculator(self.reagent1_grams, self.volume)
        self.reagent2_molarity = self.reagent2.molarity_calculator(self.reagent2_grams, self.volume)
        self.rate_constant = self.rxn_rate_constant_calculator(celcius = self.celcius, Ea = self.Ea, A = self.collision_frequency)
        self.product_molarity = self.product_molarity_calculator()
        self.product_grams = self.molarity_to_grams(molarity = self.product_molarity,
        volume = self.volume, molecular_weight = self.product.molecular_weight)

    def rxn_rate_constant_calculator(self, celcius, Ea, A):
        R = 8.314e-3 #kJ K−1 mol−1
        C = celcius
        T = C + 273 # K
        k = A * exp(-Ea/(R*T)) # units of min-1
        return k

    def product_molarity_calculator(self):
        k = self.rate_constant * 1/(1 + abs(10 - self.pH))**2 # units of min-1, adjusting the rate_constant for pH's different than the optimal pH = 10
        t = self.duration # minutes
        Ao = self.reagent1_molarity # Ao is the initial concentration of A
        Bo = self.reagent2_molarity # Bo is the initial concentration of B
        limiting_reagent_at_0 = min(Ao, Bo)
        product_molarity = limiting_reagent_at_0 - limiting_reagent_at_0 * exp(-k * t)
        return product_molarity

    def molarity_to_grams(self, molarity, volume, molecular_weight):
        product_grams = molarity * volume * molecular_weight
        return product_grams
# --------------------

# ================
class factory():
    """calculate expenses, revenue, and profit of a reaction"""
    def __init__(self, reaction):
        self.reaction = reaction
        self.dollars_per_minute = 0.01
        self.expenses = (self.reaction.reagent1_grams * self.reaction.reagent1.dollars_per_gram +
        self.reaction.reagent2_grams * self.reaction.reagent2.dollars_per_gram + self.dollars_per_minute * self.reaction.duration)
        self.revenue = self.reaction.product_grams * self.reaction.product.dollars_per_gram
        self.profit = self.revenue - self.expenses
        self.max_profit = 3.798169
        self.ninety_percent_of_max_profit = 0.9 * self.max_profit
        self.pct_of_max_profit = self.profit / self.max_profit * 100
# =====================

introduction = "INTRODUCTION: A pig-virus has resulted in complete extinction of pigs. Major Food Co. has hired you to make an affordable bacon substitute. It needs to smell and taste like bacon and cost as little as possible. Tofu is the most affordable substitute, but it doesn't taste like bacon. Fortunately, you know how to give Tofu that iconic bacon smell using the Maillard reaction between glucose and an glycine to form 2,5-dimethylpyrazine. Your goal is to find reaction conditions that maximize profit. You are in competition with Baconish Inc. and in order to outperform them you will need to achieve profits > 90 percent that of the maximum theoretical profit. You can achieve this by finding the right reaction conditions. Some things to keep in mind are:"
hints = ["",
"The maximum solubility of each reagent is 1 g/ml",
"",
"The reaction is run in water so the temperature should be 0-100 C",
"",
"The is in silico reaction modeling software lets you play with impossible values (eg negative grams) to see what will happen. The results of impossible values might be informative in helping you understand the calculations used to calculate the results."]

wrapper = textwrap.TextWrapper(width=80,
    initial_indent=" " * 4,
    subsequent_indent=" " * 4,
    break_long_words=False,
    break_on_hyphens=False)

print(wrapper.fill(introduction))
[print(wrapper.fill(hint)) for hint in hints]

df = pd.DataFrame({'Molecule' : ['glucose', 'glycine', 'dimethylpyrazine'],
'$/gram' : [glucose.dollars_per_gram, glycine.dollars_per_gram, dimethylpyrazine.dollars_per_gram]})
print("\n", df[['Molecule', '$/gram']].to_string(index = False), "\n")
print("The reaction duration cost is $0.01/min", "\n")

# clear screen function **************
def clearscreen():
    """clears the screen"""
    if os.name == 'nt':
        clear_screen = 'cls'
    elif os.name != 'nt':
        clear_screen = 'clear'
    os.system(clear_screen)
# *************

# defining functions for user choices -----------------
def quit():
    print("\n", "Goodbye.")
    sys.exit()

reagent1_grams = float()
reagent2_grams = float()
volume = float()
temperature = float()
pH = float()
duration = float()

def example():
    """shows an example reaction, product yield, and percent of the theoretical maximum yield"""
    reagent1 = glucose
    reagent2 = glycine
    product = dimethylpyrazine
    reagent1_grams = 1
    reagent2_grams = 1
    volume = 0.001
    temperature = 85
    pH = 7
    duration = 60

    reaction_example = reaction(reagent1 = reagent1,
        reagent2 = reagent2,
        product = product,
        reagent1_grams = reagent1_grams,
        reagent2_grams = reagent2_grams,
        volume = volume,
        temperature = temperature,
        pH = pH,
        duration = duration)

    factory_example = factory(reaction_example)
    df = pd.DataFrame(
    {
    'glucose_grams' : [reagent1_grams],
    'glycine_grams' : [reagent2_grams],
    'volume_L' : [volume],
    'temp_C' : [temperature],
    'pH' : [pH],
    'duration_min' : [duration],
    'product_g' : ["{:.2f}".format(reaction_example.product_grams)],
    'percent of theoretical maximum profit': ["{:.0f}".format(factory_example.pct_of_max_profit)]
    })
    print(pd.melt(df[['glucose_grams', 'glycine_grams', 'volume_L', 'temp_C', 'pH', 'duration_min', 'product_g', 'percent of theoretical maximum profit']]))

# setting initial reaction conditions to 'NA' -------
def conditions_prompt(reagent1 = glucose, reagent2 = glycine, product = dimethylpyrazine):
    """Sets all the reaction conditions to 'NA'"""
    conditions = {
        'duration_min' : 'NA',
        'reagent1_grams' : 'NA',
        'reagent2_grams' : 'NA',
        'temperature_C' : 'NA',
        'volume_L' : 'NA',
        'pH' : 'NA'
    }
    assign_conditions(conditions = conditions)
    return(conditions)

def change_or_start(conditions):
    """takes user input of 'change' to change a condition, or 'start' to start the reaction"""
    try:
        print("")
        choice = input("Would you like to:\n'start': start the reaction\n'change': change a condition\n'quit': quit\n Your choice: ")
        if choice == 'quit':
            quit()
        if choice == 'change':
            conditions = assign_conditions(conditions = conditions)
            change_or_start(conditions = conditions)
        if choice == 'start':
            start(conditions = conditions)
        if choice != 'change' or choice != 'start':
            raise Exception
        print("")
    except Exception as e:
        print("\nSorry, that response didn't work. Please try again.\n")
        change_or_start(conditions = conditions)

# assigning conditions ------------------
def assign_conditions(conditions):
    """assigns reaction conditions from user input"""
    try:
        df_conditions = pd.DataFrame({
        'condition' : list(conditions.keys()),
        'value' : list(conditions.values()),
        })
        print(df_conditions[['condition', 'value']])
        print("")
        condition_assign = input(wrapper.fill("Please choose your reaction conditions by typing 'condition = value' (eg. duration_min = 60) and hitting enter (or 'quit' to quit). Your choice: "))
        if condition_assign == 'quit':
            quit()
        if condition_assign.split(' ')[0] not in conditions.keys():
            raise Exception
        conditions.update({condition_assign.split(' ')[0] : float(condition_assign.split(' ')[2])})
        df_conditions = pd.DataFrame({
        'condition' : list(conditions.keys()),
        'value' : list(conditions.values()),
        })
        #clearscreen()
        print(df_conditions[['condition', 'value']])
        while('NA' in conditions.values()):
            print("") # spacing things out
            condition_assign = input(wrapper.fill("Please choose your reaction conditions by typing 'condition = value' (eg. duration_min = 60) and hitting enter (or 'quit' to quit). Your choice: "))
            if condition_assign == 'quit':
                quit()
            conditions.update({str(condition_assign.split(' ')[0]) : float(condition_assign.split(' ')[2])})
            df_conditions = pd.DataFrame({
            'condition' : list(conditions.keys()),
            'value' : list(conditions.values()),
            })
            print(df_conditions[['condition', 'value']])
            print("")
        print("") # spacing things out
        change_or_start(conditions)
    except Exception as e:
        print("\nSorry, that response didn't work. Please try again.")
        assign_conditions(conditions)

def start(conditions, reagent1 = glucose, reagent2 = glycine, product = dimethylpyrazine):
    """instantiates reaction and factory objects with the provided conditions and prints the conditions, product produced, and the percent of the theoretical maximum profit"""
    clearscreen()
    rxn = reaction(reagent1 = reagent1,
        reagent2 = reagent2,
        product = product,
        reagent1_grams = conditions['reagent1_grams'],
        reagent2_grams = conditions['reagent2_grams'],
        volume = conditions['volume_L'],
        temperature = conditions['temperature_C'],
        pH = conditions['pH'],
        duration = conditions['duration_min'])
    factory_results = factory(rxn)
    df = pd.DataFrame(
    {
    'glucose_grams' : [rxn.reagent1_grams],
    'glycine_grams' : [rxn.reagent2_grams],
    'volume_L' : [rxn.volume],
    'temp_C' : [rxn.celcius],
    'pH' : [rxn.pH],
    'duration_min' : [rxn.duration],
    'product_g' : ["{:.2f}".format(rxn.product_grams)],
    'pct_of_max_profit': ["{:.0f}".format(factory_results.pct_of_max_profit)]
    })
    print("\n",df[['glucose_grams', 'glycine_grams', 'volume_L', 'temp_C', 'pH', 'duration_min', 'product_g', 'pct_of_max_profit']], "\n")
    if factory_results.pct_of_max_profit <= 90:
        print("", "The percent of theoretical maximum profit for these reaction conditions is", "{:.0f}".format(factory_results.pct_of_max_profit), "%. Keep trying different conditions to improve the percent of the theoretical maximum profit (or type 'quit' to quit)\n")
        assign_conditions(conditions = conditions)
    else:
        contratulations()
    del rxn
    del factory_results

# creating a dictionary of functions for user choices =================
def execute_choice(choice):
    """takes user choices and runs functions according to them"""
    function_dict = {
    'quit' : quit,
    'example' : example,
    'setup' : conditions_prompt
    }
    print("")
    function_dict[choice]()
    print("")

# ====================
def initial_choice():
    """Initial choices for user"""
    try:
        options = [
        "Enter the word from below for what you would you like to do:",
        "'setup': Set-up a new reaction",
        "'example': See an example reaction",
        "'quit': Quit",
        "", # these return characters are for aesthtetics
        ""]
        choice = input('\n'.join(options) + "Your choice: ")
        choice = choice.lower()
        execute_choice(choice)
        if choice == 'example':
            initial_choice()
    except Exception as e:
        print("")
        print(e) # remove before release
        print("Sorry, that response didn't work. Please try again.")
        print("")
        initial_choice()

def contratulations():
    print("Congratulations! You achieved a yield > 90 percent of the theoretical maximum.")
    sys.exit()

# starts the whole process ------------------------
initial_choice()
# ---------------------------------


# this is how I calculated max profit: -----------
# profit = []
# for t in range(0, 120):
#     Maillard_t = reaction(reagent1 = glucose,
#                    reagent2 = glycine,
#                    product = dimethylpyrazine,
#                    reagent1_grams = 1,
#                    reagent2_grams = 1,
#                    volume = 0.001,
#                    temperature = 100,
#                    pH = 10,
#                    duration = t)
#     profit.append(factory(Maillard_t).profit)
# print(profit)
# print(max(profit))
