# Projects Blueprint Documentation

Audience:

* Frontend developers consuming the API
* Backend contributors testing and extending the system

All endpoints below are **tested and verified using Thunder Client**.

---

## Base Information

* Base URL: `/api/v1/projects/`
* Auth: **JWT Bearer Token (`Access Token`)**
* Content-Type: `application/json`

---

## Project Model (Response Shape)

```json
{
  "id": 1,
  "title": "Digital Health Records",
  "problem_statement": "Patient records are fragmented",
  "proposed_solution": "Unified EHR platform",
  "sector": "health",
  "status": "PROPOSED",
  "vote_score": 0,
  "proposal_deadline": "2025-02-01T00:00:00Z",
  "owner": {
    "id": 1,
    "username": "alice"
  },
  "community": {
    "id": 1,
    "name": "kenya-dev"
  },
  "created_at": "2025-01-01T10:00:00Z"
}
```

---

## Endpoints Overview

| Method | Endpoint                        | Description            |
| ------ | ------------------------------- | ---------------------- |
| POST   | `/api/v1/projects/`                 | Create project         |
| GET    | `/api/v1/projects/`                 | List projects          |
| GET    | `/api/v1/projects/{id}/`            | Get single project     |
| PUT    | `/api/v1/projects/{id}/`            | Update project (owner) |
| DELETE | `/api/v1/projects/{id}/`            | Withdraw project       |
| POST   | `/api/v1/projects/{id}/vote/`       | Vote on project        |
| POST   | `/api/v1/projects/{id}/transition/` | Change project status  |

---

## Create Project

**POST** `/api/v1/projects/`

Headers:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Request Body:

```json
{
  "title": "Traffic Optimization System",
  "problem_statement": "Traffic congestion in Nairobi",
  "proposed_solution": "Smart traffic light control",
  "sector": "transport",
  "proposal_deadline": "2025-02-01",
  "community_id": 1
}
```

Responses:

* `201 Created`
* `400 Validation error`

---

## List Projects

**GET** `/api/v1/projects/`

Query Params (optional):

* `sector`
* `status`
* `community_id`

Response:

* `200 OK`

---

## Retrieve Single Project

**GET** `/api/v1/projects/{id}/`

Responses:

* `200 OK`
* `404 Not Found`

---

## Update Project

**PUT** `/api/v1/projects/{id}/`

Authorization:

* Owner only

Request Body (partial allowed):

```json
{
  "title": "Updated Project Title"
}
```

Responses:

* `200 OK`
* `403 Forbidden`

---

## Vote on Project

**POST** `/api/v1/projects/{id}/vote/`

Request Body:

```json
{
  "value": 1
}
```

Rules:

* `value`: `1` (upvote) or `-1` (downvote)
* Vote can be changed
* Voting closed after `proposal_deadline`

Responses:

* `200 OK`
* `400 Voting closed`
```json
{
  "message": "Vote cast successfully",
  "new_score": 5,
  "user_vote": 1
}

```
Update Existing Vote
```json
{
  "message": "Vote updated",
  "new_score": 3,
  "user_vote": -1
}
```
Remove Vote (same vote toggled)
```json
{
  "message": "Vote removed",
  "new_score": 2,
  "user_vote": null
}

```
Error (Voting Closed)
```json
{
  "message": "Voting period has ended"
}

```

---

## Transition Project Status

**POST** `/api/v1/projects/{id}/transition/`

Request Body:

```json
{
  "status": "APPROVED"
}
```

Allowed Transitions:

* `PROPOSED → APPROVED`
* `APPROVED → ACTIVE`
* `ACTIVE → COMPLETED`

Responses:

* `200 OK`
* `400 Invalid transition`

---

## Withdraw (Delete) Project

**DELETE** `/api/v1/projects/{id}/`

Authorization:

* Owner only

Responses:

* `200 OK`
* `403 Forbidden`

---

## Test Datasets (Thunder Client)

### Seed Projects

```json
[
  {
    "title": "Digital Health Records",
    "problem_statement": "Fragmented patient data",
    "proposed_solution": "Open-source EHR",
    "sector": "health",
    "proposal_deadline": "2025-02-01",
    "community_id": 1
  },
  {
    "title": "School Management System",
    "problem_statement": "Manual school records",
    "proposed_solution": "Cloud ERP",
    "sector": "education",
    "proposal_deadline": "2025-01-15",
    "community_id": 2
  }
]
```
---

## Contributor Notes

* All endpoints are class-based resources
* Authorization is enforced at service layer
* No hard deletes outside owner scope
* Status transitions are strictly validated

