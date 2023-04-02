# Data Structures

## Person (object)
+ id: 43 (number)
+ display_name: Ori Marash (string, required)
+ email: ori@marash.net (string)
+ role: 0 (number)
+ is_organizer: false (boolean)
+ start_location: 41 Middleway (string)
+ passenger_capacity: 3 (number)
+ event_id: 5 (number)
+ group_id: 10

## Event (object)
+ id: 10 (number)
+ description: Snow day choir group - Wednesday 20 March. (string)
+ destination_location: University of bath (string, required)

## Group (object)
+ id: 4 (number)
+ people: (array[Person])
+ event_id: 5 (number)

# Endpoints

## ✅ Create a new event
POST to /events with an event object (except id) as a JSON body.

## ✅ Create a new person
POST to /people with a person object (except id) as JSON in the body.

## ✅ Retrieve a person's event
GET to /people/:id/event. Return value is an event.

## ✅ Assign groups
POST to /events/:id/assign with no body

### ✅ Retrieve groups of an event
GET /events/:id/groups

Example response

```json
[
    // Group 1
    { "id": 1, "people": [
        { "display_name": "Andrew" ... },
        { "display_name": "Ori", ...}
    ] },

    // Group 2
    { "id": 2, "people": [
        { "display_name": "Marta" ... },
        { "display_name": "Emi", ...}
    ] }
]
```

### Retrieve the group of one person - NOT DONE
GET /people/:id/group

Returns only the group that contains person_id

```json
{
    "id": 1,
    "people": [
        { "display_name": "Andrew" ... },
        { "display_name": "Ori", ...}
    ]
}
```