import itertools

class Group:
    def __init__(self, event, people):
        self.people = people

    def assign(self):
        """Return partition of """
        self.people

        drivers = [person for person in self.people if person["driver"]]
        passengers = [person for person in self.people if not person["driver"]]
        
        # Assume all drivers are driving
        # Assume capacity for all drivers
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