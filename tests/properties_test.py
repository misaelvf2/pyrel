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
    a_set = [i for i in range(10)]

    r1 = BinaryRelation(
        relation=[(a, b) for a in a_set for b in a_set if a == b or a == -b],
        domain=a_set,
    )
    r2 = BinaryRelation(
        relation=[(a, b) for a in a_set for b in a_set if a == b + 1], domain=a_set
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
        domain=[1, 2, 3, 4],
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
        domain=[1, 2, 3, 4],
    )
    r5 = BinaryRelation(
        relation={
            (3, 4),
        },
        domain=[1, 2, 3, 4],
    )

    assert r1.is_transitive() is True
    assert r2.is_transitive() is False
    assert r3.is_transitive() is True
    assert r4.is_transitive() is True
    assert r5.is_transitive() is True


def test_union():
    pass


def test_intersection():
    pass


def test_difference():
    pass


def test_symmetric_difference():
    pass


def test_compose():
    pass
