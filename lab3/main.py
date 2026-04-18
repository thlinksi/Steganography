import tkinter as tk
from tkinter import filedialog, messagebox, ttk
z0 = '\u200b'
z1 = '\u200c'

def to_bin(t):
    return ''.join(format(ord(c), '08b') for c in t) + '11111111'

def fr_bin(b):
    m = ""
    for i in range(0, len(b), 8):
        if i + 8 > len(b): break
        bt = b[i:i + 8]
        if bt == '11111111': break
        m += chr(int(bt, 2))
    return m

def cs_enc(t, s):
    if not s.isdigit(): return t
    s = int(s)
    return "".join(chr((ord(c) + s) % 1114112) for c in t)

def cs_dec(t, s):
    if not s.isdigit(): return t
    s = int(s)
    return "".join(chr((ord(c) - s) % 1114112) for c in t)

def enc_zw(c_txt, msg):
    b = to_bin(msg)
    if len(b) > len(c_txt): raise ValueError("Текст-контейнер замалий")
    r = ""
    for i, ch in enumerate(c_txt):
        r += ch
        if i < len(b):
            r += z1 if b[i] == '1' else z0
    return r, b

def dec_zw(s_txt):
    b = ""
    for ch in s_txt:
        if ch == z0:
            b += '0'
        elif ch == z1:
            b += '1'
    return fr_bin(b)

def enc_cs(c_txt, msg):
    b = to_bin(msg)
    r = ""
    b_idx = 0
    for ch in c_txt:
        if ch.isalpha() and b_idx < len(b):
            r += ch.upper() if b[b_idx] == '1' else ch.lower()
            b_idx += 1
        else:
            r += ch
    if b_idx < len(b): raise ValueError("Замало літер у тексті")
    return r, b

def dec_cs(s_txt):
    b = ""
    for ch in s_txt:
        if ch.isalpha():
            b += '1' if ch.isupper() else '0'
    return fr_bin(b)

def enc_sp(c_txt, msg):
    b = to_bin(msg)
    w = c_txt.split(' ')
    if len(b) > len(w) - 1: raise ValueError("Замало пробілів у тексті")
    r = w[0]
    for i in range(1, len(w)):
        if i - 1 < len(b):
            r += ('  ' if b[i - 1] == '1' else ' ') + w[i]
        else:
            r += ' ' + w[i]
    return r, b

def dec_sp(s_txt):
    b = ""
    i = 0
    while i < len(s_txt) - 1:
        if s_txt[i] == ' ':
            if s_txt[i + 1] == ' ':
                b += '1'
                i += 1
            else:
                b += '0'
        i += 1
    return fr_bin(b)

def enc_cl(c_txt, msg):
    b = to_bin(msg)
    if len(b) > len(c_txt): raise ValueError("Текст замалий")
    r = "<html><body>"
    for i, ch in enumerate(c_txt):
        if ch == '\n':
            r += "<br>"
            continue
        if i < len(b):
            c = "#000001" if b[i] == '1' else "#000000"
            r += f'<span style="color:{c}">{ch}</span>'
        else:
            r += f'<span style="color:#000000">{ch}</span>'
    r += "</body></html>"
    return r, b

def dec_cl(s_txt):
    import re
    b = ""
    fnd = re.findall(r'<span style="color:(#[0-9a-fA-F]{6})">(.*?)</span>', s_txt)
    for clr, txt in fnd:
        if clr == "#000001":
            b += '1'
        elif clr == "#000000":
            b += '0'
    return fr_bin(b)

def a_enc():
    pth_i = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not pth_i: return
    with open(pth_i, 'r', encoding='utf-8') as f:
        c_txt = f.read()
    msg = e_msg.get()
    shft = e_shf.get()
    if shft: msg = cs_enc(msg, shft)
    m_type = cb_m.get()
    ext = ".html" if m_type == "Колір шрифту" else ".txt"
    pth_o = filedialog.asksaveasfilename(defaultextension=ext)
    if not pth_o: return
    try:
        if m_type == "Нульова ширина":
            res, b = enc_zw(c_txt, msg)
        elif m_type == "Регістр":
            res, b = enc_cs(c_txt, msg)
        elif m_type == "Пробіли":
            res, b = enc_sp(c_txt, msg)
        elif m_type == "Колір шрифту":
            res, b = enc_cl(c_txt, msg)
        with open(pth_o, 'w', encoding='utf-8') as f:
            f.write(res)
        t_log.delete(1.0, tk.END)
        t_log.insert(tk.END, f"Оригінал:\n{msg}\n\nБінарний вигляд:\n{b}\n\nСтеготекст збережено в:\n{pth_o}")
        messagebox.showinfo("Успіх", "Приховано")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def a_dec():
    pth_i = filedialog.askopenfilename(filetypes=[("Files", "*.txt *.html")])
    if not pth_i: return
    with open(pth_i, 'r', encoding='utf-8') as f:
        s_txt = f.read()
    m_type = cb_m.get()
    shft = e_shf.get()
    try:
        if m_type == "Нульова ширина":
            r = dec_zw(s_txt)
        elif m_type == "Регістр":
            r = dec_cs(s_txt)
        elif m_type == "Пробіли":
            r = dec_sp(s_txt)
        elif m_type == "Колір шрифту":
            r = dec_cl(s_txt)
        if shft: r = cs_dec(r, shft)
        t_log.delete(1.0, tk.END)
        t_log.insert(tk.END, f"Вилучене повідомлення:\n{r}")
        messagebox.showinfo("Результат", "Успішно вилучено")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))
wnd = tk.Tk()
wnd.title("Text Steganography")
wnd.geometry("450x450")
tk.Label(wnd, text="Секретне повідомлення:").pack(pady=2)
e_msg = tk.Entry(wnd, width=50)
e_msg.pack(pady=2)
tk.Label(wnd, text="Ключ Цезаря:").pack(pady=2)
e_shf = tk.Entry(wnd, width=10)
e_shf.pack(pady=2)
tk.Label(wnd, text="Метод:").pack(pady=2)
cb_m = ttk.Combobox(wnd, values=["Нульова ширина", "Регістр", "Пробіли", "Колір шрифту"], state="readonly")
cb_m.current(0)
cb_m.pack(pady=2)
tk.Button(wnd, text="Приховати", command=a_enc).pack(pady=5)
tk.Button(wnd, text="Вилучити", command=a_dec).pack(pady=5)
tk.Label(wnd, text="Лог виконання:").pack(pady=2)
t_log = tk.Text(wnd, height=12, width=50)
t_log.pack(pady=2)
wnd.mainloop()