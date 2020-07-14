import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from fractions import Fraction
import sys
import seaborn as sns
import pandas as pd


def dot(x, w):
    return sum([a * b for (a, b) in zip(x, w)])


def cov(x, y, w):
    E_x = dot(x, w)
    E_y = dot(y, w)
    return dot([(x1 - E_x) * (y1 - E_y) for (x1, y1) in zip(x, y)], p)


def var(x, w):
    return cov(x, x, w)


# an option that pays 1 if and only if the "coin flip" result is 1 (out of 1, 2, and 3)
u = 2
strike = 7
SLICE = 100
initial_stock_price = 4

S0 = Fraction(initial_stock_price)
S1 = [u * S0, S0, S0 / u]
V1 = [max([Fraction(0), Fraction(s1 - strike)]) for s1 in S1]
delta_S1 = [i - S0 for i in S1]

"""
fixed probabiliy measure
"""

p = np.array([Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)])

# sequential regression formula
fixed_xi_1 = cov(V1, delta_S1, p) / var(delta_S1, p)
fixed_V0 = dot(V1, p) - fixed_xi_1 * dot(delta_S1, p)

# compute L1 from follmer schweizer decomposition
fixed_L1 = [v1 - fixed_V0 - fixed_xi_1 * dS1 for (v1, dS1) in zip(V1, delta_S1)]
fixed_risk = var(fixed_L1, p) + dot(fixed_L1, p) ** 2


"""
explore a space of probability measures
"""

# list containing 3d coords (p1, p2, E(L) or V0)
residual = []
fairTimeZeroPrice = []
strategy = []

for p1 in range(1, SLICE, 1):
    for p2 in range(1, SLICE - p1):
        p3 = SLICE - p1 - p2
        p = [Fraction(p1, SLICE), Fraction(p2, SLICE), Fraction(p3, SLICE)]

        # sequential regression formula
        xi_1 = cov(V1, delta_S1, p) / var(delta_S1, p)
        fair_V0 = dot(V1, p) - xi_1 * dot(delta_S1, p)

        # compute L1 from follmer schweizer decomposition
        L1 = [v1 - fair_V0 - xi_1 * dS1 for (v1, dS1) in zip(V1, delta_S1)]

        L1sq = [i ** 2 for i in L1]
        E_L1sq = dot(L1sq, p)

        risk = E_L1sq
        # risk = var(L1, p) + dot(L1, p) ** 2

        strategy.append([p1, p2, p3, float(xi_1 - fixed_xi_1)])
        residual.append((p1, p2, float(risk)))
        fairTimeZeroPrice.append([p1, p2, p3, float(fair_V0 - fixed_V0)])
        # fairTimeZeroPrice.append((p1, p2, float(fair_V0)))

fig = plt.figure()
plt.rc("text", usetex=True)
plt.rc("font", family="sans-serif")
params = {"text.latex.preamble": [r"\usepackage{amsmath}"]}
plt.rcParams.update(params)

"""
Plot Expectation of E(L^2)
"""


if sys.argv[1] == "loss":
    ax = plt.axes(projection="3d")
    xdata, ydata, e_l1 = zip(*residual)
    p = ax.scatter3D(xdata, ydata, e_l1, c=e_l1, cmap="YlGn")

    ax.set_xlabel("p1")
    ax.set_ylabel("p2")
    ax.set_zlabel("E[L^2]")
    fig.colorbar(p)
    plt.show()

elif sys.argv[1] == "price":
    """
    3d plot
    """
    # xdata, ydata, v0 = zip(*fairTimeZeroPrice)
    # # p = ax.scatter3D(xdata, ydata, v0, c=v0, cmap="RdYlBu", vmin=-0.20, vmax=0.20)
    # p = ax.scatter3D(xdata, ydata, v0, c=v0, cmap="RdYlBu")

    # ax.set_xlabel("p1")
    # ax.set_ylabel("p2")
    # ax.set_zlabel("optimal V0")

    # fig.colorbar(p)
    # plt.show()

    """
    heatmap divided into p3
    """
    # def draw_heatmap(*args, **kwargs):
    #     data = kwargs.pop("data")
    #     d = pd.pivot_table(data, index="p1", columns="p2", values="V0")
    #     sns.heatmap(d, center=0, cmap="RdBu_r")

    # filtered_ftzp = [i for i in fairTimeZeroPrice if i[2] % 10 == 0]
    # df1_cols = ["p1", "p2", "p3", "V0"]
    # df1 = pd.DataFrame(filtered_ftzp, index=range(len(filtered_ftzp)), columns=df1_cols)
    # g = sns.FacetGrid(df1, col="p3")
    # g.map_dataframe(draw_heatmap)

    # for i in range(9):
    #     g.axes[0, i].set_ylim(0, 100)
    #     g.axes[0, i].set_xlim(0, 100)

    # plt.show()

    """
    heatmap
    """
    df1_cols = ["p1", "p2", "p3", "V0"]
    df1 = pd.DataFrame(
        fairTimeZeroPrice, index=range(len(fairTimeZeroPrice)), columns=df1_cols
    )
    g = df1.pivot("p1", "p2", "V0")
    ax = sns.heatmap(
        g, center=0, cmap="viridis", cbar_kws={"label": "Fair option price at time 0"}
    )
    ax.set(xlabel="p1", ylabel="p2")

    plt.show()

elif sys.argv[1] == "strat":
    """
    3d plot
    """
    ax = plt.axes(projection="3d")
    xdata, ydata, _, xi = zip(*strategy)
    p = ax.scatter3D(xdata, ydata, xi, c=xi, cmap="RdYlBu", vmin=-0.10, vmax=0.075)

    ax.set_xlabel("p1")
    ax.set_ylabel("p2")
    # ax.set_zlabel("strategy at time 0")

    cbar = fig.colorbar(p)
    cbar.ax.set_title(r"$\xi_1^{\nu} - \hat{\xi}_1$")
    plt.show()

    """
    heatmap
    """
    # df2_cols = ["p1", "p2", "p3", "xi_1"]
    # df2 = pd.DataFrame(strategy, index=range(len(strategy)), columns=df2_cols)
    # g = df2.pivot("p1", "p2", "xi_1")
    # ax = sns.heatmap(
    #     g, center=0, cmap="viridis", cbar_kws={"label": "Optimal Strategy"}
    # )
    # plt.show()
