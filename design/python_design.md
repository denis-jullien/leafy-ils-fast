# Python design

At the end the project will have the following architecture:

```
project
|--- src/
|--- |--- database_management
|--- |--- |--- database.py
|--- |--- |--- models.py
|--- |--- ...
|--- tests/
|--- |--- unit/
|--- |--- integration/
```

Most of the time, we will have one class per file for simplicity and maintainability.

## Source

### database_management

The manipulation of the tables will pass by one class that will manage the database and handle the CRUD operations on all tables. This class is in database file.

The models file will contain all SQLModel classes that type the database's tables.

## Tests

Unit testing is about testing components separately. Integration testing is about testing components with each others.

Here, a component will be a python class.

Tests will be made with **pytest** tool.

### Unit tests

We expect a 100% branch coverage for the unit tests.

Plus, we expect at least the following test cases by CRUD APIs:

- create operation:
    - only mandatory parameters
    - all parameters
- read operation:
    - one test for normal type (str, int, bool)
    - if present: one test for date type
- update operation:
    - one parameter updated
    - all parameters updated
    - no parameter updated
- delete operation:
    - one test case

### Integration tests

TODO
