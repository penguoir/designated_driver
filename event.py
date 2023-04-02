class EventMapper:
    @staticmethod
    def create(cursor, event):
        keys = ','.join(event.keys())
        value_placeholders = ','.join('?' for _ in event)
        values = [str(x) for x in event.values()]

        res = cursor.execute(
            f"""
            INSERT INTO events (destination_location, description)
            VALUES (?, ?)
            RETURNING *
            """,
            [event.get('destination_location'), event.get('description')]
        )

        new_event = res.fetchone()
        return new_event

    @staticmethod
    def find_by_person(cursor, person_id):
        event = cursor.execute(
            """
            SELECT events.*
            FROM events
            JOIN people ON events.id = people.event_id
            WHERE people.id = ?
            """,
            [person_id]
        ).fetchone()

        assert event, f"Couldn't find an event with {person_id=}"
        return event
