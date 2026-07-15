from scipy.optimize import brentq
from datetime import datetime
import formulas

def implied_volatility(price, s, k, r, t):

    def objective(vol):
        model_price = formulas.c0(
            formulas.d1(s,k,r,t,vol),
            formulas.d2(s,k,r,t,vol),
            s,k,r,t
        )

        return model_price - price

    return brentq(objective, 0.001, 5)

def days_between(d2):
    d1 = datetime.today().date()
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days) / 365