# CTF Writeup — Riddle Registry

**Platform:** CyLab Security Academy  
**Category:** Forensics  
**Difficulty:** Beginner  
**Flag:** `picoCTF{puzzl3d_m3tadata_f0und!_42440c7d}`

---

## Challenge Description

> Hi, intrepid investigator! 📄🔍 You've stumbled upon a peculiar PDF filled with what seems like nothing more than garbled nonsense. But beware! Not everything is as it appears. Amidst the chaos lies a hidden treasure—an elusive flag waiting to be uncovered.

**File:** `riddle_registry.pdf`

---

## Reconnaissance

Bước đầu tiên — check magic bytes của file:

```
25 50 44 46 2D 31 2E 37  →  %PDF-1.7
```

Confirm đây là PDF hợp lệ. Dump hex header để xem nội dung raw:

```
25 50 44 46 2D 31 2E 37 0A 25 E2 E3 CF D3 0A 31 20 30 20 6F 62 6A...
2F 41 75 74 68 6F 72 20 28 63 47 6C 6A 62 30 4E 55 52 6E 74 77 64 58 70...
```

Nhìn vào hex dump thấy chuỗi `/Author (cGljb0NURn...)` — đây là **PDF metadata field**.

---

## Phân tích

### Bước 1 — Nhận diện dữ liệu ẩn trong metadata

PDF có các metadata field chuẩn:
- `/Author` — tác giả
- `/Title` — tiêu đề
- `/Subject` — chủ đề
- `/Creator` — phần mềm tạo

Trong challenge này, field `/Author` chứa chuỗi bất thường:

```
cGljb0NURntwd1p6dGFkYXRhX2YwdW5kIV80MjQ0MGM3ZH0=
```

### Bước 2 — Nhận diện encoding

Chuỗi có đặc điểm:
- Chứa `A-Z`, `a-z`, `0-9`, `+`, `/`
- Kết thúc bằng `=`
- → Đây là **Base64**

Thêm hint: `cGljb0NURn` decode ra `picoCTF` — confirm đây là flag bị encode.

### Bước 3 — Decode Base64

Dùng CyberChef với operation **From Base64**:

```
Input:  cGljb0NURntwd1p6dGFkYXRhX2YwdW5kIV80MjQ0MGM3ZH0=
Recipe: From Base64
Output: picoCTF{puzzl3d_m3tadata_f0und!_42440c7d}
```

---

## Result

```
picoCTF{puzzl3d_m3tadata_f0und!_42440c7d}
```

Flag ẩn trong **Author metadata** của PDF dưới dạng Base64.

---

## Kiến thức rút ra

**1. PDF Metadata**

PDF có nhiều field metadata có thể chứa thông tin ẩn:

| Field | Mô tả |
|-------|-------|
| `/Author` | Tác giả tài liệu |
| `/Title` | Tiêu đề |
| `/Subject` | Chủ đề |
| `/Creator` | Phần mềm tạo PDF |
| `/Producer` | Phần mềm render PDF |
| `/Keywords` | Từ khóa |

**2. Cách check metadata nhanh**

Trên Linux:
```bash
exiftool file.pdf        # xem toàn bộ metadata
pdfinfo file.pdf         # thông tin cơ bản
strings file.pdf | grep -i "author\|title\|flag\|ctf"
```

Trên Windows/Online:
- CyberChef → Strings operation
- metadata2go.com
- exifdata.com

**3. Quy trình forensics PDF**

```
Nhận PDF lạ
    → file pdf          # verify magic bytes %PDF
    → exiftool pdf      # check metadata
    → strings pdf       # tìm text ẩn
    → binwalk pdf       # detect file nhúng bên trong
    → pdftotext pdf     # extract text content
```

**4. Base64 nhận diện nhanh**

- Chỉ dùng ký tự `A-Z`, `a-z`, `0-9`, `+`, `/`
- Kết thúc bằng `=` hoặc `==`
- Độ dài chia hết cho 4

---

## Tools Used

- **CyberChef** — From Base64 operation
- **Hex Dump** — đọc raw header PDF

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