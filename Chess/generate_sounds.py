import wave
import struct
import math
import os

def generate_beep(filename, frequency=440, duration=0.1, volume=0.5):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1) # Mono
        wav.setsampwidth(2) # 2 bytes per sample
        wav.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Sine wave
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav.writeframesraw(data)

def create_game_sounds(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Move: Short, slightly high pitch
    generate_beep(os.path.join(output_dir, "move.wav"), 600, 0.05, 0.3)
    # Capture: Slightly lower, double beep
    generate_beep(os.path.join(output_dir, "capture.wav"), 400, 0.1, 0.4)
    # Check: High pitch, sharp
    generate_beep(os.path.join(output_dir, "check.wav"), 800, 0.2, 0.5)
    # Mate: Deep, long
    generate_beep(os.path.join(output_dir, "mate.wav"), 200, 0.5, 0.6)
    # Illegal: Buzz
    generate_beep(os.path.join(output_dir, "illegal.wav"), 150, 0.1, 0.4)
    print("Generated sounds.")

if __name__ == "__main__":
    create_game_sounds(r"c:\Users\Anjana Enterprises\OneDrive\Pictures\Chess\assets\sounds")
