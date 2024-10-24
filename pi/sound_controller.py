import subprocess
import re

class SoundController:
    def __init__(self, device_name='wm8960soundcard'):
        self.device_name = device_name
        self.card = self.find_card()
        self.device = f'plughw:{self.card},0'

        # Play sound 3 times in a row so you know it's online.
        for _ in range(3):
            self.set_volume(100)
            self.play_sound('confirm.wav')

    def find_card(self):
        """Find the card number for the specified device name using arecord -l."""
        try:
            result = subprocess.run(['arecord', '-l'], capture_output=True, text=True, check=True)
            output = result.stdout
            match = re.search(rf'card (\d+): {self.device_name}', output)
            if match:
                return match.group(1)
            else:
                raise ValueError(f"Device {self.device_name} not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error finding card: {e}")
            raise

    def play_sound(self, sound_file):
        """Play a sound file using aplay."""
        try:
            self.set_volume(100)
            subprocess.run(['aplay', '-D', self.device, sound_file], check=True)
            print(f"Playing sound: {sound_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error playing sound: {e}")

    def set_volume(self, volume):
        """Set the volume using amixer."""
        try:
            subprocess.run(['amixer', '-c', str(self.card), 'set', 'Speaker', f'{volume}%'], check=True)
            print(f"Volume set to: {volume}%")
        except subprocess.CalledProcessError as e:
            print(f"Error setting volume: {e}")

# Example usage
if __name__ == "__main__":
    controller = SoundController()
    controller.set_volume(100)
    controller.play_sound('confirm.wav')