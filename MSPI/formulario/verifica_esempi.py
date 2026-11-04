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

print("--- argomento 15: gaussiana e funzione Q")
from math import erfc, sqrt
Q = lambda x: 0.5 * erfc(x / sqrt(2))
print("Q(1)", r(Q(1), 3), "1-2Q(1)", r(1 - 2 * Q(1), 3), "Q(2)", r(Q(2)), "Q(1.5)", r(Q(1.5)), "Q(-0.5)", r(Q(-0.5), 3))
print("Q(1.3)", r(Q(1.3)), "Q(2.5)", r(Q(2.5), 5), "magg Q(3)", r(exp(-4.5) / (3 * sqrt(2 * pi)), 5), "Q(3)", r(Q(3), 5))
print("1-2Q(2)", r(1 - 2 * Q(2), 3), "2Q(2)", r(2 * Q(2)), "2Q(3)", r(2 * Q(3)), "Q(4)", Q(4))
print("int e^(-x^2/2) = sqrt(2 pi)", r(integra(lambda x: exp(-x * x / 2), -12, 12)), r(sqrt(2 * pi)))

print("--- argomento 16: vettori aleatori e gaussiani")
R = [[F(5, 12), F(1, 3)], [F(1, 3), F(5, 12)]]
mu = [F(7, 12), F(7, 12)]
C = [[R[i][j] - mu[i] * mu[j] for j in range(2)] for i in range(2)]
print("R*144", [[x * 144 for x in r_] for r_ in R], "C*144", [[x * 144 for x in r_] for r_ in C])
q = [1, 1]
print("var(X1+X2)", sum(q[i] * C[i][j] * q[j] for i in range(2) for j in range(2)), F(20, 144))
print("[[1,2],[2,1]] con q=[1,-1]:", 1 - 2 - 2 + 1)
print("bivariata rho=0.5: det", 1 - 0.25, "f(0,0)", r(1 / (2 * pi * sqrt(0.75)), 3))
print("cerchi:", [r(1 - exp(-k * k / 2), 3) for k in (1, 2, 3)])
print("condizionata rho=0.8: media", 0.8, "varianza", r(1 - 0.64, 2), "sd", r(sqrt(1 - 0.64), 2))
print("coppia correlata rho=0.6: sqrt(1-0.36)", r(sqrt(1 - 0.36), 2))
print("C=[[4,3],[3,9]]: det", 4 * 9 - 3 * 3, "forma con [1,-1]", 4 - 3 - 3 + 9, "matrice sigma 2,3 rho .5:", 0.5 * 2 * 3)

from math import cos
print("--- argomento 17: processi aleatori")
print("tre assi", F(4, 52) * F(3, 51) * F(2, 50), 4 * 3 * 2, 52 * 51 * 50, r(F(24, 132600), 7))
print("Bernoulli +1,+1,-1", F(1, 2)**3, "quaternario due 2", F(1, 4)**2)
a = sqrt(3)
print("uniforme (-sqrt3, sqrt3): varianza a^2/3 =", r(a * a / 3, 6), "(2a)^2/12 =", r((2 * a)**2 / 12, 6))
from itertools import product
# media mobile: Y(n) = (X(n) + X(n-1))/2, X Bernoulli +-1; R_Y(k) enumerando X(n-1..n+3)
def RY(k):
    tot = F(0)
    for xs in product((-1, 1), repeat=6):        # X(-1), X(0), ..., X(4)
        Y = lambda n: F(xs[n + 1] + xs[n], 2)    # Y(n) per n = 0..4
        tot += Y(0) * Y(k) * F(1, 64)
    return tot
print("R_Y(0..3)", [RY(k) for k in range(4)], "pmf Y", {v: sum(F(1, 4) for a_ in (-1, 1) for b_ in (-1, 1) if F(a_ + b_, 2) == v) for v in (-1, 0, 1)})
Cy = [[RY(abs(i - j)) for j in range(4)] for i in range(4)]
print("C_Y (x2)", [[2 * c for c in riga] for riga in Cy])
# sinusoide con fase a caso: R_X(k) = E[A cos(2 pi U + phi_n) A cos(2 pi U + phi_{n+k})], A = 1, f0 = 1/8
f0 = 1 / 8
for k in (0, 4, 8, 3):
    for n in (0, 5):
        v = integra(lambda u: cos(2 * pi * u + 2 * pi * f0 * n) * cos(2 * pi * u + 2 * pi * f0 * (n + k)), -0.5, 0.5, 4000)
        print("sinusoide k=%d n=%d R=%.4f formula=%.4f" % (k, n, v, 0.5 * cos(2 * pi * f0 * k)))
print("media coseno su 2 periodi", r(integra(lambda u: cos(4 * pi * u + 0.7), -0.5, 0.5, 4000), 6))
print("cos^2 medio su un periodo", r(integra(lambda u: cos(2 * pi * u)**2, 0, 1, 4000), 6))
# passeggiata aleatoria: R_S(n1, n2) enumerando
def RS(n1, n2):
    tot = F(0)
    m = max(n1, n2)
    for xs in product((-1, 1), repeat=m):
        tot += sum(xs[:n1]) * sum(xs[:n2])
    return tot / 2**m
print("R_S(1,2)", RS(1, 2), "R_S(10,11)", RS(10, 11), "var S(100) =", 100, "sd", sqrt(100))

print("--- argomento 18: grandi numeri e limite centrale")
mu_d = F(sum(range(1, 7)), 6); var_d = F(sum(k * k for k in range(1, 7)), 6) - mu_d**2
print("dado: mu", mu_d, "var", var_d, "var media 100", r(var_d / 100, 4), "sd", r(sqrt(var_d / 100), 3))
print("Chebyshev moneta: sigma2/(n eps^2) = 100/n:", F(1, 4) / F(25, 10000), "n per 0.05:", F(1, 4) / (F(5, 100) * F(25, 10000)))
print("frequenza del 6 su 600: var", F(1, 6) * F(5, 6) / 600, r(F(5, 36) / 600, 7), "sd", r(sqrt(5 / 36 / 600), 4))
print("dieci dadi: mu", 10 * mu_d, "var", 10 * var_d, r(10 * var_d, 2), "sd", r(sqrt(10 * var_d), 2))
# n per 2Q(0.1 sqrt n) = 0.05
z = 1.959963984540054
print("Q(1.96)", r(Q(1.96), 4), "n = (z/0.1)^2 =", r((z / 0.1)**2, 1), "2Q(0.1 sqrt 385)", r(2 * Q(0.1 * sqrt(385)), 4))
print("binomiale 50, 1/2: media", 50 * 0.5, "varianza", 50 * 0.25)
# M(t) gaussiana standard = e^{t^2/2}, numerica per t = 0.7
t = 0.7
print("M gauss(0.7)", r(integra(lambda x: exp(t * x) * exp(-x * x / 2) / sqrt(2 * pi), -12, 12), 5), r(exp(t * t / 2), 5))

print("--- argomento 19: decisioni bayesiane")
p1, p2, n = 0.6, 0.2, 10
eta1 = n * log((1 - p2) / (1 - p1)) / log(p1 * (1 - p2) / (p2 * (1 - p1)))
Bn = lambda k, p: comb(n, k) * p**k * (1 - p)**(n - k)
pe1 = sum(Bn(k, p1) for k in range(0, 4)); pe2 = sum(Bn(k, p2) for k in range(4, n + 1))
print("eta1", r(eta1, 3), "= 10 ln2/ln6", r(10 * log(2) / log(6), 3), "Pe|H1", r(pe1, 3), "Pe|H2", r(pe2, 3), "Pe", r((pe1 + pe2) / 2, 3))
print("soglie 1..7:", [r(0.5 * sum(Bn(k, p1) for k in range(t)) + 0.5 * sum(Bn(k, p2) for k in range(t, n + 1)), 3) for t in range(1, 8)])
Lw = lambda w: (p1 / p2)**w * ((1 - p1) / (1 - p2))**(n - w)
print("L(4)", r(Lw(4), 4), F(81, 64), "L(3)", r(Lw(3), 3), "prima w con L > 4:", min(w for w in range(11) if Lw(w) > 4))
pe1b = sum(Bn(k, p1) for k in range(0, 5)); pe2b = sum(Bn(k, p2) for k in range(5, n + 1))
print("MAP P(H1)=0.2: Pe soglia 5", r(0.2 * pe1b + 0.8 * pe2b, 3), "soglia 4", r(0.2 * pe1 + 0.8 * pe2, 3))
print("media gaussiana +-1 V, sigma 2: n=1", r(Q(0.5), 3), "n=16", r(Q(2), 3))
print("rischio", 10 * 0.03 + 1 * 0.05, "P(e)", 0.03 + 0.05)

print("--- argomento 20: Neyman-Pearson")
def Qinv(a, lo=-10.0, hi=10.0):
    for _ in range(200):
        m = (lo + hi) / 2
        if Q(m) > a: lo = m
        else: hi = m
    return (lo + hi) / 2
print("Q^-1:", {a: r(Qinv(a), 4) for a in (0.1, 0.05, 0.025, 0.01, 0.001)})
for nn in (16, 36, 64):
    print("radar n=%d potenza %.3f" % (nn, Q(Qinv(0.05) - 0.5 * sqrt(nn))), "soglia", r(Qinv(0.05) / sqrt(nn), 3))
print("ROC d=2: alpha .05 ->", r(Q(Qinv(0.05) - 2), 3), "alpha .01 ->", r(Q(Qinv(0.01) - 2), 3), "alpha .1 ->", r(Q(Qinv(0.1) - 2), 3))
n = 10
Bn = lambda k, p: comb(n, k) * p**k * (1 - p)**(n - k)
for t in (3, 4, 5, 6):
    print("bit: soglia w>=%d alpha %.4f potenza %.4f" % (t, sum(Bn(k, 0.2) for k in range(t, n + 1)), sum(Bn(k, 0.6) for k in range(t, n + 1))))

print("--- argomento 21: stima bayesiana")
eul = lambda a, b: F(factorial(a) * factorial(b), factorial(a + b + 1))
print("eulero t(1-t)", eul(1, 1), "t^3(1-t)^2", eul(3, 2), "numerico", r(integra(lambda t: t**3 * (1 - t)**2, 0, 1), 6), r(1 / 60, 6))
print("2 teste in 3: costante", 1 / eul(2, 1), "MMSE", 12 * eul(3, 1), F(3, 5), "MMSE 3 su 3", F(4, 5))
print("a posteriori U[0,2], costo quadratico: min di a^2-2a+4/3 in", 1, "check", r(0.5 * integra(lambda t: (1 - t)**2, 0, 2), 4), r(1 - 2 + 4 / 3, 4))
print("F(a)=a^2-a+1/3: a=0.3 ->", r(integra(lambda t: (0.3 - t)**2, 0, 1), 5), r(0.09 - 0.3 + 1 / 3, 5))
# errori quadratici medi della moneta, per enumerazione esatta (media su B uniforme con eulero)
def mse(stima, n):
    tot = F(0)
    for w in range(n + 1):
        # E[(s - B)^2 ; w] = C(n,w) * int (s - b)^2 b^w (1-b)^(n-w) db
        s = stima(w, n)
        tot += comb(n, w) * (s * s * eul(w, n - w) - 2 * s * eul(w + 1, n - w) + eul(w + 2, n - w))
    return tot
for n in (1, 2, 5, 10, 100):
    m1 = mse(lambda w, n: F(w + 1, n + 2), n); m2 = mse(lambda w, n: F(w, n), n)
    print("n=%d MMSE %s (%s) MAP %s (%s)" % (n, m1, F(1, 6 * (n + 2)), m2, F(1, 6 * n)), r(m1, 5), r(m2, 5))
n = 7
print("momenti n=7: E[w]", sum(comb(n, w) * w * eul(w, n - w) for w in range(n + 1)), F(n, 2),
      "E[w^2]", sum(comb(n, w) * w * w * eul(w, n - w) for w in range(n + 1)), F(n, 6) + F(n * n, 3),
      "E[wB]", sum(comb(n, w) * w * eul(w + 1, n - w) for w in range(n + 1)), F(n, 3))
