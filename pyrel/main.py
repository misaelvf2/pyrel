import itertools

from .relations import BinaryRelation

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


city_state = {
    ("Boulder", "Colorado"),
    ("Bangor", "Maine"),
    ("Ann Arbor", "Michigan"),
    ("Middletown", "New Jersey"),
    ("Cupertino", "California"),
    ("Red Bank", "New Jersey"),
}


city_in_state_relation = BinaryRelation(relation=city_state)

for pair in city_in_state_relation:
    print(pair)

print(("Boulder", "Colorado") in city_in_state_relation)


def pairs(x, f):
    for i in range(x):
        yield (i, f(i))


squares_relation = BinaryRelation(
    from_function=True, domain={i for i in range(10)}, function=lambda x: x**2
)

for pair in squares_relation:
    print(pair)
