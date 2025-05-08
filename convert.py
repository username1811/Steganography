import wave
import os

def convert_audio_to_byte_array(audio_file):
    """
    Convert a WAV audio file to a byte array.
    """
    try:
        if not os.path.isfile(audio_file):
            print("Error: File {} does not exist.".format(audio_file))
            return None, None

        audio = wave.open(audio_file, "rb")
        number_of_audio_frames = audio.getnframes()
        audio_frames = audio.readframes(number_of_audio_frames)
        audio_in_byte_array = bytearray(audio_frames)

        return audio_in_byte_array, audio

    except wave.Error:
        print("Error: File {} is not a valid WAV file.".format(audio_file))
        return None, None

if __name__ == "__main__":
    audio_path = input("Enter the path to the WAV file: ").strip()
    byte_array, audio_obj = convert_audio_to_byte_array(audio_path)

    if byte_array is not None and audio_obj is not None:
        print("Byte array of the audio file ({} bytes):".format(len(byte_array)))
        print(list(byte_array[:100]))
        audio_obj.close()
    else:
        print("Failed to convert the audio file.")