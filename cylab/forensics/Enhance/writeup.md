# CTF Writeup — Enhance!
**Platform:** CyLab Security Academy (PicoCTF)  
**Category:** Forensics  
**Difficulty:** Easy  
**Flag:** `picoCTF{3nh4nc3d_24374675}`

---

## Challenge Description
> Download this image file and find the flag.

**File:** `drawing.flag.svg`

---

## Reconnaissance

File có extension `.svg` — SVG là XML thuần, bước đầu tiên luôn là đọc source trực tiếp thay vì render:

```bash
strings ~/drawing.flag.svg
```

Trong output, phần lớn là metadata Inkscape bình thường. Điểm đáng chú ý là một `<text>` element với style bất thường:

```xml
style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
```

---

## Phân tích

### Nhận diện kỹ thuật ẩn

Hai kỹ thuật được dùng đồng thời để ẩn flag:

**1. Font size cực nhỏ** (`0.00352781px`)  
Nhỏ đến mức không thể nhìn thấy khi render dù zoom in tối đa.

**2. Màu chữ trắng trên nền trắng** (`fill:#ffffff`)  
Background là `#ffffff`, chữ cũng `#ffffff` → invisible hoàn toàn.

### Extracting the Flag

Flag được chia nhỏ thành nhiều `<tspan>` element, mỗi tspan chứa 1-2 ký tự. Follow theo ID sequence để ghép đúng thứ tự:

```
tspan3748 → "p"
tspan3754 → "i"
tspan3756 → "c"
tspan3758 → "o"
tspan3760 → "C"
tspan3762 → "T"
tspan3764 → "F{3nh4n"
tspan3752 → "c3d_24374675}"
```

Ghép lại → `picoCTF{3nh4nc3d_24374675}`

---

## Attack Chain

```
drawing.flag.svg
    ↓ strings → phát hiện <text> element với style bất thường
font-size:0.00352781px + fill:#ffffff
    ↓ follow tspan ID sequence → ghép từng ký tự theo thứ tự
picoCTF{3nh4nc3d_24374675}
```

---

## Result

```
picoCTF{3nh4nc3d_24374675}
```

---

## Kiến thức rút ra

**1. SVG forensics: đọc source trước khi render**  
SVG là XML — mọi thứ đều nằm trong text. `strings` hoặc text editor cho thấy những gì renderer cố tình ẩn.

**2. Hai kỹ thuật ẩn phổ biến trong SVG**  
- `font-size ≈ 0` → text tồn tại nhưng không thể nhìn thấy  
- `fill` trùng màu nền → invisible dù text size bình thường  
Khi thấy hai cái này kết hợp, đó là dấu hiệu rõ ràng có dữ liệu ẩn.

**3. Follow tspan ID sequence để ghép flag**  
Thay vì chỉ grep style, follow ID sequence đảm bảo ghép đúng thứ tự — đặc biệt hữu ích khi flag bị chia nhỏ thành nhiều fragment.

**4. Tên challenge = hint**  
"Enhance!" → zoom in để thấy thứ ẩn → flag bị ẩn bằng font-size cực nhỏ, cần "enhance" để đọc được.

---

## Tools Used

- **strings** — đọc raw content SVG, phát hiện `<text>` element ẩn
- **text editor** — follow tspan ID sequence, ghép flag

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
