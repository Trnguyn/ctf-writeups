# CTF Writeup — Information

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{the_m3tadata_1s_modified}`

---

## Challenge Description

> Files can always be changed in a secret way. Can you find the flag?

**File:** `cat.jpg`

---

## Reconnaissance

File JPEG — `exiftool` ngay:

```bash
exiftool ~/cat.jpg
```

Output đáng chú ý:

```
Copyright Notice    : PicoCTF
License             : cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
Rights              : PicoCTF
```

Trường `License` chứa chuỗi Base64 thay vì license text hợp lệ.

---

## Phân tích

Decode trực tiếp trên terminal:

```bash
echo "cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9" | base64 -d
```

Output:

```
picoCTF{the_m3tadata_1s_modified}
```

---

## Attack Chain

```
cat.jpg
    ↓ exiftool → License field chứa chuỗi Base64
cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
    ↓ base64 -d
picoCTF{the_m3tadata_1s_modified}
```

---

## Result

```
picoCTF{the_m3tadata_1s_modified}
```

---

## Kiến thức rút ra

**1. Metadata field hay bị lợi dụng để ẩn dữ liệu**

Hai bài liên tiếp (CanYouSee và Information) đều dùng cùng kỹ thuật — Base64 nhúng trong metadata field ít ai để ý. Các field thường bị lợi dụng:

| Field | Bài |
|-------|-----|
| `Attribution URL` | CanYouSee |
| `License` | Information |
| `Comment` | nhiều bài khác |
| `Author` | Riddle Registry |

**2. exiftool là tool đầu tiên cần chạy với mọi file ảnh**

Không cần biết file có bị tamper hay không — cứ `exiftool` trước, đọc toàn bộ output, tìm field nào chứa chuỗi bất thường.

---

## Tools Used

- **exiftool** — đọc metadata, phát hiện License field bất thường
- **base64 -d** — decode flag

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
