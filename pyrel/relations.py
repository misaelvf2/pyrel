import itertools
from inspect import isclass
from typing import Any, Callable, Generator, Self, Set, Type


class BinaryRelation:
    def __init__(
        self,
        domain: Set[Any] | Type | None = None,
        codomain: Set[Any] | Type | None = None,
        relation: Set[tuple[Any, Any]] | None = None,
        from_function: bool = False,
        function: Callable[[Any], Any] | None = None,
    ) -> None:
        if domain is None:
            self._domain: Set[Any] | Type = set()
        else:
            self._domain = domain
        if codomain is None:
            self._codomain: Set[Any] | Type = set()
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
    def domain(self) -> Set[Any] | Type:
        return self._domain

    @property
    def codomain(self) -> Set[Any] | Type:
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
        # Case 1: Domain is a type; codomain is not
        if isclass(self._domain) and not isclass(self._codomain):
            if not isinstance(a, self._domain) or b not in self._codomain:
                raise ValueError
        # Case 2: Domain and codomain are types
        elif isclass(self._domain) and isclass(self._codomain):
            if not isinstance(a, self._domain) or not isinstance(b, self._codomain):
                raise ValueError
        # Case 3: Codomain is a type; domain is not
        elif not isclass(self._domain) and isclass(self._codomain):
            if a not in self._domain or not isinstance(b, self._codomain):
                raise ValueError
        # Case 4: Neither domain nor codomain are types
        else:
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

    def update(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        if isinstance(other_relation.domain, set):
            self._domain.update(other_relation.domain)
        if isinstance(other_relation.codomain, set):
            self._codomain.update(other_relation.codomain)
        self._relation.update(other_relation.relation)
        return self

    def union(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        result_domain = self._merge_domains(other_relation)
        result_codomain = self._merge_codomains(other_relation)
        result_relation = self.relation.copy()
        result_relation.update(other_relation.relation)
        return self.__class__(
            domain=result_domain, codomain=result_codomain, relation=result_relation
        )

    def intersection(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        result_domain = self._merge_domains(other_relation)
        result_codomain = self._merge_codomains(other_relation)
        result_relation = self.relation
        result_relation &= other_relation.relation
        return self.__class__(
            domain=result_domain, codomain=result_codomain, relation=result_relation
        )

    def difference(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        result_domain = self._merge_domains(other_relation)
        result_codomain = self._merge_codomains(other_relation)
        result_relation = self.relation
        result_relation -= other_relation.relation
        return self.__class__(
            domain=result_domain, codomain=result_codomain, relation=result_relation
        )

    def symmetric_difference(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        result_domain = self._merge_domains(other_relation)
        result_codomain = self._merge_codomains(other_relation)
        result_relation = self.relation
        result_relation ^= other_relation.relation
        return self.__class__(
            domain=result_domain, codomain=result_codomain, relation=result_relation
        )

    def compose(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        if self.codomain != other_relation.domain:
            raise ValueError(
                "First relation's codomain must be equal to the second relation's \
                    domain"
            )
        result_relation = set()
        for a, b in self.relation:
            for c, d in other_relation.relation:
                if b == c:
                    result_relation.add((a, d))
        return self.__class__(
            domain=self.domain.copy(),
            codomain=other_relation.codomain.copy(),
            relation=result_relation,
        )

    def inverse(self) -> Self:
        result_relation = set()
        for a, b in self.relation:
            result_relation.add((b, a))
        return self.__class__(
            domain=self.domain.copy(),
            codomain=self.codomain.copy(),
            relation=result_relation,
        )

    def complement(self) -> Self:
        if isinstance(self.domain, set) and isinstance(self.codomain, set):
            result_relation = set(itertools.product(self.domain, self.codomain))
        else:
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        result_relation -= self._relation
        return self.__class__(
            domain=self.domain.copy(),
            codomain=self.codomain.copy(),
            relation=result_relation,
        )

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

    def _unimplemented_operation(self, other_relation: Self | None = None) -> bool:
        if isclass(self.domain) or isclass(self.codomain):
            return True
        if other_relation is not None:
            if isclass(other_relation.domain) or isclass(other_relation.codomain):
                return True
        return False

    def _merge_domains(self, other_relation) -> set:
        result_domain = self.domain.copy()
        if isinstance(other_relation.domain, set):
            result_domain.update(other_relation.domain)
        return result_domain

    def _merge_codomains(self, other_relation) -> set:
        result_codomain = self.codomain.copy()
        if isinstance(other_relation.codomain, set):
            result_codomain.update(other_relation.codomain)
        return result_codomain
