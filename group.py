import itertools
from person import Person

class GroupMapper:
    @staticmethod
    def find_by_person(cursor, person_id):
        """Retrieve a group that contains a person"""

        people = cursor.execute("""
        SELECT * FROM people
            WHERE group_id = (
                SELECT group_id FROM people WHERE people.id = ?
            );
        """, [person_id]).fetchall()

        return [{
            'id': people[0]['group_id'],
            'people': [dict(person) for person in people]
        }]

    @staticmethod
    def assign(cursor, event_id):
        people = cursor.execute("SELECT * FROM people WHERE event_id = ?", [event_id]).fetchall()
        group = Group(people)
        partitions = group.partition()

        for partition in partitions:
            res = cursor.execute("INSERT INTO groups DEFAULT VALUES RETURNING id").fetchone()
            group_id = res[0]

            for person in partition:
                cursor.execute(
                    """
                    UPDATE people
                    SET group_id = ?
                    WHERE id = ?
                    """,
                    [group_id, person['id']]
                )

        return GroupMapper.find_by_event(cursor, event_id)

    @staticmethod
    def find_by_event(cursor, event_id, person_id=None):
        """
        Retrieve all groups within an event, and the people within them.

        Filter by person_id if passed.
        """

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

class Group:
    def __init__(self, people):
        self.people = people

    def partition(self):
        """
        Return array of partitions. Each partition has a driver and some passengers.
        """
        # Assume all drivers are driving
        # Assume infinite capacity for all drivers

        drivers = [person for person in self.people if Person(person).is_driver()]
        passengers = [person for person in self.people if Person(person).is_passenger()]
        
        groups = [
            [driver] for driver in drivers
        ]

        group_cycle = itertools.cycle(groups)
        for passenger in passengers:
            next(group_cycle).append(passenger)

        return groups

# To run these tests - python3 group.py
if __name__ == "__main__":
    people = [
        {"driver": True, "name": "1" },
        {"driver": True, "name": "2" },

        {"driver": False, "name": "3" },
        {"driver": False, "name": "4" },
        {"driver": False, "name": "5" },
        {"driver": False, "name": "6" },
        {"driver": False, "name": "7" },
    ]
    group = Group(None, people)

    result = group.assign()

    assert len(result) == 2, "two drivers, two groups."

    for group in result:
        assert len(set(person['name'] for person in group if person["driver"])) == 1, "One driver in each group"

    for person in people:
        person_assigned = False
        for group in result:
            if person in group:
                person_assigned = True
            
        assert person_assigned, f"{person=} should be assigned somewhere"

    ## Each person is assigned to exactly one group