# Ecosystem as Operating Environment Constraint Vector

**Date**: 2025-11-20
**Purpose**: Model external dependencies as a continuous constraint vector, not discrete requirements
**Key Insight**: External dependencies constrain every SDLC stage, not just Design

---

## The Fundamental Shift

### ❌ **Wrong Model**: Discrete Ecosystem Requirements List

```yaml
# This implies dependencies are enumerable and fixed
REQ-ECO-LIB-001: FastAPI
REQ-ECO-LIB-002: React
REQ-ECO-INFRA-001: AWS
REQ-ECO-API-001: Auth0
# ... exhaustive list attempt
```

**Problems**:
- Implies dependencies are finite and knowable upfront
- Misses implicit dependencies (Python stdlib, OS, DNS, etc.)
- Doesn't capture **constraint propagation** across stages
- Treats ecosystem as "thing to implement" vs "environment to operate within"

---

### ✅ **Correct Model**: Operating Environment Constraint Vector

**Ecosystem** = **Continuous constraint space** that:
1. **Exists before** any requirements are written
2. **Constrains decisions** at every SDLC stage
3. **Evolves independently** of your project
4. **Cannot be exhaustively enumerated**

**Mathematical Model**:
```
E(t) = Operating Environment at time t

E(t) = {
  runtime_platforms(t),    # Python 3.11, Node 20, JVM 17, .NET 8
  cloud_providers(t),      # AWS, GCP, Azure, on-prem
  available_apis(t),       # OpenAI, Stripe, Twilio, ...
  library_ecosystem(t),    # npm, PyPI, Maven, ...
  infrastructure(t),       # Kubernetes, Docker, VMs, serverless
  protocols(t),            # HTTP/3, gRPC, GraphQL, REST
  standards(t),            # OAuth2, OpenID, SAML, JWT
  compliance_reqs(t),      # GDPR, HIPAA, SOC2, PCI-DSS
  cost_landscape(t),       # Cloud pricing, API costs, licenses
  security_landscape(t),   # Known CVEs, best practices
  team_capabilities(t)     # Skills, experience, preferences
}

where t = time (ecosystem evolves)
```

**Key Property**: E(t) is **given** (external reality), not **chosen** (design decision)

---

## Constraint Vector at Each SDLC Stage

### Stage 1: Requirements

**Constraints from E(t)**:

```yaml
requirements_stage:
  ecosystem_constraints:
    compliance:
      - GDPR (if EU customers)
      - HIPAA (if healthcare data)
      - SOC2 (if enterprise customers)

    available_services:
      - Payment: Stripe, PayPal, Square (not "build our own")
      - Auth: Auth0, Okta, AWS Cognito (not "custom OAuth server")
      - Email: SendGrid, Mailgun, SES (not "SMTP server")

    team_constraints:
      - Known languages: Python, JavaScript
      - Unknown languages: Rust, Go (would require hiring/training)

    cost_constraints:
      - Budget: $5000/month cloud spend
      - Headcount: 5 developers (can't build everything)

    time_constraints:
      - Market window: 6 months to launch
      - Cannot build foundational infrastructure

  constraint_impact:
    functional_requirements:
      # Instead of: "Build payment processing system"
      # Write: "Integrate payment provider API"
      REQ-F-PAY-001: "Process credit card payments via Stripe API"

      # Instead of: "Build authentication system"
      # Write: "Integrate OAuth provider"
      REQ-F-AUTH-001: "User login via Auth0"

    non_functional_requirements:
      # Constrained by cloud provider capabilities
      REQ-NFR-SCALE-001: "Support 10k concurrent users"
        # → Achievable with AWS/GCP
        # → Would fail with shared hosting

      REQ-NFR-PERF-001: "API latency < 100ms"
        # → Requires CDN (Cloudflare, Fastly)
        # → Cannot achieve with single-region deployment
```

**The Shift**:
- **Before**: "We need user authentication" (what)
- **After**: "We need user authentication **via existing OAuth provider** because we cannot build/maintain custom auth in 6 months with 5 devs while meeting SOC2" (what + ecosystem constraints)

---

### Stage 2: Design

**Constraints from E(t)**:

```yaml
design_stage:
  ecosystem_constraints:
    architectural_patterns:
      # Constrained by available frameworks
      - Microservices: Spring Boot, FastAPI, Express
      - Monolith: Django, Rails, Laravel
      - Serverless: Lambda, Cloud Functions, Azure Functions

    data_storage:
      # Constrained by cloud provider, compliance, cost
      - Relational: PostgreSQL (RDS), MySQL (RDS), SQL Server
      - Document: MongoDB Atlas, DynamoDB, Cosmos DB
      - Object: S3, GCS, Blob Storage
      - Cache: Redis, Memcached, ElastiCache

    infrastructure:
      # Constrained by team skills, cost, scale requirements
      - Container Orchestration: Kubernetes, ECS, Cloud Run
      - Serverless: Lambda, Cloud Functions
      - VMs: EC2, Compute Engine, Azure VMs
      - PaaS: Heroku, Vercel, Render

    integration_patterns:
      # Constrained by partner APIs, industry standards
      - REST: Most common, HTTP/JSON
      - GraphQL: If frontend needs flexibility
      - gRPC: If performance critical
      - Message Queue: SQS, Pub/Sub, Event Hub (not custom)

  constraint_propagation:
    example:
      requirement: REQ-F-AUTH-001 "User login via Auth0"

      constraints_imposed_on_design:
        - Must use OAuth2/OIDC protocol (Auth0 standard)
        - Must handle JWT tokens (Auth0 format)
        - Must implement callback URLs (Auth0 requirement)
        - Must store user profiles (Auth0 user metadata)
        - Must handle token refresh (Auth0 expiry)
        - Frontend must redirect to Auth0 login page
        - Backend must verify Auth0 JWT signatures

      design_decisions_constrained:
        - Cannot use cookie-based sessions (Auth0 uses tokens)
        - Cannot use custom password hashing (Auth0 handles)
        - Must use HTTPS (Auth0 requirement)
        - Must configure CORS (Auth0 callback)

      cascade_to_other_requirements:
        - REQ-NFR-SEC-001: SSL certificate required (Auth0 → HTTPS)
        - REQ-ECO-INFRA-001: DNS required for callback URLs
        - REQ-ECO-STORAGE-001: Session storage for tokens (Redis)
```

**Architecture Decision Records (ADRs) as Constraint Acknowledgment**:

```markdown
# ADR-001: Select Backend Framework

## Context
Operating environment E(t) provides:
- Team knows: Python, JavaScript
- Team doesn't know: Go, Rust, Elixir
- Timeline: 6 months to launch
- Scale requirement: 10k concurrent users (REQ-NFR-SCALE-001)

## Constraint Analysis
| Framework | Team Skill | Performance | Async | Learning Curve | Viable? |
|:---|:---|:---|:---|:---|:---|
| Django | High | Medium | Partial | None | ⚠️ Performance |
| Flask | High | Low | No | None | ❌ Scale |
| **FastAPI** | **Medium** | **High** | **Yes** | **1 week** | ✅ **Selected** |
| Express.js | Medium | High | Yes | None | ⚠️ TypeScript switch |
| Go + Gin | None | Highest | Yes | 3 months | ❌ Timeline |

## Decision
Use **FastAPI** - balances team capability constraint with performance constraint

## Constraints Acknowledged
- Team constraint: 1 week learning acceptable
- Performance constraint: Async required for 10k users
- Timeline constraint: Cannot learn Go in 6 months
- Ecosystem constraint: Python ecosystem already familiar

## Constraints Imposed
- Requires Python 3.11+ (FastAPI async features)
- Requires Pydantic for validation (FastAPI peer dependency)
- Requires ASGI server (uvicorn, hypercorn)
- Development environment must support async/await
```

**The Shift**:
- **Before**: ADR as "we chose X"
- **After**: ADR as "given constraints from E(t), X is the viable choice"

---

### Stage 3: Tasks

**Constraints from E(t)**:

```yaml
tasks_stage:
  ecosystem_constraints:
    estimation_constraints:
      # Tasks constrained by available libraries/services

      task: "Implement user login"

      if_using_auth0:  # Ecosystem provides solution
        estimate: 2 days
        subtasks:
          - Configure Auth0 tenant (2 hours)
          - Implement OAuth callback (4 hours)
          - Frontend redirect logic (2 hours)
          - Token verification (2 hours)
          - User profile storage (4 hours)

      if_building_custom:  # Ecosystem doesn't provide
        estimate: 4 weeks
        subtasks:
          - Design password hashing (1 day)
          - Implement registration (3 days)
          - Implement login (2 days)
          - Session management (3 days)
          - Password reset flow (2 days)
          - Email verification (2 days)
          - OAuth (if needed) (1 week)
          - Security audit (1 week)

    dependency_constraints:
      # Task ordering constrained by ecosystem

      cannot_start_coding_until:
        - AWS account provisioned
        - Auth0 tenant created
        - Domain registered (for OAuth callback)
        - SSL certificate obtained
        - CI/CD pipeline configured

    external_blockers:
      # Tasks blocked by ecosystem availability

      task: "Deploy to production"
      blocked_by:
        - AWS account approval (3-5 days)
        - Domain DNS propagation (24-48 hours)
        - SSL certificate issuance (minutes to hours)
        - Third-party API approval (Auth0 tenant review)
```

---

### Stage 4: Code

**Constraints from E(t)**:

```yaml
code_stage:
  ecosystem_constraints:
    language_version:
      # Constrained by cloud provider support
      python: "3.11"  # AWS Lambda supports 3.11, not 3.12 yet

    framework_version:
      # Constrained by compatibility matrix
      fastapi: ">=0.104.0,<1.0.0"
      pydantic: ">=2.0,<3.0"  # Peer dependency

    api_contracts:
      # Constrained by external service
      auth0:
        endpoint: "https://{tenant}.auth0.com"
        token_format: "JWT (RS256)"
        required_scopes: ["openid", "profile", "email"]
        callback_url: "https://yourapp.com/callback"

    coding_standards:
      # Constrained by team/org standards
      linting: "ruff"  # Fast Python linter
      formatting: "black"
      type_checking: "mypy --strict"

    security_requirements:
      # Constrained by compliance
      secrets_management: AWS Secrets Manager (not .env files)
      encryption: TLS 1.3 minimum
      dependencies: No critical/high CVEs

  constraint_examples:

    example_1_auth_implementation:
      code: |
        # Constrained by Auth0 API contract
        import jwt
        from fastapi import FastAPI, Depends, HTTPException

        # CONSTRAINT: Auth0 uses RS256 (ecosystem dictates)
        # CONSTRAINT: Must verify audience and issuer (Auth0 requirement)
        def verify_token(token: str):
            # Ecosystem constraint: Auth0 JWKS endpoint format
            jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

            # Ecosystem constraint: PyJWT library API
            jwks_client = jwt.PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            # Ecosystem constraint: Auth0 token structure
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],  # Auth0 dictates algorithm
                audience=AUTH0_AUDIENCE,  # Auth0 configuration
                issuer=f"https://{AUTH0_DOMAIN}/"  # Auth0 format
            )
            return payload

      constraints_visible:
        - Auth0 JWKS endpoint format (cannot change)
        - PyJWT library API (must use their methods)
        - RS256 algorithm (Auth0 standard)
        - Token structure (Auth0 defines fields)

    example_2_database_connection:
      code: |
        # Constrained by cloud provider, database, ORM
        from sqlalchemy import create_engine

        # CONSTRAINT: PostgreSQL connection string format
        # CONSTRAINT: AWS RDS endpoint format
        # CONSTRAINT: SQLAlchemy engine API
        engine = create_engine(
            f"postgresql://{user}:{password}@{rds_endpoint}:5432/{dbname}",
            pool_size=20,  # Constrained by RDS instance type
            max_overflow=10
        )

      constraints_visible:
        - PostgreSQL connection string format (industry standard)
        - AWS RDS endpoint format (AWS dictates)
        - SQLAlchemy API (library defines interface)
        - Connection pool limits (RDS instance type)
```

---

### Stage 5: System Test

**Constraints from E(t)**:

```yaml
system_test_stage:
  ecosystem_constraints:
    test_environments:
      # Constrained by cost, cloud provider
      staging: "AWS environment mimicking production"
      test_data: "Cannot use production data (GDPR)"

    external_service_mocking:
      # Constrained by third-party API availability

      auth0_testing:
        option_1: "Use Auth0 test tenant (free tier limits)"
        option_2: "Mock Auth0 responses (loses integration testing)"
        option_3: "Use Auth0 sandbox (costs money)"

    test_frameworks:
      # Constrained by language ecosystem
      python:
        unit: pytest
        integration: pytest + testcontainers
        e2e: playwright, selenium
        load: locust, k6

    bdd_constraints:
      # Constrained by Gherkin syntax and Auth0 behavior

      feature: |
        Feature: User Authentication

          Scenario: Successful login
            Given Auth0 is available  # Ecosystem dependency
            And a test user exists in Auth0  # Ecosystem data
            When user submits valid credentials
            Then Auth0 redirects to callback URL  # Ecosystem behavior
            And app receives valid JWT  # Ecosystem contract
            And token has required scopes  # Ecosystem configuration
```

---

### Stage 6: UAT

**Constraints from E(t)**:

```yaml
uat_stage:
  ecosystem_constraints:
    test_users:
      # Constrained by Auth0 user limits
      free_tier: 7000 users maximum
      test_tenant: Separate from production

    business_user_environment:
      # Constrained by what business users have
      browsers: Chrome, Safari, Edge (not IE11 anymore)
      devices: Desktop, mobile (iOS/Android)
      network: Corporate VPN (may block external APIs)

    third_party_availability:
      # Constrained by external service uptime
      auth0_uptime: 99.9% SLA
      payment_gateway: Cannot test real transactions (use sandbox)
```

---

### Stage 7: Runtime Feedback

**Constraints from E(t)**:

```yaml
runtime_stage:
  ecosystem_constraints:
    observability:
      # Constrained by cloud provider, cost
      logs: CloudWatch, Datadog, or self-hosted ELK
      metrics: CloudWatch, Prometheus, Datadog
      traces: X-Ray, Jaeger, Datadog APM

    sla_constraints:
      # Constrained by external dependencies
      overall_sla: min(app_sla, auth0_sla, aws_sla, stripe_sla)

      calculation:
        app_target: 99.9%  # Our goal
        auth0_sla: 99.9%   # Auth0 guarantee
        aws_sla: 99.99%    # AWS guarantee
        stripe_sla: 99.99% # Stripe guarantee

        realistic_sla: 99.9%  # Limited by weakest link (Auth0)

    incident_response:
      # Constrained by external service status pages

      incident: "Users cannot login"

      check_constraints:
        - Auth0 status page (is Auth0 down?)
        - AWS status (is our infrastructure down?)
        - DNS status (is our domain resolving?)
        - SSL certificate (has cert expired?)

    cost_feedback:
      # Constrained by ecosystem pricing changes

      eco_intent_triggers:
        - Auth0 changes pricing → migrate users or accept cost
        - AWS raises prices → optimize or switch regions/services
        - Stripe fee increase → pass to customers or absorb
```

---

## Formalizing as Constraint Vector (Category Theory)

### Mathematical Model

```
For each SDLC stage S ∈ {Requirements, Design, Tasks, Code, Test, UAT, Runtime}:

Decisions(S) = f(Intent(S), E(t))

where:
  Intent(S) = what we want to build at stage S
  E(t) = operating environment constraint vector at time t
  Decisions(S) = actual viable choices given constraints

Constraint Propagation:
  E(t) → Requirements → Design → Tasks → Code → Test → UAT → Runtime

Each stage inherits constraints from:
  1. Upstream stages (Requirements → Design)
  2. Ecosystem E(t) (external reality)

Each stage adds constraints to:
  1. Downstream stages (Design → Code)
```

### Fibration Extended

**Original Fibration** (from Category Theory formalization):
```
p: 𝓔_Assets → 𝓑_Req
```

**Extended with Operating Environment**:
```
p': (𝓔_Assets × 𝓒_SDLC) → (𝓑_Req × E(t))

Each asset is created in:
  - A specific SDLC stage
  - Under specific ecosystem constraints at time t

Traceability now includes:
  - What requirement it implements (𝓑_Req)
  - What ecosystem constraints it operated under (E(t))
```

**Example Trace**:
```python
# code/auth_service.py

# Implements: REQ-F-AUTH-001 (functional requirement)
#
# Operating under ecosystem constraints E(2025-11-20):
#   - Python 3.11 (AWS Lambda constraint)
#   - Auth0 API contract (external service constraint)
#   - PyJWT library API (ecosystem tool constraint)
#   - GDPR compliance (regulatory constraint)
#   - $5000/mo budget (cost constraint)
#   - 6 month timeline (time constraint)
#   - Team knows Python (capability constraint)

import jwt  # Ecosystem constraint: must use PyJWT library
from auth0 import Auth0  # Ecosystem constraint: Auth0 SDK

def verify_token(token: str):
    """
    Implements: REQ-F-AUTH-001

    Constrained by:
      - Auth0 token format (RS256 JWT)
      - Auth0 JWKS endpoint
      - PyJWT verification API
    """
    # Ecosystem dictates all of this code structure
    ...
```

---

## Documentation Model: Constraint Declaration, Not Enumeration

### ❌ **Wrong Approach**: Try to List All Dependencies

```yaml
# This is impossible and wrong
ecosystem_requirements:
  REQ-ECO-001: Python 3.11
  REQ-ECO-002: FastAPI 0.104
  REQ-ECO-003: Pydantic 2.0
  REQ-ECO-004: SQLAlchemy 2.0
  REQ-ECO-005: psycopg2
  REQ-ECO-006: requests
  REQ-ECO-007: Auth0 SDK
  # ... 500 more dependencies
  # ... implicit dependencies on OS, stdlib, DNS, HTTP, TLS, ...
```

---

### ✅ **Correct Approach**: Declare Constraint Context Per Stage

```yaml
# Requirements Stage
requirements_stage:
  operating_environment_context:
    compliance: [GDPR, SOC2]
    team_capabilities: [Python, JavaScript]
    budget: $5000/month
    timeline: 6 months
    available_services: [Auth0, Stripe, AWS, SendGrid]

  constraint_impact_on_requirements:
    - Cannot build custom auth (time/cost/compliance constraints)
    - Must use cloud storage (scale constraints)
    - Must integrate payment provider (PCI-DSS constraint)

---

# Design Stage
design_stage:
  operating_environment_context:
    inherited_from: requirements_stage

    architecture_constraints:
      cloud_provider: AWS (team knowledge)
      container_orchestration: ECS (simpler than Kubernetes)
      authentication: Auth0 (compliance + timeline)

    framework_choices:
      backend: FastAPI (performance + team capability)
      frontend: React (team expertise)
      database: PostgreSQL (ACID + compliance)

  adr_references:
    - ADR-001: Backend framework selection (acknowledges constraints)
    - ADR-002: Cloud provider selection (acknowledges constraints)
    - ADR-003: Auth provider selection (acknowledges constraints)

---

# Code Stage
code_stage:
  operating_environment_context:
    inherited_from: design_stage

    concrete_constraints:
      python_version: "3.11"  # AWS Lambda support
      fastapi_version: ">=0.104.0,<1.0.0"
      auth0_api: "https://{tenant}.auth0.com"
      postgresql_version: "15"  # RDS latest stable

  constraint_manifestation:
    # Every code file operates under these constraints
    # No need to enumerate - they're implicit in the code
```

---

## Practical Guidance: Acknowledging vs Enumerating

### Do This: Acknowledge Major Strategic Constraints

**In ADRs** (Design Stage):
```markdown
# ADR-001: Cloud Provider Selection

## Operating Environment Constraints
- Team knows AWS (5 years experience)
- Team doesn't know GCP (would require 3 months training)
- Timeline: 6 months to launch (cannot afford training)
- Compliance: SOC2 (requires US data residency)
- Budget: $5000/month initial (AWS free tier helpful)

## Decision
AWS - constrained by team capability and timeline

## Ecosystem Dependencies Introduced
- AWS SDK (boto3)
- AWS services (EC2, RDS, S3, CloudWatch)
- AWS IAM (authentication/authorization)
- AWS CloudFormation or Terraform (IaC)

## Constraints Imposed on Downstream
- All infrastructure must be AWS-compatible
- Developers must learn AWS console/SDK
- CI/CD must integrate with AWS
- Monitoring must use CloudWatch or AWS-compatible tools
```

---

### Don't Do This: Exhaustive Dependency Lists

**❌ Bad**:
```yaml
dependencies:
  python: 3.11.5
  fastapi: 0.104.1
  pydantic: 2.5.0
  pydantic-core: 2.14.1
  pydantic-settings: 2.1.0
  starlette: 0.32.0
  uvicorn: 0.24.0
  typing-extensions: 4.8.0
  annotated-types: 0.6.0
  # ... 200 more transitive dependencies
```

**Why bad**: This is what `requirements.txt` / `package-lock.json` is for

---

### Instead: Declare Constraint Sources

**✅ Good**:
```yaml
code_stage:
  ecosystem_constraint_sources:

    language_runtime:
      python: ">=3.11,<3.13"
      reason: "AWS Lambda supports 3.11; team experienced with 3.11"

    core_frameworks:
      backend: FastAPI
      reason: "Performance requirements + async support"
      constraint_file: requirements.txt

    external_services:
      authentication: Auth0
      reason: "Compliance + timeline constraints"
      api_contract: https://auth0.com/docs/api

    cloud_infrastructure:
      provider: AWS
      reason: "Team expertise"
      terraform_dir: infrastructure/

    compliance_constraints:
      data_residency: US
      encryption: TLS 1.3+
      secrets: AWS Secrets Manager

  constraint_documentation:
    detailed_dependencies: requirements.txt (auto-generated)
    architecture_decisions: docs/adrs/
    api_contracts: docs/external_apis/
    infrastructure: infrastructure/terraform/
```

---

## Summary: Constraint Vector Thinking

### Key Mindset Shifts

| Old Thinking | New Thinking |
|:---|:---|
| "List all dependencies" | "Acknowledge constraint context" |
| "REQ-ECO-* for everything" | "E(t) as given environment" |
| "Ecosystem is our choice" | "Ecosystem constrains our choices" |
| "Document what we use" | "Document why we couldn't use alternatives" |
| "Dependencies are requirements" | "Ecosystem is the operating reality" |

### Practical Application

**At each SDLC stage, ask**:
1. **What constraints does E(t) impose on this stage?**
2. **What decisions are constrained by ecosystem?**
3. **What constraints does this stage add for downstream stages?**
4. **How do we document the constraint context (not enumerate dependencies)?**

**Examples**:
- Requirements: "We must integrate Auth0 because we cannot build custom auth given compliance and timeline constraints"
- Design: "We choose FastAPI because it's the only Python framework that meets performance requirements with acceptable team learning curve"
- Code: "We use PyJWT library because Auth0 uses JWT tokens and PyJWT is the ecosystem standard"

---

## Integration with Category Theory Formalization

### Updated Structures

**Ecosystem Category 𝓔_Eco** is **NOT** a category we build - it's the **ambient category** we operate within:

```
𝓔_Eco(t) = Background category (given, external)

𝓒_SDLC = Category we build (our project)

Functor F: 𝓒_SDLC → 𝓔_Eco
  Maps each SDLC stage decision to its ecosystem constraint context

F(Requirements) = {compliance_constraints, available_services, ...}
F(Design) = {frameworks, cloud_providers, architectural_patterns, ...}
F(Code) = {language_versions, library_APIs, external_APIs, ...}
```

**Key Insight**: We don't "select from marketplace" - we **operate within ecosystem constraints**.

The marketplace utility function becomes:
```
U: (Decision × E(t)) → ℝ

Given ecosystem constraints E(t), what's the utility of decision D?

Not: "What's the best service?"
But: "Given constraints, what's viable?"
```

---

## Conclusion

**External dependencies are not discrete requirements to enumerate** - they are the **continuous constraint vector** that:

1. ✅ **Pre-exists** before we write any requirements
2. ✅ **Constrains decisions** at every SDLC stage
3. ✅ **Evolves independently** (Eco-Intent captures this)
4. ✅ **Cannot be exhaustively listed** (but context can be declared)
5. ✅ **Shapes viable solution space** (not just implementation details)

**Documentation Strategy**:
- **Acknowledge** major strategic constraints in ADRs
- **Declare** constraint context per SDLC stage
- **Trace** how constraints propagate downstream
- **Monitor** ecosystem evolution (Eco-Intent)
- **Don't enumerate** every transitive dependency (that's tooling's job)

**The ecosystem is not something we build - it's the environment we build within.**

---

**Next**: Update v1.2 to reflect ecosystem as constraint vector, not discrete requirements
