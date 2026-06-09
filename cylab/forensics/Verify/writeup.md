# CTF Writeup — Verify

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{trust_but_verify_451fd69b}`

---

## Challenge Description

> People keep trying to trick my players with imitation flags. I want to make sure they get the real thing! I'm going to provide the SHA-256 hash and a decrypt script to help you know that my flags are legitimate.

**Access:** SSH instance  
```
ssh -p 64536 ctf-player@rhea.picoctf.net
```

**Checksum:** `b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2`

---

## Reconnaissance

Connect vào SSH instance:

```bash
ssh -p 64536 ctf-player@rhea.picoctf.net
# Accept fingerprint: yes
```

List files:

```bash
ls
# checksum.txt  decrypt.sh  files
```

Xem checksum:

```bash
cat checksum.txt
# b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2
```

Thư mục `files/` chứa hàng trăm file với tên random — chỉ có 1 file có SHA-256 khớp với checksum.

---

## Phân tích

### Bước 1 — Tìm file có hash khớp

```bash
sha256sum files/* | grep b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2
```

Output:
```
b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2  files/451fd69b
```

File `451fd69b` có hash khớp.

### Bước 2 — Decrypt file

```bash
./decrypt.sh files/451fd69b
```

Output:
```
picoCTF{trust_but_verify_451fd69b}
```

---

## Attack Chain

```
SSH instance
    ↓ ls → checksum.txt + decrypt.sh + files/
sha256sum files/* | grep <checksum>
    ↓ tìm được files/451fd69b
./decrypt.sh files/451fd69b
    ↓
picoCTF{trust_but_verify_451fd69b}
```

---

## Result

```
picoCTF{trust_but_verify_451fd69b}
```

---

## Kiến thức rút ra

**1. SHA-256 Hash Verification**

SHA-256 là hash function một chiều — cùng input luôn cho cùng output, không thể reverse. Dùng để verify tính toàn vẹn của file:

```bash
# Tính SHA-256 của file
sha256sum file.txt

# Verify file khớp với hash đã biết
echo "expected_hash  file.txt" | sha256sum -c
```

**2. Ứng dụng thực tế trong SOC/DFIR**

Hash verification dùng hàng ngày:
- Verify malware sample chưa bị modify
- Check log file không bị tamper
- Verify downloaded file toàn vẹn
- Chain of custody trong điều tra pháp lý số

**3. Tìm file theo hash trong nhiều file**

```bash
# Tìm file có hash cụ thể
sha256sum files/* | grep <hash>

# Hoặc dùng md5sum nếu cần MD5
md5sum files/* | grep <hash>
```

**4. Các hash algorithm phổ biến**

| Algorithm | Output length | Dùng khi |
|-----------|--------------|----------|
| MD5 | 128-bit (32 hex) | Legacy, không dùng cho security |
| SHA-1 | 160-bit (40 hex) | Deprecated |
| SHA-256 | 256-bit (64 hex) | Standard hiện tại |
| SHA-512 | 512-bit (128 hex) | High security |

---

## Tools Used

- **ssh** — connect vào remote instance
- **sha256sum** — tính và verify SHA-256 hash
- **decrypt.sh** — script decrypt được cung cấp sẵn

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
