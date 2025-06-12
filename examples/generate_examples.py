import math
import struct
import wave
from pathlib import Path

from PIL import Image, ImageDraw


def create_test_image_sequence(folder: str = "images") -> None:
    """Create test image sequence of a moving ball."""
    Path(folder).mkdir(parents=True, exist_ok=True)
    image_size = (640, 480)
    for i in range(5):
        img = Image.new('RGB', image_size, (40, 40, 40))
        draw = ImageDraw.Draw(img)
        y = int(i * 100)
        draw.circle([image_size[0] / 2, y,
        ], 70, fill=(0, 0, 255))
        # File saving
        filename = f"ball_{i:03d}.jpg"
        img.save(f"{folder}/{filename}")
        print(f"Created {folder}/{filename}")


def create_test_sound(folder: str = "sounds") -> None:
    """Generate three simple test tones."""
    Path(folder).mkdir(parents=True, exist_ok=True)
    sample_rate: int = 44100
    for freq in range(200, 400, 100):
        filename: str = f"{folder}/test_tone_{freq}.wav"
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)  # sample rate
            frames: list[bytes] = []
            for i in range(sample_rate):
                value = math.sin(2 * math.pi * freq * i / sample_rate)
                frames.append(struct.pack('<h', int(value * 16383)))
            wav_file.writeframes(b''.join(frames))
            print(f"Created {filename}")


if __name__ == "__main__":
    image_folder = r"game/images"
    sound_folder = r"game/sounds"
    create_test_image_sequence(image_folder)
    create_test_sound(sound_folder)
