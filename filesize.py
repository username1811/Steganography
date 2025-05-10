import os
from writefile import write_file

def get_wav_file_size(file_path):
    """
    Tính dung lượng của file WAV.
    
    Args:
        file_path (str): Đường dẫn đến file WAV.
    
    Returns:
        int: Kích thước file (byte), hoặc None nếu file không hợp lệ.
    """
    # Kiểm tra xem file có tồn tại không
    if not os.path.isfile(file_path):
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        return None
    
    # Kiểm tra xem file có phải WAV không
    if not file_path.lower().endswith('.wav'):
        print(f"Cảnh báo: File '{file_path}' có thể không phải file WAV.")
    
    # Lấy kích thước file (byte)
    file_size_bytes = os.path.getsize(file_path)
    
    # Chuyển đổi sang KB và MB
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    
    # In thông tin
    print(f"File size of '{file_path}': {file_size_bytes} bytes ")
    
    return file_size_bytes

def compare_file_sizes(file_path1, file_path2):
    """
    So sánh kích thước của hai file WAV.
    
    Args:
        file_path1 (str): Đường dẫn đến file WAV thứ nhất.
        file_path2 (str): Đường dẫn đến file WAV thứ hai.
    """
    size1 = get_wav_file_size(file_path1)
    size2 = get_wav_file_size(file_path2)
    
    if size1 is None or size2 is None:
        print("Không thể so sánh vì một hoặc cả hai file không hợp lệ.")
        return
    
    print("Compare size of 2 files:")
    if size1 > size2:
        print(f"'{file_path1}' bigger than '{file_path2}' {size1 - size2} bytes.")
    elif size2 > size1:
        print(f"'{file_path2}' smaller than '{file_path1}' {size2 - size1} bytes.")
    else:
        print(f"'{file_path1}' and '{file_path2}' have the same size {size1} bytes.")
    
    write_file('log.txt', 'bytes')

if __name__ == "__main__":
    file_path1 = input("Enter file wav 1: ").strip()
    file_path2 = input("Enter file wav 2: ").strip()
    compare_file_sizes(file_path1, file_path2)