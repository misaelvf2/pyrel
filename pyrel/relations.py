import itertools
from inspect import isclass
from typing import Any, Callable, Generator, Self, Set, Type


class BinaryRelation:
    def __init__(
        self,
        domain: Set[Any] | Type | None = None,
        codomain: Set[Any] | Type | None = None,
        relation: Set[tuple[Any, Any]] | None = None,
        from_func: bool = False,
        func: Callable[[Any], Any] | None = None,
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
        if from_func:
            if domain is None or func is None:
                raise ValueError
            self._func = func
        self._from_func = from_func

    @classmethod
    def from_function(
        cls,
        domain: Set[Any],
        func: Callable[[Any], Any],
    ) -> Self:
        if isclass(domain):
            raise ValueError(
                "Can't use class-based domains when defining relation from function"
            )
        return cls(domain=domain, from_func=True, func=func)

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
        if self._from_func:
            for x in self.domain:
                yield (x, self._func(x))
        else:
            if self.relation:
                for pair in self.relation:
                    yield pair

    def add_pair(self, pair: tuple[Any, Any]) -> None:
        a, b = pair
        # Case 1: Domain is a type; codomain is not
        if isclass(self.domain) and not isclass(self.codomain):
            if not isinstance(a, self.domain):
                raise ValueError(f"{a} is not domain")
            if b not in self.codomain:
                raise ValueError(f"{b} is not in codomain")
        # Case 2: Domain and codomain are types
        elif isclass(self.domain) and isclass(self.codomain):
            if not isinstance(a, self.domain):
                raise ValueError(f"{a} not in domain")
            if not isinstance(b, self.codomain):
                raise ValueError(f"{b} not in codomain")
        # Case 3: Codomain is a type; domain is not
        elif not isclass(self.domain) and isclass(self.codomain):
            if a not in self.domain:
                raise ValueError(f"{a} not in domain")
            if not isinstance(b, self.codomain):
                raise ValueError(f"{b} not in codomain")
        # Case 4: Neither domain nor codomain are types
        else:
            if a not in self.domain:
                raise ValueError(f"{a} not in domain")
            if b not in self.codomain:
                raise ValueError(f"{b} not in codomain")
        self.relation.add((a, b))

    def remove_pair(self, pair: tuple[Any, Any]) -> None:
        if pair not in self.relation:
            raise KeyError
        self.relation.remove(pair)

    def is_reflexive(self) -> bool:
        for elem in self.domain:
            if (elem, elem) not in self.relation:
                return False
        return True

    def is_symmetric(self) -> bool:
        for a, b in self.relation:
            if (b, a) not in self.relation:
                return False
        return True

    def is_transitive(self) -> bool:
        for a, b in self.relation:
            for c, d in self.relation:
                if b == c:
                    if (a, d) not in self.relation:
                        return False
        return True

    def is_irreflexive(self) -> bool:
        raise NotImplementedError

    def is_antisymmetric(self) -> bool:
        raise NotImplementedError

    def is_asymmetric(self) -> bool:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def is_strongly_connected(self) -> bool:
        raise NotImplementedError

    def is_well_founded(self) -> bool:
        raise NotImplementedError

    def is_injective(self) -> bool:
        raise NotImplementedError

    def is_functional(self) -> bool:
        raise NotImplementedError

    def is_serial(self) -> bool:
        raise NotImplementedError

    def is_surjective(self) -> bool:
        raise NotImplementedError

    def is_equivalence_relation(self) -> bool:
        raise NotImplementedError

    def is_partial_order(self) -> bool:
        raise NotImplementedError

    def is_strict_partial_order(self) -> bool:
        raise NotImplementedError

    def is_total_order(self) -> bool:
        raise NotImplementedError

    def is_strict_total_order(self) -> bool:
        raise NotImplementedError

    def is_one_to_one(self) -> bool:
        raise NotImplementedError

    def is_one_to_many(self) -> bool:
        raise NotImplementedError

    def is_many_to_one(self) -> bool:
        raise NotImplementedError

    def is_many_to_many(self) -> bool:
        raise NotImplementedError

    def is_function(self) -> bool:
        raise NotImplementedError

    def is_injection(self) -> bool:
        raise NotImplementedError

    def is_surjection(self) -> bool:
        raise NotImplementedError

    def is_bijection(self) -> bool:
        raise NotImplementedError

    def update(self, other_relation: Self) -> Self:
        if self._unimplemented_operation(other_relation):
            raise ValueError(
                "Operation not implemented for class-based domains and codomains"
            )
        if isinstance(other_relation.domain, set):
            self.domain.update(other_relation.domain)
        if isinstance(other_relation.codomain, set):
            self.codomain.update(other_relation.codomain)
        self.relation.update(other_relation.relation)
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

    def converse(self) -> Self:
        raise NotImplementedError

    def restriction(self) -> Self:
        raise NotImplementedError

    def isdisjoint(self, other_relation: Self) -> bool:
        return len(self.intersection(other_relation)) == 0

    def issubset(self, other_relation: Self) -> bool:
        # TODO
        return False

    def issuperset(self, other_relation: Self) -> bool:
        # TODO
        return False

    def __contains__(self, item: tuple[Any, Any]) -> bool:
        if self._from_func:
            a, b = item
            if a not in self.domain:
                return False
            return b == self._func(a)
        return item in self._relation

    def __eq__(self, other_relation: object) -> bool:
        if not isinstance(other_relation, self.__class__):
            raise NotImplementedError
        return self.relation == other_relation.relation

    def __repr__(self) -> str:
        return f"BinaryRelation(domain={self.domain}, codomain={self.codomain}, \
            relation={self.relation})"

    def __str__(self) -> str:
        return f"{self.relation}"

    def __len__(self) -> int:
        return len(self.relation)

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
