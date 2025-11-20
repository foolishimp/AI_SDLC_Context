---
name: telemetry-tagging
description: Tag logs, metrics, and distributed traces with REQ-* keys for production traceability. Enables backward traceability from runtime issues to requirements to intent. Use when deploying code or setting up observability.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# telemetry-tagging

**Skill Type**: Actuator (Runtime Feedback)
**Purpose**: Tag production telemetry with REQ-* keys
**Prerequisites**: Code implemented and ready for deployment

---

## Agent Instructions

You are adding **REQ-* tags to telemetry** for production traceability.

**Telemetry types**:
1. **Logs**: Structured logs with REQ-* in extra fields
2. **Metrics**: Metrics tagged with `req:REQ-*`
3. **Traces**: Distributed traces tagged with REQ-*

**Goal**: Enable backward traceability (Alert → REQ-* → Intent)

---

## Workflow

### Step 1: Find Code Implementing Requirements

```bash
# Find all files implementing REQ-F-AUTH-001
grep -rn "# Implements: REQ-F-AUTH-001" src/
```

---

### Step 2: Add Logging Tags

**Python (structlog, logging)**:

```python
# Before
def login(email: str, password: str) -> LoginResult:
    # Implements: REQ-F-AUTH-001
    result = authenticate(email, password)
    return result

# After
import logging

logger = logging.getLogger(__name__)

def login(email: str, password: str) -> LoginResult:
    # Implements: REQ-F-AUTH-001
    logger.info(
        "User login attempt",
        extra={
            "req": "REQ-F-AUTH-001",  # ← Tag for traceability
            "email": email,
            "success": False  # Updated after auth
        }
    )

    result = authenticate(email, password)

    logger.info(
        "User login result",
        extra={
            "req": "REQ-F-AUTH-001",
            "email": email,
            "success": result.success
        }
    )

    if not result.success:
        logger.warning(
            "Login failed",
            extra={
                "req": "REQ-F-AUTH-001",
                "email": email,
                "error": result.error
            }
        )

    return result
```

**TypeScript (Winston, Pino)**:

```typescript
// Implements: REQ-F-AUTH-001
function login(email: string, password: string): LoginResult {
  logger.info('User login attempt', {
    req: 'REQ-F-AUTH-001',  // ← Tag
    email,
  });

  const result = authenticate(email, password);

  logger.info('User login result', {
    req: 'REQ-F-AUTH-001',
    email,
    success: result.success,
  });

  return result;
}
```

---

### Step 3: Add Metrics Tags

**Datadog (Python)**:

```python
from datadog import statsd

def login(email: str, password: str) -> LoginResult:
    # Implements: REQ-F-AUTH-001

    result = authenticate(email, password)

    # Tag metric with REQ-*
    statsd.increment(
        'auth.login.attempts',
        tags=[
            'req:REQ-F-AUTH-001',  # ← Tag for traceability
            f'success:{result.success}',
            'env:production'
        ]
    )

    if result.success:
        statsd.timing(
            'auth.login.duration',
            login_duration_ms,
            tags=['req:REQ-F-AUTH-001', 'env:production']
        )

    return result
```

**Prometheus (Python)**:

```python
from prometheus_client import Counter, Histogram

# Define metrics with labels
login_attempts = Counter(
    'auth_login_attempts_total',
    'Total login attempts',
    ['req', 'success', 'env']
)

login_duration = Histogram(
    'auth_login_duration_seconds',
    'Login duration',
    ['req', 'env']
)

def login(email: str, password: str) -> LoginResult:
    # Implements: REQ-F-AUTH-001

    with login_duration.labels(req='REQ-F-AUTH-001', env='production').time():
        result = authenticate(email, password)

    login_attempts.labels(
        req='REQ-F-AUTH-001',  # ← Tag
        success=str(result.success).lower(),
        env='production'
    ).inc()

    return result
```

---

### Step 4: Add Distributed Trace Tags

**OpenTelemetry**:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def login(email: str, password: str) -> LoginResult:
    # Implements: REQ-F-AUTH-001

    with tracer.start_as_current_span("auth.login") as span:
        span.set_attribute("req", "REQ-F-AUTH-001")  # ← Tag
        span.set_attribute("email", email)

        result = authenticate(email, password)

        span.set_attribute("success", result.success)

        if not result.success:
            span.set_attribute("error", result.error)
            span.set_status(trace.Status(trace.StatusCode.ERROR))

        return result
```

---

### Step 5: Verify Tags Added

**Check logs**:
```bash
# Search logs for REQ tags
grep "req.*REQ-F-AUTH-001" /var/log/app.log
```

**Check metrics (Datadog)**:
```
auth.login.attempts{req:REQ-F-AUTH-001,success:true}
auth.login.duration{req:REQ-F-AUTH-001}
```

**Check traces (OpenTelemetry)**:
```
Span: auth.login
  Attributes:
    - req: REQ-F-AUTH-001
    - email: user@example.com
    - success: true
```

---

## Output Format

```
[TELEMETRY TAGGING - REQ-F-AUTH-001]

Files Tagged:

src/auth/login.py:
  ✓ Logs: 3 log statements tagged
    - logger.info("Login attempt", req="REQ-F-AUTH-001")
    - logger.info("Login result", req="REQ-F-AUTH-001")
    - logger.warning("Login failed", req="REQ-F-AUTH-001")

  ✓ Metrics: 2 metrics tagged
    - auth.login.attempts{req:REQ-F-AUTH-001}
    - auth.login.duration{req:REQ-F-AUTH-001}

  ✓ Traces: 1 span tagged
    - Span "auth.login" with req="REQ-F-AUTH-001"

Total Tags Added: 6
  - Log tags: 3
  - Metric tags: 2
  - Trace tags: 1

Traceability Enabled:
  Production Alert → req:REQ-F-AUTH-001 → docs/requirements/authentication.md → INT-100

✅ Telemetry Tagged!
   Backward traceability ready
```

---

## Notes

**Why tag telemetry?**
- **Backward traceability**: Production issue → Requirement → Intent
- **Requirement-level monitoring**: Dashboards per REQ-*
- **Impact measurement**: Track success/failure per requirement
- **Feedback loop**: Alerts create new intents

**Homeostasis Goal**:
```yaml
desired_state:
  all_code_telemetry_tagged: true
  backward_traceability: complete
  req_level_dashboards: available
```

**"Excellence or nothing"** 🔥
