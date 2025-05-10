import os
import wave
import struct
from writefile import write_file


if __name__ == "__main__":
    with open('message.txt', 'r', encoding='utf-8') as secretfile:
        secret_text = secretfile.read()
    with open('message.txt', 'r', encoding='utf-8') as secretfile2:
        secret_text2 = secretfile2.read()
    if(secret_text == secret_text2):
        print("2 messages are the same")
        write_file('log.txt', 'same_messages')
    else:
        print("2 messages are not the same")