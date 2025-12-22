# Project Applications API Documentation

Audience:

* Frontend developers consuming the API
* Backend contributors testing, maintaining, or extending the system

This document describes the **Project Applications blueprint**: how users apply to projects, how applications are reviewed, and how access is governed.

All endpoints are aligned with the current implementation and tested using **Thunder Client**.

---

## Base Information

* Base Path: `/api/v1/applications/`
* Authentication: **JWT (Access Token)**
* Header:

  ```
  Authorization: Bearer <ACCESS_TOKEN>
  ```
* Content-Type: `application/json`

---

## Conceptual Overview

Project Applications enable structured, community-driven collaboration on approved projects.

Lifecycle:

```
USER → APPLY → PENDING → ACCEPTED / REJECTED
```

Rules:

* Only projects with status `APPROVED` or `ACTIVE` accept applications
* A user can apply **once per project**
* Applications are reviewed by:

  * Project owner
  * Moderator
  * Admin
* Accepted users gain access to project collaboration areas (future scope)

---

## Application Model (Response Shape)

```json
{
  "id": 12,
  "user_id": 4,
  "project_id": 7,
  "motivation": "I want to contribute to public digital infrastructure",
  "skills": "Python, Flask, PostgreSQL",
  "status": "PENDING",
  "reviewed_by_id": null,
  "reviewed_at": null,
  "created_at": "2025-01-12T14:30:00Z"
}
```

---

## Endpoints Overview

| Method | Endpoint                                                       | Description                     | Auth | Role                |
| ------ | -------------------------------------------------------------- | ------------------------------- | ---- | ------------------- |
| POST   | `/projects/{project_id}/applications/`                         | Apply to a project              | YES    | User                |
| GET    | `/projects/{project_id}/applications/`                         | List applications for a project | YES    | Owner / Mod / Admin |
| POST   | `/projects/{project_id}/applications/{application_id}/review/` | Review application              | YES    | Owner / Mod / Admin |
| GET    | `/applications/mine/`                                          | Current user applications       | YES    | User                |

---

## Apply to Project

**POST** `/projects/{project_id}/applications/`

Headers:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Request Body:

```json
{
  "motivation": "I want to help build open-source solutions",
  "skills": "Flask, API design, SQL"
}
```

Success Response:

* `201 Created`

Error Responses:

* `400 Project not accepting applications`
* `400 User has already applied`

---

## List Applications for a Project

**GET** `/projects/{project_id}/applications/`

Authorization:

* Project owner
* Moderator
* Admin

Success Response:

* `200 OK`

```json
[
  {
    "id": 12,
    "user_id": 4,
    "status": "PENDING",
    "created_at": "2025-01-12T14:30:00Z"
  }
]
```

Error Responses:

* `403 Not authorized`

---

## Review Application (Accept / Reject)

**POST** `/projects/{project_id}/applications/{application_id}/review/`

Request Body:

```json
{
  "status": "ACCEPTED"
}
```

Allowed Values:

* `ACCEPTED`
* `REJECTED`

Success Response:

* `200 OK`

Error Responses:

* `403 Not authorized`
* `400 Invalid decision`

---

## Current User Applications

**GET** `/applications/mine/`

Success Response:

* `200 OK`

```json
[
  {
    "project_id": 7,
    "status": "PENDING"
  }
]
```

---

## Thunder Client Test Datasets

### Apply to Project

```json
{
  "motivation": "I want to contribute to national digital systems",
  "skills": "Backend development, system design"
}
```

---

### Review Application

```json
{
  "status": "ACCEPTED"
}
```

---

## Testing Notes for Contributors

* Use seeded users with different roles (USER, MODERATOR, ADMIN)
* Verify role-based access control
* Verify duplicate application prevention
* Verify state transitions

---

## Contributor Guidelines

* Authorization checks live in the **service layer**
* Resources remain thin and declarative
* Do not expose review endpoints to normal users
* Do not bypass project status checks

