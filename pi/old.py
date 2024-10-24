print("Heads up! This is an OLD version of the code. It uses voice2json but that does not work well. The new version uses Alexa and AWS Lambda.")
print("Open the 'old.py' file and remove line 3 to run this code.")
exit()

import subprocess
import json
from coms import SerialCommunicator
from sound_controller import SoundController

communicator = SerialCommunicator()
controller = SoundController()

controller.set_volume(100)

# Execute the command 
command_to_run = "arecord -r 16000 -f S16_LE -c 1 | voice2json transcribe-stream --audio-source - | voice2json recognize-intent"

# Run the command, and listen for the output
process = subprocess.Popen(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=1, universal_newlines=True)

data = None

# Stream the output line by line
for line in process.stdout:
    try:
        #Parse as json
        data = json.loads(line)
    except json.JSONDecodeError as e:
        # If not json, print the line
        print("O: " + line, end='')
        continue
    
    # parsed as json, so now we want to get the intent and the confidence
    #{"text": "turn off the lights", "likelihood": 0.09360471158626865, "transcribe_seconds": 3.052369579999322, "wav_seconds": 0.006375, "tokens": ["turn", "off", "the", "lights"], "timeout": false, "intent": {"name": "ChangeLightState", "confidence": 1.0}, "entities": [{"entity": "state", "value": "off", "raw_value": "off", "source": "", "start": 5, "raw_start": 5, "end": 8, "raw_end": 8, "tokens": ["off"], "raw_tokens": ["off"]}, {"entity": "name", "value": "lights", "raw_value": "lights", "source": "", "start": 13, "raw_start": 13, "end": 19, "raw_end": 19, "tokens": ["lights"], "raw_tokens": ["lights"]}], "raw_text": "turn off the lights", "recognize_seconds": 0.0014212240002962062, "raw_tokens": ["turn", "off", "the", "lights"], "speech_confidence": null, "wav_name": null, "slots": {"state": "off", "name": "lights"}}
    try:
        intent = data["intent"]["name"]
        if not intent:
            continue
        confidence = data["intent"]["confidence"]
        slots = data["slots"]
        text = data["text"]

        state = slots["state"]
        light_name = None

        try:
            light_name = slots["name"].replace("lights", "").replace("light", "").strip()
            if(light_name == ""):
                light_name = "both"
        except:
            light_name = "both"

    except Exception as e:
        #Invalid data for some reason
        continue

    #Confidence of 0.7 and up is valid
    if(float(confidence) >= 1):
        print(f'Turning {light_name} {state}')
        if(communicator.send(state, light_name)):
            #controller.play_sound('confirm.wav')
            print("Success")
    else:
        print("Heard: " + text)
        

# Wait for the process to complete and get the return code
process.wait()

# Check for any errors
error = process.stderr.read()
if error:
    print("Error:\n" + error)