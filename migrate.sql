create table events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_location TEXT
);

create table groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

create table people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    display_name TEXT,
    role INTEGER,
    is_organizer BOOLEAN,
    start_location TEXT,

    event_id INTEGER,
    group_id INTEGER,

    FOREIGN KEY(event_id) REFERENCES events(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);