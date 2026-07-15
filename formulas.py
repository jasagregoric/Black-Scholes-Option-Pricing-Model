import math
from scipy.stats import norm

def d1(s, x, r, t, o):
    d1 = math.log((s/x)) + (r + (o ** 2)/2) * t
    d2 = o * math.sqrt(t)
    return d1/d2

def d2(s, x, r, t, o):
    d1 = math.log((s/x)) + (r - (o ** 2)/2) * t
    d2 = o * math.sqrt(t)
    return d1/d2

def c0(d1, d2, s, x, r, t):
    c1 = s * norm.cdf(d1)
    c2 = x * (math.e ** (-1 * r * t)) * norm.cdf(d2)
    return c1 - c2

def p0(d1, d2, s, x, r, t):
    p1 = x * math.e ** (-r*t) * norm.cdf(-d2)
    p2 = s * norm.cdf(-d1)
    return p1 - p2

def delta(d1):
    return norm.cdf(d1)

def gamma(d1, s, t, o):
    return (norm.pdf(d1)/(s*o*math.sqrt(t)))

def vega(d1, s, t):
    return s*norm.pdf(d1)*math.sqrt(t)

def theta_call(d1, d2, s, x, r, t, o):
    t1 = -((s*norm.pdf(d1)*o)/(2*math.sqrt(t)))
    t2 = r * x * math.e ** (-r*t) * norm.cdf(d2)
    return t1 - t2

def theta_put(d1, d2, s, x, r, t, o):
    t1 = -((s*norm.pdf(d1)*o)/(2*math.sqrt(t)))
    t2 = r * x * math.e ** (-r*t) * norm.cdf(-d2)
    return t1 + t2

def rho_call(d2, x, r, t):
    return (x * t * math.e ** (-r*t) * norm.cdf(d2))

def rho_put(d2, x, r, t):
    return -(x * t * math.e ** (-r*t) * norm.cdf(-d2))