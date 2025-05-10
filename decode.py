import os
import wave
import struct
from writefile import write_file

def hamming_decode(encoded_bits):
    """
    Giải mã chuỗi bit sử dụng mã Hamming (7,4)
    
    Args:
        encoded_bits (list): Danh sách các bit đã mã hóa Hamming
        
    Returns:
        list: Danh sách các bit dữ liệu gốc
    """
    decoded_bits = []
    
    # Xử lý từng nhóm 7 bit
    for i in range(0, len(encoded_bits), 7):
        if i + 6 < len(encoded_bits):
            # Lấy 7 bit mã hóa (p1, p2, d1, p3, d2, d3, d4)
            p1, p2, d1, p3, d2, d3, d4 = encoded_bits[i:i+7]
            
            # Kiểm tra lỗi (bỏ qua trong trường hợp này vì chúng ta 
            # chỉ sử dụng mã Hamming để mã hóa)
            
            # Thêm 4 bit dữ liệu gốc
            decoded_bits.extend([d1, d2, d3, d4])
    
    write_file("log.txt", "hamming_decode");
    return decoded_bits

def bits_to_string(bits):
    """
    Chuyển danh sách các bit thành văn bản
    
    Args:
        bits (list): Danh sách các bit
        
    Returns:
        str: Văn bản đã giải mã
    """
    # Đảm bảo số bit là bội số của 8
    while len(bits) % 8 != 0:
        bits.append(0)
    
    text = ""
    for i in range(0, len(bits), 8):
        if i + 7 < len(bits):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            
            # Dừng khi gặp ký tự '#' (dấu hiệu kết thúc)
            if byte == ord('#'):
                break
                
            text += chr(byte)
    
    write_file("log.txt", "bits_to_string");
    return text

def decode_stsm(audio_path):
    """
    Giải mã thông điệp bí mật từ file âm thanh sử dụng phương pháp STSM
    
    Args:
        audio_path (str): Đường dẫn đến file âm thanh đã mã hóa
        
    Returns:
        str: Thông điệp bí mật
    """
    # Mở file âm thanh
    with wave.open(audio_path, 'rb') as audio:
        # Đọc thông tin header
        params = audio.getparams()
        n_channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        framerate = audio.getframerate()
        n_frames = audio.getnframes()
        
        # Đọc toàn bộ dữ liệu
        frames = audio.readframes(n_frames)
    
    # Chuyển samples từ bytes sang dạng số nguyên
    samples = []
    for i in range(0, len(frames), sample_width):
        if i + sample_width <= len(frames):
            if sample_width == 1:
                sample = frames[i]
                samples.append(sample)
            elif sample_width == 2:
                sample = struct.unpack('<h', frames[i:i+2])[0]
                samples.append(sample)
            elif sample_width == 4:
                sample = struct.unpack('<i', frames[i:i+4])[0]
                samples.append(sample)
    
    # Bước 1: Trích xuất các bit mã hóa
    # Nhóm các mẫu thành nhóm 3 mẫu
    encoded_bits = []
    for i in range(0, len(samples) - 2, 3):
        # Tính tổng của 3 mẫu
        sample_sum = samples[i] + samples[i+1] + samples[i+2]
        
        # Xác định bit dựa trên tính chẵn lẻ của tổng
        if sample_sum % 2 == 1:  # Tổng lẻ -> bit 1
            encoded_bits.append(1)
        else:  # Tổng chẵn -> bit 0
            encoded_bits.append(0)
    
    # Bước 2: Giải mã Hamming
    # Giải mã các bit sử dụng mã Hamming
    decoded_bits = hamming_decode(encoded_bits)
    
    # Bước 3: Chuyển bit thành văn bản
    secret_text = bits_to_string(decoded_bits)
    
    write_file("log.txt", "decode_stsm");
    return secret_text

if __name__ == "__main__":
    audio_path = input("Enter wav file: ").strip()
    
    if not os.path.isfile(audio_path):
        print("File not found.")
        exit()
    
    try:
        # Kiểm tra xem có phải file WAV không
        with wave.open(audio_path, 'rb') as audio:
            pass
    except wave.Error:
        print("invalid wav !")
        exit()
    
    secret_text = decode_stsm(audio_path)
    write_file('message2.txt', secret_text)
    with open('message2.txt', 'w') as file:
            file.write(f"{secret_text}\n")
    print("secret text is saved at message2.txt")