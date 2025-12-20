# VOTES ENDPOINT TESTING — FULL COVERAGE
## PRECONDITIONS (MUST EXIST)

From previous steps you already have:

### Users

- `alice` (community owner)

- `bob` (community member)

- `charlie` (registered, optional)

### Community

- `kenya-devs`

### Posts (from Posts testing)

Assume these exist:

| Alias | Title | Type |
|-------|-------|------|
| P1 | National Student Records System | proposal |
| P2 | Tech gaps in rural education | discussion |
| P3 | Clinic Appointment Booking System | proposal |
| P4 | Open-source contribution culture | discussion |

### Save POST IDs:

- `POST_ID_1`

- `POST_ID_2`

- `POST_ID_3`

- `POST_ID_4`

1. VOTE ENDPOINT (ONLY ONE)

POST `/api/v1/votes/posts/<post_id>/vote/`


Payload:
```json
{ "value": 1 }   // upvote
{ "value": -1 }  // downvote
```

Header:

Authorization: Bearer `<ACCESS_TOKEN>`

Content-Type: `application/json`

2. BASIC VOTE TESTS

- Alice Upvotes a Post

POST `/api/v1/posts/posts/POST_ID_1/vote/`
```json
{ "value": 1 }
```

Expected Response:
```json
{
  "message": "Vote recorded"
}
```


Status: `201`

#### Expected DB State

* Votes table: `1` row

* `post`.`score` = `1`

Alice Upvotes Same Post Again (Remove Vote)

Same request again.

Expected:
```json
{
  "message": "Vote removed"
}
```


Status: `200`

#### Expected DB State

* Vote deleted

* `post`.`score` = `0`

3. DOWNVOTE FLOW

- Bob Downvotes Post

POST `/api/v1/votes/posts/POST_ID_1/vote/`
```json
{ "value": -1 }
```

Expected:
```json
{ "message": "Vote recorded" }
```

* `post`.`score` = `-1`

- Bob Downvotes Again (Remove)

Expected:
```json
{ "message": "Vote removed" }
```

* `post`.`score` = `0`

4. CHANGE VOTE (CRITICAL CASE)

- Alice Upvotes
```json
{ "value": 1 }
```

* `post`.`score` = `+1`

- Alice Changes to Downvote
```json
{ "value": -1 }
```

Expected
```json
{
  "message": "Vote updated"
}
```

#### Score Calculation
```diff
+1 → -1  =  -2 delta
```


`post`.`score` = `-1`

5. MULTI-USER VOTING

- Bob Upvotes Same Post
```json
{ "value": 1 }
```

- Score Change
```nginx
Alice (-1) + Bob (+1) = 0
```


`post.score = 0`

6. VERIFY VIA POST DETAIL ENDPOINT

GET `/api/v1/votes/posts/POST_ID_1/`


Expected:
```json
{
  "score": 0
}
```

7. INVALID INPUT TESTS

- Invalid Vote Value
```json
{ "value": 2 }
```

Expected:
```json
{
  "message": "Invalid vote value"
}
```


Status: `400`

- Missing Value
```json
{}
```


Expected:
```json
{
  "message": "Invalid vote value"
}
```

- Non-Integer Value 
```json
{ "value": "upvote" }
```

Expected:
```json
{
  "message": "Invalid vote value"
}
```

8. AUTH & SECURITY TESTS

- Unauthenticated Vote

Remove Authorization header.

Expected:
```pgsql
401 Missing Authorization Header
```

- Invalid Post ID

POST `/api/v1/votes/posts/00000000-0000-0000-0000-000000000000/vote/`


Expected:
```mathematica
404 Not Found
```

9. CROSS-POST DATASET TESTING

Repeat votes on:

- `POST_ID_2`

- `POST_ID_3`

- `POST_ID_4`

Ensure:

- Votes are isolated per post

- Scores do not leak

10. DATABASE VERIFICATION (OPTIONAL BUT RECOMMENDED)
```sql
SELECT post_id, SUM(value) FROM votes GROUP BY post_id;
SELECT id, title, score FROM posts;
```

Values must match.

## FINAL DATASET STATE (EXAMPLE)
| Post | Score |
|------|-------|
| P1 | 0 |
| P2 | +1 |
| P3 | -1 |
| P4 | 0 |