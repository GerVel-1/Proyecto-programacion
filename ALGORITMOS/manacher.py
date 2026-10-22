import sys


def manacher(s):
    if not s:
        return ""
    T = "^#" + "#".join(s) + "#$"
    n = len(T)
    P = [0] * n
    C = 0
    R = 0
    for i in range(1, n - 1):
        i_mirror = 2 * C - i
        if R > i:
            P[i] = min(R - i, P[i_mirror])
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1
        if i + P[i] > R:
            C = i
            R = i + P[i]

    max_len = max(P)
    center_idx = P.index(max_len)
    start = (center_idx - max_len) // 2
    return s[start: start + max_len]


def main():
    # el juez manda la secuencia por stdin, no por un archivo local
    entrada = sys.stdin.read().strip()
    if len(entrada) < 1 or len(entrada) > 50000:
        print("La secuencia esta fuera de rango (1 a 50000) caracteres.")
        return
    print(manacher(entrada))


if __name__ == "__main__":
    main()