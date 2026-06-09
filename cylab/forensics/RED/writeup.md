# CTF Writeup — RED

**Platform:** CyLab Security Academy  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}`

---

## Challenge Description

> RED, RED, RED, RED

**File:** `red.png`

---

## Reconnaissance

```bash
file ~/red.png
```

Output:
```
red.png: PNG image data, 128 x 128, 8-bit/color RGBA, non-interlaced
```

PNG 128x128 với **RGBA** — có alpha channel. Tên challenge "RED" lặp 4 lần gợi ý liên quan đến color channel.

---

## Phân tích

### Bước 1 — Check metadata

```bash
exiftool ~/red.png
```

Phát hiện field **Poem** bất thường trong metadata:

```
Poem: Crimson heart, vibrant and bold,
      Hearts flutter at your sight.
      Evenings glow softly red,
      Cherries burst with sweet life.
      Kisses linger with your warmth.
      Love deep as merlot.
      Scarlet leaves falling softly,
      Bold in every stroke.
```

### Bước 2 — Acrostic cipher

Đọc chữ cái **đầu mỗi dòng**:

```
C - Crimson heart, vibrant and bold,
H - Hearts flutter at your sight.
E - Evenings glow softly red,
C - Cherries burst with sweet life.
K - Kisses linger with your warmth.
L - Love deep as merlot.
S - Scarlet leaves falling softly,
B - Bold in every stroke.
```

→ **CHECKLSB** — hint rõ ràng: dùng tool `zsteg` check LSB steganography!

### Bước 3 — LSB Steganography

```bash
sudo gem install zsteg
zsteg ~/red.png
```

Output chứa chuỗi Base64 lặp lại 4 lần:

```
cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==
```

### Bước 4 — Decode Base64

```bash
echo "cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==" | base64 -d
```

Output:
```
picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
```

---

## Attack Chain

```
red.png
    ↓ exiftool → Poem field với acrostic hint
"CHECKLSB" (chữ đầu mỗi dòng)
    ↓ zsteg red.png
Base64 string ẩn trong LSB
    ↓ base64 -d
picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
```

**3 lớp hint:**
1. Tên challenge "RED, RED, RED, RED" → red channel / steganography
2. Poem acrostic → **CHECKLSB**
3. LSB chứa Base64 → flag

---

## Result

```
picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
```

---

## Kiến thức rút ra

**1. Acrostic Cipher**

Acrostic = ẩn thông điệp trong **chữ cái đầu** mỗi dòng/câu. Rất phổ biến trong CTF Forensics và Crypto.

Khi thấy poem/text lạ trong metadata → đọc chữ đầu mỗi dòng ngay!

**2. LSB Steganography**

LSB (Least Significant Bit) = giấu data trong bit thấp nhất của mỗi pixel. Thay đổi không đáng kể về màu sắc nhưng chứa được nhiều data.

Tool detect LSB:
```bash
# PNG
zsteg file.png

# JPEG/BMP
steghide extract -sf file.jpg

# Online
stegonline.georgeom.net
```

**3. Cài zsteg trên Kali**

```bash
sudo gem install zsteg
```

**4. Quy trình phân tích PNG trong CTF**

```bash
file image.png          # verify type
exiftool image.png      # check metadata — đọc kỹ mọi field lạ
strings image.png       # tìm text ẩn
zsteg image.png         # LSB steganography
binwalk image.png       # file ẩn bên trong
```

---

## Tools Used

- **exiftool** — đọc metadata phát hiện Poem field
- **zsteg** — detect LSB steganography trong PNG
- **base64** — decode flag

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
