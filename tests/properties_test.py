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
        relation=[(a, b) for a in a_set for b in a_set if a == b or a == -b]
    )
    r2 = BinaryRelation(relation=[(a, b) for a in a_set for b in a_set if a <= b])

    assert r1.is_symmetric() is True
    assert r2.is_symmetric() is False


def test_transitive():
    a_set = [i for i in range(10)]

    r1 = BinaryRelation(
        relation=[(a, b) for a in a_set for b in a_set if a == b or a == -b]
    )
    r2 = BinaryRelation(relation=[(a, b) for a in a_set for b in a_set if a == b + 1])

    assert r1.is_transitive() is True
    assert r2.is_transitive() is False
