# Python design

At the end the project will have the following architecture:

```
project
|--- src/
|--- |--- database_management/
|--- |--- ...
|--- tests/
|--- |--- unit/
|--- |--- integration/
```

Most of the time, we will have one class per file for simplicity and maintainability.

## Source

### database_management

The database_management folder will contains the python file that will directly manipulate the database and its tables.

The manipulation of the tables will pass by one class for each table manipulation that will handle the CRUD operations.

## Tests

Unit testing is about testing components separately. Integration testing is about testing components with each others.

Here, a component will be a python class.

Tests will be made with **pytest** tool.

### Unit tests

We expect a 100% coverage for the unit tests.

### Integration tests

TODO
