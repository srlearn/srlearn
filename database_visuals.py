# Copyright © 2021 Alexander L. Hayes

"""Visualizing data sets."""

from srlearn.datasets import load_toy_cancer
from srlearn.datasets import load_toy_father
from srlearn.database import Database


tc = load_toy_cancer()
fa = load_toy_father()


class Word:
    """A relation has a name, and operates over a set of objects."""
    def __init__(self, head, *args):
        self.head = head
        self.args = args

    @property
    def is_attribute(self):
        """An attribute is a relation with one argument."""
        return len(self.args) == 1

    @property
    def is_relation(self):
        """A relation is a relation with two arguments."""
        # TODO(hayesall): Bad grammar, check what Plotkin called them.
        return len(self.args) == 2

    def to_graphviz(self):
        """Dump the relation to a graphviz edge."""
        if self.is_relation:
            return f"\t{self.args[1]} -> {self.args[0]} [label={self.head}]\n"
        return f"\t{self.args[0]}_{self.head} -> {self.args[0]} [dir=none]\n"

    @staticmethod
    def from_string(string):
        """Return an instance after passing a string like: `friends(alice,fred).`"""
        # TODO(hayesall): I hate doing this. It feels gross and looks terrible.
        _head = string.split("(")[0]
        _obj = string.replace(" ", "").split("(")[1].split(")")[0].split(",")
        return Word(_head, *_obj)

    def __str__(self):
        return self.head + "(" + ",".join(self.args) + ")."

    def __repr__(self):
        return self.__str__()


def collect_objects(db):

    # TODO(hayesall): Currently to draw the entities, it requires making a pass
    #   over the data set to avoid drawing them multiple times.
    #   It's an easy fix for attributes, but we'd have to keep a set of
    #   "already-seen objects" around either way for entities.

    objects = set()

    _gv = ""

    for entry in db.pos + db.facts:
        rel = Word.from_string(entry)

        objects.update(rel.args)

        _gv += rel.to_graphviz()

        if rel.is_attribute:
            _gv += f"\t{rel.args[0]}_{rel.head} [shape=oval, label={rel.head}]\n"

    # TODO(hayesall): I need a better way to visualize negative information.
    #   notted? "¬"

    for _ob in objects:
        _gv += f"\t{_ob} [shape=box]\n"

    return _gv


if __name__ == "__main__":

    webkb = Database.from_files(
        pos="datasets/webkb/train1/train1_pos.txt",
        neg="datasets/webkb/train1/train1_neg.txt",
        facts="datasets/webkb/train1/train1_facts.txt",
        lazy_load=False,
    )

    obj = collect_objects(webkb)

    print("digraph G {")
    print("\tlayout=neato\n")
    print(obj)
    print("}")
