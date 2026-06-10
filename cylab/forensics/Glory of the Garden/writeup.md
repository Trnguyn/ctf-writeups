# CTF Writeup — Glory of the Garden

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{more_than_m33ts_the_3y398ee229a}`

---

## Challenge Description

> This file contains more than it seems.

**File:** `garden.jpg`

---

## Reconnaissance

File JPEG — chạy bộ 3 quen thuộc:

```bash
file ~/garden.jpg
exiftool ~/garden.jpg
xxd ~/garden.jpg | tail -20
```

`exiftool` không có gì đáng ngờ — metadata sạch, không có Base64 ẩn trong field nào.

Nhưng `xxd tail` tiết lộ ngay:

```
00230550: ...ffd9 4865  ..............He
00230560: 7265 2069 7320 6120 666c 6167 3a20 7069  re is a flag: pi
00230570: 636f 4354 467b 6d6f 7265 5f74 6861 6e5f  coCTF{more_than_
00230580: 6d33 3374 735f 7468 655f 3379 3339 3865  m33ts_the_3y398e
00230590: 6532 3239 617d 0a                        e229a}.
```

Flag được nhét thẳng dưới dạng plaintext sau `FFD9` — JPEG End of Image marker.

---

## Phân tích

`FFD9` là magic bytes kết thúc của JPEG. Bất kỳ dữ liệu nào sau offset đó đều không thuộc ảnh — tool xem ảnh sẽ bỏ qua, nhưng hex dump sẽ thấy rõ.

Cách tìm nhanh hơn bằng `strings`:

```bash
strings ~/garden.jpg | grep picoCTF
# Here is a flag: picoCTF{more_than_m33ts_the_3y398ee229a}
```

---

## Attack Chain

```
garden.jpg
    ↓ exiftool → metadata sạch
    ↓ xxd tail → thấy plaintext sau FFD9 (JPEG EOF)
"Here is a flag: picoCTF{more_than_m33ts_the_3y398ee229a}"
```

---

## Result

```
picoCTF{more_than_m33ts_the_3y398ee229a}
```

---

## Kiến thức rút ra

**1. Dữ liệu ẩn sau EOF marker**

Mỗi file format có marker kết thúc riêng. Dữ liệu nhét sau đó sẽ bị tool xem file bỏ qua hoàn toàn, nhưng vẫn tồn tại trong file:

| Format | EOF Marker |
|--------|------------|
| JPEG | `FF D9` |
| PNG | `IEND` + CRC |
| PDF | `%%EOF` |
| ZIP | `PK\x05\x06` |

**2. strings là shortcut mạnh**

Thay vì đọc hex dump thủ công, `strings` extract toàn bộ printable text trong file binary — nhanh hơn nhiều khi flag ở dạng plaintext.

**3. Quy trình đầy đủ khi gặp ảnh trong CTF**

```
exiftool   → metadata, Base64 ẩn trong field
strings    → plaintext ẩn trong file
xxd tail   → data sau EOF marker
binwalk    → file ẩn bên trong
steghide   → steganography
```

Bài này dừng ở bước 2 — `strings` hoặc `xxd tail` là đủ.

---

## Tools Used

- **exiftool** — kiểm tra metadata
- **xxd** — phát hiện plaintext sau JPEG EOF marker
- **strings** — extract text ẩn trong binary file

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
