<<<<<<< HEAD
# Mini Logistics & Order Management System (OMS)

> Enterprise-inspired full-stack Order Management System built with **FastAPI + Oracle + React + Vite** implementing JWT authentication, RBAC authorization, FSM workflow validation, audit trails, shipment tracking, and responsive operational dashboards.

---

# 🚀 Project Overview

This project simulates a production-style logistics and order management workflow where:

* Customers create and manage orders
* Admins control operational transitions
* FSM workflows validate legal order state changes
* Audit trails record all status transitions
* RBAC secures privileged operations
* Responsive dashboards provide operational visibility

The system is designed using a clean layered backend architecture:

```text
Router → Service → Repository → Database
```

---

# 🏗️ Tech Stack

## Backend

* FastAPI
* SQLAlchemy ORM
* Oracle Database
* Alembic
* JWT Authentication
* Passlib (bcrypt)
* Pydantic
* Pytest

## Frontend

* React 18
* Vite
* React Router
* Axios
* TailwindCSS
* Context API

---

# ✨ Features

## 🔐 Authentication & Security

* JWT-based authentication
* User registration & login
* Password hashing with bcrypt
* Protected API routes
* Role-based access control (RBAC)
* Ownership validation
* Secure response serialization

---

## 📦 Order Management

* Create orders
* List user orders
* Pagination support
* Status filtering
* Admin order search
* Order detail drawer
* Responsive order table/cards

---

## 🔄 FSM Workflow

```text
PENDING
  ├──→ CONFIRMED
  │        └──→ SHIPPED
  │                 └──→ DELIVERED
  │
  └──→ CANCELLED
```

### FSM Enforcement

* Service-layer validation
* Invalid transition prevention
* Immutable audit logging
* Admin-only transitions

---

## 📊 Dashboard Features

* KPI cards
* Shipment progress tracking
* Recent activity feed
* Audit timeline
* Pending confirmations queue
* Recently delivered queue

---

## 📜 Audit Trail

Every order transition is recorded with:

* Previous status
* New status
* Actor information
* Timestamp
* Transition reason

---

# 🧱 Architecture

## Backend Structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── tests/
└── requirements.txt
```

---

## Frontend Structure

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── context/
│   ├── hooks/
│   ├── layouts/
│   ├── routes/
│   └── utils/
├── public/
└── package.json
```

---

# 🗄️ Database Schema

## users

| Column          | Description        |
| --------------- | ------------------ |
| id              | Primary Key        |
| email           | Unique Email       |
| hashed_password | Encrypted Password |
| role            | USER / ADMIN       |
| is_active       | Active Status      |

---

## orders

| Column      | Description       |
| ----------- | ----------------- |
| id          | Primary Key       |
| external_id | Public Order ID   |
| status      | FSM Status        |
| customer_id | User Reference    |
| created_at  | Created Timestamp |

---

## order_status_events

| Column      | Description       |
| ----------- | ----------------- |
| id          | Primary Key       |
| order_id    | Order Reference   |
| from_status | Previous State    |
| to_status   | New State         |
| actor_id    | Transition Actor  |
| reason      | Transition Reason |
| created_at  | Timestamp         |

---

# 🔌 API Endpoints

## Auth

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

---

## Orders

```http
POST   /api/v1/orders/
GET    /api/v1/orders/my
PATCH  /api/v1/orders/{order_id}/status/{target_status}
```

---

## Health

```http
GET /healthz
```

---

# ⚙️ Local Development Setup

# 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/mini-logistics-oms.git
cd mini-logistics-oms
```

---

# 2️⃣ Backend Setup

```bash
cd backend
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create `.env`

```env
DB_HOST=localhost
DB_PORT=1521
DB_NAME=XE
DB_USER=your_user
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# 3️⃣ Frontend Setup

```bash
cd frontend
npm install
```

---

## Create `.env`

```env
VITE_API_BASE=http://localhost:8000/api/v1
```

---

## Run Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# 🧪 Testing

## Backend Tests

```bash
cd backend
pytest tests/service/test_order_service.py -v
```

---

# 🚀 Deployment

# Frontend Deployment (Recommended)

Deploy frontend on:

* [https://vercel.com](https://vercel.com)

---

# Backend Deployment (Recommended)

Deploy FastAPI backend on:

* [https://render.com](https://render.com)
  OR
* [https://railway.app](https://railway.app)

---

# Oracle Database

Use:

* Oracle XE
* Oracle Cloud Free Tier
* Local Oracle Installation

---

# 🔒 Security Features

* JWT authentication
* Password hashing
* Protected routes
* RBAC enforcement
* FSM validation
* Ownership checks
* Hidden sensitive fields
* Centralized exception handling

---

# 📱 UI/UX Features

* Responsive design
* Mobile-friendly layouts
* Toast notifications
* Skeleton loaders
* Empty states
* Keyboard accessibility
* Semantic status colors

---

# 📌 Future Improvements

* WebSocket live updates
* Email notifications
* PDF exports
* Advanced analytics
* CI/CD pipelines
* Docker production deployment
* Kubernetes support
* Monitoring & observability

---

# 📷 Suggested GitHub Screenshots

Add screenshots for:

* Swagger API Docs
* Dashboard
* Orders Page
* Shipment Tracking
* Admin Transitions
* Audit Timeline

---

# ✅ Project Status

| Module             | Status     |
| ------------------ | ---------- |
| Backend API        | ✅ Complete |
| Oracle Integration | ✅ Complete |
| JWT Auth           | ✅ Complete |
| RBAC               | ✅ Complete |
| FSM Workflow       | ✅ Complete |
| Frontend UI        | ✅ Complete |
| Swagger Docs       | ✅ Complete |
| Audit Trails       | ✅ Complete |

---

# 🎯 Assessment Highlights

* Production-inspired backend architecture
* Enterprise RBAC implementation
* FSM workflow validation
* Oracle database integration
* Clean layered architecture
* Secure API design
* Recruiter-ready implementation

---

# 👨‍💻 Author

PARVATHAM BHAVANA RUSHI 

Built using:

* FastAPI
* Oracle Database
* React
* Vite
* TailwindCSS

---

# 📄 References

Project implementation details derived from uploaded engineering and implementation documents:

*ENGINEERING DOCUMENTATION.pdf*

*
*
=======
# mini-logistics-oms
Production-style Mini Logistics &amp; Order Management System with JWT authentication, RBAC, FSM workflow, FastAPI backend, React frontend, Swagger APIs, and layered architecture.
>>>>>>> b4df4be677c5eb0dfaea773f00097460e174e0d6
