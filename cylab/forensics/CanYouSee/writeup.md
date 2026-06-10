# CTF Writeup — CanYouSee

**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{ME74D47A_HIDD3N_deca06fb}`

---

## Challenge Description

> How about some hide and seek?

**File:** `ukn_reality.jpg`

---

## Reconnaissance

File có extension `.jpg` — bắt đầu bằng `exiftool` như thường lệ:

```bash
exiftool ~/ukn_reality.jpg
```

Output:

```
File Name                       : ukn_reality.jpg
File Type                       : JPEG
Image Width                     : 4308
Image Height                    : 2875
XMP Toolkit                     : Image::ExifTool 11.88
Attribution URL                 : cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg==
Megapixels                      : 12.4
```

Trường `Attribution URL` chứa chuỗi bất thường — đây không phải URL hợp lệ mà là **Base64**.

---

## Phân tích

### Nhận diện encoding

Chuỗi `cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg==` có đặc điểm:
- Chỉ dùng ký tự `A-Z`, `a-z`, `0-9`
- Kết thúc bằng `==`
- Hint thêm: `cGljb0NURn` decode ra `picoCTF`

Decode bằng terminal:

```bash
echo "cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg==" | base64 -d
```

Output:

```
picoCTF{ME74D47A_HIDD3N_deca06fb}
```

---

## Attack Chain

```
ukn_reality.jpg
    ↓ exiftool → Attribution URL chứa chuỗi lạ
cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg==
    ↓ base64 -d
picoCTF{ME74D47A_HIDD3N_deca06fb}
```

---

## Result

```
picoCTF{ME74D47A_HIDD3N_deca06fb}
```

---

## Kiến thức rút ra

**1. Metadata field bất thường = nơi cần điều tra**

`Attribution URL` là field XMP metadata — bình thường chứa URL nguồn ảnh. Khi thấy field này chứa chuỗi không phải URL, đó là dấu hiệu rõ ràng có dữ liệu ẩn.

**2. Nhận diện Base64 nhanh**

- Chỉ dùng `A-Z`, `a-z`, `0-9`, `+`, `/`
- Kết thúc bằng `=` hoặc `==`
- Độ dài chia hết cho 4
- Test nhanh: `cGljb0NURn` → `picoCTF` — confirm ngay đây là flag encode Base64

**3. Tên challenge = hint**

"CanYouSee" → can you see **what's hidden** → metadata. "Hide and seek" → flag đang ẩn trong một chỗ không ai để ý — đúng với `Attribution URL`, field ít ai kiểm tra nhất.

---

## Tools Used

- **exiftool** — đọc metadata, phát hiện Attribution URL bất thường
- **base64 -d** — decode flag

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
