import tkinter as tk
from tkinter import filedialog, messagebox
import wave
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import random

def m2w(m_p, w_p):
    if not os.path.exists(m_p):
        messagebox.showerror( " ", "MP3 не знайдено!")
        return
    cmd = ['ffmpeg', '-y', '-i', m_p, w_p]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        messagebox.showinfo("", "Конвертація успішна!")
    except Exception:
        messagebox.showerror( "", "Помилка конвертації. Перевір ffmpeg.")

def embd_msg(in_w, out_w, msg):
    msg += chr(0)
    b = ''.join(f'{ord(c):08b}' for c in msg)
    with wave.open(in_w, 'rb') as w:
        prms = w.getparams()
        smpls = np.frombuffer(w.readframes(prms.nframes), dtype=np.int16)
    if len(b) > len(smpls):
        messagebox.showerror( "", "Текст задовгий!")
        return
    mod_s = smpls.copy()
    for i, bit in enumerate(b):
        mod_s[i] = (mod_s[i] & ~1) | int(bit)
    with wave.open(out_w, 'wb') as w:
        w.setparams(prms)
        w.writeframes(mod_s.tobytes())
    messagebox.showinfo("", "Сховано!")

def extr_msg(stg_w):
    with wave.open(stg_w, 'rb') as w:
        smpls = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    bits = ""
    msg = ""
    for s in smpls:
        bits += str(s & 1)
        if len(bits) == 8:
            ch = chr(int(bits, 2))
            if ch == chr(0):
                break
            msg += ch
            bits = ""
    return msg

def embd_prng(in_w, out_w, msg, key):
    if not key:
        messagebox.showerror("", "Треба ввести пароль!")
        return
    msg += chr(0)
    b = ''.join(f'{ord(c):08b}' for c in msg)
    with wave.open(in_w, 'rb') as w:
        prms = w.getparams()
        smpls = np.frombuffer(w.readframes(prms.nframes), dtype=np.int16)
    if len(b) > len(smpls):
        messagebox.showerror("", "Текст задовгий!")
        return
    random.seed(key)
    a_idx = list(range(len(smpls)))
    random.shuffle(a_idx)
    idxs = a_idx[:len(b)]
    mod_s = smpls.copy()
    for i, bit in zip(idxs, b):
        mod_s[i] = (mod_s[i] & ~1) | int(bit)
    with wave.open(out_w, 'wb') as w:
        w.setparams(prms)
        w.writeframes(mod_s.tobytes())
    messagebox.showinfo("", "Сховано з паролем!")

def extr_prng(stg_w, key):
    if not key:
        messagebox.showerror("", "Треба ввести пароль!")
        return "Нема пароля"
    with wave.open(stg_w, 'rb') as w:
        smpls = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    random.seed(key)
    a_idx = list(range(len(smpls)))
    random.shuffle(a_idx)
    bits = ""
    msg = ""
    for idx in a_idx:
        bits += str(smpls[idx] & 1)
        if len(bits) == 8:
            ch = chr(int(bits, 2))
            if ch == chr(0):
                break
            msg += ch
            bits = ""
    return msg

def plt_wv(w1, w2):
    def rd_w(p):
        with wave.open(p, 'rb') as w:
            d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
            t = np.linspace(0, len(d)/w.getframerate(), num=len(d))
            return t, d
    t1, s1 = rd_w(w1)
    t2, s2 = rd_w(w2)
    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1); plt.plot(t1, s1); plt.title("Ориг")
    plt.subplot(2,1,2); plt.plot(t2, s2, linestyle='--'); plt.title("Стего")
    plt.tight_layout(); plt.show()

app = tk.Tk()
app.title("Стеганографія LSB")
app.geometry("500x600")
m_path = tk.StringVar()
orig_w = tk.StringVar()
stg_w = tk.StringVar()
def sel_f(var, is_save=False):
    if is_save:
        p = filedialog.asksaveasfilename(defaultextension=".wav")
    else:
        p = filedialog.askopenfilename()
    if p: var.set(p)
tk.Label(app, text="1. Конвертер MP3 -> WAV", font="bold").pack(pady=5)
tk.Button(app, text="Обрати MP3", command=lambda: sel_f(m_path)).pack()
tk.Label(app, textvariable=m_path, fg="gray").pack()
tk.Button(app, text="Куди зберегти WAV", command=lambda: sel_f(orig_w, True)).pack()
tk.Label(app, textvariable=orig_w, fg="gray").pack()
tk.Button(app, text="Конвертувати", command=lambda: m2w(m_path.get(), orig_w.get()), bg="lightblue").pack(pady=5)
tk.Label(app, text="2. Файли", font="bold").pack(pady=5)
tk.Button(app, text="Ориг WAV (Cover)", command=lambda: sel_f(orig_w)).pack()
tk.Label(app, textvariable=orig_w, fg="gray").pack()
tk.Button(app, text="Стего WAV (Результат)", command=lambda: sel_f(stg_w, True)).pack()
tk.Label(app, textvariable=stg_w, fg="gray").pack()
tk.Label(app, text="Повідомлення:").pack()
msg_ent = tk.Entry(app, width=50)
msg_ent.pack()
tk.Label(app, text="Пароль (для PRNG):").pack()
pwd_ent = tk.Entry(app, width=20)
pwd_ent.pack()
f_btns = tk.Frame(app)
f_btns.pack(pady=10)
tk.Button(f_btns, text="Сховати (Звичайний)", command=lambda: embd_msg(orig_w.get(), stg_w.get(), msg_ent.get())).grid(row=0, column=0, padx=5)
tk.Button(f_btns, text="Вилучити (Звичайний)", command=lambda: messagebox.showinfo("Текст", extr_msg(stg_w.get()))).grid(row=0, column=1, padx=5)
tk.Button(f_btns, text="Сховати (PRNG)", command=lambda: embd_prng(orig_w.get(), stg_w.get(), msg_ent.get(), pwd_ent.get())).grid(row=1, column=0, padx=5, pady=5)
tk.Button(f_btns, text="Вилучити (PRNG)", command=lambda: messagebox.showinfo("Текст", extr_prng(stg_w.get(), pwd_ent.get()))).grid(row=1, column=1, padx=5, pady=5)
tk.Button(app, text="Показати графіки хвиль", command=lambda: plt_wv(orig_w.get(), stg_w.get()), bg="lightgreen").pack(pady=10)
app.mainloop()