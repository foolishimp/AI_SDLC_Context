# requirements-skills Plugin

**Transform Intent into Structured, Traceable Requirements for AI SDLC v3.0**

Version: 1.0.0

---

## Overview

The `requirements-skills` plugin transforms raw intent into structured requirements with REQ-* keys, disambiguates into business rules (BR-*), constraints (C-*), and formulas (F-*), and supports the requirements refinement loop from TDD/BDD discoveries.

**Key Innovation**: Requirements refinement loop - discoveries during implementation flow back to update requirements.

---

## Capabilities

### 1. Requirement Extraction (1 skill)

**Skill**: `requirement-extraction`

**Purpose**: Transform raw intent into structured REQ-* requirements

**Workflow**:
```
Raw Intent: "Add user login feature"
  ↓ (extraction)
REQ-F-AUTH-001: User login with email/password
  - Unique key
  - Description
  - Acceptance criteria
  - Business context
  - Traceability to INT-042
```

---

### 2. Requirement Disambiguation (4 skills)

**Orchestrator**: `disambiguate-requirements`

**Sub-skills**:
- `extract-business-rules` - Extract BR-* (validation, logic)
- `extract-constraints` - Extract C-* (ecosystem E(t) constraints)
- `extract-formulas` - Extract F-* (calculations, algorithms)

**Purpose**: Break vague requirements into precise specifications for code generation

**Workflow**:
```
Vague: "Users can log in with email and password"
  ↓ (disambiguation)
Precise:
  BR-001: Email regex validation
  BR-002: Password min 12 chars
  BR-003: Lockout after 3 attempts (15min)
  C-001: Database timeout 100ms
  C-002: bcrypt hashing (cost 12)
  F-001: lockout_expiry = last_attempt + 900 sec
  ↓ (enables)
Code Autogeneration:
  validate_email() from BR-001
  validate_password() from BR-002
  LockoutTracker class from BR-003
  calculate_lockout_expiry() from F-001
```

---

### 3. Requirements Refinement Loop (1 skill)

**Skill**: `refine-requirements`

**Purpose**: Update requirements from TDD/BDD discoveries

**The Refinement Loop**:
```
Requirements (REQ-*, BR-*, C-*, F-*)
  ↓ used for
TDD/BDD Implementation
  ↓ discovers
Edge Cases, Race Conditions, Missing Rules
  ↓ feeds back to
Updated Requirements (new BR-*, C-*, F-*)
  ↓ used for
Next Implementation (better specs)
```

**Example**:
```
Developer: "What if two users register with same email simultaneously?"
  ↓ (refine-requirements captures)
BR-015: Concurrent registration prevention
  - Use database unique constraint
  - Discovered: 2025-11-20 during TDD GREEN phase
  - Test added: test_concurrent_registration_prevented()
  ↓ (prevents)
Next Developer: Sees BR-015, doesn't ask same question
```

---

### 4. Traceability Management (2 skills)

**Skills**:
- `create-traceability-matrix` - Map INT-* → REQ-* → all artifacts
- `validate-requirements` - Quality gate for requirements

**Purpose**: Ensure complete traceability and requirement quality

---

## Installation

### From Marketplace

```bash
/plugin marketplace add foolishimp/ai_sdlc_method
/plugin install @aisdlc/requirements-skills
```

### Local Installation

```bash
git clone https://github.com/foolishimp/ai_sdlc_method.git
cd your-project
/plugin marketplace add ../ai_sdlc_method
/plugin install requirements-skills
```

---

## Usage Examples

### Example 1: Extract Requirements from Intent

```
You: "We need payment processing with credit cards"

Claude: (invokes requirement-extraction)

I need more details to extract requirements:
  1. What payment methods? (Visa, Mastercard, Amex?)
  2. Payment provider? (Stripe, Braintree?)
  3. Compliance? (PCI-DSS level?)
  4. Currency? (USD, EUR, multi-currency?)

You: "Visa and Mastercard via Stripe, PCI-DSS Level 1, USD only"

Claude: Creating requirements...

Requirements Extracted:
  REQ-F-PAY-001: Credit card payment via Stripe
  REQ-NFR-SEC-001: PCI-DSS Level 1 compliance
  REQ-DATA-AQ-001: Card number validation

Created: docs/requirements/payments.md
```

---

### Example 2: Disambiguate Requirements

```
You: "Disambiguate REQ-F-PAY-001"

Claude: (invokes disambiguate-requirements)

Extracting business rules, constraints, and formulas...

Disambiguated:

Business Rules (5):
  BR-001: Card type validation (Visa, Mastercard only)
  BR-002: Card number Luhn algorithm
  BR-003: CVV 3 digits
  BR-004: Expiry not in past
  BR-005: Amount $0.01 - $10,000

Constraints (4):
  C-001: PCI-DSS (never store full card numbers)
  C-002: Stripe API timeout (10 seconds)
  C-003: Idempotency required
  C-004: 3D Secure for amounts >$1,000

Formulas (2):
  F-001: Stripe fee = (amount * 0.029) + 0.30
  F-002: Idempotency key = SHA256(merchant + time + amount)

Updated: docs/requirements/payments.md
Ready for code generation!
```

---

### Example 3: Refine from TDD Discovery

```
You: "I'm implementing REQ-F-PAY-001 and discovered an issue"

Claude: What did you discover?

You: "What if user clicks 'Pay' button twice?"

Claude: (invokes refine-requirements)

Great catch! That's a duplicate payment issue.

Adding to REQ-F-PAY-001:

  BR-015: Duplicate payment prevention ⭐ NEW
    - Use Stripe idempotency keys
    - Same key = same charge (no duplicate)
    - Key from F-002
    - Discovered: 2025-11-20 during TDD GREEN phase
    - Source: Developer question

Updated:
  - docs/requirements/payments.md (added BR-015)
  - docs/traceability/requirement-refinements.yml

Next developer won't need to discover this!
```

---

## Configuration

```yaml
plugins:
  - name: "@aisdlc/requirements-skills"
    config:
      extraction:
        auto_extract_on_intent: true
        require_acceptance_criteria: true
        ask_clarifying_questions: true
        max_questions: 6

      disambiguation:
        auto_disambiguate: true
        min_br_per_requirement: 2
        require_autogeneration_specs: true

      refinement:
        auto_refine_on_discovery: true
        track_discovery_source: true
        update_traceability_on_refine: true

      validation:
        require_unique_keys: true
        require_testable_criteria: true
        block_ambiguous_language: true
```

---

## Dependencies

- **Required**: `@aisdlc/aisdlc-core` (^3.0.0) - REQ-* key patterns

**Works With**:
- `@aisdlc/code-skills` - Uses BR-*, C-*, F-* for code generation
- `@aisdlc/design-skills` - Uses requirements for design
- `@aisdlc/testing-skills` - Uses requirements for test generation

---

## Skills Completion Status

| Skill | Status | Type | Lines |
|-------|--------|------|-------|
| requirement-extraction | ✅ Complete | Actuator | 407 |
| disambiguate-requirements | ✅ Complete | Orchestrator | 376 |
| extract-business-rules | ✅ Complete | Actuator | 239 |
| extract-constraints | ✅ Complete | Actuator | 249 |
| extract-formulas | ✅ Complete | Actuator | 104 |
| refine-requirements | ✅ Complete | Actuator | 359 |
| create-traceability-matrix | ✅ Complete | Sensor | 217 |
| validate-requirements | ✅ Complete | Sensor | 202 |
| **TOTAL** | **✅ 100%** | **-** | **2,153** |

---

## Integration Example

**Complete Workflow** (Requirements → Code):

```
User: "Add payment processing feature"

1. requirement-extraction:
   → Creates REQ-F-PAY-001

2. disambiguate-requirements:
   → Extracts BR-001 through BR-005 (validation rules)
   → Extracts C-001 through C-004 (Stripe constraints, PCI-DSS)
   → Extracts F-001, F-002 (fee calc, idempotency key)

3. validate-requirements:
   → Checks quality (unique keys, testable, clear)
   → Quality gate: PASS ✅

4. (Design stage - different plugin)

5. (Code stage - code-skills plugin)
   tdd-workflow for REQ-F-PAY-001:
     → RED: Write tests for BR-001 through BR-005
     → GREEN: Implement payment processing
     → Developer discovers: "What about duplicate payments?"

6. refine-requirements:
   → Adds BR-015 (duplicate prevention)
   → Adds F-003 (idempotency key formula)
   → Updates requirements doc
   → Next implementation uses refined specs ✓
```

---

## Roadmap

**v1.0.0** (Current):
- ✅ 8 skills complete
- ✅ Extraction, disambiguation, refinement
- ✅ Traceability and validation

**v1.1.0** (Future):
- AI-assisted requirement generation from user interviews
- Requirement templates by domain
- Automatic refinement suggestions
- Requirements versioning

---

**"Excellence or nothing"** 🔥
