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
            self._domain = domain
            self._function = function
        self._from_function = from_function

    @property
    def relation(self) -> Iterable[tuple[Any, Any]] | None:
        return self._relation

    def elements(self) -> tuple[Any, Any]:
        if self._from_function:
            for x in self._domain:
                yield (x, self._function(x))
        else:
            if self._relation:
                for pair in self._relation:
                    yield pair

    def __contains__(self, item) -> bool:
        if self._relation is None:
            return False
        return item in self._relation
