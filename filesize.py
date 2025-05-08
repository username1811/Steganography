import os

def get_wav_file_size(file_path):
    """
    Tính và in ra dung lượng của file WAV.
    
    Args:
        file_path (str): Đường dẫn đến file WAV.
    
    Returns:
        None: In ra thông tin dung lượng.
    """
    # Kiểm tra xem file có tồn tại không
    if not os.path.isfile(file_path):
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        return
    
    # Kiểm tra xem file có phải WAV không
    if not file_path.lower().endswith('.wav'):
        print(f"Cảnh báo: File '{file_path}' có thể không phải file WAV.")
    
    # Lấy kích thước file (byte)
    file_size_bytes = os.path.getsize(file_path)
    
    # Chuyển đổi sang KB và MB
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    
    # In thông tin
    print(f"File size of '{file_path}':" + f"{file_size_bytes} byte")

if __name__ == "__main__":
    file_path = input("Enter file WAV: ").strip()
    get_wav_file_size(file_path)