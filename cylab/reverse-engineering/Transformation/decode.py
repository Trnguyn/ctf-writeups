with open("enc", "r", encoding="utf-8") as f:
    enc = f.read()

flag = "".join(
    chr(ord(c) >> 8) + chr(ord(c) & 0xff)
    for c in enc
)

print(flag)
