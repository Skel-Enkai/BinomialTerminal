from flask import Flask, request, jsonify
import simplejson
from decimal import *
from binomialmodules.binomial import faces, combinations, mean, prob_one_event, prob_all_event
from binomialmodules.hashtable import *
import sys

app = Flask(__name__)

# {prob:{number_of_trials:{number_of_successes:{'specific_prob':, 'cumulative_prob'}}}}
try:
    table = load_hash_table()
except FileNotFoundError:
    table = {}

@app.route('/hashstats', methods=['POST'])
def stats():
    add_context = Context(prec=20, rounding=ROUND_HALF_DOWN, traps=[FloatOperation])
    setcontext(add_context)

    try:
        data = request.get_json()

        face = faces(data)
        comb_faces = combinations(data, face)

        final_mean = mean(data, comb_faces) 
        one_event_prob = prob_one_event(data, comb_faces)
        all_event_prob = prob_all_event(data, one_event_prob)

        if one_event_prob == 1:
            binomial = 1
        elif one_event_prob == 0:
            binomial = 0
        else:
            print('Beginning search.', file=sys.stderr)
            prob = one_event_prob
            number_of_trials = data['number_of_dice']
            number_of_successes = data['number_of_successes']
            try:
                binomial = table[prob][number_of_trials][number_of_successes]['cumulative_prob']
                print('Entry found.', file=sys.stderr)
            except KeyError:
                try:
                    binomial = table[str(prob)][str(number_of_trials)][str(number_of_successes)]['cumulative_prob']
                    print('Entry found.', file=sys.stderr)
                except KeyError:
                    print('Populating table.', file=sys.stderr)
                    populate_table(prob, number_of_trials, table)
                    save_hash_table(table)
                    binomial = table[prob][number_of_trials][number_of_successes]['cumulative_prob']
            
        response = {
            'prob_one_event': float(one_event_prob),
            'prob_all_event': float(all_event_prob),
            'final_mean': float(final_mean),
            'binomial' : float(binomial)
        }

        return simplejson.dumps(response, use_decimal=True), 200

    except KeyError:
        return jsonify({'error': 'Invalid JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
