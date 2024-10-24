from flask import Flask, request, jsonify
from coms import SerialCommunicator

communicator = SerialCommunicator()

app = Flask(__name__)
port = 3000

@app.route('/lights', methods=['POST'])
def lights():
    if not request.json:
        return jsonify({'error': 'Request body is missing'}), 400

    light_data = request.json

    if light_data.get('auth') != "CHANGEME":
        # return jsonify({'error': 'Unauthorized'}), 401
        return "Unauthorized", 401

    valid_states = ['on', 'off']
    valid_discriminators = ['left', 'right', 'both']

    print(light_data)

    if light_data.get('state') not in valid_states:
        #return jsonify({'error': 'Invalid state'}), 400
        return "Invalid state", 400
    elif light_data.get('discriminator') not in valid_discriminators:
        #return jsonify({'error': 'Invalid discriminator'}), 400
        return "Invalid discriminator", 400
    
    if(communicator.send(light_data.get('state'), light_data.get('discriminator'))):
        return "Success", 200
    else:
        return "Failed", 500

    # #return jsonify({'message': 'Success'}), 200
    # return "Success", 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'message': 'OK'}), 200

if __name__ == '__main__':
    app.run(port=port)