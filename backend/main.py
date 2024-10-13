from flask import Flask, jsonify, request, make_response
import requests
from flask_cors import CORS

# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("cerberal-ki-firebase-adminsdk-fopd6-37311c0e89.json")
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'cerberal-ki.appspot.com'
# })

FRONTED_PORT = "http://localhost:3000"
app = Flask(__name__)
KINDOAI_API_KEY = "9340154f-dd30-433f-8088-16cfbd7338a2-f8fd715b6f049f02"
# Allowing cross origin tracking
CORS(app)


@app.route('/api/items', methods=['GET'])
def get_items():
    return make_response(jsonify({'items': items}), 200)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return make_response(jsonify(item), 200)
    else:
        return make_response(jsonify({'error': 'Item not found'}), 404)

@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    new_item = {
        'id': items[-1]['id'] + 1 if items else 1,
        'name': request.json['name'],
        'value': request.json.get('value', "")
    }
    items.append(new_item)
    return make_response(jsonify(new_item), 201)

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return make_response(jsonify({'error': 'Item not found'}), 404)
    if not request.json:
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    item['name'] = request.json.get('name', item['name'])
    item['value'] = request.json.get('value', item['value'])
    return make_response(jsonify(item), 200)



@app.route('/api/gpt4', methods=['GET'])
def call_gpt4():

    print(request.args['q'])
    prompt = request.args['q']
    KINDOAI_API_KEY = "9340154f-dd30-433f-8088-16cfbd7338a2-f8fd715b6f049f02"
    url = "https://llm.kindo.ai/v1/chat/completions"
    headers = {
        'api-key': f'Bearer {KINDOAI_API_KEY}',
        'content-type': 'application/json'
    }


    cont = str({"input": {
            "Age": 29,
            "HealthHistory": "No major issues, occasional migraines",
            "Date": "2024-10-12",
            "CycleDay": 15,
            "PeriodStatus": "Pre-menstrual",
            "FlowIntensity": "Moderate",
            "PhysicalSymptoms": ["Cramps", "Fatigue"],
            "MoodSymptoms": ["Irritability", "Anxiety"],
            "BBT (°C)": 36.8,
            "Weight (kg)": 68,
            "SleepQuality": "Restless",
            "SleepDuration": 6.5,
            "ExerciseIntensity": "Low",
            "SexualActivity": "Yes",
            "DietNotes": "High protein, low carbs, hydrated"
        }})

    payload = {
        "model": "groq/llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Take into account all this information about a women's menstrual cycle:" + cont + "and then answer this prompt: " + prompt
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return jsonify(response.text)
    # data = request.args
    # print(jsonify(data))
    # input_text = "data.get('input_text')"

    # if not input_text:
    #     return jsonify({"error": "input_text is required"}), 400

    # # Set up the headers and payload for the Kindo AI API call
    # url = "https://llm.kindo.ai/v1/chat/completions"
    # headers = {
    #     'api-key': f'{KINDOAI_API_KEY}',
    #     'content-type': 'application/json'
    # }

    # payload = {
    #     "model": "groq/llama3-70b-8192",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": "Hello world!"
    #         }
    #     ]
    # }
    # response = requests.post(url, headers=headers, json=payload)
    # response.raise_for_status()
    # Make the API call
    # try:
    #     response = request.post('https://api.kindo.ai/v1/gpt4/', headers=headers, json=payload)
    #     response.raise_for_status()  # Raise an error for bad status codes
    # except request.exceptions.RequestException as e:
    #     return jsonify({"error": str(e)}), 500

    # Return the response from Kindo AI API
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)