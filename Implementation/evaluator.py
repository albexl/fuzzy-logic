#we define evaluable as a class that has an evaluator
class evaluable:

    #builder (evaluator)
    def __init__(self, evaluator):
        self.evaluator = evaluator

    #an abstract evaluator doesn't know how to evaluate itself
    def evaluate(self, evaluator = None):
        pass

#condition_token is a class derived from evaluable who knows how to
#evaluate sentences of the form "if(x)"
class condition_token(evaluable):

    #builder (variable and state, for instance ("temperature", "cold"))
    def __init__(self, variable, state):
        super().__init__(None)
        self.variable = variable
        self.state = state
    
    #how to evaluate something like "if temperature is cold"
    #we get the belonging value associated with the state of the variable
    #variable knows how to evaluate itself within a state according to its current value
    def evaluate(self):
        return self.variable.get_value(self.state)

class fuzzy_condition(evaluable):

    def __init__(self, evaluator):
        self.evaluator = evaluator
    
    def evaluate(self):
        pass

class unary_condition(fuzzy_condition):

    def __init__(self, only_condition_token, evaluator):
        super().__init__(evaluator)
        self.only_condition_token = only_condition_token
        
    def evaluate(self):
        return self.evaluator(self.only_condition_token)

#evaluates sentences like "x and y"
class binary_condition(fuzzy_condition):

    #builder (left condition token, right condition token, evaluator)
    def __init__(self, left_condition_token, right_condition_token, evaluator):
        super().__init__(evaluator)
        self.left_condition_token = left_condition_token
        self.right_condition_token = right_condition_token
    
    def evaluate(self):
        return self.evaluator(self.left_condition_token, self.right_condition_token)

#rules of the form if(x) then(y)
class rule(evaluable):

    #builder (condition or precedent, conclusion or consecuent)
    def __init__(self, condition, conclusion):
        self.condition = condition
        self.conclusion = conclusion
    
    def evaluate(self):
        return (self.conclusion, self.condition.evaluate())

#fuzzy experiment is the class that contains all the rules
#like if(x) and if(y) then z
#also contains the variable that we are interested about
#for example the working rate of a processor
class fuzzy_experiment(evaluable):

    #builder (rules ans interest variable)
    def __init__(self, rules, interest_variable):
        self.rules = rules
        self.interest_variable = interest_variable
    
    #evaluate
    def evaluate(self, defuzzyfication_method):
        
        pairs = [r.evaluate() for r in self.rules]
        self.interest_variable.clear_agregation()
        self.interest_variable.agregate(pairs)

        if defuzzyfication_method == "centroid":
            return self.interest_variable.defuzzyfication_centroid()
        if defuzzyfication_method == "max":
            return self.interest_variable.defuzzyfication_max()
        if defuzzyfication_method == "bisection":
            return self.interest_variable.defuzzyfication_bisection()
        raise RuntimeError("Deffuzyfication method not specified")
