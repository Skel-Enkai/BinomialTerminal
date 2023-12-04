from flask import Flask, request, jsonify
import simplejson
from decimal import *
from binomialmodules.binomial import *

app = Flask(__name__)

@app.route('/stats', methods=['POST'])
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
        # removing some obvious cases
        if one_event_prob == 1:
            binomial = 1
        elif one_event_prob == 0:
            binomial = 0
        else:
            binomial = prob_specific_event(data, one_event_prob)
            
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
