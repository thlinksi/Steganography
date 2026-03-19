import math

INTERVALS = [
    (0, 7, 3), (8, 15, 3), (16, 31, 4),
    (32, 63, 5), (64, 127, 6), (128, 255, 7)
]

def get_interval(d):
    for l_k, u_k, n in INTERVALS:
        if l_k <= d <= u_k:
            return l_k, u_k, n
    return 0, 0, 0

def run_pvd():
    p1 = int(input("Введіть Pixel 1: "))
    p2 = int(input("Введіть Pixel 2: "))
    char = input("Введіть секретний символ (1 літера): ")
    bin_char = format(ord(char), '08b')
    print(f"\n[HIDE] Символ '{char}' -> ASCII: {ord(char)} -> Бінарно: {bin_char}")
    d = abs(p2 - p1)
    print(f"[HIDE] Початкова різниця (d): {d}")
    l_k, u_k, n = get_interval(d)
    print(f"[HIDE] Інтервал: [{l_k}, {u_k}], Можна вбудувати бітів (n): {n}")
    b_bits = bin_char[:n]
    b = int(b_bits, 2)
    print(f"[HIDE] Вбудовуємо перші {n} біт: '{b_bits}' (десяткове b = {b})")
    d_prime = l_k + b
    print(f"[HIDE] Нова різниця (d_new): {d_prime}")
    m = d_prime - d
    print(f"[HIDE] Різниця m: {m}")
    delta_p1 = math.floor(abs(m) / 2)
    delta_p2 = math.ceil(abs(m) / 2)
    print(f"[HIDE] Зміщення: delta_p1 = {delta_p1}, delta_p2 = {delta_p2}")
    p1_new, p2_new = p1, p2

    if m > 0:
        if p2 >= p1:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2
        else:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
    elif m < 0:
        if p2 >= p1:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
        else:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2
    p1_new = max(0, min(255, p1_new))
    p2_new = max(0, min(255, p2_new))
    print(f"[HIDE] Результат: Pixel 1_new = {p1_new}, Pixel 2_new = {p2_new}")
    print("\n" + "-" * 40)
    print(" ВИЛУЧЕННЯ (EXTRACT)")
    print("-" * 40)
    ext_d = abs(p2_new - p1_new)
    ext_l_k, _, ext_n = get_interval(ext_d)
    ext_b = ext_d - ext_l_k
    ext_b_bits = format(ext_b, f'0{ext_n}b')
    print(f"[EXTRACT] Вилучена різниця: {ext_d}")
    print(f"[EXTRACT] Нижня межа інтервалу: {ext_l_k}")
    print(f"[EXTRACT] Вилучені біти: '{ext_b_bits}'")
    print("=" * 40 + "\n")

if __name__ == "__main__":
    while True:
        run_pvd()
        if input("Продовжити тестування? (y/n): ").lower() != 'y':
            break