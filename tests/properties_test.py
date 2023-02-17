import numbers

import pytest
from pyrel.relations import BinaryRelation


def test_reflexive():
    reflexive_relation = {
        (1, 1),
        (1, 2),
        (1, 4),
        (2, 1),
        (2, 2),
        (3, 3),
        (4, 1),
        (4, 4),
    }

    irreflexive_relation = {
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 4),
        (4, 1),
        (4, 4),
    }

    r1 = BinaryRelation(relation=reflexive_relation, domain=[1, 2, 3, 4])
    r2 = BinaryRelation(relation=irreflexive_relation, domain=[1, 2, 3, 4])

    assert r1.is_reflexive() is True
    assert r2.is_reflexive() is False


def test_symmetric():
    a_set = [i for i in range(10)]

    r1 = BinaryRelation(
        relation=[(a, b) for a in a_set for b in a_set if a == b or a == -b],
        domain=a_set,
    )
    r2 = BinaryRelation(
        relation=[(a, b) for a in a_set for b in a_set if a <= b], domain=a_set
    )

    assert r1.is_symmetric() is True
    assert r2.is_symmetric() is False


def test_transitive():
    a_set = set(i for i in range(10))

    r1 = BinaryRelation(
        relation={(a, b) for a in a_set for b in a_set if a == b or a == -b},
        domain=a_set,
    )
    r2 = BinaryRelation(
        relation=set((a, b) for a in a_set for b in a_set if a == b + 1), domain=a_set
    )
    r3 = BinaryRelation(
        relation={
            (2, 1),
            (3, 1),
            (3, 2),
            (4, 1),
            (4, 2),
            (4, 3),
        },
        domain={1, 2, 3, 4},
    )
    r4 = BinaryRelation(
        relation={
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 3),
            (3, 4),
            (4, 4),
        },
        domain={1, 2, 3, 4},
    )
    r5 = BinaryRelation(
        relation={
            (3, 4),
        },
        domain={1, 2, 3, 4},
    )

    assert r1.is_transitive() is True
    assert r2.is_transitive() is False
    assert r3.is_transitive() is True
    assert r4.is_transitive() is True
    assert r5.is_transitive() is True


def test_union():
    r1 = BinaryRelation(
        domain={1, 2, 3}, codomain={1, 2, 3, 4}, relation={(1, 1), (2, 2), (3, 3)}
    )

    r2 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 2), (1, 3), (1, 4)},
    )

    expected = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (1, 4)},
    )

    assert r1.union(r2) == expected


def test_intersection():
    r1 = BinaryRelation(
        domain={1, 2, 3}, codomain={1, 2, 3, 4}, relation={(1, 1), (2, 2), (3, 3)}
    )

    r2 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 2), (1, 3), (1, 4)},
    )

    expected = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1)},
    )

    assert r1.intersection(r2) == expected


def test_difference():
    r1 = BinaryRelation(
        domain={1, 2, 3}, codomain={1, 2, 3, 4}, relation={(1, 1), (2, 2), (3, 3)}
    )

    r2 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 2), (1, 3), (1, 4)},
    )

    expected = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(2, 2), (3, 3)},
    )

    assert r1.difference(r2) == expected


def test_symmetric_difference():
    r1 = BinaryRelation(
        domain={1, 2, 3}, codomain={1, 2, 3, 4}, relation={(1, 1), (2, 2), (3, 3)}
    )

    r2 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 2), (1, 3), (1, 4)},
    )

    expected = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(2, 2), (3, 3), (1, 2), (1, 3), (1, 4)},
    )

    assert r1.symmetric_difference(r2) == expected


def test_compose():
    r1 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 4), (2, 3), (3, 1), (3, 4)},
    )

    r2 = BinaryRelation(
        domain={1, 2, 3, 4},
        codomain={0, 1, 2},
        relation={(1, 0), (2, 0), (3, 1), (3, 2), (4, 1)},
    )

    expected = BinaryRelation(
        domain=r1.domain.copy(),
        codomain=r2.codomain.copy(),
        relation={(1, 0), (1, 1), (2, 1), (2, 2), (3, 0), (3, 1)},
    )

    assert r1.compose(r2) == expected


def test_inverse():
    r1 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3, 4},
        relation={(1, 1), (1, 4), (2, 3), (3, 1), (3, 4)},
    )

    expected = BinaryRelation(
        domain=r1.domain.copy(),
        codomain=r1.codomain.copy(),
        relation={(1, 1), (4, 1), (3, 2), (1, 3), (4, 3)},
    )

    assert r1.inverse() == expected


def test_complement():
    r1 = BinaryRelation(
        domain={1, 2, 3},
        codomain={1, 2, 3},
        relation={(1, 1), (2, 3), (3, 1)},
    )

    expected = BinaryRelation(
        domain=r1.domain.copy(),
        codomain=r1.codomain.copy(),
        relation={(1, 2), (1, 3), (2, 1), (2, 2), (3, 2), (3, 3)},
    )

    assert r1.complement() == expected


def test_add_pair():
    r = BinaryRelation(domain={"Misael", "Ashley"}, codomain={"Valentin", "Villanueva"})
    r.add_pair(("Misael", "Valentin"))
    r.add_pair(("Ashley", "Villanueva"))

    with pytest.raises(ValueError):
        r.add_pair(("Valentin", "Misael"))

    assert ("Misael", "Valentin") in r
    assert ("Ashley", "Villanueva") in r


def test_remove_pair():
    r = BinaryRelation(domain={"Misael", "Ashley"}, codomain={"Valentin", "Villanueva"})
    r.add_pair(("Misael", "Valentin"))
    r.add_pair(("Ashley", "Villanueva"))

    with pytest.raises(KeyError):
        r.remove_pair(("Misael", "Villanueva"))

    r.remove_pair(("Ashley", "Villanueva"))

    assert ("Ashley", "Villanueva") not in r


def test_length():
    r = BinaryRelation(domain={1, 2, 3}, codomain={1, 2, 3})
    r.add_pair((1, 2))
    r.add_pair((1, 3))
    r.add_pair((1, 3))
    r.add_pair((1, 2))

    assert len(r) == 2


def test_update():
    pass


def test_isdisjoint():
    pass


def test_real_domain():
    r = BinaryRelation(domain=numbers.Real, codomain={1, 2, 3})

    with pytest.raises(ValueError):
        r.add_pair((5j, 1))

    r.add_pair((-0.5, 3))

    assert (-0.5, 3) in r


def test_real_relation():
    r = BinaryRelation(domain=numbers.Real, codomain=numbers.Real)

    with pytest.raises(ValueError):
        r.add_pair((10, 1j))

    with pytest.raises(ValueError):
        r.add_pair((5j, 0))

    r.add_pair((-10, 0.76))

    assert (-10, 0.76) in r


def test_from_function():
    r = BinaryRelation.from_function(domain={1, 2, 3, 4}, func=lambda x: x**2)

    assert (4, 16) in r
    assert (5, 25) not in r
