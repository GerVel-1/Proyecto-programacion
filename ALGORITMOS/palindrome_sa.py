import sys

def construir_suffix_array(t):
    """Suffix array por duplicacion de rangos. O(n log^2 n)."""
    n = len(t)
    sa = list(range(n))
    rank = [ord(c) for c in t]
    k = 1
    while k < n:
        segundo = rank[k:] + [-1] * k
        clave = list(zip(rank, segundo))
        sa.sort(key=lambda i: clave[i])
        nuevo_rank = [0] * n
        nuevo_rank[sa[0]] = 0
        for i in range(1, n):
            nuevo_rank[sa[i]] = nuevo_rank[sa[i - 1]] + (1 if clave[sa[i - 1]] < clave[sa[i]] else 0)
        rank = nuevo_rank
        if rank[sa[-1]] == n - 1:
            break
        k <<= 1
    return sa, rank
def construir_lcp_kasai(t, sa, rank):
    """Arreglo LCP con el algoritmo de Kasai. O(n)."""
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
        else:
            h = 0
    return lcp
def construir_sparse_table(lcp):
    """Tabla dispersa (RMQ de minimos) sobre el arreglo LCP. O(n log n)."""
    n = len(lcp)
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1
    st = [lcp[:]]
    j = 1
    while (1 << j) <= n:
        anterior = st[-1]
        mitad = 1 << (j - 1)
        actual = [min(anterior[i], anterior[i + mitad]) for i in range(n - (1 << j) + 1)]
        st.append(actual)
        j += 1
    return st, log
def rmq_min(st, log, l, r):
    """Minimo en lcp[l..r] inclusive."""
    if l > r:
        return float("inf")
    j = log[r - l + 1]
    return min(st[j][l], st[j][r - (1 << j) + 1])
def lcp_entre_sufijos(p, q, rank, st, log):
    """LCP entre el sufijo que empieza en p y el que empieza en q (indices en T)."""
    rp, rq = rank[p], rank[q]
    if rp > rq:
        rp, rq = rq, rp
    return rmq_min(st, log, rp + 1, rq)
def secuencia_espejo_mas_larga(s):
    """
    Encuentra el palindromo (secuencia espejo) contiguo mas largo en s
    con Suffix Array + LCP (Kasai) + RMQ, usando(Longest Common Substring vía Suffix Array),
    aplicada a T = S + '#' + reverse(S) + '$'.
    """
    n = len(s)
    if n <= 1:
        return s
    rev = s[::-1]
    t = s + "#" + rev + "$"
    sa, rank = construir_suffix_array(t)
    lcp = construir_lcp_kasai(t, sa, rank)
    st, log = construir_sparse_table(lcp)
    mejor_len = 1
    mejor_inicio = 0
    # Centros impares: palindromo centrado en i (S[i-k] == S[i+k])
    for i in range(n):
        j = 2 * n - i  # posicion en T del sufijo espejo correspondiente
        l = lcp_entre_sufijos(i, j, rank, st, log)
        l = min(l, i + 1, n - i)
        longitud = 2 * l - 1
        if longitud > mejor_len:
            mejor_len = longitud
            mejor_inicio = i - l + 1
    # Centros pares: palindromo centrado entre i e i+1
    for i in range(n - 1):
        j = 2 * n - i
        l = lcp_entre_sufijos(i + 1, j, rank, st, log)
        l = min(l, i + 1, n - i - 1)
        longitud = 2 * l
        if longitud > mejor_len:
            mejor_len = longitud
            mejor_inicio = i - l + 1
    return s[mejor_inicio:mejor_inicio + mejor_len]
def leer_genoma(ruta):
    """Lee el genoma de un archivo .txt, soporta FASTA basico (ignora lineas '>')."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    secuencia = "".join(l.strip() for l in lineas if not l.startswith(">"))
    secuencia = secuencia.upper()
    validos = set("ACGT")
    if not set(secuencia).issubset(validos):
        invalidos = set(secuencia) - validos
        print(f"Aviso se encontraron caracteres fuera de A,C,G,T: {invalidos}", file=sys.stderr)
    return secuencia

def main():
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
    else:
        ruta = input("Ruta del archivo .txt con el genoma: ").strip()
    s = leer_genoma(ruta)
    if not (1 <= len(s) <= 50000):
        print(f"Aviso: longitud fuera de rango (1 <= n <= 50000). n = {len(s)}", file=sys.stderr)
    resultado = secuencia_espejo_mas_larga(s)
    print(f"Longitud de la secuencia: {len(s)}")
    print(f"Secuencia espejo mas larga: {resultado}")
    print(f"Longitud del palindromo: {len(resultado)}")

if __name__ == "__main__":
    main()
