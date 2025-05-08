import os
import wave


def encode_text_to_audio(audio_byte_array, secret_text, max_bytes):
    """
    Encode a secret text into the audio byte array using the LSB method.

    Args:
        audio_byte_array (bytearray): The byte array of the audio file.
        secret_text (str): The secret text to encode.
        max_bytes (int): Maximum number of bytes that can be used for encoding.

    Returns:
        bytes: The encoded audio byte array, or None if an error occurs.
    """
    try:
        number_of_secret_text_bits = len(secret_text) * 8
        if number_of_secret_text_bits > max_bytes * 8:
            print("Error: Secret text is too long to encode in the audio file.")
            return None

        encoding_text = secret_text + '#' * (max_bytes - len(secret_text))

        byte_array = []
        for char in encoding_text:
            binary_char = bin(ord(char)).lstrip('0b').rjust(8, '0')
            byte_array.append(binary_char)

        encoding_text_in_bits = ''.join(byte_array)
        bits = [int(bit) for bit in encoding_text_in_bits]

        for i in range(len(bits)):
            audio_byte_array[i] = (audio_byte_array[i] & 254) | bits[i]

        encoded_audio = bytes(audio_byte_array)

        return encoded_audio
    except Exception as e:
        print("Error: Could not encode the text. {}".format(str(e)))
        return None


def save_encoded_audio(encoded_audio, original_audio_path, audio_obj):
    """
    Save the encoded audio byte array to a new WAV file.

    Args:
        encoded_audio (bytes): The encoded audio byte array.
        original_audio_path (str): Path to the original audio file.
        audio_obj (wave.Wave_read): Wave object of the original file.

    Returns:
        str: Path to the new WAV file, or None if an error occurs.
    """
    try:
        addr = os.path.dirname(original_audio_path)
        ori_file_name = os.path.basename(original_audio_path).replace('.wav', '')

        new_audio_file_address = os.path.join(addr, "{}-stego.wav".format(ori_file_name))

        new_audio_file = wave.open(new_audio_file_address, 'wb')
        new_audio_file.setparams(audio_obj.getparams())
        new_audio_file.writeframes(encoded_audio)
        new_audio_file.close()

        return new_audio_file_address
    except Exception as e:
        print("Error: Could not save audio file. {}".format(str(e)))
        return None


if __name__ == "__main__":
    audio_path = input("Enter the path to the WAV file (to hide the message): ").strip()

    if not os.path.isfile(audio_path):
        print("Error: The file does not exist.")
        exit()

    try:
        audio = wave.open(audio_path, "rb")
        n_frames = audio.getnframes()
        frames = audio.readframes(n_frames)
        audio_byte_array = bytearray(frames)
    except wave.Error:
        print("Error: Not a valid WAV file.")
        exit()

    secret_text = input("Enter the secret text to encode: ").strip()

    max_bytes = len(audio_byte_array) // 8

    encoded_audio = encode_text_to_audio(audio_byte_array, secret_text, max_bytes)

    if encoded_audio is not None:
        output_path = save_encoded_audio(encoded_audio, audio_path, audio)

        if output_path:
            print("Encoding successful! Output saved to: {}".format(output_path))
        else:
            print("Failed to save encoded audio file.")
    else:
        print("Encoding failed.")

    audio.close()