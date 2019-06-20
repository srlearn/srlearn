"""
Plotting a Matplotlib Plot
==========================

An example using :class:`boostsrl.database.database`
"""

from boostsrl.database import database

import numpy as np
from matplotlib import pyplot as plt

db = database()
db.target = "cancer"

X = np.arange(50, dtype=np.float).reshape(-1, 1)
X /= 50

plt.plot(X.flatten(), label="Original")
plt.title("Example plot maybe")
plt.show()
