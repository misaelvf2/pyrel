import itertools
import numbers

from pyrel.relations import BinaryRelation


def students_test():
    students = {
        "Jason Goodfriend",
        "Deborah Sherman",
    }

    courses = {"CS518", "CS510"}

    cartesian_product = itertools.product(students, courses)

    student_course = {
        ("Jason Goodfriend", "CS518"),
        ("Deborah Sherman", "CS518"),
        ("Jason Goodfriend", "CS510"),
    }

    student_takes_course_relation = BinaryRelation(relation=student_course)

    for elem in cartesian_product:
        if elem in student_takes_course_relation:
            print(f"{elem} in relation")
        else:
            print(f"{elem} not in relation")


def cities_test():
    city_state = {
        ("Boulder", "Colorado"),
        ("Bangor", "Maine"),
        ("Ann Arbor", "Michigan"),
        ("Middletown", "New Jersey"),
        ("Cupertino", "California"),
        ("Red Bank", "New Jersey"),
    }

    city_in_state_relation = BinaryRelation(relation=city_state)

    for pair in city_in_state_relation.elements():
        print(pair)

    print(("Boulder", "Colorado") in city_in_state_relation)


def squares_relation_test():
    squares_relation = BinaryRelation(
        from_function=True,
        domain=[x for x in range(10)],
        function=lambda x: x**2,
    )

    for elem in squares_relation.elements():
        print(elem)


def a_divides_b_test():
    a_set = (1, 2, 3, 4)

    relation_set = ((a, b) for a in a_set for b in a_set if b % a == 0)

    relation = BinaryRelation(relation=relation_set)

    for elem in relation.elements():
        print(elem)


def example_5():
    a_set = [i for i in range(10)]

    relations = [
        (
            "r1",
            BinaryRelation(relation=[(a, b) for a in a_set for b in a_set if a <= b]),
        ),
        (
            "r2",
            BinaryRelation(relation=[(a, b) for a in a_set for b in a_set if a > b]),
        ),
        (
            "r3",
            BinaryRelation(
                relation=[(a, b) for a in a_set for b in a_set if a == b or a == -b]
            ),
        ),
        (
            "r4",
            BinaryRelation(relation=[(a, b) for a in a_set for b in a_set if a == b]),
        ),
        (
            "r5",
            BinaryRelation(
                relation=[(a, b) for a in a_set for b in a_set if a == b + 1]
            ),
        ),
        (
            "r6",
            BinaryRelation(
                relation=[(a, b) for a in a_set for b in a_set if a + b <= 3]
            ),
        ),
    ]

    pairs = [(1, 1), (1, 2), (2, 1), (1, -1), (2, 2)]

    for pair in pairs:
        for relation in relations:
            if pair in relation[1]:
                print(f"{pair} in {relation[0]}")


if __name__ == "__main__":
    domain = numbers.Real
    codomain = numbers.Real
    relation = BinaryRelation(
        domain=domain,
        codomain=codomain,
    )

    relation.add_pair((5, 7))
    print(relation)
