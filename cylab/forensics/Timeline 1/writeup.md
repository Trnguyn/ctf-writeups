# CTF Writeup — Timeline 1
**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Medium  
**Flag:** `picoCTF{573417h13r_7h4n_7h3_1457_58527bb222}`

---

## Challenge Description

> Can you find the flag in this disk image? Wrap what you find in the picoCTF flag format.

**File:** `partition4.img`

---

## Reconnaissance

File là disk image — không thể đọc trực tiếp, cần dùng Sleuthkit để phân tích filesystem.

```bash
file partition4.img
```

---

## Phân tích

### Bước 1 — Tạo MAC Timeline

```bash
fls -r -m / partition4.img > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv
```

`fls` list toàn bộ file trong disk image kèm metadata. `mactime` convert sang timeline có thể đọc được theo thứ tự thời gian.

### Bước 2 — Filter file mới tạo bằng macb

```bash
grep "macb" timeline.csv > macb_files.txt
```

**macb** = Modified + Accessed + Changed + Born cùng timestamp → file vừa được tạo mới hoàn toàn. Đây là cách nhanh nhất để tìm file nào xuất hiện trên hệ thống.

### Bước 3 — Tìm Anti-forensic Action

Đọc `/root/.ash_history`:

```bash
icat partition4.img 4943
# Output: poweroff
```

Chỉ có 1 lệnh `poweroff` — đây là **anti-forensic action**: ai đó cố tắt máy đột ngột để xóa dấu vết. Theo hint 3: *"Pay close attention to timestamps near an anti-forensic action"*.

### Bước 4 — Phân tích Timeline xung quanh poweroff

```
16:41:31  system boot files          ← bình thường
16:42:02  package install (apk)      ← bình thường
16:42:05  package install done       ← bình thường
          ↓ im lặng 8 phút
16:50:07  /etc/chat                  ← BẤT THƯỜNG
16:50:23  /root/.ash_history         ← poweroff
```

`/etc/chat` nổi bật vì:
- **Timing**: xuất hiện 8 phút sau khi mọi system activity dừng lại
- **Không thuộc package nào**: Alpine Linux không tự tạo file này
- **16 giây trước poweroff**: gần nhất với anti-forensic action

### Bước 5 — Extract nội dung file

```bash
icat partition4.img 32716
# Output: NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK
```

Nhận ra đây là **Base64** (ký tự A-Z, a-z, 0-9, kết thúc bằng K).

```bash
echo "NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK" | base64 -d
# Output: 573417h13r_7h4n_7h3_1457_58527bb222
```

---

## Attack Chain

```
partition4.img
    ↓ fls + mactime → tạo MAC timeline
timeline.csv
    ↓ grep "macb" → filter file mới tạo
    ↓ tìm anti-forensic action → poweroff trong .ash_history
    ↓ tìm outlier gần poweroff → /etc/chat (16:50:07, 16s trước poweroff)
icat 32716 → NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK
    ↓ base64 -d
picoCTF{573417h13r_7h4n_7h3_1457_58527bb222}
```

---

## Result

```
picoCTF{573417h13r_7h4n_7h3_1457_58527bb222}
```

---

## Kiến thức rút ra

**1. macb = file mới tạo hoàn toàn**  
Khi cả 4 timestamp (Modified, Accessed, Changed, Born) giống nhau = file vừa xuất hiện. Grep `macb` để filter nhanh thay vì đọc toàn bộ timeline.

**2. Anti-forensic action = điểm neo điều tra**  
`poweroff` trong shell history là dấu hiệu ai đó cố xóa dấu vết. Tìm file được tạo ngay trước thời điểm đó — đó thường là file chứa bằng chứng.

**3. Outlier detection trong timeline**  
Phần lớn file là system/package noise. File đáng ngờ = không giải thích được bởi system activity + timing bất thường + location lạ.

**4. icat — đọc file từ disk image bằng inode**  
```bash
icat disk.img <inode_number>
```
Không cần mount disk — lấy inode từ fls/timeline rồi dump nội dung trực tiếp.

---

## Tools Used

- **fls** — list file trong disk image kèm inode và metadata
- **mactime** — convert bodyfile thành MAC timeline có thể đọc
- **icat** — extract nội dung file từ disk image bằng inode number
- **base64** — decode flag

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
