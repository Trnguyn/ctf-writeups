# CTF Writeup — Secret of the Polyglot

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{f1u3n7_1n_pn9_&_pdf_1f991f77}`

---

## Challenge Description

> The Network Operations Center (NOC) of your local institution picked up a suspicious file, they're getting conflicting information on what type of file it is. They've brought you in as an external expert to examine the file. Can you extract all the information from this strange file?

**File:** `flag2of2-final.pdf`

---

## Reconnaissance

Bước đầu tiên — check type và metadata:

```bash
file /home/kali/flag2of2-final.pdf
```

Output bất ngờ:

```
flag2of2-final.pdf: PNG image data, 50 x 50, 8-bit/color RGBA, non-interlaced
```

File có extension `.pdf` nhưng `file` command nhận diện là **PNG** — đây là dấu hiệu rõ ràng của polyglot file.

Check metadata với `exiftool`:

```bash
exiftool /home/kali/flag2of2-final.pdf
```

Phần lớn metadata bình thường, nhưng có 1 dòng quan trọng:

```
Warning: [minor] Trailer data after PNG IEND chunk
```

**IEND** là chunk kết thúc của PNG — sau đó không được có gì nữa. "Trailer data" xác nhận có dữ liệu ẩn phía sau phần PNG.

---

## Phân tích

### Bước 1 — Confirm cấu trúc polyglot

Check hex dump phần đầu:

```bash
xxd /home/kali/flag2of2-final.pdf | head -3
```

```
00000000: 8950 4e47 0d0a 1a0a ...   .PNG........
```

Magic bytes `89 50 4E 47` → đầu file là PNG hợp lệ.

Check phần cuối:

```bash
xxd /home/kali/flag2of2-final.pdf | tail -20
```

```
...trailer.<< /Size 10 /Root 1 0 R...
...startxref.2095.%%EOF
```

`%%EOF` là End of File marker của PDF — xác nhận phần cuối file là PDF hợp lệ.

Cấu trúc file:

```
[PNG data] → IEND chunk → [PDF data] → %%EOF
```

### Bước 2 — Đọc phần PDF

Mở trực tiếp bằng evince:

```bash
evince /home/kali/flag2of2-final.pdf
```

PDF hiện ra text:

```
1n_pn9_&_pdf_1f991f77}
```

Đây là **phần 2** của flag — tên file `flag2of2` đã hint trước rồi.

### Bước 3 — Extract và đọc phần PNG

`eog` không mở được vì extension `.pdf` gây nhầm lẫn. Extract phần PNG ra riêng bằng Python:

```bash
python3 -c "
data = open('/home/kali/flag2of2-final.pdf', 'rb').read()
iend = data.find(b'IEND')
png_data = data[:iend+8]  # IEND (4 bytes) + CRC (4 bytes)
open('/home/kali/flag1.png', 'wb').write(png_data)
print('Done, size:', len(png_data))
"
eog /home/kali/flag1.png
```

PNG hiện ra text:

```
picoCTF{f1u3n7_
```

Đây là **phần 1** của flag.

---

## Attack Chain

```
flag2of2-final.pdf
    ↓ file → nhận diện PNG, không phải PDF
    ↓ exiftool → "Trailer data after PNG IEND chunk"
    ↓ xxd tail → thấy %%EOF → confirm có PDF nhúng bên trong
Mở bằng evince → PDF hiện "1n_pn9_&_pdf_1f991f77}"  (phần 2)
Extract PNG bằng Python (cắt tại IEND+8) → eog → hiện "picoCTF{f1u3n7_"  (phần 1)
Ghép lại → picoCTF{f1u3n7_1n_pn9_&_pdf_1f991f77}
```

---

## Result

```
picoCTF{f1u3n7_1n_pn9_&_pdf_1f991f77}
```

---

## Kiến thức rút ra

**1. Polyglot file là gì**

Một file hợp lệ với 2 định dạng cùng lúc. Tùy tool mở, nó sẽ hiện nội dung khác nhau. Trong thực tế, kỹ thuật này được dùng để bypass file type validation — upload file trông như PNG nhưng thực ra chứa PDF/JavaScript/ZIP bên trong.

**2. Warning trong exiftool là hint quan trọng**

```
Warning: [minor] Trailer data after PNG IEND chunk
```

Dòng warning này không phải lỗi vô hại — nó báo hiệu có dữ liệu bất thường sau phần kết thúc của PNG. Trong Forensics, warning = nơi cần điều tra tiếp.

**3. Cấu trúc PNG**

PNG kết thúc bằng chunk `IEND` (4 bytes) + CRC (4 bytes). Bất kỳ dữ liệu nào sau offset đó đều không thuộc PNG — có thể là file ẩn, steganography, hoặc như bài này là PDF.

**4. Tên file là hint**

`flag2of2` → "flag 2 of 2" → có 2 mảnh flag, cần tìm cả 2. Luôn đọc kỹ tên file trước khi bắt đầu điều tra.

---

## Tools Used

- **file** — nhận diện file type
- **exiftool** — phát hiện trailer data bất thường
- **xxd** — confirm cấu trúc polyglot qua hex dump
- **evince** — mở phần PDF
- **Python** — extract phần PNG bằng cách cắt tại IEND chunk
- **eog** — mở phần PNG đã extract

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
