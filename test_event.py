from event import EventMapper
from person import PersonMapper

from main import get_db, app

def test_create_event(conn):
    cursor = conn.cursor()

    event = EventMapper.create(cursor, destination_location="ABC")
    old_id = event['id']
    new_event = EventMapper.create(cursor, destination_location="ABC")
    assert new_event['id'] == old_id + 1

    assert type(event['id']) == int
    assert event['destination_location'] == "ABC"

def test_find_event_by_person(conn):
    cursor = conn.cursor()

    event = EventMapper.create(cursor, destination_location="University of Bath")
    conn.commit()

    person = PersonMapper.create(
        cursor,
        email="ori@ori.com",
        display_name="Ori",
        role=1,
        is_organizer=False,
        start_location="221B Baker Street",
        event_id=event['id'],
    )
    conn.commit()

    found_event = EventMapper.find_by_person(cursor, person['id'])
    assert found_event['id'] == event['id']


def run_tests():
    with app.app_context():
        with get_db() as conn:
            test_create_event(conn)
            test_find_event_by_person(conn)

if __name__ == "__main__":
    run_tests()