# CTF Writeup — Ph4nt0m 1ntrud3r

**Platform:** CyLab Security Academy  
**Category:** Forensics / Network Analysis  
**Difficulty:** Easy  
**Flag:** `picoCTF{1t_w4snt_th4t_34sy_tbh_4r_36f4a666}`

---

## Challenge Description

> A digital ghost has breached my defenses, and my sensitive data has been stolen! 😱💻 Your mission is to uncover how this phantom intruder infiltrated my system and retrieve the hidden flag.
> To solve this challenge, you'll need to analyze the provided PCAP file and track down the attack method. The attacker has cleverly concealed his moves in well timely manner. Dive into the network traffic, apply the right filters and show off your forensic prowess and unmask the digital intruder!

**File:** `myNetworkTraffic.pcap`

**Hints:**
1. Filter your packets to narrow down your search.
2. Attacks were done in timely manner.
3. Time is essential.

---

## Reconnaissance

```bash
capinfos myNetworkTraffic.pcap
```

Output:
```
File type:     Wireshark/tcpdump/... - pcap
Encapsulation: Raw IPv4
Packets:       22
Duration:      0.006872 seconds
```

Chỉ 22 packets trong 0.007 giây — rất nhỏ, dễ phân tích.

Mở Wireshark thấy:
- Source: `192.168.0.2` → Destination: `192.168.1.2` port 80
- Toàn TCP SYN + TCP Retransmission
- **Packets không theo thứ tự thời gian** (Strict time order: False)

---

## Phân tích

### Bước 1 — Xem TCP payload

Mở từng packet trong Wireshark, phát hiện mỗi packet chứa **TCP payload** dạng Base64:

```
Packet 1: bnRfdGg0dA==
Packet 2: Ws69hc8=
...
```

### Bước 2 — Extract payload thô

```bash
tshark -r myNetworkTraffic.pcap -T fields -e tcp.payload 2>/dev/null
```

Output là 22 hex strings — mỗi packet chứa một phần data.

### Bước 3 — Phát hiện vấn đề thứ tự

Decode thẳng payload theo thứ tự packet → kết quả garbage, không ra flag hoàn chỉnh.

**Key insight từ hints:** *"Time is essential"* + *"Attacks were done in timely manner"* → packets được gửi **không theo thứ tự thời gian** để confuse analyst. Cần **sort theo timestamp** trước!

Kiểm tra timestamps:
```bash
tshark -r myNetworkTraffic.pcap -T fields -e frame.time_epoch 2>/dev/null
```

Confirm: `Strict time order: False` — packets trong PCAP không theo thứ tự chronological.

### Bước 4 — Sort theo timestamp rồi decode

```bash
tshark -r myNetworkTraffic.pcap -T fields -e frame.time_epoch -e tcp.payload 2>/dev/null \
    | sort -n \
    | awk '{print $2}' \
    | tr -d '\n' \
    | xxd -r -p \
    | base64 -d 2>/dev/null
```

Giải thích pipeline:
- `tshark ... -e frame.time_epoch -e tcp.payload` → lấy timestamp + payload
- `sort -n` → **sắp xếp theo timestamp tăng dần**
- `awk '{print $2}'` → chỉ lấy cột payload
- `tr -d '\n'` → ghép tất cả lại một dòng
- `xxd -r -p` → convert hex → binary
- `base64 -d` → decode Base64

Output:
```
...picoCTF{1t_w4snt_th4t_34sy_tbh_4r_36f4a666}
```

---

## Attack Chain

```
myNetworkTraffic.pcap (22 TCP SYN packets, out of order)
    ↓ sort by timestamp
Packets theo thứ tự đúng
    ↓ extract TCP payload (hex)
Hex strings ghép lại
    ↓ xxd -r -p
Binary data
    ↓ base64 -d
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_36f4a666}
```

**Kỹ thuật attacker dùng:**
- Giấu data trong TCP payload của SYN packets
- Gửi packets **không theo thứ tự thời gian** để confuse analyst
- Encode data bằng Base64

---

## Result

```
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_36f4a666}
```

---

## Kiến thức rút ra

**1. Packet ordering trong PCAP**

PCAP file không đảm bảo packets theo thứ tự thời gian. Luôn kiểm tra:
```bash
capinfos file.pcap | grep "Strict time order"
```

Nếu `False` → sort trước khi phân tích:
```bash
tshark -r file.pcap -T fields -e frame.time_epoch -e [field] | sort -n
```

**2. Data exfiltration qua TCP payload**

Attacker có thể giấu data trong:
- TCP payload của SYN packets (bình thường SYN không có payload)
- TCP sequence numbers
- IP TTL
- ICMP data field
- DNS queries

**3. Quy trình phân tích PCAP cơ bản**

```bash
# 1. Tổng quan
capinfos file.pcap

# 2. Xem packets
tshark -r file.pcap

# 3. Lọc theo protocol
tshark -r file.pcap -Y "tcp"

# 4. Extract field cụ thể
tshark -r file.pcap -T fields -e tcp.payload

# 5. Sort theo thời gian nếu cần
tshark -r file.pcap -T fields -e frame.time_epoch -e tcp.payload | sort -n
```

**4. One-liner decode TCP payload**

```bash
tshark -r file.pcap -T fields -e frame.time_epoch -e tcp.payload 2>/dev/null \
    | sort -n \
    | awk '{print $2}' \
    | tr -d '\n' \
    | xxd -r -p \
    | base64 -d
```

---

## Tools Used

- **Wireshark** — visual packet analysis
- **tshark** — command line packet analysis
- **capinfos** — PCAP file info
- **xxd** — hex to binary conversion
- **base64** — decode Base64

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
