import get_data
import formulas

s = get_data.stock_price()
x = get_data.exercise_price()
r = get_data.risk()
t = get_data.time()
o = get_data.volatility()

d1 = formulas.d1(s, x, r, t, o)
d2 = formulas.d2(s, x, r, t, o)
c0 = formulas.c0(d1, d2, s, x, r, t)
print("CALL Value: " + str(round(c0, 2)))

p0 = formulas.p0(d1, d2, s, x, r, t)
print("PUT Value: " + str(round(p0, 2)))

print("\nGeeks:\n")

delta_call = formulas.delta(d1)
delta_put = 1 - formulas.delta(d1)
print("Delta CALL: " + str(round(delta_call, 2)))
print("Delta PUT: " + str(round(delta_put, 2)))

gamma = formulas.gamma(d1, s, t, o)
print("Gamma: " + str(round(gamma, 2)))

vega = formulas.vega(d1, s, t)
print("Theta: " + str(round(vega, 2)))

theta_call = formulas.theta_call(d1, d2, s, x, r, t, o)
theta_put = formulas.theta_put(d1, d2, s, x, r, t, o)
print("Theta CALL: " + str(round(theta_call, 2)))
print("Theta PUT: " + str(round(theta_put, 2)))

rho_call = formulas.rho_call(d2, x, r, t)
rho_put = formulas.rho_put(d2, x, r, t)
print("Rho CALL: " + str(round(rho_call, 2)))
print("Rho PUT: " + str(round(rho_put, 2)))