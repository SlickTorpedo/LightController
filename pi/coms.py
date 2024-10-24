import serial
import serial.tools.list_ports
import time

class SerialCommunicator:
    def __init__(self):
        self.serial_port = self.find_serial_port()
        self.ser = serial.Serial(self.serial_port, 115200)
        print(f"Connected to {self.serial_port}")

    @staticmethod
    def find_serial_port():
        """Finds the first available serial port."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if ports:
            return ports[0]
        else:
            raise ValueError("No serial ports found.")

    def send(self, state, light):
        """
        Translates 'on/off' and 'left/right/both' into the correct integer command and sends it.
        """
        # Translation logic based on your mapping
        command = None
        if state == "on":
            if light == "left":
                command = 2
            elif light == "right":
                command = 4
            elif light == "both":
                command = 6
        elif state == "off":
            if light == "left":
                command = 1
            elif light == "right":
                command = 3
            elif light == "both":
                command = 5

        if command is not None:
            print(f"Sending command: {command}")
            self._send_data(command)
            return True
        else:
            print(f"Invalid combination: {state} {light}")
            return False

    def _send_data(self, data):
        """Send data over the serial connection with retry mechanism."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.ser.write(str(data).encode('utf-8'))  # Convert the data to bytes and send
                success = False
                for _ in range(10):  # Check every 0.1 seconds for up to 1 second
                    time.sleep(0.1)
                    if self.ser.in_waiting > 0:
                        response = self.ser.readline().decode('utf-8').strip()
                        if "success" in response:
                            success = True
                            break
                        elif "error" in response or "fail" in response:
                            print("Failed. Response: " + str(response))
                            break
                if success:
                    break
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("Failed to send data after 3 attempts.")

    def close(self):
        """Close the serial connection."""
        self.ser.close()
        print("Serial connection closed.")


# # Example usage
# if __name__ == "__main__":
#     communicator = SerialCommunicator()

#     # Example commands
#     communicator.send("on", "left")   # Sends 1
#     communicator.send("off", "right") # Sends 4
#     communicator.send("on", "both")   # Sends 5
#     communicator.send("off", "both")  # Sends 6

#     communicator.close()


#Decode table int to meaning
# 1. Left light on:
#    - left light on
#    - turn on the left light
#    - turn left light on

# 2. Left light off:
#    - left light off
#    - turn off the left light
#    - turn left light off

# 3. Right light on:
#    - right light on
#    - turn on the right light
#    - turn right light on

# 4. Right light off:
#    - right light off
#    - turn off the right light
#    - turn right light off

# 5. Lights on (both lights on):
#    - lights on
#    - turn on the lights
#    - turn lights on

# 6. Lights off (both lights off):
#    - lights off
#    - turn off the lights
#    - turn lights off