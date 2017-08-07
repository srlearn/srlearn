# boostsrl

Python module for performing training/testing with BoostSRL.

---

### Usage

```python
from boostsrl import boostsrl

...
model = boostsrl.train('cancer', train_pos, train_neg, train_facts)

...
results = boostsrl.test('cancer', test_pos, test_neg, test_facts)

```
