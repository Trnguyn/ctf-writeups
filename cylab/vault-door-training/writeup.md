# CTF Writeup — Vault Door Training

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Reverse Engineering  
**Difficulty:** Easy  
**Flag:** `picoCTF{w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp}`

---

## Challenge Description

> Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project. The laboratory is protected by a series of locked vault doors. Each door is controlled by a computer and requires a password to open. Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors, but one of our junior agents obtained the source code for each vault's computer! You will need to read the source code for each level to figure out what the password is for that vault door. As a warmup, we have created a replica vault in our training facility.

**File:** `VaultDoorTraining.java`

---

## Phân tích source code

Đề bài cho thẳng source code Java — đọc thẳng, không cần disassembler.

```java
public boolean checkPassword(String password) {
    return password.equals("w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp");
}
```

Password hardcode thẳng trong source — comment của tác giả còn tự nhận thức được vấn đề:

```java
// The password is below. Is it safe to put the password in the source code?
// What if somebody stole our source code? Then they would know what our
// password is.
// -Minion #9567
```

### Điểm tinh tế cần chú ý

Trước khi gọi `checkPassword`, chương trình xử lý input:

```java
String input = userInput.substring("".length(), userInput.length()-1);
```

`"".length()` = 0, nên dòng này tương đương:

```java
String input = userInput.substring(0, userInput.length()-1);
```

Tức là **strip bỏ ký tự cuối cùng** của input trước khi compare. Nếu nhập đúng password mà không tính đến bước này sẽ bị Access denied.

---

## Giải

Password trong source: `w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp`

Khi nhập vào chương trình, cần thêm 1 ký tự bất kỳ ở cuối để bù cho bước strip:

```
Input: w4rm1ng_Up_w1tH_jAv4_0009yrGMeEpX
Sau substring: w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp  ← khớp password
```

Flag wrap theo format picoCTF:

```
picoCTF{w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp}
```

---

## Attack Chain

```
VaultDoorTraining.java
    ↓ đọc checkPassword() → password hardcode trong source
    ↓ đọc substring() → chương trình strip ký tự cuối trước khi compare
Nhập "w4rm1ng_Up_w1tH_jAv4_0009yrGMeEpX" → Access granted
picoCTF{w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp}
```

---

## Result

```
picoCTF{w4rm1ng_Up_w1tH_jAv4_0009yrGMeEp}
```

---

## Kiến thức rút ra

**1. Hardcoded password là lỗi bảo mật nghiêm trọng**

Đây là lỗi thực tế gặp nhiều trong code production — developer hardcode credential vào source rồi push lên GitHub public. Trong Blue Team, công cụ như **truffleHog** hoặc **git-secrets** scan repo để phát hiện pattern này.

**2. Đọc kỹ toàn bộ flow, không chỉ hàm kiểm tra**

Bài này có bẫy nhỏ ở bước xử lý input trước `checkPassword`. Nếu chỉ đọc hàm `checkPassword` mà bỏ qua `substring`, sẽ nhập sai và bị Access denied. Trong RE, luôn trace toàn bộ flow từ input đến điểm so sánh.

**3. Vault Door series**

Đây là bài warmup của series — các bài tiếp theo (`vault-door-1`, `vault-door-2`...) sẽ obfuscate password theo nhiều cách phức tạp hơn thay vì hardcode thẳng.

---

## Tools Used

- **source code analysis** — đọc và hiểu `VaultDoorTraining.java`

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
