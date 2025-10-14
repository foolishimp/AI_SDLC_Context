# Dynamic Context Management for Claude

## The Big Picture

**AI_SDLC_config MCP Service** is a **dynamic context management system** that allows Claude to:
- Switch between different project contexts on-demand
- Load relevant configurations, policies, and documentation
- Apply appropriate standards based on project type
- Make context-aware decisions using project-specific requirements

## How It Works

### Traditional Approach (Static Context)
```
User: "Write a payment processing function"
Claude: *uses general knowledge, no project-specific context*
```

### With MCP Context Management (Dynamic Context)
```
User: "Load payment_gateway project context"
Claude: *loads via MCP*
  ✓ PCI compliance requirements
  ✓ 95% test coverage requirement
  ✓ Security policies and SLAs
  ✓ Deployment approval chain
  ✓ Architecture documentation

User: "Write a payment processing function"
Claude: *applies payment_gateway context*
  ✓ Follows PCI compliance guidelines
  ✓ Includes security checks (fraud detection, tokenization)
  ✓ Writes tests to meet 95% coverage
  ✓ References architecture documentation
```

---

## Use Cases

### 1. Context Switching Between Projects

```python
# Working on payment gateway (strict requirements)
>>> inspect_project("payment_gateway", "What are the requirements?")

Response:
  • Min coverage: 95%
  • Security: PCI DSS compliant
  • Testing: unit, integration, security, penetration, load
  • Critical fix SLA: 4 hours
  • Max code smells: 0

# Switch to admin dashboard (relaxed requirements)
>>> inspect_project("admin_dashboard", "What are the requirements?")

Response:
  • Min coverage: 75%
  • Security: Standard corporate policies
  • Testing: unit, integration
  • Max code smells: 30
```

**Claude now knows** which standards to apply based on project context!

---

### 2. Policy-Aware Code Generation

```
User: "Load payment_gateway context"
Claude: ✓ Loaded (PCI compliant, 95% coverage, strict security)

User: "Generate a function to process credit card payments"

Claude generates:
```python
from typing import Dict, Optional
from payment_gateway.security import tokenize_card, fraud_check
from payment_gateway.audit import log_transaction

async def process_payment(
    card_number: str,
    amount: float,
    merchant_id: str
) -> Dict[str, any]:
    """
    Process credit card payment with PCI DSS compliance.

    Security:
    - Card tokenization (PCI DSS requirement)
    - Fraud detection (real-time ML scoring)
    - Immutable audit logging

    Args:
        card_number: Tokenized card number
        amount: Payment amount
        merchant_id: Merchant identifier

    Returns:
        Transaction result with status and transaction_id

    Raises:
        FraudDetectedException: If fraud score exceeds threshold
        PaymentProcessingException: If payment fails
    """
    # Fraud detection (payment_gateway requirement)
    fraud_score = await fraud_check(card_number, amount, merchant_id)
    if fraud_score > 85:  # From payment_gateway.security config
        await log_transaction(merchant_id, "FRAUD_REJECTED", amount)
        raise FraudDetectedException(f"High fraud score: {fraud_score}")

    # Tokenize card (PCI DSS compliance)
    token = await tokenize_card(card_number)

    # Process payment
    result = await payment_processor.charge(token, amount, merchant_id)

    # Audit log (compliance requirement)
    await log_transaction(
        merchant_id,
        result.status,
        amount,
        transaction_id=result.transaction_id
    )

    return result


# Tests (meets 95% coverage requirement)
@pytest.mark.asyncio
async def test_process_payment_success():
    """Test successful payment processing."""
    result = await process_payment("tok_123", 100.00, "merch_456")
    assert result["status"] == "SUCCESS"

@pytest.mark.asyncio
async def test_process_payment_fraud_detection():
    """Test fraud detection blocks suspicious transactions."""
    with pytest.raises(FraudDetectedException):
        await process_payment("tok_fraud", 10000.00, "merch_suspicious")

# ... more tests to reach 95% coverage
```

**Without context**: Generic payment function
**With context**: PCI-compliant, fraud detection, audit logging, 95% coverage

---

### 3. Environment-Aware Deployments

```python
# Merge for production with runtime context
merged = merge_projects(
    source_projects=["corporate_base", "python_standards", "payment_gateway"],
    target_project="payment_gateway_prod_v1_0_0",
    runtime_overrides={
        "environment": "production",
        "security.scan_frequency": "continuous",
        "deployment.replicas": 5
    }
)

# Claude now knows production requirements
inspect_project("payment_gateway_prod_v1_0_0", "What are deployment requirements?")

Response:
  • Environment: production
  • Replicas: 5
  • Security scans: continuous (not daily)
  • Approval chain: tech_lead → qa_lead → security_lead → compliance → cto
  • Region: us-east-1
```

---

### 4. Cross-Project Comparison

```
User: "Compare payment_gateway and admin_dashboard requirements"

Claude: Let me load both contexts and compare...

Payment Gateway (High Security):
  • Classification: Restricted
  • PCI Compliant: YES
  • Min Coverage: 95%
  • Security SLA: 4 hours
  • Test Types: 5 (including penetration testing)
  • Approvers: 5 people

Admin Dashboard (Internal Tool):
  • Classification: Internal
  • PCI Compliant: NO
  • Min Coverage: 75%
  • Security SLA: 24 hours
  • Test Types: 2 (basic)
  • Approvers: 2 people

Recommendation: Use payment_gateway standards for customer-facing features,
admin_dashboard standards for internal tools.
```

---

## Context Management Patterns

### Pattern 1: Session Context

```python
class ClaudeSession:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.current_context = None

    async def load_context(self, project_name: str):
        """Load project context into Claude's working memory."""
        self.current_context = await self.mcp.call_tool(
            "inspect_project",
            arguments={
                "project": project_name,
                "query": "Load full project context including requirements, policies, and documentation"
            }
        )
        return self.current_context

    async def apply_context(self, task: str):
        """Apply current context to task."""
        if not self.current_context:
            raise ValueError("No context loaded")

        # Claude uses context to inform its responses
        return f"Applying {self.current_context['project']['name']} standards to: {task}"
```

### Pattern 2: Multi-Context Awareness

```python
# Load multiple contexts for comparison
payment_ctx = load_context("payment_gateway")
dashboard_ctx = load_context("admin_dashboard")

# Ask Claude to apply appropriate context
if is_customer_facing(feature):
    apply_context(payment_ctx)  # Use strict standards
else:
    apply_context(dashboard_ctx)  # Use relaxed standards
```

### Pattern 3: Hierarchical Context

```python
# Load merged context (inherits from all layers)
prod_ctx = load_context("payment_gateway_prod_v1_0_0")

# Claude now has access to:
#   • Corporate policies (from acme_corporate)
#   • Python standards (from python_standards)
#   • Project requirements (from payment_gateway)
#   • Runtime config (from merge overrides)
```

---

## MCP Tools for Context Management

### 1. `load_project_context` (New Tool Concept)

```python
@server.call_tool()
async def load_project_context(project_name: str):
    """
    Load full project context into Claude's working memory.

    Returns:
    - Project metadata
    - All configuration values (merged)
    - Referenced documentation content
    - Policy requirements
    - Quality gates
    - Deployment requirements
    """
    config = repo.get_project_config(project_name)

    # Build comprehensive context
    context = {
        "project": {
            "name": config.get_value("project.name"),
            "classification": config.get_value("project.classification"),
            "pci_compliant": config.get_value("project.pci_compliant")
        },
        "requirements": {
            "testing": {
                "min_coverage": config.get_value("methodology.testing.min_coverage"),
                "required_types": config.get_value("methodology.testing.required_types")
            },
            "coding": {
                "max_complexity": config.get_value("methodology.coding.max_complexity"),
                "style_guide": config.get_value("methodology.coding.standards.style_guide")
            }
        },
        "policies": {
            "security": config.get_content("corporate.policies.security.uri"),
            "code_review": config.get_content("corporate.policies.code_review.uri")
        },
        "documentation": {
            # Load all referenced docs
        }
    }

    return context
```

### 2. `switch_context` (New Tool Concept)

```python
@server.call_tool()
async def switch_context(from_project: str, to_project: str):
    """
    Switch from one project context to another.

    Shows differences in requirements so Claude knows what changed.
    """
    comparison = compare_projects(from_project, to_project)
    return {
        "switched_from": from_project,
        "switched_to": to_project,
        "requirement_changes": comparison
    }
```

### 3. `context_query` (New Tool Concept)

```python
@server.call_tool()
async def context_query(question: str):
    """
    Query current context using natural language.

    Examples:
    - "What testing is required?"
    - "Who needs to approve production deployments?"
    - "What's the security SLA?"
    """
    if not current_context:
        return "No context loaded. Use load_project_context first."

    # Use LLM to answer based on current context
    return llm_answer(question, current_context)
```

---

## Claude Desktop Integration

### Configuration

```json
{
  "mcpServers": {
    "context-manager": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/AI_SDLC_config/mcp_service",
      "env": {
        "DEFAULT_CONTEXT": "corporate_base"
      }
    }
  }
}
```

### Usage in Claude Desktop

```
User: Load payment_gateway context

Claude: *calls load_project_context("payment_gateway")*
✓ Context loaded: Payment Gateway (PCI compliant, 95% coverage)

User: Write a function to validate credit card numbers

Claude: *applies payment_gateway context*

Here's a PCI-compliant credit card validation function following
payment_gateway requirements:

[Generates code with appropriate security, testing, documentation]

User: Switch to admin_dashboard context

Claude: *calls switch_context("payment_gateway", "admin_dashboard")*
✓ Context switched: Admin Dashboard (Internal tool, 75% coverage)
Note: Standards relaxed - min coverage decreased from 95% to 75%

User: Write a function to display user stats

Claude: *applies admin_dashboard context*

Here's a simpler function for the internal dashboard:

[Generates code with relaxed requirements, simpler testing]
```

---

## Benefits of Dynamic Context Management

### For Developers
✅ **Context-Aware Coding**: Claude applies right standards for each project
✅ **Fast Context Switching**: Switch between projects instantly
✅ **Policy Compliance**: Automatic adherence to project policies
✅ **Reduced Cognitive Load**: Don't need to remember all requirements

### For Organizations
✅ **Governance**: Ensure standards are followed
✅ **Risk Management**: Strict standards for high-risk projects
✅ **Flexibility**: Different requirements per project
✅ **Audit Trail**: Git tracks all context changes

### For Claude
✅ **Better Responses**: Context-informed decisions
✅ **Accurate Recommendations**: Based on actual project requirements
✅ **Policy Awareness**: Knows which rules apply
✅ **Documentation Access**: Has relevant docs in context

---

## Advanced Use Cases

### 1. Automatic Context Detection

```python
# Detect project from file path
file_path = "/code/payment-service/api/charge.py"
project = detect_project_from_path(file_path)  # → "payment_gateway"
load_context(project)
```

### 2. Context Inheritance

```python
# Work in prod context (inherits from all layers)
load_context("payment_gateway_prod_v1_0_0")

# Claude has access to:
# - Corporate policies (layer 1)
# - Python standards (layer 2)
# - Payment gateway requirements (layer 3)
# - Production overrides (layer 4)
```

### 3. Context-Based Code Review

```python
# Review code against project context
load_context("payment_gateway")

review_result = review_code(
    code=pull_request_code,
    context=current_context
)

# Claude checks:
# ✓ Meets 95% coverage requirement?
# ✓ Follows PCI compliance?
# ✓ Has required security checks?
# ✓ Proper error handling?
```

---

## Future Enhancements

### 1. Context Stacking
```python
# Stack multiple contexts
push_context("corporate_base")      # Base layer
push_context("python_standards")    # Add Python layer
push_context("payment_gateway")     # Add project layer
push_context("production")          # Add runtime layer

pop_context()  # Remove production, back to project
```

### 2. Context Versioning
```python
# Load specific version of context
load_context("payment_gateway", version="v1.0.0")
load_context("payment_gateway", version="v2.0.0")

# Compare versions
compare_contexts("payment_gateway@v1.0.0", "payment_gateway@v2.0.0")
```

### 3. Context Recommendations
```python
# Ask Claude to recommend context based on task
recommend_context("Build a user authentication system")
# → Suggests: "Use python_standards + security_framework contexts"

recommend_context("Build payment processing")
# → Suggests: "Use payment_gateway context (PCI compliant required)"
```

---

## Summary

**AI_SDLC_config MCP Service** transforms configuration management into **dynamic context management for Claude**:

🎯 **Core Concept**: Projects are contexts that Claude can load, switch between, and apply

🔄 **Dynamic**: Load/unload contexts on-demand during conversation

📚 **Rich Context**: Not just config values - policies, docs, requirements, standards

🧠 **Informed Decisions**: Claude uses context to generate appropriate code, reviews, advice

🎭 **Multi-Context**: Switch between strict (payments) and relaxed (internal tools) contexts

📖 **Audit Trail**: Every context load/switch tracked in git

This is **way more powerful** than static configuration - it's Claude with **situational awareness**! 🚀
