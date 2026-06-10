# CTF Writeup — EVEN RSA CAN BE BROKEN???

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{tw0_1$_pr!m375129bb1}`

---

## Challenge Description

> This service provides you an encrypted flag. Can you decrypt it with just N & e?

**File:** `encrypt.py`  
**Instance:** `nc verbal-sleep.picoctf.net 51392`

---

## Reconnaissance

Kết nối instance:

```
N: 25048635201464706517970478340750066550977839009513152029298151828252990611341397053184321451237219789675237242683950607480918929605101174296346670772361018
e: 65537
cyphertext: 6559835775103731005679401094839508389547944065895589625750914422997780720981809510421314847084347252468024460312991756065740167212851429257143992948501907
```

RSA chuẩn với `e = 65537` và N 1024-bit — nhìn bề ngoài không có gì đặc biệt.

---

## Phân tích

### Quan sát quan trọng

```python
N % 2 == 0  # True
```

N là số **chẵn**.

Trong RSA, `N = p * q` với p, q là hai số nguyên tố. Số nguyên tố chẵn duy nhất là `2` — vậy nếu N chẵn, bắt buộc một trong hai thừa số phải là `2`.

Suy ra ngay:

```python
q = 2
p = N // 2
```

Không cần bất kỳ thuật toán factoring nào (Pollard rho, Fermat, ECM...) — chỉ 1 phép chia nguyên.

### Decrypt RSA chuẩn

Có p và q rồi, phần còn lại là RSA decrypt tiêu chuẩn:

```python
from Crypto.Util.number import inverse, long_to_bytes

N = 25048635201464706517970478340750066550977839009513152029298151828252990611341397053184321451237219789675237242683950607480918929605101174296346670772361018
e = 65537
c = 6559835775103731005679401094839508389547944065895589625750914422997780720981809510421314847084347252468024460312991756065740167212851429257143992948501907

q = 2
p = N // 2

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, N)
print(long_to_bytes(m).decode())
```

Output:

```
picoCTF{tw0_1$_pr!m375129bb1}
```

---

## Attack Chain

```
N % 2 == 0 → N chẵn → một thừa số phải là 2
    ↓ q = 2, p = N // 2
    ↓ phi = (p-1)(q-1), d = e⁻¹ mod phi
    ↓ m = c^d mod N
picoCTF{tw0_1$_pr!m375129bb1}
```

---

## Result

```
picoCTF{tw0_1$_pr!m375129bb1}
```

---

## Kiến thức rút ra

**1. RSA an toàn dựa trên giả định cơ bản**

RSA giả định p và q là hai số nguyên tố lẻ **lớn**. Nếu vi phạm giả định đó — dù chỉ một số — toàn bộ hệ thống sụp đổ ngay lập tức. Bài này vi phạm giả định theo cách đơn giản nhất có thể: `q = 2`.

**2. Flag là hint**

`tw0_1$_pr!m3` = "two is prime" — tác giả nhúng thẳng hint vào flag. Nhận ra điều này sau khi giải xác nhận đúng hướng tư duy.

**3. Trước khi dùng tool phức tạp, kiểm tra điều kiện cơ bản**

Thứ tự kiểm tra khi gặp bài RSA:

```
N % 2 == 0?     → q = 2, factor ngay
N nhỏ (<512)?   → factordb.com tra luôn
e nhỏ (e=3)?    → small exponent attack
p, q gần nhau?  → Fermat factorization
Không có gì?    → Pollard rho, yafu, msieve
```

Luôn bắt đầu từ kiểm tra đơn giản nhất trước khi leo thang lên tool phức tạp.

---

## Tools Used

- **nc** — kết nối instance
- **Python + pycryptodome** — tính phi, d và decrypt

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
