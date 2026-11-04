# Verifica dei numeri usati negli esempi delle schede d'uso del formulario
from fractions import Fraction as F
from math import comb, exp, factorial, perm

def r(x, n=4):
    return round(float(x), n)

print("--- calcolo combinatorio")
print("targhe", 22**4 * 10**3)
print("podi", perm(8, 3), "quaterne ordinate", perm(52, 4))
print("anagrammi ANNA", factorial(4) // (factorial(2) * factorial(2)))
print("superenalotto", comb(90, 6), "due assi su 52", comb(4, 2) * comb(48, 3), comb(48, 3))
print("binom(8,5)", comb(8, 5), "stifel", comb(4, 1) + comb(4, 2), comb(5, 2))
print("gelato", comb(7, 3), "dieci lanci tre teste", comb(10, 3))

print("--- probabilita'")
print("almeno un 6 in 2 lanci", F(11, 36), r(F(11, 36), 3))
p_c2 = F(comb(4, 2) * comb(28, 3), comb(32, 5))
print("poker esattamente 2 assi", comb(4, 2) * comb(28, 3), comb(32, 5), r(p_c2))
print("dado truccato dispari", F(5, 6) + 2 * F(1, 30))
print("almeno un 6 in 10 lanci", r(1 - F(5, 6)**10))
print("pari o >=5", F(3, 6) + F(2, 6) - F(1, 6))
print("pari ma non 6", F(1, 2) - F(1, 6))
# tre eventi: dado, A = pari, B = {1,2,3}, C = {3,6}
A, B, C = {2, 4, 6}, {1, 2, 3}, {3, 6}
P = lambda S: F(len(S), 6)
incl = P(A) + P(B) + P(C) - P(A & B) - P(A & C) - P(B & C) + P(A & B & C)
print("tre eventi incl-escl", incl, "diretto", P(A | B | C), sorted(A | B | C))

print("--- condizionamento")
print("P(6|pari)", F(1, 6) / F(3, 6), "P(dispari|<=3)", F(2, 6) / F(3, 6))
print("due assi di fila", F(4, 52) * F(3, 51), r(F(4, 52) * F(3, 51)))
print("tre assi di fila", F(4, 52) * F(3, 51) * F(2, 50), float(F(4, 52) * F(3, 51) * F(2, 50)))
p1 = F(1, 10) * F(6, 10) + F(9, 10) * F(4, 10)
print("canale P(1 ric)", p1, float(p1))
print("bayes canale", (F(9, 10) * F(4, 10)) / p1, r((F(9, 10) * F(4, 10)) / p1, 3))
num = F(99, 100) * F(1, 100); den = num + F(5, 100) * F(99, 100)
print("test diagnostico", num, den, num / den, r(num / den, 3))
print("indip pari e {1,2}", F(1, 6), F(1, 2) * F(1, 3))

print("--- variabili discrete")
print("somma pmf", F(1, 2) + F(1, 4) + F(1, 8) + F(1, 8))
print("media pmf", 1 * F(1, 2) + 2 * F(1, 4) + 3 * F(1, 8) + 4 * F(1, 8), float(1 * F(1, 2) + 2 * F(1, 4) + 3 * F(1, 8) + 4 * F(1, 8)))
lanci = [5, 3, 6, 3, 6, 6, 6, 5, 1, 4, 2, 6, 1, 2, 1, 3, 4, 2, 4, 5]
print("media 20 lanci", sum(lanci), F(sum(lanci), 20), float(F(sum(lanci), 20)))
print("media dado truccato", F(5, 6) + F(20, 30))
N, p = 10, F(1, 10)
pk = lambda k: comb(N, k) * p**k * (1 - p)**(N - k)
print("binomiale 10 bit P(X=2)", r(pk(2)), "P(X>=1)", r(1 - (1 - p)**N), "E", N * p, "var", N * p * (1 - p))
M = 256
print("byte media", F(M - 1, 2), float(F(M - 1, 2)), "var", F(M * M - 1, 12), float(F(M * M - 1, 12)))
lam = 3
pois = lambda k: lam**k / factorial(k) * exp(-lam)
print("poisson 3: P0", r(pois(0)), "P(X>=1)", r(1 - pois(0)), "P3", r(pois(3)))
print("binom(30,0.1) P3", r(comb(30, 3) * 0.1**3 * 0.9**27))

print("--- richiami")
print("gauss 100", sum(range(1, 101)), "quadrati 3", 1 + 4 + 9, 3 * 4 * 7 // 6)
print("geometrica 1/3", 1 / (1 - F(1, 3)), "da 1 con 1/2", F(1, 2) / (1 - F(1, 2)))
print("e approx", (1 + 1 / 10**6)**(10**6))
print("rms uniforme 0..3", F(sum(i * i for i in range(4)), 4), F((4 - 1) * (2 * 4 - 1), 6))
