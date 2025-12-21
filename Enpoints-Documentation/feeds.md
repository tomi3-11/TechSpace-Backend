# Feeds Blueprint – API Documentation

This document describes the **Feeds blueprint** for the community-driven developer platform backend. It is intended for:

* Frontend developers consuming the API
* Backend contributors testing and extending the system
* QA and reviewers validating behavior

The Feeds blueprint **does not create data**. It aggregates data from existing blueprints:

* Auth
* Communities
* Posts
* Votes

---

## 1. Purpose of the Feeds Blueprint

The Feeds blueprint provides **read-only endpoints** that generate curated timelines of posts for users. It mirrors the core idea of Reddit-like feeds while aligning with the project vision:

* Surface relevant discussions
* Promote high-impact, community-approved content
* Enable discovery of projects and ideas

Feeds are computed dynamically from the database.

---

## 2. Blueprint Registration

**Blueprint Name:** `feeds`

**URL Prefix:**

```
/api/v1/feeds/
```

---

## 3. Data Sources (Dependencies)

Feeds aggregate data from the following models:

* `Post`
* `Community`
* `User`
* `Vote`

There are **no Feed tables** in the database.

---

## 4. Endpoints Overview

| Endpoint                    | Method | Auth | Description                          |
| --------------------------- | ------ | ---- | ------------------------------------ |
| `/latest/`                   | GET    | NO    | Latest posts across all communities  |
| `/top/`                      | GET    | NO    | Top posts ranked by vote score       |
| `/community/<community_id>/` | GET    | NO    | Latest posts in a specific community |

---

## 5. Endpoint Details

### 5.1 Get Latest Posts Feed

**Request**

```
GET /api/v1/feeds/latest/
```

**Query Parameters (optional)**

| Parameter  | Type | Default | Description     |
| ---------- | ---- | ------- | --------------- |
| `page`     | int  | 1       | Pagination page |
| `per_page` | int  | 20      | Items per page  |

**Response (200)**

```json
{
  "page": 1,
  "per_page": 20,
  "total": 42,
  "items": [
    {
      "id": 10,
      "title": "Digitizing Rural Clinics",
      "content": "Proposal for health system upgrades",
      "author": "alice",
      "community": "t/kenya-dev",
      "vote_score": 15,
      "created_at": "2025-01-20T10:15:00Z"
    }
  ]
}
```

---

### 5.2 Get Top Posts Feed

**Request**

```
GET /api/v1/feeds/top/
```

**Query Parameters (optional)**

| Parameter    | Type   | Default | Description                   |
| ------------ | ------ | ------- | ----------------------------- |
| `page`       | int    | 1       | Pagination page               |
| `per_page`   | int    | 20      | Items per page                |
| `time_range` | string | `all`   | `day`, `week`, `month`, `all` |

**Ranking Logic**

* Ordered by `vote_score DESC`
* Secondary order: `created_at DESC`

**Response (200)**

```json
{
  "page": 1,
  "per_page": 20,
  "total": 18,
  "items": [
    {
      "id": 3,
      "title": "Open-source School ERP",
      "vote_score": 42,
      "community": "t/education-tech",
      "created_at": "2025-01-15T09:00:00Z"
    }
  ]
}
```

---

### 5.3 Get Community Feed

**Request**

```
GET /api/v1/feeds/community/<community_id>/
```

**Example**

```
GET /api/v1/feeds/community/1/
```

**Response (200)**

```json
{
  "community": "t/kenya-dev",
  "items": [
    {
      "id": 5,
      "title": "Traffic System Optimization",
      "vote_score": 9,
      "author": "bob"
    }
  ]
}
```

---

## 6. Authentication & Authorization

* Feeds are **publicly accessible**
* No JWT required
* User-specific feeds may be introduced later

---

## 7. Error Responses

| Status | Meaning                  |
| ------ | ------------------------ |
| 400    | Invalid query parameters |
| 404    | Community not found      |
| 500    | Server error             |

---

## 8. Testing Guide (Thunder Client / Postman)

### 8.1 Test Dataset Prerequisites

Ensure the following exist:

* At least 2 users
* At least 2 communities
* At least 5 posts
* Votes applied to posts

---

### 8.2 Sample Thunder Client Requests

#### Latest Feed

```
GET http://localhost:5000/api/v1/feeds/latest?page=1&per_page=10/
```

#### Top Feed

```
GET http://localhost:5000/api/v1/feeds/top?time_range=week/
```

#### Community Feed

```
GET http://localhost:5000/api/v1/feeds/community/1/
```


## 9. Design Notes for Contributors

* Feeds are **derived views**, not persisted
* All logic lives in `feeds/service.py`
* Resources remain thin and stateless
* Easy to extend for:

  * Personalized feeds
  * Project feeds
  * Search-based feeds

---

## 10. Related Blueprints

| Blueprint   | Purpose                 |
| ----------- | ----------------------- |
| Auth        | Authentication & tokens |
| Communities | Community organization  |
| Posts       | Core content            |
| Votes       | Ranking mechanism       |
| Comments    | Discussion threads      |
