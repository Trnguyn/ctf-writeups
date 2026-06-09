# CTF Writeup — Flag in Flame

**Platform:** CyLab Security Academy  
**Category:** Forensics  
**Difficulty:** Easy (100 pts)  
**Author:** Prince Niyonshuti N.  
**Flag:** `picoCTF{forensics_analysis_is_amazing_782e55c9}`

---

## Challenge Description

> The SOC team discovered a suspiciously large log file after a recent breach. When they opened it, they found an enormous block of encoded text instead of typical logs. Could there be something hidden within? Your mission is to inspect the resulting file and reveal the real purpose of it. The team is relying on your skills to uncover any concealed information within this unusual log.

**File:** `logs.txt`

---

## Reconnaissance

Mở file `logs.txt` ra thấy toàn bộ nội dung là một khối text lớn — không phải log bình thường. Nhận diện encoding:

- Chỉ dùng ký tự `A-Z`, `a-z`, `0-9`, `+`, `/`
- Kết thúc bằng `=`
- → **Base64**

---

## Phân tích

### Bước 1 — Decode Base64

Thay vì dùng CyberChef (có thể bị lỗi encoding khi save), decode trực tiếp trên Linux:

```bash
base64 -d logs.txt > flag.png
file flag.png
```

Output:
```
flag.png: PNG image data, 896 x 1152, 8-bit/color RGB, non-interlaced
```

File Base64 thực chất là một **ảnh PNG** bị giấu bên trong log file giả.

> **Lưu ý quan trọng:** Nếu dùng CyberChef để decode và save, file PNG có thể bị corrupt do encoding sai. Nên dùng terminal để decode binary data chính xác hơn.

### Bước 2 — Xem ảnh

```bash
eog flag.png
```

Ảnh hiện ra là một hình cyberpunk/SOC theme với một dãy ký tự ở phía dưới:

```
7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F37383265353563397D
```

### Bước 3 — Nhận diện encoding

Dãy ký tự chỉ gồm `0-9` và `A-F` → **Hex encoding**.

Decode bằng CyberChef → **From Hex**:

```
7069636F4354467B...7D  →  picoCTF{forensics_analysis_is_amazing_782e55c9}
```

---

## Attack Chain

```
logs.txt (Base64)
    ↓ base64 -d
flag.png (PNG image 896x1152)
    ↓ mở ảnh → thấy dãy hex ở dưới
7069636F...7D (Hex string)
    ↓ From Hex
picoCTF{forensics_analysis_is_amazing_782e55c9}
```

**3 lớp:**
1. Log file giả — thực chất là Base64
2. PNG ẩn chứa Hex string
3. Hex → Flag

---

## Result

```
picoCTF{forensics_analysis_is_amazing_782e55c9}
```

---

## Kiến thức rút ra

**1. File giả mạo (File Disguise)**

Attacker thường giấu file bên trong file khác bằng encoding:
- Text file chứa Base64 → thực ra là ảnh/binary
- Log file bất thường → luôn check encoding trước

**2. Decode binary data đúng cách**

Khi decode Base64 ra binary (ảnh, zip, exe...) nên dùng terminal thay vì CyberChef:

```bash
# Đúng — decode ra binary chính xác
base64 -d input.txt > output.bin
file output.bin

# Sai — CyberChef có thể lỗi encoding khi save
```

**3. Hex trong ảnh**

Flag ẩn trong ảnh không phải lúc nào cũng dùng steganography — đôi khi chỉ đơn giản là **in thẳng vào ảnh dưới dạng encoded text**.

Quy trình khi thấy ảnh trong CTF:
```
1. Đọc kỹ toàn bộ ảnh — tìm text ẩn, QR code, pattern lạ
2. Check metadata — exiftool
3. Check strings — strings file.png
4. Check steganography — zsteg, binwalk, steghide
```

**4. Nhận diện Hex nhanh**

- Chỉ dùng ký tự `0-9` và `A-F` (hoặc `a-f`)
- Độ dài luôn **chẵn** (mỗi byte = 2 ký tự)
- Ví dụ: `7069636F` = `pico`

---

## Tools Used

- **base64** — decode Base64 trên Linux terminal
- **file** — verify file type sau khi decode
- **eog** — mở ảnh PNG trên Kali
- **CyberChef** — From Hex decode

---

## Author

| | |
|---|---|
| **Author** | Nguyễn Trung Nguyên |
| **Team** | grep_and_pray |
| **CTFtime** | [grep_and_pray](https://ctftime.org) |
| **Date** | 2026-06-09 |
| **Platform** | CyLab Security Academy |

---

*Writeup by **grep_and_pray** (Nguyễn Trung Nguyên)*  
*AI-assisted documentation: Claude (Anthropic) — dùng để hỗ trợ viết writeup và giải thích kiến thức. Challenge được tự giải.*
