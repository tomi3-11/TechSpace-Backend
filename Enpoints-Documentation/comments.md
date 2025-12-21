# Comments Blueprint API Documentation

This document describes the **Comments Blueprint** for the backend API. It is intended for **frontend developers**, **API consumers**, and **contributors** who need to understand how to interact with the comments system and how to test it locally.

---

## 1. Overview

The Comments Blueprint enables **flat and nested (threaded) discussions** on posts. It supports:

* Creating comments on posts
* Replying to comments (nested threads)
* Retrieving comments for a post (with replies)
* Updating and deleting comments (author-only)

All write operations require **JWT authentication**.

---

## 2. Blueprint Information

* **Blueprint name:** `comments`
* **URL prefix:** `/api/comments`
* **Authentication:** JWT (`Access Token`)

---

## 3. Related Blueprints

| Blueprint   | Purpose                            |
| ----------- | ---------------------------------- |
| Auth        | User authentication and JWT tokens |
| Communities | Community grouping of posts        |
| Posts       | Parent entity for comments         |
| Comments    | Discussion threads under posts     |

---

## 4. Data Model (Logical)

### Comment

| Field      | Type              | Description                  |
| ---------- | ----------------- | ---------------------------- |
| id         | integer           | Comment ID                   |
| content    | text              | Comment body                 |
| post_id    | integer           | Associated post              |
| author_id  | integer           | User who created the comment |
| parent_id  | integer, nullable | Parent comment (for replies) |
| created_at | datetime          | Creation timestamp           |
| updated_at | datetime          | Last update timestamp        |

**Threading logic:**

* `parent_id = null` → top-level comment
* `parent_id = <comment_id>` → reply

---

## 5. Authentication

Include the access token in all protected requests:

```
Authorization: Bearer <access_token>
```

---

## 6. API Endpoints

### 6.1 Create a Comment on a Post

**POST** `/api/v1/comments/post/{post_id}`

**Auth required:** Yes

**Request body:**

```json
{
  "content": "This is a comment"
}
```

**Success response (201):**

```json
{
  "id": 10,
  "content": "This is a comment",
  "author": "alice",
  "post_id": 1,
  "parent_id": null,
  "created_at": "2025-12-21T10:00:00",
  "replies": []
}
```

---

### 6.2 Get Comments for a Post (Flat + Nested)

**GET** `/api/v1/comments/post/{post_id}`

**Auth required:** No

**Description:**
Returns all **top-level comments**, each including nested replies recursively.

**Success response (200):**

```json
[
  {
    "id": 1,
    "content": "Top-level comment",
    "author": "alice",
    "post_id": 1,
    "parent_id": null,
    "created_at": "2025-12-21T01:00:00",
    "replies": [
      {
        "id": 2,
        "content": "Reply to comment",
        "author": "bob",
        "post_id": 1,
        "parent_id": 1,
        "created_at": "2025-12-21T02:00:00",
        "replies": []
      }
    ]
  }
]
```

---

### 6.3 Reply to a Comment

**POST** `/api/v1/comments/{comment_id}/replies`

**Auth required:** Yes

**Request body:**

```json
{
  "content": "This is a reply"
}
```

**Success response (201):**

```json
{
  "id": 11,
  "content": "This is a reply",
  "author": "bob",
  "post_id": 1,
  "parent_id": 1,
  "created_at": "2025-12-21T11:00:00",
  "replies": []
}
```

---

### 6.4 Update a Comment

**PUT** `/api/v1/comments/{comment_id}`

**Auth required:** Yes (author only)

**Request body:**

```json
{
  "content": "Updated comment text"
}
```

**Success response (200):** Updated comment object

---

### 6.5 Delete a Comment

**DELETE** `/api/v1/comments/{comment_id}`

**Auth required:** Yes (author only)

**Success response (200):**

```json
{
  "message": "Comment deleted successfully"
}
```

---


---

## 7. Error Handling

| Status | Meaning                   |
| ------ | ------------------------- |
| 401    | Missing or invalid token  |
| 403    | Not comment owner         |
| 404    | Comment or post not found |

---

## 8. Contribution Notes

* Keep business logic in `service.py`
* Resources should remain thin
* Do not add chat or real-time logic here
* Maintain recursive reply structure

