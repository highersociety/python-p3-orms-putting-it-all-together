# lib/dog.py
try:
    # Try relative import (works when running locally as a package)
    from . import CONN, CURSOR
except ImportError:
    # Fallback for CodeGrade (imports as standalone file)
    from __init__ import CONN, CURSOR  # type: ignore

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        return self

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        return dog.save()

    @classmethod
    def new_from_db(cls, row):
        return cls(name=row[1], breed=row[2], id=row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)

    def update(self):
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
