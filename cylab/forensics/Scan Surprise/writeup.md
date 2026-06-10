# CTF Writeup — Scan Surprise

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{p33k_@_b00_3f7cf1ae}`

---

## Challenge Description

> I've gotten bored of handing out flags as text. Wouldn't it be cool if they were an image instead?

**File:** `flag.png`

---

## Reconnaissance

Giải nén file challenge:

```bash
unzip challenge.zip
# creating: home/ctf-player/drop-in/
# extracting: home/ctf-player/drop-in/flag.png
```

Bước đầu tiên — check metadata với `exiftool`:

```bash
exiftool home/ctf-player/drop-in/flag.png
```

Output:

```
File Name                       : flag.png
File Size                       : 341 bytes
Image Width                     : 99
Image Height                    : 99
Bit Depth                       : 1
Color Type                      : Palette
```

Metadata sạch, không có gì ẩn. File là PNG 99x99 pixels — kích thước nhỏ, gợi ý đây là QR code.

---

## Phân tích

### Bước 1 — Nhận diện QR Code

Tên challenge "Scan Surprise" → "Scan" là hint rõ ràng. Kết hợp với kích thước ảnh 99x99 pixels → đây là QR code chứa flag.

### Bước 2 — Decode QR Code

Kali không có sẵn `zbar-tools`, dùng Python thay thế:

```bash
sudo apt install libzbar0 -y
pip install pyzbar pillow --break-system-packages

python3 -c "
from pyzbar.pyzbar import decode
from PIL import Image
print(decode(Image.open('home/ctf-player/drop-in/flag.png')))
"
```

Output:

```
[Decoded(data=b'picoCTF{p33k_@_b00_3f7cf1ae}', type='QRCODE', 
rect=Rect(left=12, top=12, width=74, height=74), quality=1, orientation='UP')]
```

---

## Attack Chain

```
flag.png (PNG 99x99)
    ↓ exiftool → metadata sạch
Tên bài "Scan" + ảnh nhỏ → nghi ngờ QR code
    ↓ pyzbar decode
picoCTF{p33k_@_b00_3f7cf1ae}
```

---

## Result

```
picoCTF{p33k_@_b00_3f7cf1ae}
```

---

## Kiến thức rút ra

**1. Tên challenge là hint mạnh nhất**

"Scan Surprise" → "Scan" = quét QR. Trong CTF, tên bài thường gợi ý trực tiếp kỹ thuật cần dùng.

**2. pyzbar thay thế zbar-tools**

Trên Kali, `zbar-tools` đôi khi không tìm thấy trong repo. `pyzbar` là Python wrapper cho libzbar, cài dễ hơn và kết quả tương đương.

**3. Quy trình chuẩn khi gặp ảnh trong CTF**

```
exiftool    → check metadata
strings     → tìm text ẩn
binwalk     → tìm file ẩn bên trong
steghide    → check steganography
pyzbar      → decode QR nếu nghi ngờ
```

---

## Tools Used

- **exiftool** — kiểm tra metadata ảnh
- **libzbar0 + pyzbar** — decode QR code
- **Pillow** — đọc file ảnh trong Python

---

## Author

|              |                                        |
| ------------ | -------------------------------------- |
| **Author**   | Nguyễn Trung Nguyên                    |
| **Team**     | grep\_and\_pray                        |
| **CTFtime**  | [grep\_and\_pray](https://ctftime.org) |
| **Date**     | 2026-06-10                             |
| **Platform** | CyLab Security Academy                 |

---

*Writeup by **grep_and_pray** (Nguyễn Trung Nguyên)*  
*AI-assisted documentation: Claude (Anthropic) — dùng để hỗ trợ viết writeup và giải thích kiến thức. Challenge được tự giải.*
