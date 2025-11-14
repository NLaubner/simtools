import numpy as np
from scipy.integrate import quad

f1 = lambda x: np.exp(-(x**2))
f2 = lambda x: np.sqrt(x)

val1, err1 = quad(f1, 0, 1)
val2, err2 = quad(f2, 0, 1)

print("I1 (quad) =", val1, "+/-", err1)
print("I2 (quad) =", val2, "+/-", err2)
