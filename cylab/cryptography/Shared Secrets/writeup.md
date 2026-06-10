# CTF Writeup — Shared Secrets

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{dh_s3cr3t_9982ffe6}`

---

## Challenge Description

> A message was encrypted using a shared secret... but it looks like one side of the exchange leaked something. Can you piece together the secret and get the flag?

**Files:** `message.txt`, `encryption.py`

---

## Reconnaissance

`encryption.py` cho thấy đây là **Diffie-Hellman key exchange**:

```python
# Public parameters
g = 2
p = getPrime(1048)

# Server's secret
a = randint(2, p-2)
A = pow(g, a, p)

# Client secret
b = '???'
B = pow(g, b, p)

# Shared key
shared = pow(A, b, p)

# Encrypt flag
enc = bytes([x ^ (shared % 256) for x in flag])
```

Thuật toán XOR flag với `shared % 256` làm key.

`message.txt` chứa toàn bộ thông tin cần thiết — bao gồm cả `b` lẽ ra phải được giữ bí mật:

```
g = 2
p = 2549189574813286...
A = 9854453750409656...
b = 2531748005435027...   ← client secret bị leak
enc = 4d545e527e697b46...
```

---

## Phân tích

### Diffie-Hellman hoạt động như thế nào

Trong DH bình thường:
- Server có secret `a`, public `A = g^a mod p`
- Client có secret `b`, public `B = g^b mod p`
- Shared secret = `A^b mod p` = `B^a mod p` = `g^(ab) mod p`

Bài này dùng shared secret trực tiếp làm XOR key (lấy `shared % 256` để ra 1 byte).

### Khai thác

`b` bị leak trong `message.txt` — tính lại shared secret và XOR ngược:

```python
A = 98544537504096566...
p = 25491895748132868...
b = 25317480054350273...
enc = bytes.fromhex("4d545e527e697b465955624e0e5e4f0e49620404050f5b5b580b40")

shared = pow(A, b, p)
key = shared % 256
flag = bytes([x ^ key for x in enc])
print(flag)
```

Output:

```
picoCTF{dh_s3cr3t_9982ffe6}
```

---

## Attack Chain

```
encryption.py → hiểu thuật toán DH + XOR với shared % 256
message.txt → b bị leak
    ↓ shared = pow(A, b, p)
    ↓ key = shared % 256
    ↓ flag = enc XOR key
picoCTF{dh_s3cr3t_9982ffe6}
```

---

## Result

```
picoCTF{dh_s3cr3t_9982ffe6}
```

---

## Kiến thức rút ra

**1. Diffie-Hellman cơ bản**

DH cho phép 2 bên tạo ra shared secret mà không cần trao đổi secret trực tiếp:

```
shared = A^b mod p = B^a mod p = g^(ab) mod p
```

An toàn vì bài toán discrete logarithm — biết `A = g^a mod p` nhưng không tính ngược ra `a` được (với p đủ lớn).

**2. Điểm yếu của bài này**

Hai lỗi nghiêm trọng:
- `b` bị leak trong file challenge → shared secret tính được ngay
- Key chỉ là `shared % 256` = 1 byte → không gian key chỉ có 256 giá trị, brute force được dù không có `b`

**3. XOR cipher yếu khi key ngắn**

1-byte XOR key là cipher yếu nhất — chỉ có 256 khả năng. Trong thực tế, shared secret từ DH phải được đưa qua KDF (Key Derivation Function) như HKDF trước khi dùng làm key.

---

## Tools Used

- **Python** — tính shared secret và XOR decrypt

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
