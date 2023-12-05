from threading import Thread
from decimal import Decimal

def faces(data):
    return list(range(1, data['number_of_sides'] + 1))

def reroll_list(data, face):
    return tuple([x for x in face if x not in range(data['lower_bound'], data['upper_bound'] + 1)])

def combinations(data, face):
    reroll = reroll_list(data, face)
    comb = []
    for x in face:
        sub = list(reroll)
        while len(sub) < len(face):
            sub.append(x)
        comb.append(sub)
    return comb

def mean(data, comb):
    poss = comb
    count = 0
    total = 0
    for x in poss:
        for y in x:
            count += 1
            total += y
    mean =  (total / count)
    return mean * data['number_of_dice']

def prob_one_event(data, comb):
    above = 0
    below = 0
    for x in comb:
        below += len(x)
        for y in x:
            if y >= data['lowest_success']:
                above += 1
    return Decimal(above) / Decimal(below)

def prob_all_event(data, prob_one_event):
    probability = prob_one_event
    final_probability = probability
    for i in range(data['number_of_dice'] - 1):
        final_probability *= probability
    return final_probability

def factorial(n):
    fact = 1
    for num in range(2, int(n) + 1):
        fact *= num
    return Decimal(fact)

def binomial_expansion(n, r):
    return factorial(n) / (factorial(r) * factorial(n-r))

# n = number of trials, x = number of successes, p = probability of one success, q = probability of failure
def binomial_event(n,x,p,q):
    x = Decimal(x)
    return binomial_expansion(n,x) * Decimal(p ** x) * Decimal(q ** Decimal(n-x))

def binomial_thread(lower, upper, n, p, result):
    total_prob = Decimal(0)
    for i in range(lower, upper):
        total_prob += binomial_event(n,i,p,1-p)
    result.append(total_prob)

def prob_specific_event(data, one_event_prob):
    dice = data['number_of_dice']
    successes = data['number_of_successes']
    n = dice
    x = successes
    p = one_event_prob

    midpoint = (successes + dice) // 2
    result = []
    t_1 = Thread(target=binomial_thread, args=[successes, midpoint, n, p, result])
    t_2 = Thread(target=binomial_thread, args=[midpoint, dice+1, n, p, result])
    t_1.start()
    t_2.start()

    t_1.join(timeout=100)
    t_2.join(timeout=100)
    return sum(result)

# this does not work as sum(result) approaches 1, precision is discarded
def prob_specific_event_with_effiency(data, one_event_prob):
    dice = data['number_of_dice']
    successes = data['number_of_successes']
    n = dice
    x = successes
    p = one_event_prob

    result = []
    if successes > dice // 2:
        midpoint = (successes + dice) // 2
        t_1 = Thread(target=binomial_thread, args=[successes, midpoint, n, p, result])
        t_2 = Thread(target=binomial_thread, args=[midpoint, dice+1, n, p, result])
    else:
        midpoint = successes // 2
        t_1 = Thread(target=binomial_thread, args=[1, midpoint, n, p, result])
        t_2 = Thread(target=binomial_thread, args=[midpoint, successes, n, p, result])

    t_1.start()
    t_2.start()
    t_1.join(timeout=100)
    t_2.join(timeout=100)

    if successes > dice // 2:
        return sum(result)
    else: 
        return (1 - sum(result))
