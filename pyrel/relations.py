import itertools
from typing import Any, Callable, Generator, Self, Set


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
    def domain(self) -> Set[Any]:
        return self._domain

    @property
    def codomain(self) -> Set[Any]:
        return self._codomain

    @property
    def relation(self) -> Set[tuple[Any, Any]]:
        return self._relation

    def elements(self) -> tuple[Any, Any] | Generator:
        if self._from_function:
            for x in self._domain:
                yield (x, self._function(x))
        else:
            if self._relation:
                for pair in self._relation:
                    yield pair

    def add_pair(self, pair: tuple[Any, Any]) -> None:
        a, b = pair
        if a not in self._domain or b not in self._codomain:
            raise ValueError
        self._relation.add((a, b))

    def remove_pair(self, pair: tuple[Any, Any]) -> None:
        if pair not in self._relation:
            raise KeyError
        self._relation.remove(pair)

    def is_reflexive(self) -> bool:
        for elem in self._domain:
            if (elem, elem) not in self._relation:
                return False
        return True

    def is_symmetric(self) -> bool:
        for a, b in self._relation:
            if (b, a) not in self._relation:
                return False
        return True

    def is_transitive(self) -> bool:
        for a, b in self._relation:
            for c, d in self._relation:
                if b == c:
                    if (a, d) not in self._relation:
                        return False
        return True

    def update(self, other_relation: Self) -> None:
        self._domain |= other_relation.domain
        self._codomain |= other_relation.codomain
        self._relation |= other_relation.relation

    def union(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation |= other_relation.relation
        return self.__class__(relation=result_relation)

    def intersection(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation &= other_relation.relation
        return self.__class__(relation=result_relation)

    def difference(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation -= other_relation.relation
        return self.__class__(relation=result_relation)

    def symmetric_difference(self, other_relation: Self) -> Self:
        result_relation = self.relation
        result_relation ^= other_relation.relation
        return self.__class__(relation=result_relation)

    def compose(self, other_relation: Self) -> Self:
        result_relation = set()
        for a, b in self.relation:
            for c, d in other_relation.relation:
                if b == c:
                    result_relation.add((a, d))
        return self.__class__(relation=result_relation)

    def inverse(self) -> Self:
        result_relation = set()
        for a, b in self.relation:
            result_relation.add((b, a))
        return self.__class__(relation=result_relation)

    def complement(self) -> Self:
        result_relation = set(itertools.product(self._domain, self._codomain))
        result_relation -= self._relation
        return self.__class__(relation=result_relation)

    def isdisjoint(self, other_relation: Self) -> bool:
        return len(self.intersection(other_relation)) == 0

    def issubset(self, other_relation: Self) -> bool:
        # TODO
        return False

    def issuperset(self, other_relation: Self) -> bool:
        # TODO
        return False

    def __contains__(self, item: tuple[Any, Any]) -> bool:
        return item in self._relation

    def __eq__(self, other_relation: object) -> bool:
        if not isinstance(other_relation, self.__class__):
            raise NotImplementedError
        return self.relation == other_relation.relation

    def __repr__(self) -> str:
        return f"BinaryRelation(domain={self._domain}, codomain={self._codomain}, \
            relation={self._relation})"

    def __str__(self) -> str:
        return f"{self._relation}"

    def __len__(self) -> int:
        return len(self._relation)
