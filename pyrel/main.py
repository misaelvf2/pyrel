import itertools

from relations import BinaryRelation


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


if __name__ == "__main__":
    students_test()
    cities_test()
    squares_relation_test()
