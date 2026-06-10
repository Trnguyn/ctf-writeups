# CTF Writeup — Hashcrack

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{UseStr0nG_h@shEs_&PaSswDs!_5b836723}`

---

## Challenge Description

> A company stored a secret message on a server which got breached due to the admin using weakly hashed passwords. Can you gain access to the secret stored within the server?

**Instance:** `nc verbal-sleep.picoctf.net 60175`

---

## Phân tích

Kết nối instance — server yêu cầu crack 3 hash liên tiếp:

```
Welcome!! Looking For the Secret?
We have identified a hash: 482c811da5d5b4bc6d497ffa98491e38
Enter the password for identified hash:
```

### Hash 1 — MD5

```
482c811da5d5b4bc6d497ffa98491e38
```

Tra CrackStation → `password123`

```
Correct! You've cracked the MD5 hash with no secret found!
```

### Hash 2 — SHA-1

```
b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3
```

Tra CrackStation → `letmein`

```
Correct! You've cracked the SHA-1 hash with no secret found!
```

### Hash 3 — SHA-256

```
916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745
```

Tra CrackStation → `qwerty098`

```
Correct! You've cracked the SHA-256 hash with a secret found.
The flag is: picoCTF{UseStr0nG_h@shEs_&PaSswDs!_5b836723}
```

---

## Attack Chain

```
nc → 3 hash liên tiếp (MD5 → SHA-1 → SHA-256)
    ↓ CrackStation tra từng hash
password123 / letmein / qwerty098
    ↓ submit đúng cả 3
picoCTF{UseStr0nG_h@shEs_&PaSswDs!_5b836723}
```

---

## Result

```
picoCTF{UseStr0nG_h@shEs_&PaSswDs!_5b836723}
```

---

## Kiến thức rút ra

**1. Hash không phải encryption**

Hash là one-way function — không có key, không decrypt ngược được. Nhưng nếu password yếu và có trong wordlist, attacker tra rainbow table hoặc brute force là ra.

**2. Tại sao MD5/SHA-1 không nên dùng cho password**

| Hash | Vấn đề |
|------|--------|
| MD5 | Quá nhanh (~10 tỷ hash/giây trên GPU), collision đã tìm được |
| SHA-1 | Tương tự MD5, collision đã được chứng minh (SHAttered 2017) |
| SHA-256 | Nhanh hơn bcrypt/argon2 nhiều — vẫn không lý tưởng cho password |

Password nên hash bằng **bcrypt**, **argon2**, hoặc **scrypt** — các thuật toán được thiết kế đặc biệt để chậm và tốn memory, khiến brute force không khả thi.

**3. CrackStation hoạt động như thế nào**

CrackStation duy trì rainbow table với hàng tỷ hash được precompute từ wordlist phổ biến. Bất kỳ password nào có trong rockyou.txt hoặc common password list đều bị crack ngay lập tức.

**4. Liên hệ thực tế Blue Team**

Khi điều tra breach, một trong những bước đầu tiên là kiểm tra password policy — nếu admin dùng password yếu với hash không salted, toàn bộ credential database có thể bị crack chỉ trong vài phút. Đây đúng là scenario của bài này.

---

## Tools Used

- **nc** — kết nối instance
- **CrackStation** — tra rainbow table crack MD5, SHA-1, SHA-256

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
