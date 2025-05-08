import os
import wave

def decode_text_from_audio(audio_byte_array):
    """
    Decode the hidden text from an audio byte array using the LSB method.

    Args:
        audio_byte_array (bytearray): The byte array of the encoded audio file.

    Returns:
        str: The decoded secret text, or None if an error occurs.
    """
    try:
        # Extract the least significant bit from each byte
        bits = [byte & 1 for byte in audio_byte_array]

        # Convert every 8 bits into a character
        secret_chars = []
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i + 8]
            if len(byte_bits) < 8:
                break
            char_code = int(''.join(map(str, byte_bits)), 2)
            character = chr(char_code)
            secret_chars.append(character)

        # Join characters and cut off at the terminator symbol '#'
        padded_text = ''.join(secret_chars)
        original_text = padded_text.split('#')[0]

        return original_text
    except Exception as e:
        print("Error: Could not decode the text. {}".format(str(e)))
        return None


if __name__ == "__main__":
    audio_path = input("Enter the path to the WAV file (to extract the hidden message): ").strip()

    if not os.path.isfile(audio_path):
        print("Error: The file does not exist.")
        exit()

    try:
        audio = wave.open(audio_path, "rb")
        n_frames = audio.getnframes()
        frames = audio.readframes(n_frames)
        audio_byte_array = bytearray(frames)
        audio.close()
    except wave.Error:
        print("Error: Not a valid WAV file.")
        exit()
    except Exception as e:
        print("Error reading the audio file: {}".format(str(e)))
        exit()

    decoded_text = decode_text_from_audio(audio_byte_array)

    if decoded_text:
        print("Decoded secret text: {}".format(decoded_text))
    else:
        print("Could not extract any secret text.")