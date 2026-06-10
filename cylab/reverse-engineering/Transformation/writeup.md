# CTF Writeup — Transformation

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Reverse Engineering  
**Difficulty:** Easy  
**Flag:** `picoCTF{16_bits_inst34d_of_8_b7f62ca5}`

---

## Challenge Description

```python
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
```

**Files:** `enc` (file kết quả sau khi mã hóa)

---

## Phân tích thuật toán mã hóa

Đề bài cho thẳng thuật toán encode:

```python
chr((ord(flag[i]) << 8) + ord(flag[i + 1]))
```

Phân tích từng bước:

- Lấy 2 ký tự liên tiếp trong flag: `flag[i]` và `flag[i+1]`
- `ord(flag[i]) << 8` → shift trái 8 bit (nhân 256) → đưa ký tự đầu lên byte cao
- `+ ord(flag[i+1])` → đặt ký tự thứ 2 vào byte thấp
- `chr(...)` → gộp 2 byte ASCII (8-bit) thành 1 ký tự Unicode (16-bit)

Ví dụ với `pi`:

```
ord('p') = 0x70 → 0x70 << 8 = 0x7000
ord('i') = 0x69
0x7000 + 0x69 = 0x7069 → chr(0x7069) = '灩'
```

Kết quả: 2 ký tự ASCII gộp thành 1 ký tự Unicode → file `enc` trông như text tiếng Trung/Nhật.

---

## Giải mã (Decode)

Đảo ngược thuật toán — tách 1 ký tự Unicode 16-bit thành 2 ký tự ASCII 8-bit:

```python
with open("enc", "r", encoding="utf-8") as f:
    enc = f.read()

flag = "".join(
    chr(ord(c) >> 8) + chr(ord(c) & 0xff)
    for c in enc
)

print(flag)
```

Giải thích từng bước:

- `ord(c) >> 8` → shift phải 8 bit → lấy byte cao (ký tự đầu)
- `ord(c) & 0xff` → AND với 0xFF → lấy byte thấp (ký tự thứ 2)
- `chr(...)` → chuyển lại thành ký tự ASCII

---

## Attack Chain

```
Đọc thuật toán encode: 2 ASCII chars → 1 Unicode char (16-bit)
    ↓ đảo ngược
1 Unicode char → >> 8 lấy byte cao + & 0xff lấy byte thấp
    ↓ chạy decode.py
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```

---

## Result

```
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```

---

## Kiến thức rút ra

**1. Bit manipulation cơ bản**

| Operation | Ý nghĩa |
|-----------|---------|
| `x << 8` | Shift trái 8 bit = nhân 256 = đưa lên byte cao |
| `x >> 8` | Shift phải 8 bit = chia 256 = lấy byte cao |
| `x & 0xff` | AND mask = lấy byte thấp |

**2. Encoding ≠ Encryption**

Bài này là **encoding** (biến đổi có thể đảo ngược hoàn toàn, không cần key), không phải encryption. Flag không được bảo vệ bằng key — chỉ cần hiểu thuật toán là decode được ngay.

**3. Quy trình RE khi có thuật toán encode**

```
1. Đọc và hiểu thuật toán encode
2. Xác định operation ngược lại
   - << 8  →  >> 8
   - +     →  & 0xff (lấy phần dư)
3. Implement decode script
4. Chạy với file enc → flag
```

---

## Tools Used

- **Python** — viết script decode ngược thuật toán

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
