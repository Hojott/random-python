import os
import sqlite3

db_path = "courses.db"

# Delete db for debugging
if os.path.exists(db_path):
    os.remove(db_path)

db = sqlite3.connect(db_path)
cur = db.cursor()

def create_tables() -> None:
    """ Create neccessary tables """

    cur.execute("""--sql
        CREATE TABLE teachers (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """)
    cur.execute("""--sql
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """)
    cur.execute("""--sql
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            credits INTEGER
        );
    """)
    cur.execute("""--sql
        CREATE TABLE course_teachers (
            id INTEGER PRIMARY KEY,
            course_id INTEGER REFERENCES courses(id),
            teacher_id INTEGER REFERENCES teachers(id)
        );
    """)
    cur.execute("""--sql
        CREATE TABLE accomplishments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            course_id INTEGER REFERENCES courses(id),
            date DATE,
            grade INTEGER
        );
    """)
    cur.execute("""--sql
        CREATE TABLE groups (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """)
    cur.execute("""--sql
        CREATE TABLE group_students (
            id INTEGER PRIMARY KEY,
            group_id INTEGER REFERENCES groups(id),
            student_id INTEGER REFERENCES students(id)
        );
    """)
    cur.execute("""--sql
        CREATE TABLE group_teachers (
            id INTEGER PRIMARY KEY,
            group_id INTEGER REFERENCES groups (id),
            teacher_id INTEGER REFERENCES teachers(id)
        );
    """)

def create_teacher(name: str) -> int:
    """ Add teacher """

    cur.execute("""--sql
        INSERT INTO teachers (name)
        VALUES (?);
    """, (name,))

    db.commit()

    res = cur.execute("""--sql
        SELECT MAX(id) FROM teachers
        WHERE name = ?;
    """, (name,))

    return int(res.fetchone()[0])

def create_course(name: str, credits: int, teacher_ids: list[int]) -> int:
    """ Add course """

    cur.execute("""--sql
        INSERT INTO courses (name, credits)
        VALUES (?, ?)
    """, (name, credits))

    res = cur.execute("""--sql
        SELECT MAX(id) FROM courses
        WHERE name = ?;
    """, (name,))
    
    course_id = res.fetchone()[0]
    
    for teacher_id in teacher_ids:
        cur.execute("""--sql
            INSERT INTO course_teachers (course_id, teacher_id)
            VALUES (?, ?)
        """, (course_id, teacher_id))
    
    db.commit()

    return int(course_id)

def create_student(name: str) -> int:
    """ Add student """

    cur.execute("""--sql
        INSERT INTO students (name)
        VALUES (?);
    """, (name,))

    db.commit()

    res = cur.execute("""--sql
        SELECT MAX(id) FROM students
        WHERE name = ?;
    """, (name,))

    return int(res.fetchone()[0])

def add_credits(student_id: int, course_id: int, date: str, grade: int) -> int:
    """ Add credits """

    cur.execute("""--sql
        INSERT INTO accomplishments (student_id, course_id, date, grade)
        VALUES (?, ?, ?, ?);
    """, (student_id, course_id, date, grade))

    db.commit()

    res = cur.execute("""--sql
        SELECT MAX(id) FROM accomplishments
        WHERE student_id == ?;
    """, (student_id,))

    return res.fetchone()[0]

def create_group(name: str, teacher_ids: list[int], student_ids: list[int]) -> int:
    """ Add group """
    cur.execute("""--sql
        INSERT INTO groups (name)
        VALUES (?)
    """, (name,))

    res = cur.execute("""--sql
        SELECT MAX(id) FROM groups
        WHERE name = ?;
    """, (name,))
    
    group_id = res.fetchone()[0]
    
    for teacher_id in teacher_ids:
        cur.execute("""--sql
            INSERT INTO group_teachers (group_id, teacher_id)
            VALUES (?, ?)
        """, (group_id, teacher_id))

    for student_id in student_ids:
        cur.execute("""--sql
            INSERT INTO group_students (group_id, student_id)
            VALUES (?, ?)
        """, (group_id, student_id))

    db.commit()

    return group_id

#==== FETH DATA ====#


def courses_by_teacher(name: str) -> list[str]:
    """ Fetch courses """

    res = cur.execute("""--sql
        SELECT C.name FROM
        course_teachers CT JOIN courses C ON C.id = CT.course_id
                           JOIN teachers T ON T.id = CT.teacher_id
        WHERE T.name = ?
        ORDER BY T.name;
    """, (name,))

    courses = []
    for course in res.fetchall():
        courses.append(course[0])

    return courses

def credits_by_teacher(name: str) -> int:
    """ Fetch credits """

    res = cur.execute("""--sql
        SELECT SUM(C.credits) FROM
        course_teachers CT JOIN courses C ON C.id = CT.course_id
                           JOIN teachers T ON T.id = CT.teacher_id
                           JOIN accomplishments A ON A.course_id = CT.course_id
        WHERE T.name = ?;
    """, (name,))

    return res.fetchone()[0]

def courses_by_student(name: str) -> list[tuple[str, int]]:
    """ Fetch courses """

    res = cur.execute("""--sql
        SELECT C.name, A.grade  FROM
        accomplishments A JOIN courses C ON C.id = A.course_id
                          JOIN students S ON S.id = A.student_id
        WHERE S.name = ?
        ORDER BY C.name;
    """, (name,))

    return res.fetchall()

def credits_by_year(year: int) -> int:
    """ Fetch credits (agan) """

    res = cur.execute("""--sql
        SELECT IFNULL(SUM(C.credits),0) FROM
        courses C JOIN accomplishments A ON C.id = A.course_id
        WHERE (SELECT STRFTIME("%Y", A.date)) = ?;
    """, (str(year),))

    return res.fetchone()[0]

def grade_distribution(course_name: str) -> dict[int:int]:
    """ Fetch distribution """

    res = cur.execute("""--sql
        SELECT A.grade, COUNT(A.grade) FROM
        courses C JOIN accomplishments A ON C.id = A.course_id
        WHERE C.name = ?
        GROUP BY A.grade
        ORDER BY A.grade;
    """, (course_name,))

    distribution = dict(res.fetchall())
    for i in range(1, 6):
        if i not in distribution:
            distribution[i] = 0

    return dict(sorted(distribution.items()))

def course_list() -> list[tuple[str, int, int]]:
    """ Fetch courses """
    
    res = cur.execute("""--sql
        SELECT C.name, COUNT(DISTINCT CT.teacher_id), COUNT(DISTINCT A.student_id) FROM
        courses C LEFT JOIN course_teachers CT ON C.id = CT.course_id
                  LEFT JOIN accomplishments A ON C.id = A.course_id
        GROUP BY C.name
        ORDER BY C.name;
    """)

    return res.fetchall()

def teacher_list() -> list[tuple[str, list[str]]]:
    """ Fetch teachers """

    res = cur.execute("""--sql
        SELECT name FROM teachers
        ORDER BY name;
    """)

    teachers = res.fetchall()
    teachers_courses = []

    for teacher in teachers:
        res = cur.execute("""--sql
            SELECT C.name FROM
            course_teachers CT JOIN teachers T ON T.id = CT.teacher_id
                               JOIN courses C ON C.id = CT.course_id
            WHERE T.name = ?;
        """, (teacher[0],))

        courses = []
        for course in res.fetchall():
            courses.append(course[0])

        teachers_courses.append((teacher[0], courses))

    return teachers_courses

def group_people(group: str) -> list[str]:
    """ Fetch people """

    res = cur.execute("""--sql
        SELECT S.name FROM
        group_students GS JOIN groups G ON G.id = GS.group_id
                          JOIN students S ON S.id = GS.student_id
        WHERE G.name = ?;
    """, (group,))

    people = []
    for student in res.fetchall():
        people.append(student[0])

    res = cur.execute("""--sql
        SELECT T.name FROM
        group_teachers GT JOIN groups G ON G.id = GT.group_id
                          JOIN teachers T ON T.id = GT.teacher_id
        WHERE G.name = ?;
    """, (group,))

    for teacher in res.fetchall():
        people.append(teacher[0])

    return sorted(people)

def credits_in_groups() -> list[tuple[str, int]]:
    """ Fetch credits """

    res = cur.execute("""--sql
        SELECT G.name, iFNULL(SUM(C.credits),0) FROM
        group_students GS LEFT JOIN accomplishments A ON A.student_id = GS.student_id
                          LEFT JOIN courses C ON C.id = A.course_id
                          LEFT JOIN groups G ON G.id = GS.group_id
        GROUP BY G.name
        ORDER BY G.name ;
    """)

    return res.fetchall()

def common_groups(teacher_name, student_name) -> list[str]:
    """ Fetch groups """

    res = cur.execute("""--sql
        SELECT G.name FROM
        groups G JOIN group_teachers GT ON G.id = GT.group_id
                 JOIN teachers T ON T.id = GT.teacher_id
                 JOIN group_students GS ON G.id = GS.group_id
                 JOIN students S ON S.id = GS.student_id
        WHERE T.name = ? AND S.name = ?
        ORDER BY G.name ;                  
    """, (teacher_name, student_name))

    groups = []
    for group in res.fetchall():
        groups.append(group[0])
    
    return groups

#==== DEBUG ====#

if __name__ == "__main__":
    
    create_tables()

    t1 = create_teacher("Erkki Kaila")
    t2 = create_teacher("Antti Laaksonen")
    t3 = create_teacher("Matti Luukkainen")
    t4 = create_teacher("Emilia Oikarinen")
    t5 = create_teacher("Leena Salmela")

    c1 = create_course("Laskennan mallit", 5, [t1])
    c2 = create_course("Ohjelmistotuotanto", 5, [t2, t4, t5])
    c3 = create_course("Ohjelmoinnin perusteet", 5, [])
    c4 = create_course("Tietokantojen perusteet", 5, [t3, t5])
    c5 = create_course("Tietokoneen toiminta", 5, [t1])

    s1 = create_student("Heikki Lokki")
    s2 = create_student("Liisa Marttinen")
    s3 = create_student("Otto Nurmi")
    s4 = create_student("Esko Ukkonen")
    s5 = create_student("Arto Wikla")

    add_credits(s1, c2, "2020-06-01", 5)
    add_credits(s1, c3, "2021-01-08", 3)
    add_credits(s2, c5, "2022-03-23", 2)
    add_credits(s4, c3, "2022-01-27", 4)
    add_credits(s4, c4, "2021-05-05", 4)
    add_credits(s4, c2, "2021-10-03", 5)
    add_credits(s4, c5, "2021-10-04", 5)
    add_credits(s5, c2, "2020-12-24", 1)

    create_group("Basic-koodarit", [t2, t3], [s1, s2, s3])
    create_group("Cobol-koodarit", [t1], [s2, s4])
    create_group("Fortran-koodarit", [t1, t2, t3, t4, t5], [s1, s2, s3, s4, s5])
    create_group("PHP-koodarit", [t4, t5], [s3])

    print(courses_by_teacher("Leena Salmela"))
    print(credits_by_teacher("Leena Salmela"))
    print(courses_by_student("Esko Ukkonen"))

    print(credits_by_year(2020))
    print(credits_by_year(2021))
    print(credits_by_year(2022))

    print(grade_distribution("Ohjelmoinnin perusteet"))
    print(grade_distribution("Tietokoneen toiminta"))

    print(course_list())
    print(teacher_list())

    print(group_people("Basic-koodarit"))
    print(credits_in_groups())
    print(common_groups("Antti Laaksonen", "Otto Nurmi"))