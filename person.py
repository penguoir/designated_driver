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

    @staticmethod
    def retrieve_event_groups(cursor, event_id, person_id=None):
        """Retrieve all people within an event, partitioned into groups"""

        response = cursor.execute(f"""
        SELECT * FROM people
            WHERE event_id = ?
            ORDER BY group_id
        """, [event_id])

        groups = {}

        # Partition people into groups
        for person in response:
            assert person['group_id'], f"Person doesn't have group id {person['id']=}"

            # Create a new partition
            if not groups.get(person['group_id']):
                groups[person['group_id']] = list()

            # Add person to its assigned group
            groups[person['group_id']].append(dict(person))

        if person_id:
            groups = {group_id: people for group_id, people in groups.items()
                      if person_id in (person['id'] for person in people)}

        return [{"id": group_id, "people": people} for group_id, people in groups.items()]


if __name__ == "__main__":
    from main import app, get_db
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            print(PersonMapper.retrieve_event_groups(cursor, 3))