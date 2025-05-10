import os
import wave
import struct
from writefile import write_file

def hamming_encode(data_bits):
    """
    Mã hóa chuỗi bit sử dụng mã Hamming (7,4)
    
    Args:
        data_bits (list): Danh sách các bit dữ liệu (mỗi phần tử 4 bit)
        
    Returns:
        list: Danh sách các bit đã mã hóa Hamming (mỗi phần tử 7 bit)
    """
    encoded_bits = []
    
    # Xử lý từng nhóm 4 bit
    for i in range(0, len(data_bits), 4):
        if i + 3 < len(data_bits):
            # Lấy 4 bit dữ liệu
            d1, d2, d3, d4 = data_bits[i:i+4]
            
            # Tính các bit chẵn lẻ
            p1 = d1 ^ d2 ^ d4
            p2 = d1 ^ d3 ^ d4  
            p3 = d2 ^ d3 ^ d4
            
            # Thêm vào danh sách bit đã mã hóa
            encoded_bits.extend([p1, p2, d1, p3, d2, d3, d4])
    write_file("log.txt", "hamming_encode");
    return encoded_bits

def string_to_bits(text):
    """
    Chuyển văn bản thành danh sách các bit
    
    Args:
        text (str): Văn bản cần chuyển đổi
        
    Returns:
        list: Danh sách các bit
    """
    bits = []
    for char in text:
        # Chuyển mỗi ký tự thành 8 bit
        char_bits = bin(ord(char))[2:].zfill(8)
        for bit in char_bits:
            bits.append(int(bit))
    write_file("log.txt", "string_to_bits");
    return bits

if __name__ == "__main__":
    file_path = input("Enter file message: ").strip()
    with open(file_path, 'r', encoding='utf-8') as secretfile:
        secret_text = secretfile.read()
    secret_text += "#"  # Thêm ký tự kết thúc
    text_bits = string_to_bits(secret_text)
    
    # Đảm bảo độ dài là bội số của 4
    while len(text_bits) % 4 != 0:
        text_bits.append(0)
    
    # Áp dụng mã Hamming (7,4)
    encoded_bits = hamming_encode(text_bits)
    print('hamming code of message is: ' + str(encoded_bits))
    write_file('log.txt', 'hamming')