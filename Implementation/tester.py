
from fuzzy_core import fuzzy_linguistic_value
from fuzzy_core import fuzzy_variable
from evaluator import binary_condition
from evaluator import unary_condition
from evaluator import fuzzy_experiment
from evaluator import fuzzy_condition
from evaluator import condition_token
from evaluator import rule


#VARIABLE WORK

#belonging functions of work
low_function = lambda x : 1.0 if x <= 1000 else -(1.0) * (x - 1000) / 9000 + 1 if x <= 10000 else 0.0
medium_function = lambda x : 0.0 if x < 1000 or x > 10000 else (1.0 / 4000) * (x - 1000) if x <= 5000 else (-1.0 / 5000) * (x - 5000) if x < 10000 else 0.0
high_function = lambda x : 0.0 if x < 5000 else (1.0 / 10000) * (x - 5000) if x <= 15000 else 1.0

#domain of work
work_domain = {
    'low' : fuzzy_linguistic_value(low_function),
    'medium' : fuzzy_linguistic_value(medium_function),
    'high' : fuzzy_linguistic_value(high_function)
}

#definition of variable work, with its domain and initial value
work = fuzzy_variable(150, work_domain)

#VARIABLE TEMPERATURE

#belonging functions of temperature
cold_function = lambda x : 1.0 if x <= 13 else (1.0 / 35) * (x - 13) if x <= 30 else 0.0
hot_function = lambda x : 0.0 if x < 20 else (1.0 / 35) * (x - 20) if x < 33 else 1.0
soso_function = lambda x : 0.0 if x < 13 or x > 32 else (1.0 / 15) * (x - 13) if x <= 25 else (-1.0 / 15) * (x - 25) if x < 32 else 0.0

#domain of temperature
temperature_domain = {
    'cold' : fuzzy_linguistic_value(cold_function),
    'hot' : fuzzy_linguistic_value(hot_function),
    'soso' : fuzzy_linguistic_value(soso_function)
}

#definition of variable temperature, with its domain and initial value
temperature = fuzzy_variable(30.0, temperature_domain)

#VARIABLE CHANGE(interest variable)

#change belonging functions
lower_function = lambda x : 1.0 if x <= -1000 else (-1.0 / 1000) * (x + 1000) if x <= 0 else 0.0
maintain_function = lambda x : 0.0 if x < -500 or x > 500 else (1.0 / 500) * (x + 500) if x <= 0 else (-1.0 / 500) * x if x < 500 else 0.0
increase_function = lambda x : 0.0 if x < 0 else (1.0 / 1000) * x if x <= 1000 else 1.0

lower_inverse_function = lambda val : -10000 if val == 1.0 else (1 - val)*1000 - 1000 if val > 0.0 else 1000
maintain_inverse_function = lambda val : 1000 if val == 0.0 else val * 500 - 500
increase_inverse_function = lambda val : -500 if val == 0.0 else val * 1000 if val != 1.0 else 10000

#domain of change
change_domain = {
    'lower' : fuzzy_linguistic_value(lower_function, lower_inverse_function),
    'maintain' : fuzzy_linguistic_value(maintain_function, maintain_inverse_function),
    'increase' : fuzzy_linguistic_value(increase_function, increase_inverse_function)
}

#definition of variable temperature, with its domain and initial value
change = fuzzy_variable(0.0, change_domain)

#STABLISHING RULES

#rule 1: if temperature is hot or work rate is high then lower the work rate
condition1 = binary_condition(condition_token(temperature, 'hot'), condition_token(work, 'high'), lambda a, b : max(a.evaluate(), b.evaluate()))
conclusion1 = 'lower'
rule1 = rule(condition1, conclusion1)

#rule2: if temperature is so so and work rate is medium then maintain current work rate
condition2 = binary_condition(condition_token(temperature, 'soso'), condition_token(work, 'medium'), lambda a, b : min(a.evaluate(), b.evaluate()))
conclusion2 = 'maintain'
rule2 = rule(condition2, conclusion2)

#rule3: if temperature is cold and work rate is low then increase the work rate
condition3 = binary_condition(condition_token(temperature, 'cold'), condition_token(work, 'low'), lambda a, b : min(a.evaluate(), b.evaluate()))
conclusion3 = 'increase'
rule3 = rule(condition3, conclusion3)

#all our rules
rules = [rule1, rule2, rule3]

#this is the fuzzy model, with its rules and interest variable
experiment = fuzzy_experiment(rules, change)

iterations = 10

while iterations > 0:
    iterations -= 1
    print('Current temperature is ' + str(temperature.value))
    print('Current work rate is ' + str(work.value))
    print('Current change of work rate is ' + str(change.value))
    print()
    print('Insert temperature value')

    new_value = int(input())
    temperature.change_value(new_value)

    eval_change = experiment.evaluate('max')
    print('new change of work rate ' + str(eval_change))
    change.change_value(eval_change)
    work.change_value(work.value + change.value)

    print()
    print()