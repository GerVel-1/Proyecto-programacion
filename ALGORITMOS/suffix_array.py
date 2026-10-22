import sys


def suffix_array(t):
    n = len(t)
    sa = list(range(n))

    # normalizacion obligatoria: rank debe quedar en [0, n-1] para
    # poder empacar (rank[i], rank[i+k]) en un solo entero mas abajo
    caracteres = sorted(set(t))
    mapa = {c: i for i, c in enumerate(caracteres)}
    rank = [mapa[c] for c in t]

    k = 1
    base = n + 2
    while True:
        segunda = rank[k:] + [-1] * min(k, n)
        llave = [r * base + s for r, s in zip(rank, segunda)]
        sa.sort(key=llave.__getitem__)

        nuevo_rank = [0] * n
        llave_prev = llave[sa[0]]
        actual = 0
        for idx in sa[1:]:
            llave_actual = llave[idx]
            if llave_actual != llave_prev:
                actual += 1
                llave_prev = llave_actual
            nuevo_rank[idx] = actual
        rank = nuevo_rank

        if rank[sa[-1]] == n - 1:
            break
        k *= 2

    return sa, rank


def lcp_array(t, sa, rank):
    n = len(t)
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and t[i + h] == t[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1
    return lcp


def tabla_minimos(arr):
    n = len(arr)
    tabla = [arr]
    j = 1
    while (1 << j) <= n:
        paso = 1 << (j - 1)
        anterior = tabla[-1]
        tabla.append(list(map(min, anterior, anterior[paso:])))
        j += 1
    return tabla


def minimo_en_rango(tabla, l, r):
    largo = r - l + 1
    j = largo.bit_length() - 1
    paso = 1 << j
    nivel = tabla[j]
    return min(nivel[l], nivel[r - paso + 1])


def coincidencia(sa, rank, tabla, longitud_t, p, q):
    if p == q:
        return longitud_t - p
    rp, rq = rank[p], rank[q]
    if rp > rq:
        rp, rq = rq, rp
    return minimo_en_rango(tabla, rp + 1, rq)


def palindromo_mas_largo(s):
    n = len(s)
    if n <= 1:
        return s

    reverso = s[::-1]
    t = s + "#" + reverso + "$"
    longitud_t = len(t)

    sa, rank = suffix_array(t)
    lcp = lcp_array(t, sa, rank)
    tabla = tabla_minimos(lcp)

    def espejo(i):
        return n + 1 + (n - 1 - i)

    mejor_inicio, mejor_largo = 0, 1

    for i in range(n):
        pos_espejo = espejo(i)

        extension = coincidencia(sa, rank, tabla, longitud_t, i, pos_espejo)
        extension = min(extension, i + 1, n - i)
        largo = 2 * extension - 1
        if largo > mejor_largo:
            mejor_largo = largo
            mejor_inicio = i - extension + 1

        if i + 1 < n:
            extension = coincidencia(sa, rank, tabla, longitud_t, i + 1, pos_espejo)
            extension = min(extension, i + 1, n - i - 1)
            largo = 2 * extension
            if largo > mejor_largo:
                mejor_largo = largo
                mejor_inicio = i - extension + 1

    return s[mejor_inicio: mejor_inicio + mejor_largo]


def main():
    entrada = sys.stdin.read().strip()
    if not entrada:
        print("")
        return
    print(palindromo_mas_largo(entrada))


if __name__ == "__main__":
    main()
    
