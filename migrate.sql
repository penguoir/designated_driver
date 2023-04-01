create table events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    destination_location TEXT NOT NULL
);

create table groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

create table people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    display_name TEXT NOT NULL,
    role INTEGER NOT NULL,
    is_organizer BOOLEAN NOT NULL,
    start_location TEXT NOT NULL,

    passenger_capacity INTEGER, -- if role = driver, this can be anything

    event_id INTEGER NOT NULL,
    group_id INTEGER,

    FOREIGN KEY(event_id) REFERENCES events(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);