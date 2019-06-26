"""
========================
Using the Database class
========================

An example using :class:`boostsrl.Database`
"""

from boostsrl.rdn import RDN
from boostsrl import Background
from boostsrl import example_data

import numpy as np
from matplotlib import pyplot as plt

for n_trees in np.arange(1, 11):
    pass

# Toy-Cancer set from boostsrl.example_data
bk = Background(
    modes=example_data.train.modes
)
dn = RDN(background=bk, target="cancer")

X = np.arange(50, dtype=np.float).reshape(-1, 1)
X /= 50

plt.plot(X.flatten(), label="Original")
plt.title("Example plot maybe")
plt.show()
