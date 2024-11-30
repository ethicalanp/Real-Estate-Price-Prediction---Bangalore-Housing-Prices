from flask import Flask , request , jsonify
import util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@app.route('/get_location_names')
def get_location_names():
    if util.__locations is None:
        util.load_saved_artifacts()

    return jsonify({
        "locations": util.get_location_names()})

@app.route('/predict_home_price', methods = ['POST'])
def predict_home_price():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400  # Return an error if JSON is not provided
    
    # Extract data from the JSON
    try:
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400 
    if util.__model is None:
            util.load_saved_artifacts()

    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    return jsonify({
            'estimated_price': estimated_price
        })


if __name__ == "__main__" :
    print('Starting Python Falsk Server For Home Price Prediction...')
    app.run(debug=True)