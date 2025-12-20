# POSTS ENDPOINT TESTING — FULL COVERAGE
1. PRECONDITIONS (MUST EXIST)

From previous steps (Communities blueprint) you already have:

- Users:
    - alice (owner)
    - bob (member)

- Community:
    - kenya-devs

- Both users are members of `kenya-devs`
- You have saved:
    - Alice access token
    - Bob access token

2. CREATE POSTS (DATASET PREP)

We will create multiple posts to test filters and ordering.
<hr>

#### Proposal Post (Alice)
POST `/api/v1/posts/communities/kenya-devs/posts/` <br>
Authorization: Bearer <ALICE_TOKEN>

```json
{
    "title": "National Student Records System",
    "content": "A centralized open-source platform for schools and universities.",
    "post_type": "proposal"
}
```
Expected: `201` Created

#### Discussion Post (Alice)
```json
{
  "title": "Tech gaps in rural education",
  "content": "What digital tools are missing in rural schools?",
  "post_type": "discussion"
}
```

#### Proposal Post (Bob)
```json
{
  "title": "Clinic Appointment Booking System",
  "content": "Simple mobile-first booking system for public clinics.",
  "post_type": "proposal"
}
```

#### Discussion Post (Bob)
```json
{
  "title": "Open-source contribution culture",
  "content": "How can we encourage more local devs to contribute?",
  "post_type": "discussion"
}
```

### At this point, DB has:

| Type | Count |
|------|-------|
| Proposal | 2 |
| Discussion | 2 |

3. LIST POSTS (ALL)

GET `/api/v1/posts/communities/kenya-devs/posts/`

Expected: <br>
`4 posts` <br>

Ordered newest → oldest
```json
[
  {
    "id": "...",
    "title": "Open-source contribution culture",
    "post_type": "discussion"
  },
  ...
]
```

4. FILTER POSTS BY TYPE
- Proposal Only <br>
GET `/api/v1/posts/communities/kenya-devs/posts/?type=proposal`

Expected: <br>

Only proposal posts <br>

Count = 2

- Discussion Only
GET `/api/communities/kenya-devs/posts/?type=discussion`

Expected: <br>

Only discussion posts <br>

Count = 2

- Invalid Filter 
GET `/api/v1/posts/communities/kenya-devs/posts/?type=random`

Expected: <br>

Empty array
```json
[]
```

Status `200` <br>

(No crash, frontend-safe)

5. POST DETAIL ENDPOINT

Pick any post ID from list response. <br>

GET `/api/v1/posts/<POST_ID>/`

Expected:
```json
{
  "id": "...",
  "title": "Clinic Appointment Booking System",
  "content": "...",
  "post_type": "proposal",
  "score": 0,
  "author": "bob",
  "community": "kenya-devs",
  "created_at": "..."
}
```

6. AUTH & PERMISSION TESTS
- Unauthenticated Create 

Remove Authorization header. <br>

POST `/api/v1/posts/communities/kenya-devs/posts/`

Expected:

`401` Missing Authorization Header

- Non-member Create 

Create a new user:
```json
{
  "username": "charlie",
  "email": "charlie@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

Login as Charlie (do NOT join community). <br>

Try: <br>

POST `/api/v1/posts/communities/kenya-devs/posts/`


Expected:
```json
{
  "message": "Join community to post"
}
```


Status: `403`

- Missing Fields
```json
{
  "title": "",
  "content": ""
}
```

Expected:
```json
{
  "message": "Title and content are required"
}
```

- Invalid Post Type
```json
{
  "title": "Invalid type",
  "content": "Test",
  "post_type": "announcement"
}
```


Expected:
```json
{
  "message": "Invalid post type"
}
```

7. SLUG & ID EDGE CASES
- Invalid Community Slug <br>
POST `/api/v1/posts/communities/unknown/posts/`


Expected:

`404` Not Found

- Invalid Post ID <br>
GET `/api/v1/posts/00000000-0000-0000-0000-000000000000/`


Expected:

`404` Not Found

8. DATASET YOU NOW HAVE (SUMMARY)

| Entity | Count |
|--------|-------|
| Users | 3 |
| Communities | 1 |
| Posts | 4 |
| Proposals | 2 |
| Discussions | 2 |

Perfect for:
- Feed testing
- Sorting
- Voting next
- Project incubation logic

9. OPTIONAL SQL VERIFICATION
```sql
SELECT title, post_type, created_at FROM posts ORDER BY created_at DESC;
```