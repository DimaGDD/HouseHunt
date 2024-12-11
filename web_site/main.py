from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)
model = joblib.load('apartment_cost.pkl')

@app.route('/api/data', methods=['POST'])
def handle_post():
  try:
    data = request.get_json()
    if not data:
      return jsonify({'error': 'No data provided'}), 400
    
    place = [0, 0, 0, 0, 0, 0, 0]
    place[int(data['place'])] = 1

    model_data = [
      [int(data['room_number']), int(data['squares']), int(data['floor'])] + place
    ]

    print(model_data)

    predicted_cost = model.predict(model_data)

    return jsonify({ 'cost': str(predicted_cost[0]) }), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 500

    # Lox

if __name__ == '__main__':
  app.run(debug=True)
