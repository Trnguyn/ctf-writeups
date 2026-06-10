# CTF Writeup — The Numbers

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{thenumbersmason}`

---

## Challenge Description

> The numbers... what do they mean?

**File:** `the_numbers.png`

---

## Reconnaissance

File PNG chứa dãy số:

```
16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
```

Dấu `{` và `}` giữ nguyên — đây rõ ràng là flag format với phần số bị encode.

---

## Phân tích

Tên bài "Mod 26" ở bài trước và dãy số từ 1–26 gợi ý **A1Z26** — mỗi số tương ứng với một chữ cái trong bảng chữ cái (A=1, B=2, ..., Z=26).

Decode bằng CyberChef với recipe **A1Z26 Cipher Decode**, separator = Space:

```
16 → P
9  → I
3  → C
15 → O
3  → C
20 → T
6  → F
{
20 → T
8  → H
5  → E
14 → N
21 → U
13 → M
2  → B
5  → E
18 → R
19 → S
13 → M
1  → A
19 → S
15 → O
14 → N
}
```

---

## Attack Chain

```
the_numbers.png
    ↓ đọc dãy số: 16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
    ↓ CyberChef A1Z26 Cipher Decode
picoCTF{thenumbersmason}
```

---

## Result

```
picoCTF{thenumbersmason}
```

---

## Kiến thức rút ra

**A1Z26 là encoding cơ bản nhất**

Mỗi chữ cái ánh xạ thẳng sang số thứ tự trong bảng chữ cái. Nhận diện nhanh khi thấy dãy số nguyên từ 1–26 xen kẽ với ký tự đặc biệt như `{` `}`.

---

## Tools Used

- **CyberChef** — A1Z26 Cipher Decode

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
