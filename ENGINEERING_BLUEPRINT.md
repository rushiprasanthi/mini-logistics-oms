# Engineering Intelligence Blueprint
## Mini Logistics & Order Management System (OMS)
### Production-Grade Architecture Reference · v1.0

> Synthesized from: Business Workflow Research · Backend Architecture Research · Database Research ·  
> API Design Research · Authentication & Security Research · Frontend UX Research · DevOps Research ·  
> Requirements Gap Analysis PDF

---

## Table of Contents

1. [Executive Project Analysis](#1-executive-project-analysis)
2. [Functional & Non-Functional Requirements](#2-functional--non-functional-requirements)
3. [Production-Grade Architecture Design](#3-production-grade-architecture-design)
4. [Advanced Data Architecture](#4-advanced-data-architecture)
5. [API & Backend Engineering Blueprint](#5-api--backend-engineering-blueprint)
6. [End-to-End Execution Workflow](#6-end-to-end-execution-workflow)
7. [Engineering Decision Analysis](#7-engineering-decision-analysis)
8. [Scalability & Production Evolution](#8-scalability--production-evolution)
9. [AI-Assisted Development Structuring](#9-ai-assisted-development-structuring)
10. [Step-by-Step Implementation Roadmap](#10-step-by-step-implementation-roadmap)
11. [README & GitHub Presentation Blueprint](#11-readme--github-presentation-blueprint)
12. [Final Engineering Checklist](#12-final-engineering-checklist)

---

## 1. Executive Project Analysis

### 1.1 Project Purpose

This project is a **production-modeled logistics and order management system (OMS)** — not a CRUD form application. It replicates the core operational patterns used by platforms like Amazon Seller Central, Shopify Admin, and Delhivery: a workflow orchestration engine that coordinates order intake, status transitions, fulfillment tracking, admin operations, and audit history across multiple user roles.

### 1.2 Business / Domain Understanding

An OMS is responsible for:

| Domain Concern | Operational Role |
|---|---|
| Order intake & validation | Verify, deduplicate, and initialize orders |
| Status lifecycle management | Enforce FSM transitions across workflow stages |
| Fulfillment tracking | Coordinate shipment from creation to delivery |
| Admin workflow operations | Status overrides, audit visibility, order investigation |
| Customer self-service | Create, view, and cancel own orders |
| Audit trail | Immutable, actor-attributed history of every state change |
| RBAC enforcement | Role-differentiated access across all surfaces |

### 1.3 Core Engineering Objectives

1. Implement a **strict finite state machine (FSM)** for order lifecycle management
2. Enforce **layered backend architecture** — Router → Middleware → Service → Repository → Database
3. Build **immutable audit history** as a first-class data entity
4. Design **consistent, versioned REST APIs** with standardized response envelopes
5. Implement **JWT + RBAC** authentication and authorization across all routes
6. Create an **operational frontend** optimized for workflow throughput, not decorative aesthetics
7. Deliver **Dockerized deployment** with environment isolation and health monitoring

### 1.4 Real-World Problem Being Solved

Without architectural discipline, OMS systems degrade into:
- Duplicate shipments from unvalidated status transitions
- Inventory corruption from race-condition-prone writes
- Impossible debugging due to missing audit history
- Security gaps from frontend-only RBAC enforcement
- Fragile APIs that break frontend integrations across changes

This system solves those problems through explicit state machines, layered validation, immutable events, and middleware-enforced security.

### 1.5 Technical Complexity Assessment

| Dimension | Complexity | Notes |
|---|---|---|
| Workflow logic | High | FSM with exception paths (failed, returned, cancelled) |
| Authentication | Medium-High | JWT + refresh tokens + RBAC + ownership validation |
| Database design | High | Hybrid current-state + immutable event tables |
| API contract design | Medium-High | Versioned, paginated, filterable, error-consistent |
| Frontend architecture | Medium | Operational dashboard with timeline, table, and UX systems |
| Deployment | Medium | Docker Compose + Vercel + Render with env separation |

### 1.6 Hidden / Implied Requirements

From the gap analysis PDF, the following are inferred as **required even if unstated**:

- Order ID must be a unique, human-readable identifier (e.g., `ORD-2026-XXXXX`) not just a UUID
- All admin status updates must write to `order_status_events` — logging is non-optional
- Customers must **not** be able to access another customer's orders (ownership enforcement)
- API errors must never expose stack traces, SQL details, or internal paths
- Pagination is mandatory on all list endpoints — returning unbounded result sets is a bug, not a feature

### 1.7 Architectural Pressure Points

| Pressure Point | Risk | Mitigation |
|---|---|---|
| FSM enforcement location | Business rules scattered into controllers | FSM lives exclusively in service layer |
| Audit history completeness | Missing events break forensic debugging | Every status mutation triggers an event insert |
| JWT secret management | Hardcoded secrets = credential exposure | Runtime env injection, never committed |
| Concurrent order writes | Race conditions → inventory corruption | Row-level locking in PostgreSQL |
| API contract drift | Frontend breaks silently | Versioned prefix `/api/v1/`, additive-only changes |

---

## 2. Functional & Non-Functional Requirements

### 2.1 Functional Requirements

#### Authentication & Identity

- Users register with email/password; passwords stored as Argon2/bcrypt hashes
- JWT access token issued on login; short-lived (15 min recommended)
- Refresh token issued on login; longer-lived (7–30 days), rotation on use
- Logout must revoke refresh token server-side
- Two roles: `CUSTOMER`, `ADMIN`

#### Customer Workflows

- Create an order (pickup address, delivery address, package details)
- View list of own orders (paginated, filterable by status)
- View individual order detail with full status timeline
- Cancel an order if status allows (`PENDING` → `CANCELLED`, `CONFIRMED` → `CANCELLED`)

#### Admin Workflows

- View all orders (paginated, filterable, sortable, searchable)
- Update order status (FSM-validated transitions)
- View complete audit history for any order (actor-attributed, timestamped)
- Cannot create orders; manages existing workflow

#### Status Lifecycle (FSM)

```
PENDING → CONFIRMED → SHIPPED → DELIVERED
    ↓           ↓
CANCELLED   CANCELLED

DELIVERED → RETURNED (optional)
RETURNED  → REFUNDED (optional)
Any state → FAILED (system-triggered)
```

Blocked transitions: Any reversal to earlier states (e.g., `DELIVERED → PENDING`), any skip transitions (e.g., `PENDING → SHIPPED`).

#### API Layer

- REST APIs with versioned prefix `/api/v1/`
- Consistent response envelope (`success`, `data`, `error`, `meta`)
- Standard pagination contract (`page`, `page_size`, `total`, `next_cursor`)
- Centralized error handling — no raw exceptions reach response
- Input validation via Pydantic at request boundary

#### Frontend

- Responsive admin dashboard: KPI cards, order table, filtering, pagination
- Customer portal: order list, order detail with shipment timeline
- Skeleton loaders, toast notifications, inline validation errors
- Auth flow: login, register, protected routes with redirect

### 2.2 Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Security** | HTTPS everywhere, CORS restricted to trusted origins, JWT expiration enforced, RBAC server-side |
| **Reliability** | Database transactions for order creation + audit event (atomic writes) |
| **Maintainability** | Layered architecture, no DB access in routers, no business logic in repositories |
| **Observability** | Structured audit logs, correlation IDs on requests, health endpoint |
| **Scalability** | Indexed filterable columns, cursor-ready pagination, no N+1 queries |
| **Portability** | Docker Compose for local dev, environment-variable-driven config |
| **Extensibility** | Service layer isolates business logic; swap repositories without touching services |

---

## 3. Production-Grade Architecture Design

### 3.1 System Architecture Overview

```
┌─────────────────────────────────────┐
│           FRONTEND (Next.js)        │
│   Admin Dashboard | Customer Portal │
│   React Query | Tailwind | shadcn   │
└─────────────────┬───────────────────┘
                  │  HTTPS / REST API
┌─────────────────▼───────────────────┐
│           FASTAPI BACKEND           │
│                                     │
│  ┌──────────────────────────────┐   │
│  │       Router Layer           │   │
│  │  /api/v1/auth  /orders       │   │
│  │  /api/v1/admin /shipments    │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│  ┌──────────▼───────────────────┐   │
│  │      Middleware Stack        │   │
│  │  JWT Auth | RBAC | CORS      │   │
│  │  RateLimit | RequestID       │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│  ┌──────────▼───────────────────┐   │
│  │       Service Layer          │   │
│  │  OrderService | AuthService  │   │
│  │  ShipmentService | AuditSvc  │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│  ┌──────────▼───────────────────┐   │
│  │     Repository Layer         │   │
│  │  OrderRepo | UserRepo        │   │
│  │  ShipmentRepo | AuditRepo    │   │
│  └──────────┬───────────────────┘   │
└────────────┬┴──────────────────────-┘
             │
┌────────────▼────────────────────────┐
│           DATA LAYER                │
│                                     │
│   PostgreSQL (primary store)        │
│   Redis     (cache / sessions)      │
└─────────────────────────────────────┘
```

### 3.2 Frontend Layer

| Concern | Technology | Rationale |
|---|---|---|
| Framework | Next.js (App Router) | SSR for authenticated dashboards; static for auth pages |
| Styling | Tailwind CSS | Utility-first; works with shadcn component primitives |
| Components | shadcn/ui | Accessible, composable, production-grade primitives |
| Data fetching | React Query (TanStack Query) | Server-state management, caching, retry, background refetch |
| Tables | TanStack Table | Virtualized, filterable, sortable without re-renders |
| Charts | Recharts | KPI cards, order-volume sparklines |
| Auth state | Zustand or Context | Lightweight JWT/session management |

**Rendering strategy:**
- Auth pages: Static (no server data needed)
- Customer dashboard: SSR with session validation
- Admin dashboard: SSR with admin token validation
- Order detail: SSR with ownership/admin check

### 3.3 Backend Layer

**Request lifecycle:**

```
HTTP Request
    ↓
CORS Middleware
    ↓
Rate Limiting Middleware
    ↓
JWT Authentication Middleware
    ↓
Router (thin — parse + delegate)
    ↓
Pydantic Request Validation (auto via FastAPI)
    ↓
Service Layer (business logic + FSM + audit)
    ↓
Repository Layer (DB queries, no logic)
    ↓
PostgreSQL (ACID transaction)
    ↓
Response Serialization (Pydantic schema)
    ↓
HTTP Response (standardized envelope)
```

**Module layout:**

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── orders.py
│   │   │   ├── admin/
│   │   │   │   ├── orders.py
│   │   │   │   └── audit.py
│   │   │   └── shipments.py
│   ├── middleware/
│   │   ├── auth.py         # JWT decode + inject current_user
│   │   ├── rbac.py         # Role enforcement decorators
│   │   ├── rate_limit.py
│   │   └── request_id.py
│   ├── services/
│   │   ├── order_service.py
│   │   ├── auth_service.py
│   │   ├── shipment_service.py
│   │   └── audit_service.py
│   ├── repositories/
│   │   ├── order_repo.py
│   │   ├── user_repo.py
│   │   ├── shipment_repo.py
│   │   └── audit_repo.py
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic request/response schemas
│   ├── core/
│   │   ├── config.py       # Pydantic settings from env
│   │   ├── security.py     # JWT helpers, hashing
│   │   ├── exceptions.py   # Custom domain exceptions
│   │   └── fsm.py          # Order FSM transition table
│   ├── db/
│   │   ├── session.py      # SQLAlchemy engine + session factory
│   │   └── migrations/     # Alembic
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### 3.4 Data Layer

- **PostgreSQL**: Primary transactional store — ACID, relational constraints, indexing, row-locking
- **Redis**: Session metadata, refresh token revocation list, optional caching layer

### 3.5 Infrastructure Layer

```
Docker Compose (local dev)
├── fastapi-app  (gunicorn + uvicorn workers)
├── postgres     (persistent volume)
├── redis        (ephemeral or persistent)
└── next-app     (optional; or run locally)

Production
├── Frontend → Vercel  (CDN + SSR edge)
├── Backend  → Render  (Docker container, managed TLS)
├── Database → Render Managed PostgreSQL
└── Redis    → Render Redis or Upstash
```

---

## 4. Advanced Data Architecture

### 4.1 Core Design Philosophy

Enterprise OMS databases separate two distinct data concerns:

| Concern | Tables | Purpose |
|---|---|---|
| **Operational state** | `orders`, `shipments` | Fast filtering, pagination, dashboard joins |
| **Immutable history** | `order_status_events`, `audit_logs` | Forensic replay, timeline reconstruction, analytics |

**Why this separation exists:**  
Storing history inside `orders` (e.g., `previous_status`, `status_timestamp_1`) produces update-heavy rows, breaks auditability, and prevents timeline reconstruction. Append-only event tables never delete — each transition becomes a new row.

### 4.2 Entity Relationship Design

```
users
  ├── id (UUID PK)
  ├── email (UNIQUE, indexed)
  ├── password_hash
  ├── role (ENUM: CUSTOMER | ADMIN)
  ├── created_at
  └── deleted_at (soft delete)

orders
  ├── id (UUID PK)
  ├── order_number (UNIQUE, human-readable: ORD-2026-XXXXX)
  ├── customer_id (FK → users.id, indexed)
  ├── status (ENUM: PENDING | CONFIRMED | SHIPPED | DELIVERED | CANCELLED | FAILED | RETURNED | REFUNDED)
  ├── pickup_address (TEXT)
  ├── delivery_address (TEXT)
  ├── package_weight (DECIMAL)
  ├── package_description (TEXT)
  ├── metadata (JSONB)           ← flexible carrier / pricing data
  ├── created_at (indexed)
  ├── updated_at
  └── deleted_at

order_status_events              ← APPEND-ONLY, NEVER UPDATE/DELETE
  ├── id (UUID PK)
  ├── order_id (FK → orders.id, indexed)
  ├── from_status (ENUM)
  ├── to_status (ENUM)
  ├── actor_id (FK → users.id)  ← who triggered transition
  ├── actor_role (ENUM)
  ├── reason_code (TEXT, nullable)
  ├── metadata (JSONB)
  └── created_at (indexed)

shipments
  ├── id (UUID PK)
  ├── order_id (FK → orders.id, indexed)
  ├── tracking_number (UNIQUE, indexed)
  ├── carrier (TEXT)
  ├── shipment_status (ENUM: CREATED | IN_TRANSIT | OUT_FOR_DELIVERY | DELIVERED | FAILED)
  ├── estimated_delivery (DATE)
  ├── metadata (JSONB)
  ├── created_at
  └── updated_at

shipment_tracking_events         ← APPEND-ONLY
  ├── id (UUID PK)
  ├── shipment_id (FK → shipments.id, indexed)
  ├── status (TEXT)
  ├── location (TEXT)
  ├── carrier_raw_status (TEXT)
  ├── metadata (JSONB)
  └── created_at (indexed)

refresh_tokens
  ├── id (UUID PK)
  ├── user_id (FK → users.id, indexed)
  ├── token_hash (TEXT, indexed)
  ├── device_hint (TEXT, nullable)
  ├── expires_at (TIMESTAMP)
  ├── revoked_at (TIMESTAMP, nullable)
  └── created_at

audit_logs                       ← Cross-system audit
  ├── id (UUID PK)
  ├── entity_type (TEXT: "order" | "user" | "shipment")
  ├── entity_id (UUID, indexed)
  ├── actor_id (FK → users.id)
  ├── action (TEXT: "STATUS_UPDATE" | "CANCEL" | "LOGIN" etc.)
  ├── metadata (JSONB)           ← before/after state diff
  └── created_at (indexed)
```

### 4.3 FSM Transition Table

```python
# core/fsm.py
ALLOWED_TRANSITIONS = {
    "PENDING":   ["CONFIRMED", "CANCELLED", "FAILED"],
    "CONFIRMED": ["SHIPPED",   "CANCELLED", "FAILED"],
    "SHIPPED":   ["DELIVERED", "FAILED"],
    "DELIVERED": ["RETURNED"],
    "RETURNED":  ["REFUNDED"],
    # Terminal states — no further transitions
    "CANCELLED": [],
    "FAILED":    [],
    "REFUNDED":  [],
}

def validate_transition(from_status: str, to_status: str) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, [])
```

### 4.4 Indexing Strategy

```sql
-- users
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- orders (most critical — admin dashboard + customer portal)
CREATE UNIQUE INDEX idx_orders_number   ON orders(order_number);
CREATE INDEX        idx_orders_customer ON orders(customer_id);
CREATE INDEX        idx_orders_status_created
    ON orders(status, created_at DESC);
CREATE INDEX        idx_orders_created  ON orders(created_at DESC);

-- order_status_events (timeline reconstruction)
CREATE INDEX idx_order_events_order_timeline
    ON order_status_events(order_id, created_at);
CREATE INDEX idx_order_events_actor
    ON order_status_events(actor_id);

-- shipments
CREATE UNIQUE INDEX idx_shipments_tracking
    ON shipments(tracking_number);
CREATE INDEX        idx_shipments_order
    ON shipments(order_id);

-- refresh_tokens
CREATE INDEX idx_refresh_tokens_user
    ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_hash
    ON refresh_tokens(token_hash);

-- audit_logs
CREATE INDEX idx_audit_entity
    ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_created
    ON audit_logs(created_at DESC);
```

**Rationale per index:**
- `idx_orders_status_created`: Powers admin dashboard filter-by-status + sort-by-date (composite avoids multi-scan)
- `idx_orders_customer`: Powers `GET /orders` customer portal query
- `idx_order_events_order_timeline`: Powers timeline reconstruction (`SELECT ... WHERE order_id = ? ORDER BY created_at`)
- `idx_shipments_tracking`: Powers customer tracking lookup by tracking number

### 4.5 Caching Candidates

| Data | Cache Strategy | TTL |
|---|---|---|
| Admin KPI summary (total orders per status) | Redis key, invalidate on status write | 60s |
| Order list (paginated, no filter) | Skip — too dynamic | — |
| Individual order detail | Redis key by order_id | 30s with invalidation |
| Refresh token revocation list | Redis SET for fast blacklist lookup | Match token expiry |

---

## 5. API & Backend Engineering Blueprint

### 5.1 Response Envelope Standard

All API responses conform to:

```json
// Success
{
  "success": true,
  "message": "Order created successfully",
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-05-17T10:00:00Z"
  }
}

// Error
{
  "success": false,
  "error": {
    "code": "INVALID_TRANSITION",
    "message": "Cannot transition DELIVERED to PENDING",
    "details": {
      "current_status": "DELIVERED",
      "requested_status": "PENDING"
    }
  },
  "meta": {
    "request_id": "req_abc123"
  }
}

// Paginated list
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 450,
    "next_cursor": "eyJpZCI6IjEyMyJ9"
  }
}
```

### 5.2 Endpoint Specification

#### Auth Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Public | Register new customer |
| `POST` | `/api/v1/auth/login` | Public | Issue JWT + refresh token |
| `POST` | `/api/v1/auth/refresh` | Refresh token | Rotate tokens |
| `POST` | `/api/v1/auth/logout` | JWT | Revoke refresh token |

#### Customer Order Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/v1/orders` | CUSTOMER | List own orders (paginated, filterable) |
| `POST` | `/api/v1/orders` | CUSTOMER | Create new order |
| `GET` | `/api/v1/orders/{id}` | CUSTOMER (owner) | Order detail |
| `GET` | `/api/v1/orders/{id}/history` | CUSTOMER (owner) | Status timeline |
| `PATCH` | `/api/v1/orders/{id}/cancel` | CUSTOMER (owner) | Cancel if FSM allows |

#### Admin Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/v1/admin/orders` | ADMIN | All orders (filter, sort, search, paginate) |
| `GET` | `/api/v1/admin/orders/{id}` | ADMIN | Any order detail |
| `PATCH` | `/api/v1/admin/orders/{id}/status` | ADMIN | FSM status transition |
| `GET` | `/api/v1/admin/orders/{id}/audit` | ADMIN | Full audit history |
| `GET` | `/api/v1/admin/users` | ADMIN | User listing |

#### Shipment Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/v1/shipments/{id}` | JWT | Shipment detail |
| `GET` | `/api/v1/shipments/{id}/tracking` | JWT | Tracking event timeline |

#### System Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | Public | Health check (`{ "status": "healthy" }`) |

### 5.3 Key API Behaviors

#### Order Creation — `POST /api/v1/orders`

**Input validation (Pydantic):**
```python
class CreateOrderRequest(BaseModel):
    pickup_address: str = Field(..., min_length=10, max_length=500)
    delivery_address: str = Field(..., min_length=10, max_length=500)
    package_weight: float = Field(..., gt=0.0, le=50.0)
    package_description: Optional[str] = Field(None, max_length=500)
```

**Service execution sequence:**
1. Validate request schema (Pydantic — auto by FastAPI)
2. Extract `current_user` from JWT dependency
3. Call `order_service.create_order(user_id, payload)`
4. Inside service: generate `order_number`, set `status=PENDING`
5. Inside transaction: insert `orders`, insert `order_status_events` (system-created event)
6. Return created order via response schema

#### Status Update — `PATCH /api/v1/admin/orders/{id}/status`

**Service execution sequence:**
1. Fetch order by ID (404 if not found)
2. Validate FSM: `validate_transition(order.status, requested_status)` → 422 if invalid
3. Inside transaction:
   - Update `orders.status`
   - Insert `order_status_events` (from, to, actor_id, timestamp)
   - Insert `audit_logs` entry
4. Trigger downstream (optional): async notification event
5. Return updated order

#### Admin Order Listing — `GET /api/v1/admin/orders`

**Supported query params:**
```
?status=SHIPPED
&created_after=2026-01-01
&search=ORD-2026
&sort=-created_at
&page=1
&page_size=20
```

**SQL pattern:**
```sql
SELECT * FROM orders
WHERE (status = :status OR :status IS NULL)
  AND (created_at >= :created_after OR :created_after IS NULL)
  AND (order_number ILIKE :search OR :search IS NULL)
ORDER BY created_at DESC
LIMIT :page_size OFFSET (:page - 1) * :page_size;
```

### 5.4 HTTP Status Code Usage

| Code | When to Use |
|---|---|
| 200 | Successful GET, PATCH |
| 201 | Successful POST (resource created) |
| 400 | Malformed request / bad input |
| 401 | Missing or invalid JWT |
| 403 | Valid JWT, but wrong role / not owner |
| 404 | Resource not found |
| 409 | Duplicate order / conflict |
| 422 | Validation failure (Pydantic) / invalid FSM transition |
| 500 | Unhandled server exception (log internally, sanitize externally) |

### 5.5 Centralized Exception Handling

```python
# core/exceptions.py
class InvalidTransition(HTTPException):
    def __init__(self, from_s: str, to_s: str):
        super().__init__(
            status_code=422,
            detail={
                "code": "INVALID_TRANSITION",
                "message": f"Cannot transition {from_s} to {to_s}"
            }
        )

class OrderNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail={"code": "ORDER_NOT_FOUND", "message": "Order does not exist"}
        )

class ForbiddenAccess(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "Access denied"}
        )
```

Global exception handler in `main.py` catches unhandled exceptions, logs them with correlation ID, returns sanitized 500.

---

## 6. End-to-End Execution Workflow

### 6.1 Order Creation Lifecycle

```
Customer Browser
    │  POST /api/v1/orders { payload }
    ▼
FastAPI Router (orders.py)
    │  Parse HTTP request
    │  Inject current_user via Depends(get_current_customer)
    ▼
JWT Middleware
    │  Extract Bearer token
    │  Verify signature, expiration
    │  Inject user context into request state
    ▼
Pydantic Validation
    │  Validate CreateOrderRequest schema
    │  422 if invalid (auto-raised by FastAPI)
    ▼
OrderService.create_order(user, payload)
    │  Generate order_number (e.g., ORD-2026-A1B2C)
    │  Set initial status = PENDING
    │  Open database transaction
    │  ├── INSERT INTO orders (...)
    │  └── INSERT INTO order_status_events (SYSTEM → PENDING)
    │  Commit transaction
    │  (Optional) Emit domain event: OrderCreated
    ▼
Response Schema Serialization
    │  Convert ORM model → Pydantic OrderResponse
    ▼
HTTP 201 Response
    │  { "success": true, "data": { order }, "meta": { request_id } }
    ▼
Customer Browser
```

### 6.2 Admin Status Update Lifecycle

```
Admin Browser
    │  PATCH /api/v1/admin/orders/{id}/status { "status": "SHIPPED" }
    ▼
JWT Middleware → RBAC Middleware (require_admin)
    │  Verify token → Verify role == ADMIN → 403 if not
    ▼
AdminOrderRouter
    │  Extract order_id from path
    │  Parse UpdateStatusRequest
    ▼
AdminOrderService.update_status(order_id, new_status, admin_user)
    │  OrderRepository.get_by_id(order_id) → 404 if missing
    │  fsm.validate_transition(order.status, new_status) → 422 if invalid
    │  Open transaction:
    │  ├── UPDATE orders SET status = new_status, updated_at = now()
    │  ├── INSERT INTO order_status_events (from, to, actor_id, timestamp)
    │  └── INSERT INTO audit_logs (entity_type=order, action=STATUS_UPDATE, diff)
    │  Commit
    │  (Optional) async: push notification to customer
    ▼
HTTP 200 Response
    │  { "success": true, "data": { updated_order }, "message": "Status updated" }
```

### 6.3 Customer Order Timeline Fetch

```
Customer Browser
    │  GET /api/v1/orders/{id}/history
    ▼
JWT Middleware → Ownership Validation
    │  order.customer_id == current_user.id → 403 if mismatch
    ▼
OrderService.get_order_history(order_id)
    │  AuditRepository.get_events(order_id)
    │  SELECT from_status, to_status, actor_role, created_at
    │  FROM order_status_events
    │  WHERE order_id = ? ORDER BY created_at ASC
    ▼
Serialization → Timeline response
    │  [{ from: "PENDING", to: "CONFIRMED", at: "...", actor: "ADMIN" }, ...]
    ▼
HTTP 200 → Frontend Timeline component renders vertical workflow progression
```

---

## 7. Engineering Decision Analysis

### 7.1 Technology Choices

| Decision | Choice | Why | Alternatives Considered |
|---|---|---|---|
| Backend framework | FastAPI | Async, auto-OpenAPI, Pydantic-native, production-capable | Django REST (heavier), Flask (no validation), NestJS (Node) |
| Database | PostgreSQL | ACID, FK enforcement, row-locking, JSONB, indexing | MongoDB (weak transactions for OMS), SQLite (no production use) |
| ORM | SQLAlchemy | Mature, repository-pattern friendly, migration tooling | Tortoise ORM, raw SQL |
| Migrations | Alembic | Version-controlled schema, rollback-safe | Flyway, raw SQL files |
| Auth | JWT + Refresh Tokens | Stateless scaling, API-native, mobile-compatible | Session cookies (server memory, not API-first) |
| Password hashing | Argon2 (bcrypt fallback) | Memory-hard, brute-force resistant | MD5/SHA (never), SHA-256 without salt (never) |
| Frontend framework | Next.js | SSR for auth-protected dashboards, Vercel-native | CRA (no SSR), Vite+React (manual SSR needed) |
| Component library | shadcn/ui | Accessible, composable, Tailwind-compatible | MUI (heavy), Ant Design (opinionated) |
| Data fetching | React Query | Server-state, retry, background refetch, caching | SWR, manual useEffect |
| Deployment (backend) | Render | Managed PostgreSQL, Docker support, HTTPS auto | Railway, Fly.io, bare VPS |
| Deployment (frontend) | Vercel | Next.js native, CDN edge, preview environments | Netlify, self-hosted |
| Containerization | Docker + Compose | Reproducible local env, production parity | bare venv (no isolation) |

### 7.2 Architectural Tradeoffs

**Monolith vs Microservices:**
For this scope, a **well-structured modular monolith** is correct. Microservices add deployment complexity, distributed transaction overhead, and inter-service auth that are unnecessary at this scale. The layered service architecture makes a future extraction to microservices straightforward — each service module becomes a candidate deployment unit.

**Hybrid state vs pure event sourcing:**
Pure event sourcing (no `orders.status` column — derive from events) is operationally expensive: every dashboard query requires replaying event history. The hybrid approach (current state in `orders`, history in `order_status_events`) offers fast operational reads while preserving full auditability. This is the industry-standard pattern.

**Offset vs cursor pagination:**
Admin order lists use offset (`page`, `page_size`) for simplicity and UI page-number display. Audit log timelines use keyset/cursor pagination (`WHERE created_at < ?`) for performance at high row counts. Both strategies are appropriate for their respective contexts.

**JWT vs session cookies:**
JWT is chosen for its API-first, stateless nature. The tradeoff is revocation complexity — mitigated by short access token TTL (15 min) combined with a refresh token rotation strategy and a Redis-backed revocation list for logout.

### 7.3 Why Specific Patterns Were Selected

**Thin controllers:**  
Controllers that contain business logic duplicate rules across endpoints, make testing require a running HTTP server, and become maintenance liabilities. Thin controllers that only parse requests and delegate to services allow unit-testing the entire FSM and validation logic in isolation.

**Repository abstraction:**  
Direct SQLAlchemy queries in services scatter SQL logic and make query optimization difficult. Repositories centralize queries, enable mock injection for testing, and allow optimizing a single location when an N+1 problem is identified.

**Immutable audit events:**  
A `PATCH` that overwrites status history destroys forensic capability. Every logistics system debugged after a production incident relies on the event log. Making `order_status_events` append-only (no update, no delete) ensures this data survives even if `orders.status` is somehow corrupted.

---

## 8. Scalability & Production Evolution

### 8.1 MVP Architecture (Current Target)

```
Single FastAPI instance
    + Single PostgreSQL instance
    + Single Redis instance
    + Vercel CDN (frontend)
```

Scaling bottlenecks at this stage: database connection pool exhaustion, sequential request processing on heavy admin list queries.

### 8.2 Evolution Path: MVP → Production Scale

#### Phase 1 — Database Optimization (before scaling)
- Add `EXPLAIN ANALYZE` to all dashboard queries — verify index usage
- Enable connection pooling (PgBouncer or SQLAlchemy pool tuning)
- Add composite indexes for most common filter combinations
- Implement cursor-based pagination for audit logs

#### Phase 2 — Read Replica
- Route `SELECT` queries for dashboard/reporting to read replica
- Write operations remain on primary
- Eliminates read/write contention on admin dashboard

#### Phase 3 — Background Workers
- Extract notification sends to Celery/ARQ workers
- Extract audit log writes to async queue (decouple from request path)
- Prevents slow external calls (email, SMS) from blocking API response

#### Phase 4 — Caching Layer
- Cache admin KPI aggregates in Redis with invalidation on write
- Cache individual order detail with short TTL
- Reduces database load for frequently viewed orders

#### Phase 5 — Event-Driven Architecture
- Replace direct service calls with Redis Streams / RabbitMQ
- OrderCreated → fan-out to NotificationService, AnalyticsService
- Enables independent scaling of downstream consumers
- Provides replay capability for failed notifications

#### Phase 6 — Observability Stack
- Structured JSON logging (replace print/debug logs)
- OpenTelemetry tracing for request correlation
- Prometheus + Grafana for API latency, error rate, DB query time
- Alerting on: API p99 > 500ms, error rate > 1%, DB connections near pool limit

### 8.3 Security Hardening Roadmap

| Current | Future |
|---|---|
| Basic CORS config | Strict allowlist per environment |
| Manual rate limiting | WAF-level rate limiting |
| JWT secret in env var | Secrets manager (AWS Secrets Manager / Vault) |
| No brute-force protection | Redis-backed login attempt counter with lockout |
| No request signing | HMAC request signing for internal service calls |

---

## 9. AI-Assisted Development Structuring

### 9.1 Recommended Project Memory Files

```
PROJECT_BRAIN.md     ← Architecture reference, decisions, constraints
PROJECT_STATE.md     ← Current implementation status, what's done
CHANGELOG.md         ← What changed and why (per phase)
API_CONTRACTS.md     ← Full endpoint spec, request/response schemas
DB_SCHEMA.md         ← All table definitions, indexes, migration notes
TASK_QUEUE.md        ← Prioritized implementation tasks
```

### 9.2 `PROJECT_BRAIN.md` — Content Template

```markdown
# Project Brain

## Architecture
- Stack: FastAPI + PostgreSQL + Redis + Next.js
- Pattern: Router → Middleware → Service → Repository → Database
- Auth: JWT (15min) + Refresh Token rotation (7d)
- FSM: PENDING → CONFIRMED → SHIPPED → DELIVERED (see core/fsm.py)

## Critical Decisions
- Order FSM enforced in service layer ONLY — never in controllers or DB triggers
- Every status mutation MUST write to order_status_events in same transaction
- No business logic in repositories — queries only
- No DB access in routers — service delegation only

## Inferred Constraints
- order_number format: ORD-YYYY-XXXXX (human-readable)
- Access tokens: 15 min expiry
- Refresh tokens: 7 day expiry, rotated on use
- Customers can only see their own orders (ownership check in service)
- Admin list endpoint supports: status, created_after, search, sort, page, page_size

## Error Standards
- All errors use: { success: false, error: { code, message, details } }
- Never expose stack traces externally
- Use custom exception classes in core/exceptions.py
```

### 9.3 `PROJECT_STATE.md` — Content Template

```markdown
# Project State

## Phase 1 — Database + Models
- [x] Alembic initialized
- [x] users table + migration
- [x] orders table + migration
- [ ] order_status_events table
- [ ] shipments table
- [ ] audit_logs table

## Phase 2 — Auth
- [ ] Register endpoint
- [ ] Login endpoint (JWT + refresh)
- [ ] Refresh endpoint
- [ ] JWT middleware
- [ ] RBAC middleware

## Phase 3 — Order APIs
- [ ] Customer: POST /orders
- [ ] Customer: GET /orders
- [ ] Admin: GET /admin/orders
- [ ] Admin: PATCH /admin/orders/{id}/status
```

### 9.4 `API_CONTRACTS.md` — Content Template

```markdown
# API Contracts

## POST /api/v1/orders
Auth: CUSTOMER JWT
Request: { pickup_address, delivery_address, package_weight, package_description? }
Response 201: { success, data: { order }, meta }
Response 422: { success: false, error: { code: VALIDATION_ERROR, fields: [...] } }

## PATCH /api/v1/admin/orders/{id}/status
Auth: ADMIN JWT
Request: { status: "SHIPPED" }
Response 200: { success, data: { order } }
Response 422: { success: false, error: { code: INVALID_TRANSITION, ... } }
Response 404: { success: false, error: { code: ORDER_NOT_FOUND } }
Response 403: { success: false, error: { code: FORBIDDEN } }
```

### 9.5 Copilot / AI Prompt Strategy

When prompting for code generation, always include:

1. **Context block:** "This is a FastAPI logistics system. Architecture: Router → Service → Repository. All business logic lives in services. Repositories do SQL only."
2. **Schema reference:** Paste the relevant Pydantic schema and ORM model
3. **FSM reference:** Paste `ALLOWED_TRANSITIONS` dict if generating status logic
4. **Error standard:** "Raise custom exceptions from `core/exceptions.py`. Never return raw dicts or strings."
5. **Constraint list:** "This function must write an `order_status_events` row in the same transaction as any status update."

---

## 10. Step-by-Step Implementation Roadmap

### Phase 0 — Project Initialization (1–2 hours)
- [ ] Initialize Git repo with `.gitignore` (Python, Node, `.env`)
- [ ] Create `backend/` and `frontend/` directory structure
- [ ] Create `docker-compose.yml` with postgres, redis services
- [ ] Create `backend/requirements.txt` (fastapi, sqlalchemy, alembic, pydantic, python-jose, argon2-cffi, psycopg2-binary)
- [ ] Initialize Alembic: `alembic init db/migrations`
- [ ] Create `core/config.py` with Pydantic `BaseSettings` from env
- [ ] Create `.env.example` with all required variables documented

### Phase 1 — Database Foundation (2–3 hours)
- [ ] Write SQLAlchemy models: `User`, `Order`, `OrderStatusEvent`, `Shipment`, `ShipmentTrackingEvent`, `RefreshToken`, `AuditLog`
- [ ] Write Alembic migration for all tables
- [ ] Apply all indexes defined in DB_SCHEMA.md
- [ ] Verify migration with `alembic upgrade head`
- [ ] Write `db/session.py` (engine, SessionLocal, get_db dependency)

### Phase 2 — Auth Layer (3–4 hours)
- [ ] Implement `core/security.py`: `hash_password`, `verify_password`, `create_access_token`, `create_refresh_token`, `decode_token`
- [ ] Implement `UserRepository`: `get_by_email`, `create`, `get_by_id`
- [ ] Implement `RefreshTokenRepository`: `create`, `revoke`, `get_valid_by_hash`
- [ ] Implement `AuthService`: `register`, `login`, `refresh`, `logout`
- [ ] Implement JWT middleware as FastAPI dependency: `get_current_user`, `require_admin`, `require_customer`
- [ ] Implement auth router: `/register`, `/login`, `/refresh`, `/logout`
- [ ] Write unit tests: `test_cannot_login_wrong_password`, `test_admin_cannot_access_customer_route`, `test_refresh_token_rotation`

### Phase 3 — Order Service + FSM (3–4 hours)
- [ ] Implement `core/fsm.py`: `ALLOWED_TRANSITIONS`, `validate_transition()`
- [ ] Implement `OrderRepository`: `create`, `get_by_id`, `get_by_customer`, `get_all_admin`, `update_status`
- [ ] Implement `AuditRepository`: `create_event`, `get_events_for_order`
- [ ] Implement `OrderService`:
  - `create_order` (atomic: orders insert + event insert)
  - `get_customer_orders` (ownership enforced)
  - `cancel_order` (FSM validation, ownership enforced)
  - `update_order_status` (FSM validation, admin-only, event + audit in transaction)
  - `get_order_history`
- [ ] Write unit tests: `test_cannot_cancel_shipped_order`, `test_invalid_transition_raises_422`, `test_customer_cannot_see_other_orders`

### Phase 4 — API Routers (2–3 hours)
- [ ] Customer order router: `GET /orders`, `POST /orders`, `GET /orders/{id}`, `PATCH /orders/{id}/cancel`, `GET /orders/{id}/history`
- [ ] Admin order router: `GET /admin/orders`, `GET /admin/orders/{id}`, `PATCH /admin/orders/{id}/status`, `GET /admin/orders/{id}/audit`
- [ ] Implement pagination helper, filter/sort query param parsing
- [ ] Implement global exception handler in `main.py`
- [ ] Add `/health` endpoint

### Phase 5 — Frontend Architecture (4–5 hours)
- [ ] Initialize Next.js App Router project with TypeScript
- [ ] Install: `tailwindcss`, `shadcn/ui`, `@tanstack/react-query`, `@tanstack/react-table`, `axios`, `zustand`
- [ ] Build auth flow: `/login`, `/register` pages with form validation
- [ ] Build customer portal: `/dashboard`, `/orders`, `/orders/[id]` with timeline component
- [ ] Build admin dashboard: `/admin`, `/admin/orders` with filter/sort table, status update modal
- [ ] Implement `StatusBadge`, `Timeline`, `DataTable`, `Pagination`, `FilterBar` as reusable components
- [ ] Add skeleton loaders, empty states, error states, toast notifications

### Phase 6 — Dockerization (1–2 hours)
- [ ] Write `backend/Dockerfile` (python:3.12-slim, gunicorn + uvicorn)
- [ ] Write `frontend/Dockerfile` (node:20-alpine, next build + start)
- [ ] Write `docker-compose.yml` with all 4 services + volumes + healthchecks
- [ ] Create `.env.example`, `.env.local.example`
- [ ] Verify `docker compose up` builds and starts cleanly

### Phase 7 — Deployment (2–3 hours)
- [ ] Deploy backend to Render (Docker service, managed PostgreSQL)
- [ ] Set all production env vars in Render dashboard
- [ ] Run `alembic upgrade head` as deploy hook or startup script
- [ ] Deploy frontend to Vercel with `NEXT_PUBLIC_API_URL` set to Render URL
- [ ] Smoke test all endpoints in production
- [ ] Verify CORS is restricted to Vercel domain only

### Phase 8 — Polish + Documentation (2 hours)
- [ ] Fill `PROJECT_BRAIN.md`, `API_CONTRACTS.md`, `DB_SCHEMA.md`
- [ ] Write `README.md` following the blueprint in Section 11
- [ ] Add Swagger UI screenshot or API table to README
- [ ] Verify all test cases pass
- [ ] Final production smoke test

---

## 11. README & GitHub Presentation Blueprint

### Recommended README Structure

```markdown
# OMS — Logistics & Order Management System

> Production-grade order management system with workflow-driven state machine,
> RBAC-enforced API, immutable audit history, and operational admin dashboard.

## Architecture

[ ASCII diagram of Router → Service → Repository → DB ]

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js + shadcn/ui | SSR operational dashboard |
| API | FastAPI | Layered REST API |
| Auth | JWT + Refresh Tokens | Stateless RBAC |
| Database | PostgreSQL | ACID workflow persistence |
| Cache | Redis | Session + revocation |
| Deploy | Vercel + Render + Docker | Full stack production |

## Order Lifecycle (FSM)

[ FSM diagram ]

## Key Engineering Decisions

- **State machine enforcement** in service layer only — prevents invalid workflow transitions
- **Hybrid state + event model** — fast operational reads, immutable audit history
- **Layered architecture** — thin controllers, service-layer business logic, repository DB access
- **JWT + refresh rotation** — stateless auth with secure session continuity

## Setup

### Local (Docker)
\`\`\`bash
cp .env.example .env
docker compose up
\`\`\`

### API
http://localhost:8000/docs

## API Reference

[ Table of all endpoints with auth, method, path, description ]

## Database Schema

[ ERD or table listing ]

## Deployment

- Backend: Render (auto-deploys from main branch)
- Frontend: Vercel (auto-deploys from main branch)
- DB: Render Managed PostgreSQL

## Engineering Depth

This project demonstrates:
- Finite state machine design for logistics workflows
- Production-grade layered FastAPI architecture
- Normalized relational schema with immutable event history
- JWT + RBAC authentication with refresh token rotation
- Responsive operational frontend (admin + customer portals)
- Dockerized multi-service deployment

## Future Improvements

- WebSocket live order tracking
- Redis Streams for async notifications
- Read replica for dashboard queries
- Celery background workers for email/SMS
```

---

## 12. Final Engineering Checklist

Use this before considering the project complete.

### Backend
- [ ] FSM transition table defined in `core/fsm.py`; enforced in service layer only
- [ ] Every status update writes to `order_status_events` in the same transaction
- [ ] No raw SQL queries in service layer; all queries via repository
- [ ] No business logic in repository layer; queries only
- [ ] JWT middleware validates token; RBAC middleware validates role — separate concerns
- [ ] Customers cannot access other customers' orders (ownership check in service)
- [ ] Global exception handler returns sanitized errors — no stack traces exposed
- [ ] All response envelopes use `{ success, data, error, meta }` shape
- [ ] `/health` endpoint returns 200 with `{ "status": "healthy" }`
- [ ] All secrets loaded from environment variables — none hardcoded
- [ ] Startup validates all required env vars are present
- [ ] Alembic migrations cover all tables and indexes

### Database
- [ ] `order_status_events` has no UPDATE/DELETE privileges in application code
- [ ] All FK relationships have indexes
- [ ] `orders(status, created_at DESC)` composite index exists
- [ ] `orders(customer_id)` index exists
- [ ] Soft delete implemented with `deleted_at` on users and orders

### Frontend
- [ ] All protected routes redirect unauthenticated users to `/login`
- [ ] Admin routes validate role claim — not just authentication
- [ ] Order status updates show FSM-friendly error messages (not raw API errors)
- [ ] Tables have skeleton loaders during fetch
- [ ] Forms have inline validation errors (not only toast errors)
- [ ] Empty states present for all list views
- [ ] Mobile layout verified at 375px, 768px, 1280px breakpoints

### Security
- [ ] CORS restricted to specific origin(s) in production
- [ ] Refresh tokens stored as hash in DB, not plaintext
- [ ] Logout revokes refresh token server-side
- [ ] Rate limiting applied to `/auth/login`
- [ ] JWT expiry set to 15 minutes in production

### Deployment
- [ ] `docker compose up` builds and starts without manual intervention
- [ ] `.env.example` documents all required variables with descriptions
- [ ] Production deploy runs `alembic upgrade head` before starting server
- [ ] Frontend `NEXT_PUBLIC_API_URL` points to production backend, not localhost
- [ ] Health endpoint returns 200 in production deployment

---

*Engineering Intelligence Blueprint · Mini Logistics OMS · Generated from 7 research domains + requirements gap analysis*  
*Architecture tier: Production-modeled modular monolith, evolution-ready for microservices extraction*
