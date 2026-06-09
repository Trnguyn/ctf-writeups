# CTF Writeup — DISKO 1

**Platform:** CyLab Security Academy  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{1t5_ju5t_4_5tr1n9_e3408eef}`

---

## Challenge Description

> Can you find the flag in this disk image?

**File:** `disko-1.dd.gz` (compressed disk image)

---

## Reconnaissance

File được nén bằng gzip — giải nén trước:

```bash
gunzip disko-1.dd.gz
file disko-1.dd
```

Output:
```
disko-1.dd: DOS/MBR boot sector, ... FAT32
```

Confirm đây là FAT32 disk image. Kiểm tra magic bytes:

```bash
xxd disko-1.dd | head -3
```

```
00000000: eb58 906d 6b66 732e 6661 7400 ...  .X.mkfs.fat...
```

`mkfs.fat` ở header confirm FAT32 filesystem.

---

## Phân tích

### Bước 1 — Mount disk image

```bash
sudo mkdir -p /mnt/disko
sudo mount -o loop disko-1.dd /mnt/disko
ls /mnt/disko
```

Chỉ có thư mục `/bin` chứa toàn system binaries — không có gì lạ.

### Bước 2 — Tìm deleted files với PhotoRec

```bash
sudo photorec disko-1.dd
```

PhotoRec recover được **254 files** vào `recup_dir.1` — chủ yếu là ELF binaries, shell scripts, Perl scripts. Không tìm thấy flag trong các file này.

### Bước 3 — Grep thẳng trên raw disk image

Thay vì phân tích từng file, tìm thẳng string trong raw image:

```bash
grep -a "picoCTF\|flag{" disko-1.dd
```

Output:
```
picoCTF{1t5_ju5t_4_5tr1n9_e3408eef}KALI-W~1 ...
```

Flag nằm thẳng trong raw disk data!

---

## Attack Chain

```
disko-1.dd.gz
    ↓ gunzip
disko-1.dd (FAT32 disk image)
    ↓ grep -a "picoCTF" disko-1.dd
picoCTF{1t5_ju5t_4_5tr1n9_e3408eef}
```

---

## Result

```
picoCTF{1t5_ju5t_4_5tr1n9_e3408eef}
```

---

## Kiến thức rút ra

**1. Luôn thử grep/strings trước**

Trước khi dùng tool phức tạp, thử tìm thẳng string trong raw file:

```bash
# Tìm flag format
grep -a "picoCTF{" file.dd
strings file.dd | grep -i "flag\|ctf"
```

`-a` flag trong grep = treat binary file as text — quan trọng khi grep binary/disk image.

**2. FAT32 Disk Image — quy trình phân tích**

```bash
# 1. Identify
file disk.dd

# 2. Mount
sudo mount -o loop disk.dd /mnt/point
ls /mnt/point

# 3. Tìm deleted files
sudo photorec disk.dd
sudo foremost -i disk.dd -o output/

# 4. Grep raw
grep -a "flag" disk.dd
strings disk.dd | grep "flag"
```

**3. PhotoRec vs foremost**

| Tool | Ưu điểm | Nhược điểm |
|------|---------|------------|
| PhotoRec | UI dễ dùng, nhiều format | Chậm hơn |
| foremost | Nhanh, command line | Ít format hơn |
| grep -a | Nhanh nhất | Chỉ tìm được plaintext |

**4. Lesson learned**

> "Đừng over-engineer. Thử cách đơn giản nhất trước."

Flag nằm thẳng trong disk dưới dạng plaintext — `grep -a` một lệnh là xong, không cần mount hay recover files.

---

## Tools Used

- **gunzip** — giải nén file .gz
- **file** — identify disk image type
- **mount** — mount FAT32 disk image
- **photorec** — recover deleted files
- **grep -a** — tìm string trong binary file

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
