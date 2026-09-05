import yaml
from tabulate import tabulate


def load_cases(path):
    with open(path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data["cases"]


def parse(case):
    return list(case)


def solve(seq):
    last = {}
    left = best_i = best_n = 0
    for right, char in enumerate(seq):
        if char in last and last[char] >= left:
            left = last[char] + 1
        last[char] =  right
        n = right - left + 1
        if n > best_n:
            best_n, best_i = n, left
    if best_n == 0:
        return "", 0, None, None
    end = best_i + best_n - 1
    return seq[best_i:end + 1], best_n, best_i, end


def main():
    cases = load_cases("data.yaml")
    rows = []
    best_n, best_len, best_sub = None, -1, ""
    for n, case in enumerate(cases):
        seq = parse(case)
        sub, length, start, end = solve(seq)

        rows.append([n, case, "".join(sub) if isinstance(sub, list) else sub, length, start, end])
        if length > best_len:
            best_n, best_len, best_sub = n, length, sub
    print(tabulate(rows, headers=["line", "source", "substring", "length", "start", "end"], tablefmt="github"))
    print("\nBest case: %s, substring = %s, length = %s" % (best_n, "".join(best_sub) if isinstance(best_sub, list) else best_sub, best_len))


if __name__ == "__main__":
    main()

# 1. Строка 32: cases — загружаем строки из файла data.yaml, было case
# 2. Строки 19–20: исправлен сдвиг left, чтобы левая граница окна не двигалась назад.
# 3. В main убрали обработку пустой строки, так как solve() уже возвращает None для позиций.
# 4. Строки 23 и 40: оставили >, а не >=, чтобы при одинаковой длине сохранялся первый, то есть левый вариант.