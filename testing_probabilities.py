def expected(x,y,p):
    expectation=0
    if y==1:
        for i in range(len(x)):
            expectation+=(x[i]*p[i])
        return expectation
    else:
        for i in range(len(x)):
            expectation+=(x[i]*y[i]*p[i])
        return expectation

def cov(x, y, p):
    return expected(x,y,p)-(expected(x,1,p)*expected(y,1,p))


def var(x, p):
    return expected(x,x,p)-(expected(x,1,p)**2)


# an option that pays 1 if and only if the "coin flip" result is 1 (out of 1, 2, and 3)
V1 = [1, 0, 0]

# So if up-factor=2 and S_0=4, corresponds to strike price=7 for a European call
u = 2
S0 = 4

# assume d = 1/u
S1 = [u * S0, S0, S0 / u]

delta_S1 = [i - S0 for i in S1]


###Fixed
fixed_p=[1/6,1/6,2/3]
fixed_xi=cov(V1,delta_S1,fixed_p)/var(delta_S1,fixed_p)
fixed_V0=expected(V1,1,fixed_p)-(fixed_xi*expected(delta_S1,1,fixed_p))

fixed_L1=[]
for i in range(len(V1)):
    fixed_L1.append(V1[i]-fixed_V0-(fixed_xi*delta_S1[i]))
fixed_risk=var(fixed_L1,fixed_p)+(expected(fixed_L1,1,fixed_p)**2)
###


less_V0=[]
eq_V0=[]
more_V0=[]

best_risk=fixed_risk
best_p=[]
best_risk_v0=0

for p1 in range(1, 1000):
    for p2 in range(1, 1000 - p1):
        p3 = 1000 - p1 - p2
        p = [p1/1000, p2/1000, p3/1000]

        # sequential regression formula
        xi_1= cov(V1, delta_S1, p) / var(delta_S1, p)
        fair_V0 = expected(V1,1,p) - (xi_1 * expected(delta_S1,1,p))
        
        # compute L1 from follmer schweizer decomposition
        L1=[]
        for j in range(len(V1)):
            L1.append(V1[j]-fair_V0-(xi_1*delta_S1[j]))
        risk=var(L1,p)+(expected(L1,1,p)**2) #E((L_1)^2)
        
        ##Make Changes
        if fair_V0<fixed_V0:
            less_V0.append([fair_V0,risk,p])
            if fixed_risk-risk>(fixed_risk-best_risk):
                best_risk=risk
                best_p=p
                best_risk_v0=fair_V0
        elif fair_V0>fixed_V0:
            more_V0.append([fair_V0,risk,p])
            if fixed_risk-risk>(fixed_risk-best_risk):
                best_risk=risk
                best_p=p
                best_risk_v0=fair_V0
        else:
            eq_V0.append([fair_V0,risk,p])
            if fixed_risk-risk>(fixed_risk-best_risk):
                best_risk=risk
                best_p=p
                best_risk_v0=fair_V0

           
###Results

###Generally seems like leads to higher risk when we have a lesser V0
                """
print("Less:")
for each in less_V0:
    print("Probabilities:", each[2], "Price Difference", each[0]-fixed_V0, "Risk Difference",each[1]-fixed_risk)

###Notice that Equal Has None Here Since Not High Enough Estimation of Fixed_P (only to thousandth Place)
print("Equal:")
for each in eq_V0:
    print("Probabilities:", each[2], "Price Difference", each[0]-fixed_V0, "Risk Difference",each[1]-fixed_risk)

###Generally seems like leads to lower risk when we have a greater V0
print("More:")
for each in more_V0:
    print("Probabilities:", each[2], "Price Difference", each[0]-fixed_V0, "Risk Difference",each[1]-fixed_risk)
"""


###Seems like Less Risk When Higher Probability of Getting Heads and Lower Probability of Other Two 
###Also Change in Fixed_p Can Change whether the best V_0 is higher or lower priced!
print(best_risk, fixed_risk, best_p, fixed_p)
print(fixed_V0, best_risk_v0, best_risk_v0-fixed_V0)