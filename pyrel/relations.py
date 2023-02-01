from typing import Any, Callable, Iterable


class BinaryRelation:
    def __init__(
        self,
        relation: Iterable[tuple[Any, Any]] | None = None,
        from_function: bool = False,
        domain: Iterable[Any] | None = None,
        function: Callable[[Any], Any] | None = None,
    ) -> None:

        self._relation = relation
        if from_function:
            if domain is None or function is None:
                raise ValueError
            self._function = function
        self._domain = domain
        self._from_function = from_function

    @property
    def relation(self) -> Iterable[tuple[Any, Any]] | None:
        return self._relation

    def elements(self) -> tuple[Any, Any]:
        if self._from_function and self._domain is not None:
            for x in self._domain:
                yield (x, self._function(x))
        else:
            if self._relation:
                for pair in self._relation:
                    yield pair

    def is_reflexive(self):
        if self._domain is not None and self._relation is not None:
            for elem in self._domain:
                if (elem, elem) not in self._relation:
                    return False
        return True

    def is_symmetric(self):
        return False

    def is_transitive(self):
        return False

    def __contains__(self, item: tuple[Any, Any]) -> bool:
        if self._relation is None:
            return False
        return item in self._relation
