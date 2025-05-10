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
    return bits

def encode_stsm(audio_path, secret_text, output_path=None):
    """
    Mã hóa văn bản bí mật vào file âm thanh sử dụng phương pháp STSM
    
    Args:
        audio_path (str): Đường dẫn đến file âm thanh gốc
        secret_text (str): Văn bản bí mật cần mã hóa
        output_path (str, optional): Đường dẫn file đầu ra
        
    Returns:
        str: Đường dẫn đến file âm thanh đã mã hóa
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
    
    # Tạo output path nếu chưa có
    if output_path is None:
        dir_name = os.path.dirname(audio_path)
        file_name = os.path.basename(audio_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        output_path = os.path.join(dir_name, f"{file_name_without_ext}_steg.wav")
    
    # Bước 1: Mã hóa văn bản thành các bit
    secret_text += "#"  # Thêm ký tự kết thúc
    text_bits = string_to_bits(secret_text)
    
    # Đảm bảo độ dài là bội số của 4
    while len(text_bits) % 4 != 0:
        text_bits.append(0)
    
    # Áp dụng mã Hamming (7,4)
    encoded_bits = hamming_encode(text_bits)
    
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
    
    # Bước 2: Giấu tin
    # Kiểm tra đủ không gian
    required_samples = len(encoded_bits) * 3
    if len(samples) < required_samples:
        print(f"Lỗi: File âm thanh quá ngắn để giấu thông điệp. Cần ít nhất {required_samples} mẫu.")
        return None
    
    bit_index = 0
    # Xử lý từng nhóm 3 mẫu liên tiếp
    for i in range(0, len(samples) - 2, 3):
        if bit_index >= len(encoded_bits):
            break
        
        # Lấy bit hiện tại cần giấu
        current_bit = encoded_bits[bit_index]
        
        # Tính tổng của 3 mẫu
        sample_sum = samples[i] + samples[i+1] + samples[i+2]
        is_odd = sample_sum % 2 == 1
        
        if current_bit == 1:
            # Nếu bit là 1, tổng phải là lẻ
            if not is_odd:  # Tổng hiện tại là chẵn
                samples[i+1] += 1  # Điều chỉnh mẫu thứ 2
        else:
            # Nếu bit là 0, tổng phải là chẵn
            if is_odd:  # Tổng hiện tại là lẻ
                # Điều chỉnh mẫu 1 hoặc mẫu 3
                samples[i] += 1  # Chọn điều chỉnh mẫu thứ 1
        
        bit_index += 1
    
    # Chuyển samples trở lại thành bytes
    modified_frames = bytearray()
    for sample in samples:
        if sample_width == 1:
            modified_frames.append(sample & 0xFF)
        elif sample_width == 2:
            modified_frames.extend(struct.pack('<h', sample))
        elif sample_width == 4:
            modified_frames.extend(struct.pack('<i', sample))
    
    # Ghi ra file mới
    with wave.open(output_path, 'wb') as new_audio:
        new_audio.setparams(params)
        new_audio.writeframes(bytes(modified_frames))
    
    write_file("log.txt", "encode_stsm");
    return output_path

if __name__ == "__main__":
    audio_path = input("Enter wav file: ").strip()
    
    if not os.path.isfile(audio_path):
        print("File not found.")
        exit()
    
    try:
        # Kiểm tra xem có phải file WAV không
        with wave.open(audio_path, 'rb') as audio:
            n_frames = audio.getnframes()
            sample_width = audio.getsampwidth()
            n_channels = audio.getnchannels()
    except wave.Error:
        print("Invalid wav file.")
        exit()
    
    secret_text_file = input("Enter secret text file: ").strip()
    with open(secret_text_file, 'r', encoding='utf-8') as secretfile:
        secret_text = secretfile.read()
    
    # Tính toán số byte tối đa có thể giấu
    max_bits = n_frames // 3  # Mỗi bit cần 3 mẫu
    max_hamming_groups = max_bits // 7  # Mỗi nhóm 7 bit hamming mã hóa cho 4 bit dữ liệu
    max_chars = (max_hamming_groups * 4) // 8  # Chuyển bit thành ký tự (8 bit/ký tự)
    
    if len(secret_text) > max_chars:
        print(f"Secret text is too long.")
        exit()
    
    output_path = encode_stsm(audio_path, secret_text)
    
    if output_path:
        print(f"Encode successfully, file save at: {output_path}")
    else:
        print("Encode failed.")