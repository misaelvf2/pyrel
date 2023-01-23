import itertools
from typing import Any, Callable, Iterator, Set


class BinaryRelation:
    def __init__(
        self,
        relation: Set[tuple[Any, Any]] | Iterator[tuple[Any, Any]] | None = None,
        from_function: bool = False,
        domain: Set[Any] = None,
        function: Callable[[Any], Any] = None,
    ) -> None:
        if from_function:
            if domain is None or function is None:
                raise ValueError
            self._relation = self.from_function(domain=domain, function=function)
        else:
            self._relation = relation

    def from_function(
        self, domain: Set[Any], function: Callable[[Any], Any]
    ) -> Iterator[tuple[Any, Any]]:
        return zip(domain, map(function, domain))

    @property
    def relation(self) -> Set[tuple[Any, Any]] | None:
        if isinstance(self._relation, set):
            return self._relation

    def __iter__(self) -> Iterator[tuple[Any, Any]]:
        if self._relation is not None:
            for elem in self._relation:
                yield elem

    def __contains__(self, item) -> bool:
        # TODO: Rework this so that the entire generator does not get consumed.
        if self._relation is None:
            return False
        if isinstance(self._relation, set):
            return item in self._relation
        pairs = {pair for pair in self._relation}
        return item in pairs


students = {
    "Jason Goodfriend",
    "Deborah Sherman",
}

courses = {"CS518", "CS510"}

cartesian_product = itertools.product(students, courses)

student_course = {
    ("Jason Goodfriend", "CS518"),
    ("Deborah Sherman", "CS518"),
    ("Jason Goodfriend", "CS510"),
}

student_takes_course_relation = BinaryRelation(relation=student_course)


city_state = {
    ("Boulder", "Colorado"),
    ("Bangor", "Maine"),
    ("Ann Arbor", "Michigan"),
    ("Middletown", "New Jersey"),
    ("Cupertino", "California"),
    ("Red Bank", "New Jersey"),
}


city_in_state_relation = BinaryRelation(relation=city_state)

for pair in city_in_state_relation:
    print(pair)

print(("Boulder", "Colorado") in city_in_state_relation)

# square_relation = BinaryRelation(
#     relation=(range(10), map(lambda x: x**2, range(10)))
# )


def pairs(x, f):
    for i in range(x):
        yield (i, f(i))


squares_relation = BinaryRelation(
    from_function=True, domain={i for i in range(10)}, function=lambda x: x**2
)

for pair in squares_relation:
    print(pair)
