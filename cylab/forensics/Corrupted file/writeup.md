# CTF Writeup — Corrupted File

**Platform:** CyLab Security Academy  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{r3st0r1ng_th3_by73s_1512b52a}`

---

## Challenge Description

> This file seems broken... or is it? Maybe a couple of bytes could make all the difference. Can you figure out how to bring it back to life?

**File:** `file` (no extension)

---

## Reconnaissance

File không có extension, `file` command trả về `data` — không nhận diện được type. Dump hex để xem magic bytes:

```bash
xxd ~/file | head -3
```

Output:
```
00000000: 5c78 ffe0 0010 4a46 4946 0001 0100 0001  \x....JFIF......
00000010: 0001 0000 ffdb 0043 0008 0606 0706 0508  .......C........
00000020: 0707 0709 0908 0a0c 140d 0c0b 0b0c 1912  ................
```

---

## Phân tích

### Bước 1 — Nhận diện file type

Nhìn vào hex dump:
- Offset 6: `4a46 4946` = **`JFIF`** → đây là JPEG signature text
- Byte 0-1: `5c 78` → **SAI**, không phải magic bytes JPEG

File này là JPEG bị corrupt ở 2 byte đầu tiên.

### Bước 2 — So sánh magic bytes

| | Byte 0 | Byte 1 |
|---|--------|--------|
| **File hiện tại** | `5C` | `78` |
| **JPEG chuẩn** | `FF` | `D8` |

Chỉ cần fix 2 byte đầu từ `5C 78` → `FF D8`.

### Bước 3 — Patch magic bytes

```bash
printf '\xff\xd8' | dd of=~/file bs=1 seek=0 count=2 conv=notrunc
```

Giải thích lệnh:
- `printf '\xff\xd8'` → tạo 2 byte FF D8
- `dd of=~/file` → ghi vào file
- `bs=1 seek=0 count=2` → ghi từ byte 0, chỉ 2 byte
- `conv=notrunc` → không xóa phần còn lại

Verify:
```bash
file ~/file
# Output: JPEG image data, JFIF standard 1.01
```

### Bước 4 — Mở ảnh

```bash
eog ~/file
```

Ảnh hiện ra với flag in đỏ:

```
picoCTF{r3st0r1ng_th3_by73s_1512b52a}
```

---

## Attack Chain

```
file (data — không nhận diện được)
    ↓ xxd → thấy JFIF ở offset 6 → đây là JPEG
Magic bytes sai: 5C 78 → phải là FF D8
    ↓ printf '\xff\xd8' | dd ... conv=notrunc
file (JPEG image data)
    ↓ mở ảnh
picoCTF{r3st0r1ng_th3_by73s_1512b52a}
```

---

## Result

```
picoCTF{r3st0r1ng_th3_by73s_1512b52a}
```

---

## Kiến thức rút ra

**1. Magic Bytes — File Signature**

Mỗi file type có magic bytes cố định ở phần header. `file` command dùng database magic bytes để nhận diện — không dựa vào extension.

Bảng magic bytes quan trọng:

| File Type | Magic Bytes (Hex) | ASCII |
|-----------|------------------|-------|
| JPEG | `FF D8 FF E0` | `ÿØÿà` |
| PNG | `89 50 4E 47` | `‰PNG` |
| ZIP | `50 4B 03 04` | `PK..` |
| PDF | `25 50 44 46` | `%PDF` |
| GIF | `47 49 46 38` | `GIF8` |
| ELF | `7F 45 4C 46` | `.ELF` |

**2. Patch binary file với dd**

`dd` là tool mạnh để đọc/ghi binary data chính xác:

```bash
# Ghi đè N byte tại offset X
printf '\xAA\xBB' | dd of=file bs=1 seek=X count=N conv=notrunc

# conv=notrunc quan trọng — không cắt phần còn lại của file
```

**3. Quy trình debug file corrupt**

```bash
# Bước 1 — xem magic bytes thật
xxd file | head -3

# Bước 2 — so sánh với magic bytes chuẩn
# JPEG: FF D8 FF E0
# PNG: 89 50 4E 47

# Bước 3 — patch nếu sai
printf '\xff\xd8' | dd of=file bs=1 seek=0 count=2 conv=notrunc

# Bước 4 — verify
file file
```

**4. Hint quan trọng: JFIF**

Khi thấy `JFIF` trong strings/hex dump của file → đây là JPEG, dù magic bytes có bị corrupt. `JFIF` luôn xuất hiện ở offset 6 của JPEG hợp lệ.

---

## Tools Used

- **xxd** — hex dump để xem magic bytes
- **dd** — patch binary file
- **file** — verify file type
- **eog** — mở ảnh trên Kali Linux

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
