from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/stats', methods=['POST'])
def add_numbers():
    try:
        data = request.get_json()
        num1 = data['number_of_dice']
        num2 = data['number_of_sides']
        result = num1 + num2
        response = {
            'result': result
        }
        return jsonify(response), 200
    except KeyError:
        return jsonify({'error': 'Invalid JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
