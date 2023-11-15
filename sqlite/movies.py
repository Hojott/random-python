import sqlite3
import os
import time
import random, string

db_path = "movies.db"
if os.path.exists(db_path):
    os.remove(db_path)
db = sqlite3.connect(db_path)
cur = db.cursor()

def create_table_1() -> float:
    """ Create table for first test and return time """

    start = time.time()

    cur.execute("""--sql
        CREATE TABLE movies1 (
            id INTEGER PRIMARY KEY,
            name TEXT,
            year INTEGER
        ) ;
    """)

    for _ in range(1000000):
        name = "".join(random.choices(string.ascii_lowercase, k=8))
        cur.execute("""--sql
            INSERT INTO movies1 (name, year)
            VALUES (?, RANDOM()%101 + 1900) ;
        """, (name,))
    
    db.commit()

    end = time.time()

    return end - start

def create_table_2() -> float:
    """ Create table for second test and return time """

    start = time.time()

    cur.execute("""--sql
        CREATE TABLE movies2 (
            id INTEGER PRIMARY KEY,
            name TEXT,
            year INTEGER
        ) ;
    """)

    cur.execute("""--sql
        CREATE INDEX idx_year ON movies2 (year) ;
    """)

    for _ in range(1000000):
        name = "".join(random.choices(string.ascii_lowercase, k=8))
        cur.execute("""--sql
            INSERT INTO movies2 (name, year)
            VALUES (?, RANDOM()%101 + 1900) ;
        """, (name,))
    
    db.commit()

    end = time.time()

    return end - start

def create_table_3() -> float:
    """ Create table for third test and return time """

    start = time.time()

    cur.execute("""--sql
        CREATE TABLE movies3 (
            id INTEGER PRIMARY KEY,
            name TEXT,
            year INTEGER
        ) ;
    """)

    for _ in range(1000000):
        name = "".join(random.choices(string.ascii_lowercase, k=8))
        cur.execute("""--sql
            INSERT INTO movies3 (name, year)
            VALUES (?, RANDOM()%101 + 1900) ;
        """, (name,))
    
    db.commit()

    cur.execute("""--sql
        CREATE INDEX idx_year ON movies3 (year) ;
    """)

    end = time.time()

    return end - start

def test_table_1() -> int:
    """ Test performance of first table """

    start = time.time()

    for _ in range(1000):
        cur.execute("""--sql
            SELECT COUNT(*) FROM movies1
            WHERE year = ? ;
        """, (random.randint(1900, 2000),))
    
    end = time.time()

    return end - start

def test_table_2() -> int:
    """ Test performance of second table """

    start = time.time()

    for _ in range(1000):
        cur.execute("""--sql
            SELECT COUNT(*) FROM movies2
            WHERE year = ? ;
        """, (random.randint(1900, 2000),))
    
    end = time.time()

    return end - start

def test_table_3() -> int:
    """ Test performance of third table """

    start = time.time()

    for _ in range(1000):
        cur.execute("""--sql
            SELECT COUNT(*) FROM movies3
            WHERE year = ? ;
        """, (random.randint(1900, 2000),))
    
    end = time.time()

    return end - start

if __name__ == "__main__":
    #print("test 1:", create_table_1())
    #print("test 2:", create_table_2())
    print("test 3:", create_table_3())

    #print("test 1.1", test_table_1())
    #print("test 2.2", test_table_2())
    print("test 3.3", test_table_3())