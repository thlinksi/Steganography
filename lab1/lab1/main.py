import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_img(img_path, text, out_path):
    text += "END"
    bin_msg = ''.join(format(ord(c), '08b') for c in text)
    img = Image.open(img_path)
    pixels = list(img.getdata())
    if len(bin_msg) > len(pixels) * 3:
        raise ValueError("Повідомлення занадто велике для цієї картинки.")
    b_idx = 0
    for i in range(len(pixels)):
        pix = list(pixels[i])
        for j in range(3):
            if b_idx < len(bin_msg):
                pix[j] = (pix[j] & ~1) | int(bin_msg[b_idx])
                b_idx += 1
        pixels[i] = tuple(pix)
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    new_img.save(out_path)

def decode_img(img_path):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    bin_msg = ""

    for pix in pixels:
        for val in pix[:3]:
            bin_msg += str(val & 1)

    res_text = ""
    for i in range(0, len(bin_msg), 8):
        byte = bin_msg[i:i + 8]
        char = chr(int(byte, 2))
        res_text += char
        if res_text[-3:] == "END":
            return res_text[:-3]

    raise ValueError("Приховане повідомлення не знайдено.")

def action_hide():
    path_in = filedialog.askopenfilename(filetypes=[("Images", "*.png *.bmp")])
    if not path_in:
        return
    msg = entry_msg.get()
    if not msg:
        messagebox.showerror("Помилка", "Введіть повідомлення")
        return
    path_out = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if not path_out:
        return
    try:
        encode_img(path_in, msg, path_out)
        messagebox.showinfo("Успіх", "Приховано успішно")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def action_extract():
    path_in = filedialog.askopenfilename(filetypes=[("Images", "*.png *.bmp")])
    if not path_in:
        return
    try:
        res = decode_img(path_in)
        messagebox.showinfo("Результат", f"Повідомлення: {res}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

root = tk.Tk()
root.title("LSB Steganography")
root.geometry("300x150")
label_msg = tk.Label(root, text="Повідомлення:")
label_msg.pack(pady=5)
entry_msg = tk.Entry(root, width=30)
entry_msg.pack(pady=5)
btn_hide = tk.Button(root, text="Приховати", command=action_hide)
btn_hide.pack(pady=10)
btn_extract = tk.Button(root, text="Вилучити", command=action_extract)
btn_extract.pack(pady=5)
root.mainloop()