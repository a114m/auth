# Authorization Service
Example microservice that makes sure an external user is authorized to access an internal resource, it's job is simply to answer single question as quick as possible, is specific user authorized to access a specific resource.


## Run
To run the service in development you'll only need docker daemon/client to be installed and run:
```
docker-compose up
```

Note that the service runs using built-in Flask server, in production a servers like Gunicorn or uWSGI will be used

## Tests
To run tests:
```
docker-compose -f ./docker-compose.yaml -f ./docker-compose.test.yaml up --abort-on-container-exit
```

## Data store
We can possibly use only **Redis** as datastore with AOF persistence strategy that will give us 1 second persistence guarantee

Also **Postgres** can hold well and give great response time without caching if used in different way to fit our case

Our goal is to use both.


We have three resources (models) in our authorization service:
- **User:** all what we need to know about user is the external userId to add him to a group (or to be precise add group to the user in our implementation)
- **Group:** we need to know the group name, and optional description
- **Resource:** name is needed, and can also have group or more, giving users in that group access to the resource

#### Persistent DB
From my understanding and the assumptions I made, the most frequent operation will be performed by the service are:
- Checking if a User has access to a certain resource
- Adding user to a group
- Giving group access to a certain resource

And the less performed operation are:
- Listing all users belong to a certain group
- Listing all resources a certain group are permitted to access

Based on that I went with the following:

- I chose **Postgres** as database for many reasons:
  - Like any SQL DB it provides great performance when you avoid joins
  - Postgres provides **JSONB** field I use to avoid joins, ex: storing array of data from other table to access it from one table with direct access instead of having **M2M** relationship that would require joining 3 tables (first table, through table, second table) to query frequently accessed piece of data
  - Mixing both **JSONB** (document like) and foreign key relationship can give a great mixture of performance and consistency
- I perform zero joins on critical end-points like **auth** (all required is direct access to 2 tables using indexed fields)
- We still have the advantage of being able to use relationships to achieve more consistency, and it mix with **JSONB** at the same time (in the case of write time isn't critical) to guarantee more consistency and preserve read performance, though write can get slower (to update **JSONB** column)

Example illustrating postgres tables:
```
auth=# SELECT * from groups;
 id |  name   |      description
----+---------+-----------------------
  1 | group 1 | some desc for group 1
(1 row)

auth=# SELECT * from resources;
 id |   name    |  groups
----+-----------+-----------
  1 | resource1 | [2, 5, 1]
  3 | resource2 | [2, 5, 1]
(2 rows)

auth=# SELECT * from users;
    id    |        groups
----------+----------------------
 someuser | [1, 4, 8, 9, 13, 33]
 userA    | [9, 12, 22]
 userB    | [9, 12, 22]
 userC    | [22, 33]
 userD    | [22, 33]
(5 rows)
```

As you can see to check if user has access to a resource all is done is direct accessing the **user** by `id` and the **resource** by `name` (which is indexed column) and checking if both groups intersect

#### Cache (To be implemented)
Using **Redis** as in-memory datastore to cache authorized users and update the cache on any change

## APIs

- GROUP:
  - **POST** `/group`  Create group
  - **GET**  `/group/<group_id>`  Get group by id
  - **GET**  `/group`  List all groups with their count
- USER:
  - **POST** `/group/<group_id>/user`  Add group to list of users
  - **GET**  `/group/<group_id>/user`  List users joined a specific group by group_id
- RESOURCE:
  - **POST** `/resource`  Create resource
  - **GET**  `/resource/<resource_id>`  Get resource by id
  - **GET**  `/resource`  List all resources with their count
  - **POST** `/group/<group_id>/authorize`  Add group to resource
  - **GET**  `/group/<group_id>/resource`  List resources included in group
- AUTH:
  - **GET**  `/authorized?userId=<userId>&resourceName=<resourceName>`  Check if user has access to resource

## Technologies used
- Python3
- Flask: a light weight python server with no much overhead and complication like other frameworks
- SQLAlchemy: datastore connection and ORM used through Flask-SQLAlchemy extension for Flask
- Alembic: a lightweight database migration tool
- Flask-Testing: Extension provides helpers for test cases
- nose: Python test runner
- Postgres 9.4: Our permanent datastore


## API docs

### Resource
- `POST /resource`

  Creates a new resource

  **Request**
  ```
  {
    name: String
  }
  ```
  **Response**

  The created resource

  statusCode: 200

  ```
  {
    id: String,
    name: String
  }
  ```

- `GET /resource/:id`

  Retrieves a specific resource by id.

  **Response**

  statusCode: 200

  ```
  {
    id: String,
    name: String
  }
  ```

- `GET /resource`

  Retrieves a list of all resources and their total count.

  **Response**

  statusCode: 200

  ```
  {
    count: Number,
    items: [{
      id: String,
      name: String
    }]
  }
  ```

### Group

- `POST /group`

  Creates a new empty group

  **Request**

  ```
  {
    name: String,
    description: String // (Optional)
  }
  ```

  **Response**

  The created group

  statusCode: 200

  ```
  {
    id: String,
    name: String,
    description: String
  }
  ```

- `GET /group/:id`

  Retrieves a specific group by id.

  **Response**

  statusCode: 200

  ```
  {
    id: String,
    name: String,
    description: String
  }
  ```

- `GET /group`

  Retrieves a list of all groups and their total count.

  **Response**

  statusCode: 200

  ```
  {
  count: Number,
  items: [{
      id: String,
      name: String,
      description: String
    }]
  }
  ```

- `POST /group/:id/user`

  Attaches list of userId s to the group.

  **Request**

  ```
  [
    {
      userId: String
    }
  ]
  ```

  **Response**

  statusCode: 204


- `GET /group/:id/user`

  Retrieves a list of userId s belonging to the group with id and their total count.

  **Response**

  statusCode: 200

  ```
  {
    count: Number,
    items: [{
      userId: String
    }]
  }
  ```


- `POST /group/:id/authorize`

  Authorizes the group to access any of the resources listed.

  If the group already has permissions to other resources, then the permissions are merged.

  **Request**

  ```
  [
    {
      resourceId: String
    }
  ]
  ```

  **Response**

  statusCode: 204


- `GET /group/:id/resource`

  Returns a list of resources this group can access and their total count.

  **Response**

  statusCode: 200

  ```
  {
    count: Number,
    items: [{
      id: String,
      name: String
    }]
  }
  ```


### Auth

- `GET /authorized?userId=&resourceName=`

  Checks whether this user identified by userId has access to the resource identified by resourceName through any of the groups the user belongs to.

  **Request**

  - Query Params:
    - userId
    - resourceName

  **Response**

  - **On Success:**

    statusCode: 200

    ```
    {
      authorized: true
    }
    ```

  - **On Failure:**

    statusCode: 403

    ```
    {
      authorized: false
    }
    ```
