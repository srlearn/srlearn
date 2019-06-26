"""
==========================
Plotting a Matplotlib Plot
==========================

An example using :class:`boostsrl.rdn.RDN`, and the Toy-Cancer
data from :class:`boostsrl.example_data`
"""

from boostsrl.rdn import RDN
from boostsrl import Background
from boostsrl import example_data

import numpy as np
from matplotlib import pyplot as plt

# Toy-Cancer set from boostsrl.example_data
bk = Background(
    modes=example_data.train.modes
)
dn = RDN(background=bk, target="cancer")
dn.fit(example_data.train)

for n_trees in np.arange(1, 11):

    # Set the number of trees.
    dn.set_params(n_estimators=n_trees)
    print(dn.predict(example_data.test))

X = np.arange(50, dtype=np.float).reshape(-1, 1)
X /= 50

plt.plot(X.flatten(), label="Original")
plt.title("Example plot maybe")
plt.show()
