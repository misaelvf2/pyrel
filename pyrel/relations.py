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
