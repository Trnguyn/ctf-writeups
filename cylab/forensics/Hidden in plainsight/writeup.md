# CTF Writeup — Hidden in Image

**Platform:** CyLab Security Academy  
**Category:** Forensics / Steganography  
**Difficulty:** Beginner - Intermediate  
**Flag:** `picoCTF{h1dd3n_1n_1m4g3_871ba555}`

---

## Challenge Description

> You’re given a seemingly ordinary JPG image. Something is tucked away out of sight inside the file. Your task is to discover the hidden payload and extract the flag.

**File:** `img.jpg`

---

## Reconnaissance

Bước đầu tiên — identify file type và check magic bytes:

```
FF D8 FF E0  →  ÿØÿà + JFIF
```

Confirm đây là JPEG hợp lệ. Chạy `strings` để tìm text ẩn:

```bash
strings image.jpg | head -20
```

Phát hiện dòng đáng ngờ ngay trong output:

```
c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9
```

---

## Phân tích

### Bước 1 — Nhận diện encoding lớp 1

Chuỗi `c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9` có đặc điểm:
- Chỉ dùng ký tự `A-Z`, `a-z`, `0-9`
- Kết thúc bằng `=`
- → **Base64**

Decode bằng CyberChef → **From Base64**:

```
c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9  →  steghide:cEF6ZW5kdmNyQ=
```

### Bước 2 — Nhận diện encoding lớp 2

Kết quả `steghide:cEF6ZW5kdmNyQ=` có 2 phần:
- `steghide` → tên tool steganography
- `cEF6ZW5kdmNyQ=` → chuỗi Base64 tiếp theo

Decode phần sau → **From Base64** lần 2:

```
cEF6ZW5kdmNyQ=  →  pAzzword
```

**Kết luận:** File ảnh có data ẩn được nhúng bằng **steghide** với password `pAzzword`.

### Bước 3 — Extract steganography

Dùng tool online steghide extract với password vừa tìm được:

```
Tool: futureboy.us/stegano/decinput.html
File: img.jpg
Password: pAzzword
```


Sau khi nhập password vào tool online steghide extract, flag hiện ra ngay lập tức:

```
picoCTF{h1dd3n_1n_1m4g3_871ba555}
```

---

## Attack Chain

```
image.jpg
    ↓ strings
Base64 string trong file
    ↓ From Base64 (lần 1)
"steghide:cEF6ZW5kdmNyQ="
    ↓ From Base64 (lần 2)
"steghide:pAzzword"
    ↓ steghide extract -p 'pAzzword'
picoCTF{h1dd3n_1n_1m4g3_871ba555}
```

**4 lớp bảo vệ:**
1. Base64 encoding lớp 1
2. Base64 encoding lớp 2
3. Steganography (steghide)
4. Flag

---

## Result

```
picoCTF{h1dd3n_1n_1m4g3_871ba555}
```

---

## Kiến thức rút ra

**1. Steganography là gì?**

Steganography là kỹ thuật **giấu dữ liệu bên trong file khác** mà không làm thay đổi file gốc đáng kể. Khác với mã hóa (encryption) — mã hóa làm dữ liệu không đọc được, steganography làm dữ liệu **vô hình**.

Các loại steganography phổ biến trong CTF:

| Tool | File type | Cách detect |
|------|-----------|-------------|
| steghide | JPG, BMP | `strings`, `steghide info` |
| zsteg | PNG | `zsteg file.png` |
| binwalk | Bất kỳ | `binwalk file` |
| exiftool | Ảnh | `exiftool file` |

**2. Quy trình phân tích ảnh trong CTF Forensics:**

```bash
# Bước 1 — identify
file image.jpg

# Bước 2 — metadata
exiftool image.jpg

# Bước 3 — strings
strings image.jpg | grep -i "flag\|ctf\|pass\|hidden"

# Bước 4 — embedded files
binwalk image.jpg

# Bước 5 — steganography
steghide info image.jpg
steghide extract -sf image.jpg -p "password"

# Bước 6 — LSB steganography (PNG)
zsteg image.png
```

**3. Multi-layer encoding — tư duy quan trọng**

Khi gặp chuỗi lạ, luôn hỏi:
- Đây là encoding gì? (Base64, Hex, Binary, ROT13...)
- Decode ra có ý nghĩa không?
- Nếu chưa readable → decode tiếp!

Không bao giờ dừng lại sau một bước nếu output vẫn còn "lạ".

---

## Tools Used

- **strings** — tìm text ẩn trong binary file
- **CyberChef** — From Base64, From Binary
- **futureboy.us/stegano** — online steghide extract

---

## Author

| | |
|---|---|
| **Author** | Nguyễn Trung Nguyên |
| **Team** | grep_and_pray |
| **CTFtime** | [grep_and_pray](https://ctftime.org) |
| **Date** | 2026-06-08 |
| **Platform** | CyLab Security Academy |

---

*Writeup by **grep_and_pray** (Nguyễn Trung Nguyên)*  
*AI-assisted documentation: Claude (Anthropic) — dùng để hỗ trợ viết writeup và giải thích kiến thức. Challenge được tự giải.*
