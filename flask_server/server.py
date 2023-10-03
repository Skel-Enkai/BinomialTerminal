from flask import Flask, request, jsonify
import simplejson
from threading import Thread
from decimal import * 

app = Flask(__name__)

def faces(data):
    face = list(range(1, data['number_of_sides'] + 1))
    return face

def reroll_list(data, face):
    return list([x for x in face if x not in range(data['lower_bound'], data['upper_bound'] + 1)])

def combinations(data, face):
    reroll = reroll_list(data, face)
    comb = []
    for x in face:
        while len(reroll) < len(face):
            reroll.append(x)
        comb.append(reroll)
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
    return Decimal(above / below)

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
    return binomial_expansion(n,x) * (p ** x) * (q ** (n-x))

def prob_specific_event(data, one_event_prob, add_context, sub_context):
    dice = data['number_of_dice']
    successes = data['number_of_successes']
    n = Decimal(dice)
    x = Decimal(successes)
    p = one_event_prob
    # midpoint = (successes + dice + 1) // 2
    if successes > (dice/2):
        total_prob = Decimal(0)
        for i in range(successes, dice+1):
            total_prob += binomial_event(n,i,p,1-p)
    else:
        setcontext(sub_context)
        total_prob = Decimal(1)
        for i in range(0, successes):
            total_prob -= binomial_event(n,i,p,1-p)
        setcontext(add_context)
    return total_prob


@app.route('/stats', methods=['POST'])
def stats():
    add_context = Context(prec=20, rounding=ROUND_HALF_DOWN, traps=[FloatOperation])
    sub_context = Context(prec=40, rounding=ROUND_CEILING, traps=[FloatOperation])
    setcontext(add_context)

    try:
        data = request.get_json()

        face = faces(data)
        comb_faces = combinations(data, face)

        final_mean = mean(data, comb_faces) 

        one_event_prob = prob_one_event(data, comb_faces)
        all_event_prob = prob_all_event(data, one_event_prob)
        binomial = prob_specific_event(data, one_event_prob)

        response = {
            'prob_one_event': one_event_prob,
            'prob_all_event': all_event_prob,
            'final_mean': final_mean,
            'binomial' : binomial
        }

        return simplejson.dumps(response, use_decimal=True), 200

    except KeyError:
        return jsonify({'error': 'Invalid JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)