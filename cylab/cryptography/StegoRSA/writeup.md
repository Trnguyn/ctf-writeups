# CTF Writeup — StegoRSA

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{rs4_k3y_1n_1mg_66388eb3}`

---

## Challenge Description

> A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key. Can you recover it and decrypt the message?

**Files:** `flag.enc`, `image.jpg`

---

## Reconnaissance

Tên bài **StegoRSA** = **Stego** + **RSA** — hint thẳng 2 kỹ thuật cần dùng.

Có 2 file:
- `flag.enc` — message đã encrypt bằng RSA
- `image.jpg` — bất thường trong bài Crypto, private key ẩn trong ảnh

Check metadata ảnh:

```bash
exiftool ~/image.jpg
```

Output đáng chú ý:

```
Comment: 2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a...
```

`Comment` field chứa chuỗi hex dài bất thường — không phải comment bình thường.

---

## Phân tích

### Bước 1 — Decode hex → PEM

Nhận ra pattern: `2d2d2d2d2d` = `-----` trong ASCII — đây là header của PEM key.

Decode hex bằng CyberChef (From Hex):

```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoI...
-----END PRIVATE KEY-----
```

Private key RSA hoàn chỉnh — "careless with the private key" chính là đây.

### Bước 2 — Lưu key và decrypt

```bash
cat > private_key.pem
# paste nội dung PEM vào, Ctrl+D để kết thúc

openssl pkeyutl -decrypt -inkey private_key.pem -in flag.enc -out flag.txt
cat flag.txt
# picoCTF{rs4_k3y_1n_1mg_66388eb3}
```

---

## Attack Chain

```
image.jpg
    → exiftool → Comment field chứa hex dài bất thường
    → CyberChef From Hex → RSA Private Key PEM
private_key.pem + flag.enc
    → openssl pkeyutl -decrypt
picoCTF{rs4_k3y_1n_1mg_66388eb3}
```

---

## Result

```
picoCTF{rs4_k3y_1n_1mg_66388eb3}
```

---

## Kiến thức rút ra

**1. Tên challenge = roadmap**

"StegoRSA" nói thẳng 2 bước cần làm: tìm key trong ảnh (Stego) rồi decrypt RSA. Trong CTF, tên bài luôn là hint đầu tiên cần đọc.

**2. Private key leak = toàn bộ RSA sụp đổ**

RSA an toàn dựa trên việc private key được giữ bí mật. Khi private key bị lộ — dù ẩn trong metadata ảnh — attacker decrypt được mọi message đã encrypt bằng public key tương ứng. Trong thực tế, private key leak là incident nghiêm trọng, cần revoke và reissue certificate ngay lập tức.

**3. Metadata là nơi ẩn dữ liệu phổ biến**

Các field hay bị lợi dụng để nhúng dữ liệu:

| Field | Encoding | Bài |
|-------|----------|-----|
| `Attribution URL` | Base64 | CanYouSee |
| `License` | Base64 | Information |
| `Comment` | Hex | StegoRSA |

**4. openssl pkeyutl vs rsautl**

`rsautl` đã deprecated trong OpenSSL mới — dùng `pkeyutl` thay thế cho RSA encrypt/decrypt.

---

## Tools Used

- **exiftool** — phát hiện private key ẩn trong Comment field
- **CyberChef** — decode hex thành PEM
- **openssl pkeyutl** — decrypt flag bằng private key

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
