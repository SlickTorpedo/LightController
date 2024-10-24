# Voice-Controlled Lights

This is a small project I made in a day that allows me to control my lights with my voice. My bed is on the opposite side of the room from my lights, and I hate getting into bed, deciding I'm tired and going to sleep, but then having to get out of bed to turn the lights off.

![Project Image](https://raw.githubusercontent.com/SlickTorpedo/LightController/refs/heads/main/media/workflow.png)

## Overview

I created this project so that I can use my Alexa to control my lights. Initially, I planned to use voice2json for offline voice control, but it had too many issues. Alexa offers better voice recognition, so I switched to using it instead. 

All services that control the lights communicate through a webserver, which is run via a Cloudflare tunnel since I cannot open ports on the university network. The Raspberry Pi (Pi) communicates with an ESP32 using a cable and serial, sending commands. The ESP32 then uses ESP-NOW to transmit the commands to another ESP32 running the hardware that switches the lights.

## Features

- Voice control of lights using Alexa
- Webserver integration via Cloudflare tunnel
- Communication between Raspberry Pi and ESP32 using serial and ESP-NOW
- Basic integration with voice2json (not supported, may require tweaks)

## Setup

1. Ensure you have an Alexa device set up and connected to your home network.
2. Follow the instructions to integrate your lights with Alexa.
3. Optionally, set up voice2json (though it's not officially supported and may need tweaking).
4. Run the webserver through Cloudflare Tunnel for secure communication.
5. Connect the Pi to the ESP32 using a serial connection.
6. Set up the ESP-NOW communication between the ESP32s to control the hardware that manages the lights.

## Usage

Use voice commands with your Alexa device to control the lights. For example:
- "Alexa, ask Cosmos Controller to turn off the lights" (All Lights)
- "Alexa, ask Cosmos Controller to turn on the lights"
- "Alexa, ask Cosmos Controller to turn on the left light" (My Light)
- "Alexa, ask Cosmos Controller to turn on the right light" (My Roommate's Light)
- "Alexa, ask Cosmos Controller to turn off the left light"
- "Alexa, ask Cosmos Controller to turn off the right light"

## Why This Setup?

The original plan was to use voice2json for offline voice control, which required the microphone to be near my bed for better voice capture. This setup necessitated using ESP-NOW to transmit the data from the Pi by my bed to the ESP32 controlling the lights. Now that I'm using Alexa, the Pi could technically be mounted directly on the device to control it, but since this setup works well, I decided to keep it as is.

## Limitations

- The voice2json integration is not supported and may require tweaks to work.
- Alexa provides a much better voice recognition experience.
- You may need to tweak the 3D files and code to adapt this project to your own light setup.

## Note

This is me posting the project to contribute to my profile. If you want to build it yourself, you'll likely need to adjust the setup for your specific environment, but it's a nice starting point. This project is just a simple way to control lights, it's NOT meant to be a full-fledged home automation system. It is not meant to be easily modified or adapted to other setups. It's just a fun project I made in a day.

## Door Lock

Another project I made that allows you to unlock your door using your phone IS much more polished and complete. You can check it out [here](https://github.com/SlickTorpedo/DoorLock). This has an integration to turn on the lights when you unlock the door, so it's a nice companion to this project.

## Demo

### Hardware Closeup
https://github.com/user-attachments/assets/684cc37a-7ef8-4949-914b-2eee8b53ac76

### View of Lights
https://github.com/user-attachments/assets/d54b3ac8-c69c-4060-9792-fa7098f44bc7

### Door Integration
https://github.com/user-attachments/assets/999da21b-0757-456a-83d4-3d57e6eddee5

