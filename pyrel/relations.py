import itertools
from typing import Set


class BinaryRelation:
    def __init__(
        self,
        a_set: Set | None = None,
        b_set: Set | None = None,
        relation: Set | None = None,
    ) -> None:
        self._a_set = a_set
        self._b_set = b_set
        self._relation = relation

    @property
    def relation(self) -> Set | None:
        return self._relation

    def __contains__(self, item) -> bool:
        return item in self.relation


students = {
    "Jason Goodfriend",
    "Deborah Sherman",
}

courses = {"CS518", "CS510"}

cartesian_product = itertools.product(students, courses)

relation = {
    ("Jason Goodfriend", "CS518"),
    ("Deborah Sherman", "CS518"),
    ("Jason Goodfriend", "CS510"),
}

my_relation = BinaryRelation(relation=relation)

for ordered_pair in cartesian_product:
    if ordered_pair in relation:
        print(f"{ordered_pair} in relation")
    else:
        print(f"{ordered_pair} not in relation")
