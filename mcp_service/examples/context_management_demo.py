#!/usr/bin/env python3
"""
Context Management Demo

Shows how Claude can dynamically load and switch between project contexts.
This simulates Claude's behavior when using the MCP service.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager, format_context_for_llm


def simulate_claude_session():
    """Simulate a Claude session using dynamic context management."""

    # Initialize
    repo_path = Path.cwd() / "example_projects_repo"
    repo = ProjectRepository(repo_path)
    context_mgr = ContextManager(repo)

    print("=" * 80)
    print("DYNAMIC CONTEXT MANAGEMENT DEMO")
    print("Simulating Claude switching contexts during a conversation")
    print("=" * 80)
    print()

    # ==========================================================================
    # SCENARIO 1: Working on payment gateway
    # ==========================================================================
    print("📝 User: Load payment_gateway context\n")

    context = context_mgr.load_context("payment_gateway")
    print("🤖 Claude: Context loaded! Let me review the requirements...")
    print()
    print(format_context_for_llm(context))

    print("\n" + "=" * 80)
    print("🔍 Claude's Understanding:")
    print("  • This is a RESTRICTED project (PCI compliant)")
    print("  • I need to follow strict standards:")
    print("    - 95% test coverage (very high)")
    print("    - Security testing required")
    print("    - 4-hour SLA for critical fixes")
    print("    - Zero code smells tolerated")
    print("  • I should apply PCI compliance best practices")
    print("=" * 80)
    print()

    # User asks Claude to generate code
    print("📝 User: Write a function to process credit card payments\n")

    print("🤖 Claude: Based on payment_gateway context, I'll create a PCI-compliant")
    print("   payment processing function with proper security measures...\n")

    print("```python")
    print("""from typing import Dict
from payment_gateway.security import tokenize_card, fraud_check
from payment_gateway.audit import log_transaction

async def process_payment(
    card_number: str,
    amount: float,
    merchant_id: str
) -> Dict[str, any]:
    \"\"\"
    Process credit card payment with PCI DSS compliance.

    Requirements from payment_gateway context:
    - Card tokenization (PCI DSS)
    - Fraud detection (security requirement)
    - Audit logging (compliance)
    - 95% test coverage

    Args:
        card_number: Card number (will be tokenized)
        amount: Payment amount
        merchant_id: Merchant identifier

    Returns:
        Transaction result

    Raises:
        FraudDetectedException: High fraud score
        PaymentProcessingException: Payment failed
    \"\"\"
    # Fraud detection (payment_gateway security requirement)
    fraud_score = await fraud_check(card_number, amount, merchant_id)
    if fraud_score > 85:
        await log_transaction(merchant_id, "FRAUD_REJECTED", amount)
        raise FraudDetectedException(f"Fraud score: {fraud_score}")

    # Tokenize (PCI DSS compliance)
    token = await tokenize_card(card_number)

    # Process
    result = await payment_processor.charge(token, amount, merchant_id)

    # Audit log (compliance requirement)
    await log_transaction(merchant_id, result.status, amount, result.id)

    return result


# Comprehensive tests (meeting 95% coverage requirement)
@pytest.mark.asyncio
async def test_process_payment_success():
    result = await process_payment("4532...", 100.00, "m_123")
    assert result["status"] == "SUCCESS"

@pytest.mark.asyncio
async def test_process_payment_fraud_rejected():
    with pytest.raises(FraudDetectedException):
        await process_payment("fraud_card", 10000.00, "m_suspicious")

@pytest.mark.asyncio
async def test_process_payment_audit_logging():
    await process_payment("4532...", 50.00, "m_123")
    # Verify audit log created
    logs = await get_audit_logs("m_123")
    assert len(logs) > 0
""")
    print("```\n")

    print("=" * 80)
    print("🎯 Claude's Code Decisions Based on Context:")
    print("  ✓ Added fraud detection (security requirement)")
    print("  ✓ Card tokenization for PCI compliance")
    print("  ✓ Audit logging for compliance")
    print("  ✓ Comprehensive error handling")
    print("  ✓ 3 tests to start toward 95% coverage goal")
    print("  ✓ Detailed docstring explaining requirements")
    print("=" * 80)
    print()

    # ==========================================================================
    # SCENARIO 2: Switch to admin dashboard (relaxed requirements)
    # ==========================================================================
    print("\n\n📝 User: Switch to admin_dashboard context\n")

    switch_result = context_mgr.switch_context("payment_gateway", "admin_dashboard")
    print("🤖 Claude: Switching contexts...\n")

    if switch_result["changes"]:
        print("🔄 Requirement Changes Detected:")
        for name, change in switch_result["changes"].items():
            if change:
                direction = change.get("direction", "")
                emoji = "📉" if direction == "relaxed" else "📈"
                print(f"  {emoji} {change['label']}: {change['old']} → {change['new']}")
                if direction:
                    print(f"     ({direction.upper()})")
        print()

    print("=" * 80)
    print("🔍 Claude's Updated Understanding:")
    print("  • This is an INTERNAL project (lower security)")
    print("  • Standards are more relaxed:")
    print("    - 75% test coverage (instead of 95%)")
    print("    - Basic testing only (no penetration tests)")
    print("    - 30 code smells allowed (vs 0)")
    print("  • I can use simpler implementations")
    print("=" * 80)
    print()

    # User asks for similar function but in dashboard context
    print("📝 User: Write a function to display payment statistics\n")

    print("🤖 Claude: Based on admin_dashboard context, I'll create a simpler")
    print("   internal function with basic validation...\n")

    print("```python")
    print("""from typing import Dict, List
from datetime import datetime, timedelta

def get_payment_statistics(
    merchant_id: str,
    days: int = 30
) -> Dict[str, any]:
    \"\"\"
    Get payment statistics for internal dashboard.

    Internal tool - relaxed requirements from admin_dashboard context.

    Args:
        merchant_id: Merchant to query
        days: Number of days to analyze

    Returns:
        Statistics dictionary
    \"\"\"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Query transactions
    transactions = db.query_transactions(
        merchant_id=merchant_id,
        start=start_date,
        end=end_date
    )

    # Calculate stats
    total_amount = sum(t.amount for t in transactions)
    total_count = len(transactions)
    avg_amount = total_amount / total_count if total_count > 0 else 0

    return {
        "merchant_id": merchant_id,
        "period_days": days,
        "total_transactions": total_count,
        "total_amount": total_amount,
        "average_amount": avg_amount,
        "success_rate": calculate_success_rate(transactions)
    }


# Basic tests (targeting 75% coverage)
def test_get_payment_statistics():
    stats = get_payment_statistics("m_123", days=7)
    assert stats["merchant_id"] == "m_123"
    assert "total_transactions" in stats

def test_get_payment_statistics_no_data():
    stats = get_payment_statistics("m_empty", days=30)
    assert stats["total_transactions"] == 0
    assert stats["average_amount"] == 0
""")
    print("```\n")

    print("=" * 80)
    print("🎯 Claude's Code Decisions Based on New Context:")
    print("  ✓ Simpler implementation (no fraud checks)")
    print("  ✓ No tokenization (internal data)")
    print("  ✓ Basic error handling (not mission-critical)")
    print("  ✓ 2 tests (targeting 75% coverage)")
    print("  ✓ Lighter documentation")
    print("  ✓ No audit logging (internal tool)")
    print("=" * 80)
    print()

    # ==========================================================================
    # SCENARIO 3: Query current context
    # ==========================================================================
    print("\n\n📝 User: What are the current requirements?\n")

    question = "What are the testing and security requirements?"
    context_info = context_mgr.query_context(question)
    print("🤖 Claude: Let me check the current context...\n")
    print(context_info)
    print()

    # ==========================================================================
    # SCENARIO 4: Load production merged context
    # ==========================================================================
    print("\n\n📝 User: Load payment_gateway_prod_v1_0_0 context\n")

    prod_context = context_mgr.load_context("payment_gateway_prod_v1_0_0")
    print("🤖 Claude: Loading production context (merged project)...\n")

    print("=" * 80)
    print("🔍 Claude's Production Context Understanding:")
    print(f"  • Type: {prod_context['metadata']['type']}")
    print(f"  • Merged from: {', '.join(prod_context['merge_info']['merged_from'])}")
    print(f"  • Environment: {prod_context.get('environment', 'N/A')}")
    build_info = prod_context.get('build')
    if build_info:
        print(f"  • Build version: {build_info.get('version', 'N/A')}")
    else:
        print(f"  • Build version: N/A")
    print()
    print("  Runtime overrides applied:")
    if prod_context.get('merge_info', {}).get('runtime_overrides'):
        for key, value in prod_context['merge_info']['runtime_overrides'].items():
            print(f"    • {key}: {value}")
    print("=" * 80)
    print()

    print("🤖 Claude: This is a PRODUCTION deployment context!")
    print("   I have full configuration from:")
    print("   - Corporate policies (acme_corporate)")
    print("   - Python standards (python_standards)")
    print("   - Project requirements (payment_gateway)")
    print("   - Production overrides (environment, build, deployment)")
    print()
    print("   I should assume:")
    print("   • Maximum security awareness")
    print("   • No debugging/logging of sensitive data")
    print("   • Production-grade error handling")
    print("   • Continuous security scanning")
    print()

    # ==========================================================================
    # SCENARIO 5: Context summary
    # ==========================================================================
    print("\n\n📝 User: Show me a summary of the current context\n")

    summary = context_mgr.get_context_summary()
    print("🤖 Claude: Here's the current context summary:\n")
    print(f"  Project: {summary['project']}")
    print(f"  Type: {summary['type']}")
    print(f"  Classification: {summary['classification']}")
    print()
    print("  Key Requirements:")
    for key, value in summary['key_requirements'].items():
        print(f"    • {key.replace('_', ' ').title()}: {value}")
    print()

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================
    print("\n\n" + "=" * 80)
    print("✅ DYNAMIC CONTEXT MANAGEMENT DEMONSTRATED")
    print("=" * 80)
    print()
    print("What you just saw:")
    print()
    print("1. 🎯 Context Loading")
    print("   Claude loaded payment_gateway context and understood strict requirements")
    print()
    print("2. 💻 Context-Aware Code Generation")
    print("   Claude generated PCI-compliant code with fraud detection and audit logging")
    print()
    print("3. 🔄 Context Switching")
    print("   Claude switched to admin_dashboard and detected relaxed requirements")
    print()
    print("4. 🎨 Adaptive Code Style")
    print("   Claude generated simpler code appropriate for internal tool")
    print()
    print("5. 📊 Context Querying")
    print("   Claude answered questions based on loaded context")
    print()
    print("6. 🚀 Production Context")
    print("   Claude loaded merged production config with runtime overrides")
    print()
    print("🎯 Key Insight:")
    print("   Claude doesn't just generate code - it understands PROJECT CONTEXT")
    print("   and applies appropriate standards, security measures, and testing")
    print("   requirements based on the loaded context!")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    simulate_claude_session()
