import itertools
from typing import Any, Callable, Self, Set


class BinaryRelation:
    def __init__(
        self,
        domain: Set[Any] | None = None,
        codomain: Set[Any] | None = None,
        relation: Set[tuple[Any, Any]] | None = None,
        from_function: bool = False,
        function: Callable[[Any], Any] | None = None,
    ) -> None:
        if domain is None:
            self._domain = set()
        else:
            self._domain = domain
        if codomain is None:
            self._codomain = set()
        else:
            self._codomain = codomain
        if relation is None:
            self._relation = set()
        else:
            self._relation = relation
        if from_function:
            if domain is None or function is None:
                raise ValueError
            self._function = function
        self._from_function = from_function

    @property
    def relation(self) -> Set[tuple[Any, Any]]:
        return self._relation

    def elements(self) -> tuple[Any, Any]:
        if self._from_function:
            for x in self._domain:
                yield (x, self._function(x))
        else:
            if self._relation:
                for pair in self._relation:
                    yield pair

    def add_pair(self, pair: tuple[Any, Any]) -> None:
        a, b = pair
        self._domain.add(a)
        self._codomain.add(b)
        self._relation.add((a, b))

    def is_reflexive(self) -> bool:
        if self._domain:
            for elem in self._domain:
                if (elem, elem) not in self._relation:
                    return False
        return True

    def is_symmetric(self) -> bool:
        if self._domain:
            for a, b in self._relation:
                if (b, a) not in self._relation:
                    return False
        return True

    def is_transitive(self) -> bool:
        if self._relation:
            for a, b in self._relation:
                for c, d in self._relation:
                    if b == c:
                        if (a, d) not in self._relation:
                            return False
        return True

    def union(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation |= other_relation.relation
        return BinaryRelation(relation=result_relation)

    def intersection(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation &= other_relation.relation
        return BinaryRelation(relation=result_relation)

    def difference(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation -= other_relation.relation
        return BinaryRelation(relation=result_relation)

    def symmetric_difference(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation ^= other_relation.relation
        return BinaryRelation(relation=result_relation)

    def compose(self, other_relation: Self) -> Self:
        result_relation = set()
        for a, b in self.relation:
            for c, d in other_relation.relation:
                if b == c:
                    result_relation.add((a, d))
        return BinaryRelation(relation=result_relation)

    def inverse(self) -> Self:
        result_relation = set()
        for a, b in self.relation:
            result_relation.add((b, a))
        return BinaryRelation(relation=result_relation)

    def complement(self) -> Self:
        result_relation = set(itertools.product(self._domain, self._codomain))
        result_relation -= self._relation
        return BinaryRelation(relation=result_relation)

    def __contains__(self, item: tuple[Any, Any]) -> bool:
        return item in self._relation

    def __eq__(self, other_relation: Self) -> bool:
        return self.relation == other_relation.relation

    def __repr__(self):
        return f"BinaryRelation(domain={self._domain}, codomain={self._codomain}, relation={self._relation})"

    def __str__(self):
        return f"{self._relation}"
