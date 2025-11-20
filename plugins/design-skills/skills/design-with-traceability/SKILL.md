---
name: design-with-traceability
description: Create technical solution architecture from requirements with REQ-* traceability. Designs components, APIs, data models, and interactions. Tags all design artifacts with requirement keys. Use after requirements are validated, before coding starts.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# design-with-traceability

**Skill Type**: Actuator (Design Stage)
**Purpose**: Transform requirements into technical solution architecture
**Prerequisites**: Requirements validated (REQ-*), quality gate passed

---

## Agent Instructions

You are creating **technical solution architecture** from requirements.

Your goal is to design:
1. **Components** (services, modules, classes)
2. **APIs** (endpoints, contracts, protocols)
3. **Data Models** (schemas, entities, relationships)
4. **Interactions** (sequence diagrams, data flows)

**All tagged with REQ-* keys** for traceability.

---

## Workflow

### Step 1: Review Requirements

**Understand what needs to be designed**:

```markdown
Requirements:
- REQ-F-AUTH-001: User login with email/password
- REQ-F-AUTH-002: Password reset via email
- REQ-NFR-SEC-001: Password encryption (bcrypt)
- REQ-NFR-PERF-001: Login response < 500ms

Business Rules:
- BR-001: Email validation
- BR-002: Password min 12 chars
- BR-003: Account lockout (3 attempts, 15min)

Constraints:
- C-001: bcrypt hashing (cost 12)
- C-002: JWT sessions (30min timeout)
- C-003: Database timeout 100ms
```

---

### Step 2: Design Components

**Identify components needed**:

```yaml
# docs/design/authentication-architecture.md

# Implements: REQ-F-AUTH-001, REQ-F-AUTH-002
# Acknowledges: C-001, C-002, C-003

## Components

### AuthenticationService
**Implements**: REQ-F-AUTH-001, REQ-F-AUTH-002
**Purpose**: Handle user authentication and password management
**Responsibilities**:
- User login (REQ-F-AUTH-001)
- Password reset (REQ-F-AUTH-002)
- Session management (C-002)

**Methods**:
- `login(email, password)` → LoginResult
- `request_password_reset(email)` → ResetResult
- `reset_password(token, new_password)` → ResetResult

**Dependencies**:
- EmailValidator (BR-001)
- PasswordValidator (BR-002)
- LockoutTracker (BR-003)
- PasswordHasher (C-001)
- SessionManager (C-002)

---

### EmailValidator
**Implements**: BR-001
**Purpose**: Validate email format and normalization
**Methods**:
- `validate(email)` → bool
- `normalize(email)` → str (lowercase)

---

### PasswordValidator
**Implements**: BR-002, BR-003 (partial)
**Purpose**: Validate password requirements
**Methods**:
- `validate_length(password)` → bool
- `validate_complexity(password)` → bool

---

### LockoutTracker
**Implements**: BR-003, F-001, F-002
**Purpose**: Track failed login attempts and manage lockouts
**Methods**:
- `record_failed_attempt(user_id)` → bool (is_locked)
- `is_locked(user_id)` → bool
- `get_remaining_time(user_id)` → int (minutes)
- `reset(user_id)` → void

---

### PasswordHasher
**Implements**: C-001
**Purpose**: Hash and verify passwords using bcrypt
**Methods**:
- `hash(password)` → str
- `verify(password, hash)` → bool

---

### SessionManager
**Implements**: C-002
**Purpose**: Manage JWT sessions with 30min timeout
**Methods**:
- `create_session(user_id)` → str (JWT token)
- `validate_session(token)` → bool
- `refresh_session(token)` → str (new token)
```

---

### Step 3: Design APIs

**Define API contracts**:

```yaml
# API Design (tagged with REQ-*)

## POST /api/v1/auth/login
**Implements**: REQ-F-AUTH-001

**Request**:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

**Response (Success - 200)**:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user_123",
    "email": "user@example.com"
  }
}

**Response (Error - 400)**:
{
  "success": false,
  "error": "Invalid email format"  # BR-001
}

**Response (Error - 401)**:
{
  "success": false,
  "error": "Invalid credentials"
}

**Response (Error - 429)**:
{
  "success": false,
  "error": "Account locked. Try again in 12 minutes"  # BR-003
}

**Validation**:
- Email: BR-001 (regex validation)
- Password: BR-002 (minimum length)
- Lockout: BR-003 (3 attempts, 15min)

**Performance**: REQ-NFR-PERF-001 (< 500ms response)

---

## POST /api/v1/auth/password-reset-request
**Implements**: REQ-F-AUTH-002

**Request**:
{
  "email": "user@example.com"
}

**Response (Success - 200)**:
{
  "success": true,
  "message": "If email exists, reset link sent"
}
```

---

### Step 4: Design Data Models

**Define schemas and entities**:

```yaml
# Data Model Design

## User Entity
**Implements**: REQ-F-AUTH-001, REQ-F-AUTH-002

**Schema**:
{
  "id": "uuid",
  "email": "string (unique, lowercase, max 255)",
  "password_hash": "string (bcrypt hash)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

**Constraints**:
- email: UNIQUE index, NOT NULL
- password_hash: NOT NULL (C-001: bcrypt)

**Requirements Satisfied**:
- REQ-F-AUTH-001: Stores credentials
- BR-001: Email unique and normalized
- C-001: Password hashed with bcrypt

---

## LoginAttempt Entity
**Implements**: BR-003 (account lockout)

**Schema**:
{
  "id": "uuid",
  "user_id": "uuid (foreign key to User)",
  "timestamp": "timestamp",
  "success": "boolean",
  "ip_address": "string"
}

**Indexes**:
- (user_id, timestamp) - For querying recent attempts

**Requirements Satisfied**:
- BR-003: Track failed attempts
- F-001: Calculate lockout expiry from timestamps

---

## Session Entity
**Implements**: C-002 (session management)

**Schema**:
{
  "id": "uuid",
  "user_id": "uuid (foreign key to User)",
  "token": "string (JWT)",
  "created_at": "timestamp",
  "expires_at": "timestamp",
  "last_activity": "timestamp"
}

**Constraints**:
- token: UNIQUE
- expires_at: created_at + 30 minutes (C-002)

**Requirements Satisfied**:
- C-002: JWT sessions with 30min timeout
```

---

### Step 5: Create Component Diagram

**Visualize architecture**:

```
┌─────────────────────────────────────────────┐
│ Client (Web/Mobile)                         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ API Layer           │
        │ /api/v1/auth/*      │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────────────┐
        │ AuthenticationService       │ ← REQ-F-AUTH-001, 002
        │ - login()                   │
        │ - request_password_reset()  │
        │ - reset_password()          │
        └───┬─────────────────────┬───┘
            │                     │
            ▼                     ▼
    ┌───────────────┐     ┌──────────────┐
    │ Validators    │     │ LockoutTracker│ ← BR-003
    │ - Email       │ ← BR-001
    │ - Password    │ ← BR-002
    └───────────────┘     └──────────────┘
            │                     │
            ▼                     ▼
        ┌─────────────────────────────┐
        │ Database (PostgreSQL)       │
        │ - User table                │
        │ - LoginAttempt table        │
        │ - Session table             │
        └─────────────────────────────┘

Constraints:
- C-001: PasswordHasher uses bcrypt (cost 12)
- C-002: SessionManager uses JWT (30min timeout)
- C-003: All DB queries timeout at 100ms
```

---

### Step 6: Tag All Design Artifacts

**Add REQ-* tags to all design documents**:

```markdown
# docs/design/authentication-architecture.md

# Design for: REQ-F-AUTH-001, REQ-F-AUTH-002
# Constraints: C-001, C-002, C-003
# Business Rules: BR-001, BR-002, BR-003

## Architecture Overview

This design implements user authentication (REQ-F-AUTH-001)
and password reset (REQ-F-AUTH-002).
```

---

### Step 7: Create Traceability Matrix

**Map requirements to design components**:

| REQ-* | Component | API | Data Model | Diagram |
|-------|-----------|-----|------------|---------|
| REQ-F-AUTH-001 | AuthenticationService | POST /auth/login | User, LoginAttempt, Session | Fig 1 |
| REQ-F-AUTH-002 | AuthenticationService | POST /auth/password-reset | User, PasswordResetToken | Fig 1 |
| BR-001 | EmailValidator | - | - | Fig 2 |
| BR-002 | PasswordValidator | - | - | Fig 2 |
| BR-003 | LockoutTracker | - | LoginAttempt | Fig 3 |

---

### Step 8: Commit Design

```bash
git add docs/design/
git commit -m "DESIGN: Create architecture for REQ-F-AUTH-001, REQ-F-AUTH-002

Design technical solution for user authentication.

Components:
- AuthenticationService (REQ-F-AUTH-001, REQ-F-AUTH-002)
- EmailValidator (BR-001)
- PasswordValidator (BR-002)
- LockoutTracker (BR-003)
- PasswordHasher (C-001: bcrypt)
- SessionManager (C-002: JWT)

APIs:
- POST /api/v1/auth/login
- POST /api/v1/auth/password-reset-request
- POST /api/v1/auth/password-reset

Data Models:
- User entity (email, password_hash)
- LoginAttempt entity (tracking for BR-003)
- Session entity (JWT tokens, C-002)

Traceability:
- REQ-F-AUTH-001 → AuthenticationService → login() method
- REQ-F-AUTH-002 → AuthenticationService → password reset methods

Acknowledges Ecosystem E(t):
- C-001: bcrypt (industry standard)
- C-002: JWT (existing infrastructure)
- C-003: Database RDS limits

Design Coverage: 100% (all requirements have design)
"
```

---

## Output Format

```
[DESIGN WITH TRACEABILITY - REQ-F-AUTH-001, REQ-F-AUTH-002]

Requirements: User authentication and password reset

Design Created:

Components (6):
  ✓ AuthenticationService (REQ-F-AUTH-001, REQ-F-AUTH-002)
  ✓ EmailValidator (BR-001)
  ✓ PasswordValidator (BR-002)
  ✓ LockoutTracker (BR-003, F-001, F-002)
  ✓ PasswordHasher (C-001)
  ✓ SessionManager (C-002)

APIs (3):
  ✓ POST /api/v1/auth/login (REQ-F-AUTH-001)
  ✓ POST /api/v1/auth/password-reset-request (REQ-F-AUTH-002)
  ✓ POST /api/v1/auth/password-reset (REQ-F-AUTH-002)

Data Models (3):
  ✓ User entity (email, password_hash)
  ✓ LoginAttempt entity (for BR-003 lockout tracking)
  ✓ Session entity (for C-002 JWT sessions)

Diagrams:
  ✓ Component diagram (architecture-overview.png)
  ✓ Sequence diagram (login-flow.png)
  ✓ Data model diagram (authentication-erd.png)

Files Created:
  + docs/design/authentication-architecture.md (287 lines)
  + docs/design/diagrams/authentication-components.png
  + docs/design/api-specs/auth-api.yml (OpenAPI spec)

Traceability:
  ✓ All components tagged with REQ-*
  ✓ All APIs tagged with REQ-*
  ✓ All data models tagged with REQ-*
  ✓ Traceability matrix created

Design Coverage: 100% (2/2 requirements have complete design)

✅ Design Complete!
   Ready for ADRs and implementation
```

---

## Prerequisites Check

Before invoking:
1. Requirements validated and approved
2. Requirements have BR-*, C-*, F-* (from disambiguation)

---

## Notes

**Why design with traceability?**
- **Impact analysis**: Know what design changes when requirements change
- **Complete specification**: Design + requirements = full implementation guide
- **Architecture review**: Stakeholders review tagged design
- **Code generation**: Design provides structure, BR-*/C-*/F-* provide logic

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_have_design: true
  all_design_tagged_with_req: true
  design_coverage: 100%
```

**"Excellence or nothing"** 🔥
