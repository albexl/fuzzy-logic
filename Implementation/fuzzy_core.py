#characterization of a linguistic value
#it has a belonging function and possibly its inverse function
class fuzzy_linguistic_value:

    #builder (belonging function and its inverse)
    def __init__(self, function, inverse_function = None):
        self.function = function
        self.inverse_function = inverse_function

#return the minimum between the threshold and the value x evaluated in function
def defuzzy_function(function, maximum, x):
    return min(maximum, function(x))

#definition of a fuzzy variable(value, domain, agregation, defuzzyfication methods)
class fuzzy_variable:
    
    #builder (initial value and the domain)
    def __init__(self, initial_value, domain):
        self.domain = domain
        self.value = initial_value
        self.agregation = {}
    
    #change the value of the variable to "new_value"
    def change_value(self, new_value):
        self.value = new_value
    
    #get belonging value associated with the state "state"
    def get_value(self, state):
        return self.domain[state].function(self.value)

    #reset current agregation
    def clear_agregation(self):
        self.agregation = {}

    #add more outputs to the agregation
    def agregate(self, pairs):
        for p in pairs:
            #if this value was already part of the agregation we take the minimum of the 2 values
            if p[0] in self.agregation.keys():
                self.agregation[p[0]] = (self.domain[p[0]].function, min(p[1], self.agregation[p[0]][1]))
            else: #if not, we add it to the agregation
                self.agregation[p[0]] = (self.domain[p[0]].function, p[1])

    #defuzzyfication methods

    #centroid
    def defuzzyfication_centroid(self, low = int(-1e5), high = int(1e5), delta = 1):
        a, b = 0, 0
        for x in range(low, high, delta):
            eval = -1e15
            for k in self.agregation.keys():
                eval = max(eval, defuzzy_function(self.agregation[k][0], self.agregation[k][1], x))
            a += 1.0 * x * eval
            b += eval
        
        if b == 0:
            return 0.0
        else:
            return a / b
    
    #maximum
    def defuzzyfication_max(self):
        fuzzy, maximum = None, -1e15
        for k in self.agregation.keys():
            if self.agregation[k][1] > maximum:
                fuzzy, maximum = k, self.agregation[k][1]
        
        if fuzzy == None:
            raise RuntimeError('Agregation function not defined')

        return self.domain[fuzzy].inverse_function(maximum)

    #bisection
    def defuzzyfication_bisection(self, low = int(-1e5), high = int(1e5), delta = 1):
        first, last = 0, 0
        for x in range(low, high, delta):
            first = x
            eval = -1e15
            for k in self.agregation.keys():
                eval = max(eval, defuzzy_function(self.agregation[k][0], self.agregation[k][1], x))
            if eval > 0 and first == 0:
                break
            
        for x in range(high, low, -delta):
            last = x
            eval = -1e15
            for k in self.agregation.keys():
                eval = max(eval, defuzzy_function(self.agregation[k][0], self.agregation[k][1], x))
            if eval > 0 and last == 0:
                break
        return (low + first) / 2.0
