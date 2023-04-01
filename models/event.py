class Event:
    def __init__(self, id, destination_location):
        self.id = id
        self.destination_location = destination_location

    @staticmethod
    def create(cursor, destination_location):
        """Return a new event with an assigned ID and requested destination location"""

        res = cursor.execute(
            f"INSERT INTO events (destination_location) VALUES (?) RETURNING *",
            [destination_location]
        )

        new_event = res.fetchall()[0]

        return Event(new_event[0], new_event[1])