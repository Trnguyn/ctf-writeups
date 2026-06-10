# CTF Writeup — Mod 26

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}`

---

## Challenge Description

> Cryptography can be easy, do you know what ROT13 is?

**File:** `values.txt`

---

## Reconnaissance

Nội dung `values.txt`:

```
cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}
```

Trông giống flag format bị shift — tên bài "Mod 26" và hint "ROT13" nói thẳng cách giải.

---

## Phân tích

ROT13 là Caesar cipher với shift = 13. Vì bảng chữ cái có 26 ký tự, ROT13 là phép biến đổi đối xứng — encode và decode dùng cùng một operation.

```bash
echo "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Output:

```
picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}
```

---

## Attack Chain

```
cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}
    ↓ ROT13
picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}
```

---

## Result

```
picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}
```

---

## Kiến thức rút ra

**ROT13 và Mod 26**

ROT13 là Caesar cipher mod 26 với shift = 13. Vì 13 + 13 = 26 ≡ 0 (mod 26), decode và encode là cùng một phép — áp dụng ROT13 hai lần trở về plaintext gốc. Flag tự hint luôn: `2_rounds_of_rot13` = ROT13 hai lần = không thay đổi gì 😄

---

## Tools Used

- **tr** — ROT13 trực tiếp trên terminal

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
