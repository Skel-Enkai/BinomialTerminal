from binomialmodules.binomial import binomial_event
from threading import Thread
import simplejson

def load_hash_table():
    with open('binomial.json', 'r') as f:
        file_contents = f.read()
        return simplejson.loads(file_contents, use_decimal=True)

def save_hash_table(table):
    with open('binomial.json', 'w') as f:
        binomial_json = simplejson.dumps(table, use_decimal=True)
        f.write(binomial_json)

def binomial_populate_thread(lower, upper, n, p, table):
    for i in range(lower, upper+1):
        table[p][n][i] = {'specific_event': binomial_event(n,i,p,1-p)}

def populate_table(prob, number_of_trials, table):
    n = number_of_trials
    p = prob
    try:
        table[p][n] = {}
    except KeyError:
        table[p] = {}
        table[p][n] = {}

    midpoint = (number_of_trials) // 2
    t_1 = Thread(target=binomial_populate_thread, args=[0, midpoint, n, p, table])
    t_2 = Thread(target=binomial_populate_thread, args=[midpoint, number_of_trials, n, p, table])
    t_1.start()
    t_2.start()
    t_1.join(timeout=10000)
    t_2.join(timeout=10000)

    cumulative_prob = 0
    for x in reversed(sorted(table[prob][number_of_trials].keys())):
        cumulative_prob += table[prob][number_of_trials][x]['specific_event']
        table[prob][number_of_trials][x]['cumulative_prob'] = cumulative_prob
