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

print("--- argomento 6: pmf condizionate e funzioni")
print("dado | X>4", F(1, 6) / F(2, 6), "media", 5 * F(1, 2) + 6 * F(1, 2))
b05 = comb(10, 9) * 0.5**10
b08 = comb(10, 9) * 0.8**9 * 0.2
print("due monete p(9):", r(b05), r(b08), "P(truccata|9)", r(b08 / (b05 + b08), 3))
print("media due monete", F(1, 2) * 5 + F(1, 2) * 8)
X = [-2, -1, 0, 2]
pY = {}
for x in X:
    pY[x * x] = pY.get(x * x, 0) + F(1, 4)
print("pmf di X^2", dict(sorted(pY.items())), "E[X^2]", sum(F(x * x, 4) for x in X))

print("--- argomento 7: varianza e disuguaglianze")
EX2 = 16 * F(1, 4) + 25 * F(1, 2) + 36 * F(1, 4)
print("E[X^2]", EX2, float(EX2), "Xrms", r(float(EX2) ** 0.5, 3), "var X", EX2 - 25)
print("var Y", 16 * F(1, 4) + 16 * F(1, 4), "sigma Y", r(8 ** 0.5, 3), "sigma X", r(0.5 ** 0.5, 3))
N, p = 10, F(1, 10)
print("binomiale E[X(X-1)]", N * (N - 1) * p**2, "E[X^2]", N * (N - 1) * p**2 + N * p, "var", N * (N - 1) * p**2 + N * p - (N * p)**2)
print("Fahrenheit", F(18, 10) * 20 + 32, F(18, 10) * 2, "dado", F(6 * 6 - 1, 12))
pz = sum(exp(-2) * 2**k / factorial(k) for k in range(10))
print("Markov router: limite 0.2, Poisson(2) P(Z>=10) =", 1 - pz)
print("Chebyshev k=2", 1 - F(1, 4), "k=3", F(1, 9), r(F(1, 9), 2))

print("--- argomento 8: variabili multiple")
pj = {(0, 0): F(1, 3), (0, 1): F(2, 9), (1, 0): F(1, 9), (1, 1): F(1, 3)}
pX = {x: sum(v for (a, b), v in pj.items() if a == x) for x in (0, 1)}
pY = {y: sum(v for (a, b), v in pj.items() if b == y) for y in (0, 1)}
print("somma", sum(pj.values()), "pX", pX, "pY", pY, "prodotto 00", pX[0] * pY[0], "vs", pj[(0, 0)], F(27, 81))
pXc = {0: F(6, 10), 1: F(4, 10)}
canale = lambda y, x: F(9, 10) if x == y else F(1, 10)
pjc = {(x, y): canale(y, x) * pXc[x] for x in (0, 1) for y in (0, 1)}
pYc = {y: pjc[(0, y)] + pjc[(1, y)] for y in (0, 1)}
print("canale congiunta", {k: float(v) for k, v in pjc.items()}, "pY", {k: float(v) for k, v in pYc.items()})
print("bayes", pjc[(1, 1)] / pYc[1], pjc[(0, 1)] / pYc[1])
print("catena", 0.5 * 0.8 * 0.9)

print("--- argomento 9: covarianza e correlazione")
pj = {(0, 0): F(1, 3), (0, 1): F(2, 9), (1, 0): F(1, 9), (1, 1): F(1, 3)}
E = lambda g, p: sum(g(x, y) * v for (x, y), v in p.items())
print("E[3X^2+Y]", E(lambda x, y: 3 * x * x + y, pj))
pY0, pY1 = pj[(0, 0)] + pj[(1, 0)], pj[(0, 1)] + pj[(1, 1)]
h0 = 3 * pj[(1, 0)] / pY0
h1 = 3 * pj[(1, 1)] / pY1 + 1
print("h(0)", h0, "h(1)", h1, "media in due tempi", h0 * pY0 + h1 * pY1)
mx, my = E(lambda x, y: x, pj), E(lambda x, y: y, pj)
vx, vy = E(lambda x, y: x * x, pj) - mx**2, E(lambda x, y: y * y, pj) - my**2
cov = E(lambda x, y: x * y, pj) - mx * my
print("medie", mx, my, "varianze", vx, vy, "E[XY]", E(lambda x, y: x * y, pj), "cov", cov, "rho", cov / vx)
p2 = {(1, -1): F(1, 8), (-1, -1): F(1, 4), (-1, 1): F(1, 2), (1, 1): F(1, 8)}
pz = {}
for (x, y), v in p2.items():
    pz[3 * x * x + y] = pz.get(3 * x * x + y, 0) + v
mx2, my2 = E(lambda x, y: x, p2), E(lambda x, y: y, p2)
cov2 = E(lambda x, y: x * y, p2) - mx2 * my2
vx2, vy2 = 1 - mx2**2, 1 - my2**2
print("seconda coppia pZ", pz, "cov", cov2, "rho", float(cov2) / float(vx2 * vy2) ** 0.5, -1 / 45**0.5)
print("X uniforme {-1,0,1}, Y=X^2: E[XY]", sum(F(x**3, 3) for x in (-1, 0, 1)))
print("due dadi", 2 * F(35, 12), float(2 * F(35, 12)))

print("--- argomento 10: densità e CDF")
def integra(f, a, b, n=200000):
    # regola del punto medio: basta per controllare i risultati a 4 cifre
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h
print("P(X<=1/2) con f=2x", r(integra(lambda x: 2 * x, 0, 0.5)), "costante c per c x^2", r(1 / integra(lambda x: x * x, 0, 1)))
tri = lambda x: max(0.0, 1 - abs(x))
Ftri = lambda x: integra(tri, -1, x)
print("triangolare F(1/2), F(-1/2)", r(Ftri(0.5)), r(Ftri(-0.5)), "P", r(Ftri(0.5) - Ftri(-0.5)), "attesi", 7 / 8, 1 / 8)
print("media f=2x", r(integra(lambda x: 2 * x * x, 0, 1)), "media triangolare", r(integra(lambda x: x * tri(x), -1, 1)))
print("integrale (3+x) da 0 a 2", r(integra(lambda x: 3 + x, 0, 2)), "int x^-2 da 1 a 1000", r(integra(lambda x: x ** -2, 1, 1000, 2000000)))

print("--- argomento 11: variabili continue notevoli")
from math import atan, pi, log
print("U(2,6): P(3<=X<=4)", F(1, 4), "media", F(2 + 6, 2), "varianza", F((6 - 2)**2, 12))
print("esponenziale lambda=0.5: P(X>3)", r(exp(-1.5)), "P(X<=1)", r(1 - exp(-0.5)))
print("memoria: e^-0.5", r(exp(-0.5)))
print("Laplace lambda=1: P(X<=-1)", r(0.5 * exp(-1)), "P(|X|>1)", r(exp(-1)))
print("Cauchy(0,1): P(-1<=X<=1)", r((atan(1) - atan(-1)) / pi), "P(X>1)", r(0.5 - atan(1) / pi))
print("per parti int_0^1 x e^x", r(integra(lambda x: x * exp(x), 0, 1)), "cambio variabile int_0^1 2x e^(x^2)", r(integra(lambda x: 2 * x * exp(x * x), 0, 1)), "e-1", r(exp(1) - 1))
print("logaritmo: ln10/0.5", r(log(10) / 0.5, 2), "arcotangente: (1/pi) int_-1^1 1/(1+y^2)", r(integra(lambda y: 1 / (pi * (1 + y * y)), -1, 1)))

print("--- argomento 12: PDF condizionate e funzioni")
print("E(1) | X<=1: 1-e^-1", r(1 - exp(-1), 3), "Laplace(1) P(-1<=X<=2)", r((1 - 0.5 * exp(-2)) - 0.5 * exp(-1), 3))
print("miscela: media", F(1, 2) * 1 + F(1, 2) * 3, "area", r(integra(lambda x: 0.5 * exp(-x) + 0.5 / 3 * exp(-x / 3), 0, 200, 400000)))
print("U(-1,1)^2: area di 1/(2 sqrt y) su (0,1)", r(integra(lambda y: 1 / (2 * y ** 0.5), 0, 1, 2000000), 3))
print("Cauchy^2: area di 1/(pi sqrt(y)(1+y))", r(integra(lambda y: 1 / (pi * y ** 0.5 * (1 + y)), 0, 4000, 4000000), 3))
print("inversione u=0.5: ln2", r(log(2), 3), "arcoseno A=1 in 0", r(1 / pi, 3))
print("A/D Laplace(1): p(0.5)", r(0.5 - 0.5 * exp(-1), 3), "p(3.5)", r(0.5 * exp(-3), 3))

print("--- argomento 13: media e varianza nel continuo")
print("U(0,1): E[X^2]", r(integra(lambda x: x * x, 0, 1)), "f=2x: E[X^2]", r(integra(lambda x: 2 * x**3, 0, 1)), "var", F(1, 2) - F(4, 9))
D = 2 / 2**8
print("quantizzazione 8 bit: Delta", D, "sigma^2", D * D / 12, "9 bit", (D / 2)**2 / 12, "rapporto", (D * D / 12) / ((D / 2)**2 / 12))
print("esponenziale P(X>=3)", r(exp(-3), 3))

print("--- argomento 14: variabili continue multiple")
def integra2(f, a, b, c, d, n=600):
    hx, hy = (b - a) / n, (d - c) / n
    return sum(f(a + (i + 0.5) * hx, c + (j + 0.5) * hy) for i in range(n) for j in range(n)) * hx * hy
print("P(X+Y<=1) esponenziali", r(integra2(lambda x, y: exp(-x - y) if x + y <= 1 else 0.0, 0, 1, 0, 1, 1200), 3), "1-2/e", r(1 - 2 / exp(1), 3))
g = lambda x, y: x + y
print("area x+y", r(integra2(g, 0, 1, 0, 1)), "E[XY]", r(integra2(lambda x, y: x * y * g(x, y), 0, 1, 0, 1)), F(1, 3))
EX = F(1, 3) + F(1, 4); EX2 = F(1, 4) + F(1, 6)
print("E[X]", EX, "E[X^2]", EX2, "var", EX2 - EX**2, "cov", F(1, 3) - EX**2, "rho", (F(1, 3) - EX**2) / (EX2 - EX**2))
print("E[X|Y=0]", F(1, 3) / F(1, 2), "E[X|Y=1]", (F(1, 3) + F(1, 2)) / F(3, 2))
Fc = lambda x, y: (x * x * y + x * y * y) / 2
print("rettangolo", Fc(1, 1) - Fc(1, .5) - Fc(.5, 1) + Fc(.5, .5), "diretto", r(integra2(g, .5, 1, .5, 1)))
