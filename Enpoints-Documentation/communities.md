# Communities Endpoints - Full coverage
## AUTH TEST DATA (USERS)
Register Users <br>
User 1 (Community Owner)
```json
POST /api/auth/register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

User 2 (Member) <br>
POST `/api/v1/auth/register`
```json
{
  "username": "bob",
  "email": "bob@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

Login Both Users <br>
POST `/api/v1/auth/login`
```json
{
  "email": "alice@example.com",
  "password": "password123"
}
```
Save:

- `access_token` (Alice)
- `refresh_token` (Alice)

Repeat for Bob.

1. POSTMAN SETUP (IMPORTANT)

For authenticated requests, add header: <br>

Authorization: Bearer `<ACCESS_TOKEN>` <br>
Content-Type: `application/json`

2. COMMUNITY ENDPOINT TESTS (FULL COVERAGE)
- Create Community 
Request <br>
POST `/api/v1/communities/`
```json
{
  "name": "Kenya Devs",
  "description": "Developers solving local problems"
}
```

Expected Response
```json
{
  "message": "Community created",
  "slug": "kenya-devs"
}
```

### DB Validation
- Community exists
- Alice is owner
- Membership row created

- Duplicate Community 

Same request again. <br>
Expected:
```json
{
  "message": "Community already exists"
}
```
Status: `400`

- List Communities 

GET `/api/v1/communities/` <br>

Expected:
```json
[
  {
    "id": "uuid-string-here",
    "name": "Kenya Devs",
    "slug": "kenya-devs",
    "description": "Developers solving local problems",
    "created_at": "...",
    "is_member": true,
    "total_members": 1
  }
]

```

### Notes
  - is_member: true if the current user (Alice or Bob) is a member
  - total_members: total number of members in the community

- Community Detail 

GET `/api/v1/communities/kenya-devs/` 

Expected
```json
{
  "id": "uuid-string-here",
  "name": "Kenya Devs",
  "slug": "kenya-devs",
  "description": "Developers solving local problems",
  "created_at": "...",
  "is_member": true,
  "total_members": 1
}

```

- Join Community (Bob)

Use Bob’s access token 

POST `/api/v1/communities/kenya-devs/join/` 

Expected:
```json
{
  "message": "Joined community"
}
```

- Join Twice 

Same request again. <br>

Expected:
```json
{
  "message": "Already a member"
}
```

Status: `400`

- List Members 

GET `/api/v1/communities/kenya-devs/members/`

Expected:
```json
[
  {
    "username": "alice",
    "role": "owner",
    "joined_at": "..."
  },
  {
    "username": "bob",
    "role": "member",
    "joined_at": "..."
  }
]
```

- Leave Community (Bob)

POST `/api/v1/communities/kenya-devs/leave/`

Expected:
```json
{
  "message": "Left community"
}
```

- Leave Without Membership 

Bob tries again.
```json
{
  "message": "Not a member"
}
```

Status: `400`

- Owner Leave Attempt

Alice tries to leave.
```json
{
  "message": "Owner cannot leave community"
}
```


Status: `403`

3. AUTH EDGE CASE TESTS

Unauthenticated Create

POST `/api/v1/communities/`

Expected:

`401` Missing Authorization Header

Invalid Slug 

GET `/api/v1/communities/unknown-community/`


Expected:

`404` Not Found

2. DATASET SUMMARY (WHAT YOU NOW HAVE)

| Entity | Count |
|--------|-------|
| Users | 2 |
| Communities | 1 |
| Memberships | 1–2 (depending on leave tests) |