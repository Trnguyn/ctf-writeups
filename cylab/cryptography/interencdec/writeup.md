# CTF Writeup — interencdec

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{caesar_d3cr9pt3d_ea60e00b}`

---

## Challenge Description

> Can you get the real meaning from this file.

**File:** `enc_flag`

---

## Reconnaissance

Mở file ra — nội dung là chuỗi Base64:

```
YidkM0JxZGtwQlRYdHFhR3g2YUhsZmF6TnFlVGwzWVROclgyeG9OakJzTURCcGZRPT0nCg==
```

---

## Phân tích

### Bước 1 — Base64 lớp 1

```bash
echo "YidkM0JxZGtwQlRYdHFhR3g2YUhsZmF6TnFlVGwzWVROclgyeG9OakJzTURCcGZRPT0nCg==" | base64 -d
```

Output:

```
b'd3BqdkpBTXtqaGx6aHlfazNqeTl3YTNrX2xoNjBsMDBpfQ=='
```

Vẫn còn Base64 bên trong Python bytes literal `b'...'`.

### Bước 2 — Base64 lớp 2

Extract phần bên trong và decode tiếp:

```bash
echo "d3BqdkpBTXtqaGx6aHlfazNqeTl3YTNrX2xoNjBsMDBpfQ==" | base64 -d
```

Output:

```
wpjvJAM{jhlzhy_k3jy9wa3k_lh60l00i}
```

Trông giống format picoCTF nhưng bị shift — đây là **Caesar cipher**.

### Bước 3 — Caesar cipher (ROT19)

`wpjvJAM` → `picoCTF`: tính shift = `ord('w') - ord('p') = 7`, nhưng decode ngược nên shift = `26 - 7 = 19`.

Dùng CyberChef ROT13 với amount = 19:

```
wpjvJAM{jhlzhy_k3jy9wa3k_lh60l00i}
    ↓ ROT19
picoCTF{caesar_d3cr9pt3d_ea60e00b}
```

---

## Attack Chain

```
enc_flag
    ↓ Base64 decode lớp 1 → b'<base64>'
    ↓ Base64 decode lớp 2 → wpjvJAM{...} (Caesar cipher)
    ↓ CyberChef ROT19 (dò shift bằng cách tăng amount đến khi ra picoCTF)
picoCTF{caesar_d3cr9pt3d_ea60e00b}
```

---

## Result

```
picoCTF{caesar_d3cr9pt3d_ea60e00b}
```

---

## Kiến thức rút ra

**1. Multi-layer encoding là pattern phổ biến**

Bài này có 3 lớp chồng nhau: Base64 → Base64 → Caesar. Khi decode một lớp mà output vẫn trông bất thường, tiếp tục decode lớp tiếp theo — đừng dừng lại giữa chừng.

**2. Nhận diện Caesar cipher**

Dấu hiệu nhận ra Caesar: output có cấu trúc giống flag format (`xxxCTF{...}`) nhưng các ký tự bị shift đều. Tính shift bằng cách so sánh ký tự đã biết — ở đây `w` → `p` = shift 7, decode ngược = ROT19.

**3. CyberChef là Swiss Army Knife cho Crypto CTF**

ROT13 trong CyberChef cho phép chỉnh amount tùy ý — dò shift từ 1 đến 25 cho đến khi output ra flag format là xong. Nhanh hơn viết script cho bài đơn giản.

**4. Tên bài = gợi ý**

"interencdec" = **inter**active **enc**ode/**dec**ode — hint rằng bài có nhiều lớp encoding cần xử lý lần lượt.

---

## Tools Used

- **base64 -d** — decode 2 lớp Base64
- **CyberChef ROT** — dò và decode Caesar cipher với shift 19

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
