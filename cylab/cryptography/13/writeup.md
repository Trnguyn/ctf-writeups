# CTF Writeup — 13

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Cryptography  
**Difficulty:** Easy  
**Flag:** `picoCTF{not_too_bad_of_a_problem}`

---

## Challenge Description

> Cryptography can be easy, do you know what ROT13 is?

**Ciphertext:** `cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}`

---

## Phân tích

Tên bài "13" và hint "ROT13" nói thẳng cách giải. ROT13 là Caesar cipher với shift = 13.

```bash
echo "cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Output:

```
picoCTF{not_too_bad_of_a_problem}
```

---

## Attack Chain

```
cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}
    ↓ ROT13
picoCTF{not_too_bad_of_a_problem}
```

---

## Result

```
picoCTF{not_too_bad_of_a_problem}
```

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
