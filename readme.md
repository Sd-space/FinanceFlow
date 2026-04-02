# 🚀 FinanceFlow Backend (FastAPI)

## 📌 Overview

FinanceFlow is a backend system for managing financial records with **role-based access control (RBAC)** and **analytics-driven dashboard APIs**.

The system enables multiple user roles to interact with financial data securely while providing aggregated insights such as totals, category breakdowns, and trends.

This project focuses on **backend engineering fundamentals**:

* Clean API design
* Secure authentication
* Role-based authorization
* Structured data modeling
* Aggregation & analytics

---

## 🎯 Problem Statement

In real-world finance systems, different users require **controlled access** to financial data:

* Stakeholders → view summaries only
* Analysts → explore data and insights
* Admins → manage data and users

This backend solves that by implementing:

* Controlled access using RBAC
* Structured financial record management
* Efficient data aggregation for dashboards

---

## 🧱 Tech Stack

| Component         | Technology               |
| ----------------- | ------------------------ |
| Backend Framework | FastAPI                  |
| Database          | SQLite (SQLAlchemy ORM)  |
| Authentication    | JWT (JSON Web Tokens)    |
| Password Hashing  | Passlib (bcrypt)         |
| Validation        | Pydantic                 |
| API Docs          | Swagger (auto-generated) |

---

## 🏗️ Architecture Overview

The project follows a **modular layered architecture**:

```id="archflow1"
Client → Routes → Dependencies (Auth/RBAC) → Services → Models → Database
```

### Layers:

* **Routes** → API endpoints
* **Schemas** → Request/response validation
* **Models** → Database schema
* **Dependencies** → Auth & RBAC logic
* **Core** → Security & configuration

---

## 📁 Project Structure

```id="projstruct1"
financeflow/
 ├── app/
 │    ├── main.py              # Entry point
 │    ├── database.py          # DB connection
 │    ├── models/              # SQLAlchemy models
 │    ├── schemas/             # Pydantic schemas
 │    ├── routes/              # API endpoints
 │    ├── dependencies/        # Auth & RBAC
 │    ├── services/            # Business logic (optional)
 │    └── core/                # Security & config
```

---

## 🔐 Authentication (JWT)

### Flow

```id="authflow1"
Register → Login → Generate JWT → Access Protected Routes
```

### Implementation Details

* Passwords are hashed using bcrypt
* JWT contains:

```json id="jwt1"
{
  "sub": "user_id",
  "exp": "expiration_time"
}
```

* Token is validated on every request

---

## 🛡️ Authorization (RBAC)

### Roles

| Role    | Capabilities                  |
| ------- | ----------------------------- |
| Admin   | Full CRUD + user management   |
| Analyst | Read transactions + analytics |
| Viewer  | Dashboard access only         |

---

### Design Approach

RBAC is implemented using **FastAPI dependencies**:

```id="rbacflow1"
Request → get_current_user → require_role → Allow / Deny
```

### Key Design Decision

Roles are **not stored in JWT**, instead:

```id="rbacflow2"
JWT → user_id → fetch user from DB → get latest role
```
“Roles are fetched dynamically from the database on each request to ensure real-time access control without requiring token refresh.”

✔ Ensures real-time role updates
✔ Avoids stale authorization data

---

## 👤 User Management APIs

| Method | Endpoint         | Description                     |
| ------ | ---------------- | ------------------------------- |
| POST   | `/auth/register` | Create new user                 |
| POST   | `/auth/login`    | Authenticate user               |
| GET    | `/users`         | List users (Admin only)         |
| PATCH  | `/users/{id}`    | Update role/status (Admin only) |

---

## 💰 Transaction Management

### Data Model

Each transaction includes:

```id="txnmodel1"
amount
type (income / expense)
category
date
note
```

---

### CRUD APIs

| Method | Endpoint             | Access         |
| ------ | -------------------- | -------------- |
| POST   | `/transactions`      | Admin          |
| GET    | `/transactions`      | Admin, Analyst |
| GET    | `/transactions/{id}` | Admin, Analyst |
| PUT    | `/transactions/{id}` | Admin          |
| DELETE | `/transactions/{id}` | Admin          |

---

### 🔍 Filtering & Pagination

Supports:

* Filter by type
* Filter by category
* Date range filtering
* Pagination (`limit`, `offset`)

Example:

```id="txnfilter1"
/transactions?type=expense&category=food&limit=10
```

---

## 📊 Dashboard Analytics APIs

This is the **core differentiator** of the project.

---

### 1. Summary

`GET /dashboard/summary`

Returns:

```json id="dash1"
{
  "total_income": 5000,
  "total_expense": 2000,
  "net_balance": 3000
}
```

---

### 2. Category Breakdown

`GET /dashboard/category-breakdown`

Returns:

```json id="dash2"
{
  "food": 2000,
  "salary": 5000
}
```

---

### 3. Monthly Trends

`GET /dashboard/monthly-trends`

Returns:

```json id="dash3"
{
  "1": { "income": 5000, "expense": 2000 },
  "2": { "income": 7000, "expense": 3000 }
}
```

---

### 4. Recent Transactions

`GET /dashboard/recent`

Returns latest 5 records.

---

## ⚠️ Validation & Error Handling

Handled using Pydantic + FastAPI:

| Status | Meaning               |
| ------ | --------------------- |
| 400    | Invalid input         |
| 401    | Authentication failed |
| 403    | Unauthorized action   |
| 404    | Resource not found    |

---

## 🧪 Testing Strategy

### Using Swagger UI

1. Register user
2. Login
3. Click **Authorize**
4. Enter credentials
5. Test endpoints

---

### Role Testing

| Scenario                   | Expected Result |
| -------------------------- | --------------- |
| Viewer creates transaction | ❌ 403           |
| Analyst reads data         | ✅               |
| Admin deletes record       | ✅               |

---

## 🧠 Key Engineering Decisions

### 1. SQLite for Development

* Zero setup
* Easy testing
* Replaceable with PostgreSQL

---

### 2. SQLAlchemy ORM

* Clean abstraction
* Maintainable queries
* Supports aggregation

---

### 3. Dependency-Based RBAC

* Centralized logic
* Reusable across routes
* Easy to extend

---

### 4. Aggregation Queries

Used SQL functions:

* `SUM()`
* `GROUP BY`
* `EXTRACT()`

---

## 🚀 Setup Instructions

### 1. Create virtual environment

```bash id="setup1"
python -m venv venv
source venv/bin/activate
```

---

### 2. Install dependencies

```bash id="setup2"
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt] email-validator
```

---

### 3. Run server

```bash id="setup3"
uvicorn app.main:app --reload
```

---

### 4. Access docs

```id="setup4"
http://127.0.0.1:8000/docs
```

---

## 🏆 Highlights

* Secure JWT authentication
* Real-time RBAC system
* Advanced filtering and pagination
* Analytics-driven backend
* Clean and modular architecture

---

## 📌 Conclusion

FinanceFlow demonstrates a **complete backend system** with:

* Secure user management
* Structured financial data handling
* Role-based access control
* Insightful analytics

The implementation emphasizes **clarity, maintainability, and real-world backend practices**, making it a strong foundation for scalable systems.
