import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from fractions import Fraction

def dot(x,w):
    return sum([a*b for (a,b) in zip(x,w)])

def cov(x,y,w):
    E_x = dot(x,w)
    E_y = dot(y,w)
    return dot([(x1 - E_x)*(y1 - E_y) for (x1,y1) in zip(x,y)],p)

def var(x,w):
    return cov(x,x,w)

# an option that pays 1 if and only if the "coin flip" result is 1 (out of 1, 2, and 3)
u = 2
strike = 7
S0 = Fraction(4)
S1 = [u*S0,S0, S0/u]
V1 = [max([Fraction(0),Fraction(s1-strike)]) for s1 in S1]
delta_S1 = [i - S0 for i in S1]

"""
fixed probabiliy measure
"""

p = np.array([
    Fraction(1,3),
    Fraction(1,3),
    Fraction(1,3)
    ])

# sequential regression formula
fixed_xi_1 = cov(V1, delta_S1, p) / var(delta_S1, p)
fixed_V0 = dot(V1, p) - fixed_xi_1 * dot(delta_S1, p)

# compute L1 from follmer schweizer decomposition
fixed_L1 = [v1 - fixed_V0 - fixed_xi_1 * dS1 for (v1, dS1) in zip(V1, delta_S1)]
fixed_E_L1 = dot(fixed_L1, p)


"""
explore space of probability measures
"""

# list containing 3d coords (p1, p2, E(L) or V0)
residual = []
fairTimeZeroPrice = []

for p1 in range(1, 100, 1):
    for p2 in range(1, 100 - p1, 1):
        p3 = 100 - p1 - p2
        p = [Fraction(p1,100), Fraction(p2,100), Fraction(p3,100)]

        # sequential regression formula
        xi_1 = cov(V1, delta_S1, p) / var(delta_S1, p)
        fair_V0 = dot(V1, p) - xi_1 * dot(delta_S1, p)

        # compute L1 from follmer schweizer decomposition
        L1 = [v1 - fair_V0 - xi_1 * dS1 for (v1, dS1) in zip(V1, delta_S1)]
        E_L1 = dot(L1, p)

        residual.append((p1, p2, float(E_L1)))
        fairTimeZeroPrice.append((p1, p2, float(fair_V0-fixed_V0)))

fig = plt.figure()
ax = plt.axes(projection="3d")

"""
Plot Expectation of L_1
"""

xdata, ydata, e_l1 = zip(*residual)
p = ax.scatter3D(xdata, ydata, e_l1, c=e_l1, cmap='viridis')

ax.set_xlabel('p1')
ax.set_ylabel('p2')
ax.set_zlabel('E[L1]')

"""
Plot Fair Time-zero option price
"""

# xdata, ydata, v0 = zip(*fairTimeZeroPrice)
# p = ax.scatter3D(xdata, ydata, v0, c=v0, cmap="viridis")

# ax.set_xlabel("p1")
# ax.set_ylabel("p2")
# ax.set_zlabel("optimal V0")

fig.colorbar(p)
plt.show()
