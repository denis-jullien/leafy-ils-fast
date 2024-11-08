# project: Mini Library management system

## Overview

Easy software for an associative library.

We will name it **LeafyILS** because:

- Leafy refers to the origin of the papers from the books.
- ILS means integrated library system.

### For who?

- Active members (managers)
- All other members (People borrowing books)

### To do what?

- Books database
    - Book registration
        - Several separate catalogs
        - Quick cataloging: ISBN base, generated or existing barcode support
        - Bulk operations
            - spreadsheet import
    - Book de-registration
    - Database reading access
        - Public access
        - sorting: alphabetical category, age, new items
        - Location in the shelf
- Book borrowing management
    - Allocation of borrows to a family
    - Books Out
    - Books In
- Membership management
    - Annual family membership
        - multiple users per family
    - email to families
- Newsletters
    - Email
    - Portal
        - Articles
        - Calendar of events
        - News
        - Practical information
- Reporting and usage statistics
    - Number of loans
    - Number of visitors
    - Category management (children, adults, seniors)
    - History of operations
- Role based access control
    - simple member access:
        - management of current loans
        - reservations
        - management of user data
    - admin member access:
        - simple member access
        - management of simple members
        - management of books' catalog
        - management of Newsletters
        - access of reporting
        - archiving of data
    - super admin access:
        - admin member access
        - management of roles
        - deletion of data

### Contraints

- Low cost or free
- Testable
- French must be use in UI
- High level of Accessibility

## Features to implement

### Minimal features set

- Books database
- Book borrowing management
- Membership management
- Reporting and usage statistics
- Role based access control
    - admin member access

### Improvment of next features by order

- Search bar
    - Book
    - Member
- Newsletters
    - Email
    - Portal
- Role based access control
    - super admin access
    - simple member access
- Reservation
