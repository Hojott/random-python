import sqlite3

con = sqlite3.connect("bikes.db")
cur = con.cursor()

def distance_of_user(user: str) -> int:
    res = cur.execute("""--sql
        SELECT
            SUM(T.distance)
        FROM
            trips T JOIN users U ON U.id = T.user_id
        WHERE
            U.name = ?
        ;
    """, (user,))
    return res.fetchone()[0]

def speed_of_user(user: str) -> float:
    res = cur.execute("""--sql
        SELECT
            SUM(T.distance), SUM(T.duration)
        FROM
            trips T JOIN users U ON U.id = T.user_id
        WHERE
            U.name = ?
        ;
    """, (user,))

    res = res.fetchone()
    return round((res[0]/res[1])*60/10)/100

def duration_in_each_city(day: str) -> list[tuple[str, int]]:
    res = cur.execute("""--sql
        SELECT
            C.name, SUM(T.duration)
        FROM
            bikes B JOIN trips T ON B.id = T.bike_id
                    JOIN cities C ON C.id = B.city_id
        WHERE
            T.day = ?
        GROUP BY
            C.name
        ;
    """, (day,))

    return res.fetchall()

def users_in_city(city: str) -> int:
    res = cur.execute("""--sql
        SELECT
            COUNT(DISTINCT T.user_id)
        FROM
            trips T JOIN users U ON U.id = T.user_id
                    JOIN bikes B ON B.id = T.bike_id
                    JOIN cities C ON C.id = B.city_id
        WHERE
            C.name = ?
        ;
    """, (city,))

    return res.fetchone()[0]

def trips_on_each_day(city: str) -> list[tuple[str, int]]:
    res = cur.execute("""--sql
        SELECT
            T.day, COUNT(T.id)
        FROM
            trips T JOIN bikes B ON B.id = T.bike_id
                    JOIN cities C ON C.id = B.city_id
        WHERE
            C.name = ?
        GROUP BY
            T.day
        ;
                             
    """, (city,))

    return res.fetchall()

def most_popular_start(city: str) -> tuple[str, int]:
    res = cur.execute("""--sql
        SELECT
            S.name, COUNT(T.id)
        FROM
            trips T JOIN stops S ON S.id = T.from_id
                    JOIN bikes B ON B.id = T.bike_id
                    JOIN cities C ON C.id = B.city_id
        WHERE
            C.name = ?
        GROUP BY
            S.name
        ORDER BY
            COUNT(T.id) DESC, S.name DESC
        LIMIT
            1
        ;
    """, (city,))

    return res.fetchone()

if "__main__" == __name__:
    print("Test 1:", distance_of_user("ocuber"))
    print("Test 2:", speed_of_user("ocuber"))
    print("Test 3:", duration_in_each_city("2021-06-01"))
    print("Test 4:", users_in_city("laeserii"))
    print("Test 5:", trips_on_each_day("laeserii"))
    print("Test 6:", most_popular_start("laeserii"))
