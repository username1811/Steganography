import wave
import struct
import os
from writefile import write_file

def extract_bits(audio_path, max_samples=10000):
    """
    Trích xuất các bit tiềm năng từ phần đầu file âm thanh bằng cách kiểm tra tổng của ba mẫu.
    
    Args:
        audio_path (str): Đường dẫn đến file âm thanh
        max_samples (int): Số mẫu tối đa để kiểm tra (phần đầu file)
        
    Returns:
        list: Danh sách các bit trích xuất
    """
    try:
        with wave.open(audio_path, 'rb') as audio:
            params = audio.getparams()
            sample_width = audio.getsampwidth()
            n_frames = audio.getnframes()
            # Chỉ đọc số frame cần thiết để lấy tối đa max_samples
            frames_to_read = min(n_frames, max_samples * sample_width)
            frames = audio.readframes(frames_to_read)
    except wave.Error:
        raise ValueError(f"Invalid WAV file: {audio_path}")
    
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
    
    extracted_bits = []
    for i in range(0, len(samples) - 2, 3):
        sample_sum = samples[i] + samples[i+1] + samples[i+2]
        extracted_bits.append(1 if sample_sum % 2 == 1 else 0)
    
    return extracted_bits

def check_hamming_structure(bits):
    """
    Kiểm tra xem danh sách bit có tuân theo cấu trúc mã Hamming (7,4) hay không.
    
    Args:
        bits (list): Danh sách các bit trích xuất
        
    Returns:
        bool: True nếu phù hợp với mã Hamming, False nếu không
    """
    if len(bits) < 7:
        return False
    
    valid_groups = 0
    total_groups = len(bits) // 7
    for i in range(0, len(bits) - 6, 7):
        p1, p2, d1, p3, d2, d3, d4 = bits[i:i+7]
        # Kiểm tra các bit kiểm tra của mã Hamming
        if (p1 == d1 ^ d2 ^ d4) and (p2 == d1 ^ d3 ^ d4) and (p3 == d2 ^ d3 ^ d4):
            valid_groups += 1
    
    # Nếu hơn 50% nhóm bit phù hợp với cấu trúc Hamming, coi như có giấu tin
    print("hamming structure rate is: " + str(float(valid_groups/total_groups)))
    return valid_groups > total_groups * 0.5

def detect_stsm(suspect_path):
    """
    Phát hiện giấu tin trong phần đầu file âm thanh bằng cách kiểm tra mã Hamming.
    
    Args:
        suspect_path (str): Đường dẫn đến file âm thanh nghi ngờ
        
    Returns:
        dict: Kết quả phát hiện với các thông tin chi tiết
    """
    result = {
        "steganography_detected": False,
        "hamming_structure": False,
        "message": ""
    }
    
    try:
        # Trích xuất bit từ phần đầu file nghi ngờ
        extracted_bits = extract_bits(suspect_path)
        
        # Kiểm tra cấu trúc mã Hamming
        result["hamming_structure"] = check_hamming_structure(extracted_bits)
        
        # Kết luận
        result["steganography_detected"] = result["hamming_structure"]
        
        if result["steganography_detected"]:
            result["message"] = "Steganography detected in the suspect file! (Hamming structure detected)"
            write_file('log.txt', 'Hamming structure detected')
        else:
            result["message"] = "No steganography detected."
            write_file('log.txt', 'No steganography detected')
        
        # Ghi log vào file
    
    except ValueError as e:
        result["message"] = f"Error: {str(e)}"
        write_file('log.txt', result["message"])
    
    return result

def main():
    """
    Hàm chính để chạy chương trình phát hiện giấu tin.
    """
    print("STSM Steganography Detection Tool")
    suspect_path = input("Enter suspect WAV file path: ").strip()
    
    # Kiểm tra file có tồn tại không
    if not os.path.isfile(suspect_path):
        print(f"Error: Suspect file not found: {suspect_path}")
        write_file('log.txt', f"Error: Suspect file not found: {suspect_path}")
        return
    
    # Chạy phát hiện
    result = detect_stsm(suspect_path)
    print(result["message"])

if __name__ == "__main__":
    main()