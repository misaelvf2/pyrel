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
        relation={(1, 0), (1, 1), (2, 1), (2, 2), (3, 0), (3, 1)},
    )

    assert r1.compose(r2) == expected
