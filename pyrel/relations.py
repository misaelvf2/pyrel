from typing import Any, Callable, Set


class BinaryRelation:
    def __init__(
        self,
        domain: Set[Any] | None = None,
        codomain: Set[Any] | None = None,
        relation: Set[tuple[Any, Any]] | None = None,
        from_function: bool = False,
        function: Callable[[Any], Any] | None = None,
    ) -> None:

        self._domain = domain
        self._codomain = codomain
        self._relation = relation
        if from_function:
            if domain is None or function is None:
                raise ValueError
            self._function = function
        self._from_function = from_function

    @property
    def relation(self) -> Set[tuple[Any, Any]] | None:
        return self._relation

    def elements(self) -> tuple[Any, Any]:
        if self._from_function and self._domain is not None:
            for x in self._domain:
                yield (x, self._function(x))
        else:
            if self._relation:
                for pair in self._relation:
                    yield pair

    def is_reflexive(self) -> bool:
        if self._domain is not None and self._relation is not None:
            for elem in self._domain:
                if (elem, elem) not in self._relation:
                    return False
        return True

    def is_symmetric(self) -> bool:
        if self._domain is not None and self._relation is not None:
            for a, b in self._relation:
                if (b, a) not in self._relation:
                    return False
        return True

    def is_transitive(self) -> bool:
        if self._domain is not None and self._relation is not None:
            for a, b in self._relation:
                for c, d in self._relation:
                    if b == c:
                        if (a, d) not in self._relation:
                            return False
        return True

    def union(self, other_relation: BinaryRelation) -> BinaryRelation:
        result_relation = self.relation if self.relation is not None else set()
        result_relation |= (
            other_relation.relation if other_relation.relation is not None else set()
        )
        return BinaryRelation(relation=result_relation)

    def intersection(self, other_relation: BinaryRelation) -> BinaryRelation:
        pass

    def difference(self, other_relation: BinaryRelation) -> BinaryRelation:
        pass

    def symmetric_difference(self, other_relation: BinaryRelation) -> BinaryRelation:
        pass

    def compose(self, other_relation: BinaryRelation) -> BinaryRelation:
        pass

    def __contains__(self, item: tuple[Any, Any]) -> bool:
        if self._relation is None:
            return False
        return item in self._relation

    def __eq__(self, other_relation: BinaryRelation) -> bool:
        if self.relation is None or other_relation.relation is None:
            return False
        return self.relation == self.other_relation.relation
