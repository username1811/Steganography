# 1. Chuẩn bị môi trường

- Máy ảo Ubuntu có cài đặt labtainer

- File imodule của labtainer stsm-decode

# 2. Các bước thực hiện

## 2.1 Khởi động bài lab

Tải bài lab, gõ:

    imodule https://github.com/username1811/Steganography/raw/master/imodule.tar 

Vào terminal, gõ:

    labtainer -r stsm-decode

(Chú ý: sinh viên sử dụng mã sinh viên của mình để nhập thông tin email người thực hiện bài lab khi có yêu cầu, để sử dụng khi chấm điểm)

## 2.2 Thực hiện bài lab

Bài lab gồm các file sau: 
- demo.wav: file âm thanh gốc, dùng để giấu tin
- message.txt: file chứa thông điệp cần giấu
- encode.py: Nhận một file WAV và file txt, giấu nội dung file txt vào file âm thanh bằng kỹ thuật Time Scale Modification, tạo ra file WAV mới chứa thông điệp.
- decode.py: Nhận một file WAV đã được giấu tin, ghi thông điệp giải được ra file message2.txt
- checkmessages.py: kiểm tra thông điệp trước khi giấu tin và sau khi tách tin xem có trùng khớp không.
- writefile.py: Ghi nội dung lên file cụ thể

### Bước 1: Sử dụng các lệnh ls để xem các file có trong bài thực hành

    ls -l 

### Bước 2: Xem file message.txt

    nano message.txt


### Bước 3: Tiến hành giấu tin vào file WAV và xuất ra 1 file mới 

    python3 encode.py

Nhập tên file wav và file message

Sau khi giấu tin thành công, đoạn mã sẽ tạo ra 1 file wav mới

Sử dụng lệnh ls để xem file mới được tạo


### Bước 4: Tiến hành giải mã thông điệp được giấu 

    python3 decode.py

Nhập vào file wav sau khi giấu, thông điệp giải được sẽ được lưu ở file message2.txt


### Bước 5: Kiểm tra thông điệp trước khi giấu và sau khi giải

    python3 checkmessages.py


# 3. Kiểm tra kết quả

Sử dụng lệnh: 

    checkwork

# 4. Kết thúc bài lab

    stoplab

# 5. Khởi động lại bài lab (nếu cần)

    labtainer -r stsm-decode
