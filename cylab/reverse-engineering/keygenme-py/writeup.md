# CTF Writeup — keygenme-py
**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Reverse Engineering  
**Difficulty:** Medium  
**Flag:** `picoCTF{1n_7h3_kk3y_of_08c46aa4}`

---

## Challenge Description

> *(No description provided)*

**File:** `keygenme-trial.py`

---

## Reconnaissance

Đây là một Python script giả lập phần mềm có license key. Chạy thử:

```bash
python3 keygenme-trial.py
```

Menu hiện ra với 4 option — option `(c) Enter License Key` là mục tiêu. Nhiệm vụ là tìm license key hợp lệ để unlock full version.

---

## Phân tích

### Cấu trúc chương trình

```
ui_flow()
    └── menu_trial()
            └── enter_license()
                    └── check_key(user_key, bUsername_trial)
                            └── decrypt_full_version(user_key)
```

### Các biến quan trọng

```python
bUsername_trial = b"BENNETT"
key_part_static1_trial = "picoCTF{1n_7h3_kk3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"   # 8 ký tự cần tìm
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
```

Key hợp lệ có format: `picoCTF{1n_7h3_kk3y_of_XXXXXXXX}`

### Reverse check_key()

Hàm `check_key()` validate key theo 2 bước:

**Bước 1 — Static part:** So sánh từng ký tự với `key_part_static1_trial`

**Bước 2 — Dynamic part:** 8 ký tự tiếp theo lấy từ SHA256 của `bUsername_trial` theo index:

```python
key[i] == sha256(bUsername_trial).hexdigest()[4]
key[i] == sha256(bUsername_trial).hexdigest()[5]
key[i] == sha256(bUsername_trial).hexdigest()[3]
key[i] == sha256(bUsername_trial).hexdigest()[6]
key[i] == sha256(bUsername_trial).hexdigest()[2]
key[i] == sha256(bUsername_trial).hexdigest()[7]
key[i] == sha256(bUsername_trial).hexdigest()[1]
key[i] == sha256(bUsername_trial).hexdigest()[8]
```

Index sequence: **4, 5, 3, 6, 2, 7, 1, 8** (không phải sequential)

---

## Exploit

Tính SHA256 của b"BENNETT":

```
h = "06370bd6e42f644c163923e35a5cc7a580c1ac1b7b155f97d797b944f29e81d0"
     0 1 2 3 4 5 6 7 8 ...

h[4]='0'  h[5]='8'  h[3]='c'  h[6]='4'
h[2]='6'  h[7]='a'  h[1]='6'  h[8]='a'
```

Dynamic part = `08c46aa4`

Script generate key:

```python
import hashlib

bUsername_trial = b"BENNETT"
key_part_static1_trial = "picoCTF{1n_7h3_kk3y_of_"

h = hashlib.sha256(bUsername_trial).hexdigest()
key_part_dynamic = h[4] + h[5] + h[3] + h[6] + h[2] + h[7] + h[1] + h[8]

key = key_part_static1_trial + key_part_dynamic + "}"
print(key)
# Output: picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

---

## Attack Chain

```
keygenme-trial.py
    ↓ đọc source → xác định format key
picoCTF{1n_7h3_kk3y_of_XXXXXXXX}
    ↓ reverse check_key() → SHA256(b"BENNETT") index [4,5,3,6,2,7,1,8]
h = "06370bd6e42f644c163923e35a5cc7a580c1ac1b7b155f97d797b944f29e81d0"
    ↓ ghép dynamic part
picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

---

## Result

```
picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

---

## Kiến thức rút ra

**1. Keygen challenge = reverse validation logic**  
Không cần crack hay brute force — chỉ cần đọc ngược hàm `check_key()` để biết key được tạo ra như thế nào.

**2. SHA256 output là hex string — dùng trực tiếp**  
`hashlib.sha256().hexdigest()` trả về string hex có thể index trực tiếp. Không cần convert thêm bước nào.

**3. Index sequence không phải ngẫu nhiên**  
`[4,5,3,6,2,7,1,8]` là obfuscation đơn giản — đọc kỹ từng if statement trong check_key() là giải mã được ngay.

**4. Encrypted blob không cần động vào**  
Full version được encrypt bằng Fernet với key là license key. Chỉ cần generate key đúng là chương trình tự decrypt.

---

## Tools Used

- **Python 3** — đọc source, generate key
- **hashlib** — tính SHA256

---

## Author

|              |                                        |
| ------------ | -------------------------------------- |
| **Author**   | Nguyễn Trung Nguyên                    |
| **Team**     | grep\_and\_pray                        |
| **CTFtime**  | [grep\_and\_pray](https://ctftime.org) |
| **Date**     | 2026-06-15                             |
| **Platform** | CyLab Security Academy                 |

---

*Writeup by **grep_and_pray** (Nguyễn Trung Nguyên)*  
*AI-assisted documentation: Claude (Anthropic) — dùng để hỗ trợ viết writeup và giải thích kiến thức. Challenge được tự giải.*
