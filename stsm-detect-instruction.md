
# 1. Chuẩn bị môi trường

- Máy ảo Ubuntu có cài đặt labtainer

- File imodule của labtainer stsm-detect

# 2. Các bước thực hiện

## 2.1 Khởi động bài lab

Tải bài lab, gõ:

    imodule https://github.com/username1811/Steganography/raw/master/imodule.tar 

Vào terminal, gõ:

    labtainer -r stsm-detect

(Chú ý: sinh viên sử dụng mã sinh viên của mình để nhập thông tin email người thực hiện bài lab khi có yêu cầu, để sử dụng khi chấm điểm)

## 2.2 Thực hiện bài lab

Bài lab gồm các file sau: 
- demo.wav: file âm thanh gốc, dùng để giấu tin
- message.txt: file chứa thông điệp cần giấu
- encode.py: Nhận một file WAV và file txt, giấu nội dung file txt vào file âm thanh bằng kỹ thuật Time Scale Modification, tạo ra file WAV mới chứa thông điệp.
- checksteg.py: Phát hiện file WAV đã được giấu tin bằng cách kiểm tra tỉ lệ mã hamming
- writefile.py: Ghi nội dung lên file cụ thể

### Bước 1: Sử dụng các lệnh ls để xem các file có trong bài thực hành

    ls -l 

### Bước 2: Sửa file message.txt

    nano message.txt
Điền mã sinh viên

### Bước 3: Tiến hành giấu tin vào file WAV và xuất ra 1 file mới 

    python3 encode.py

Nhập tên file wav và file message

Sau khi giấu tin thành công, đoạn mã sẽ tạo ra 1 file wav mới

Sử dụng lệnh ls để xem file mới được tạo


### Bước 4: Tiến hành phát hiện giấu tin file gốc demo.wav

    python3 checksteg.py

Nhập vào demo.wav

### Bước 5: Tiến hành phát hiện giấu tin file đã giấu demo_steg.wav

     python3 checksteg.py
Nhập vào demo_steg.wav

# 3. Kiểm tra kết quả

Sử dụng lệnh: 

    checkwork
![checkwork-stsm-detect](https://github.com/user-attachments/assets/3bc6ea10-544c-4282-9274-0d6aab3b83c3)


# 4. Kết thúc bài lab

    stoplab

# 5. Khởi động lại bài lab (nếu cần)

    labtainer -r stsm-detect
