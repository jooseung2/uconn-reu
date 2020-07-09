import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def m(x, w):
    """Weighted Mean"""
    return np.sum(x * w) / np.sum(w)


def cov(x, y, w):
    """Weighted Covariance"""
    return np.sum(w * (x - m(x, w)) * (y - m(y, w))) / np.sum(w)


def var(x, w):
    """Weighted Variance"""
    return np.sum(w * (x - m(x, w)) * (x - m(x, w))) / np.sum(w)


# an option that pays 1 if and only if the "coin flip" result is 1 (out of 1, 2, and 3)
V1 = np.array([1, 0, 0])

# So if up-factor=2 and S_0=4, corresponds to strike price=7 for a European call
u = 2
S0 = 4

# assume d = 1/u
S1 = np.array([u * S0, S0, S0 / u])

delta_S1 = [i - S0 for i in S1]

fig = plt.figure()
ax = plt.axes(projection="3d")

# list containing 3d coords (p1, p2, E(L) or V0)
points = []
fairTimeZeroPrice = []

for p1 in range(1, 100, 1):
    for p2 in range(1, 100 - p1, 1):
        p3 = 100 - p1 - p2
        p = np.array([p1 * 1.0 / 100, p2 * 1.0 / 100, p3 * 1.0 / 100])

        # sequential regression formula
        xi_1 = cov(V1, delta_S1, p) / var(delta_S1, p)
        fair_V0 = m(V1, p) - xi_1 * m(delta_S1, p)

        # compute L1 from follmer schweizer decomposition
        L1 = [v1 - fair_V0 - xi_1 * dS1 for (v1, dS1) in zip(V1, delta_S1)]
        E_L1 = m(L1, p)

        # if p3 < 67 and 2 * p1 == p3:
        #     # risk neutral when 0 < p3 < 2/3 and p1 = (1/2) * p3
        #     risk_neutral_points.append((p1, p2, E_L1))
        #     risk_neutral_fairTimeZeroPrice.append((p1, p2, fair_V0))
        # else:
        #     points.append((p1, p2, E_L1))
        #     fairTimeZeroPrice.append((p1, p2, fair_V0))

        points.append((p1, p2, E_L1))
        fairTimeZeroPrice.append((p1, p2, fair_V0))

"""
Plot Expectation of L_1
"""

xdata, ydata, e_l1 = zip(*points)
ax.scatter3D(xdata, ydata, e_l1, c=e_l1, cmap='viridis')

ax.set_xlabel('p1')
ax.set_ylabel('p2')
ax.set_zlabel('E[L1]')

"""
Plot Fair Time-zero option price
"""

# xdata, ydata, v0 = zip(*fairTimeZeroPrice)
# ax.scatter3D(xdata, ydata, v0, c=v0, cmap="viridis")

# ax.set_xlabel("p1")
# ax.set_ylabel("p2")
# ax.set_zlabel("optimal V0")


plt.show()
