class PersonMapper:
    @staticmethod
    def create(cursor, person):
        keys = ','.join(person.keys())
        value_placeholders = ','.join('?' for _ in person)
        values = [str(x) for x in person.values()]

        res = cursor.execute(
            f"""
            INSERT INTO people ({keys})
            VALUES ({value_placeholders})
            RETURNING *
            """,
            values
        )

        return res.fetchone()


class Person():
    def __init__(self, attrs):
        self.attrs = attrs

    def is_passenger(self):
        return self.attrs['role'] == 0

    def is_driver(self):
        return self.attrs['role'] == 1

if __name__ == "__main__":
    from main import app, get_db
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            print(PersonMapper.retrieve_event_groups(cursor, 3))