# API design

We will follow standard as possible for our REST APIs:

- CRUD
- Search API

## Global

For all APIs, a JSON will be returned:
- in case of success, pertinent data depending of the API's purpose
- in case of error, we will have the following parameters:
    - `detail`: message that details the error

## CRUD

At least four APIs by database's table to Create, Read, Update and Delete data.

### Delete

In case of success, the Delete APIs will return an HTTP 204 No Content with no response body.

## Search API

At least one search API by database's table with at least pagination, filter and sorting.

The pagination will be manage as following:

- query parameters for pagination:
    1. `page`: indicates the current page number
        - starting at 1 by default
        - e.g., `?page=1`
    2. `limit`: specifies the number of items to be returned per page
        - at 20 by default
        - at 100 maximum
        - e.g., `?limit=50`
    3. `sort` (optional): allows sorting by one or more fields
        - `+` for ascending, `-` for descending
        - e.g., `?sort=+name`
    4. `filter` (optional): applies filters to refine results
        - e.g., `?filter[archived]=false`
    5. date filtering (optional): allows filtering by date ranges
        - exact parameters will depends of the API research possibilities
        - format expected:
            - `start_<date_parameter>`: filter results from this date
            - `end_<date_parameter>`: filters results up to and including this date
        - e.g., `?start_date=2024-01-01&end_date=2024-12-31`
        - we will follow ISO 8601 format:
            - date format: YYYY-MM-DD
            - datetime format: YYYY-MM-DDTHH:MM:SSZ
- response structure:
    1. `data`: contains the array of items for the current page
    2. `meta`:
        - `total_items`: total number of items available in the dataset
        - `total_pages`: total number of pages
        - if needed, we could add later:
            - `count`: number of items in the current page
            - `current_page`: the current page number
            - `current_limit`: number of items per page (as specified in the query)
- HTTP status codes
    - `200 OK`: Request succeeded, data returned successfully
    - `400 Bad Request`: Generic errors from the client
    - `404 Not Found`: Requested page does not exist (e.g., page > total_pages)
    - `422 Unprocessable Entity`: Invalid query parameters (e.g., negative page or limit values)
    - `500 Internal Server Error`: Unexpected server error
