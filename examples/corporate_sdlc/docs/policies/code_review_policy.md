# Code Review Policy
**Version**: 3.0
**Last Updated**: 2024-Q4
**Status**: Mandatory

## Purpose
Ensure code quality, knowledge sharing, and compliance through structured code review.

## Requirements

### 1. All Code Must Be Reviewed
- NO direct commits to protected branches
- Minimum 1 reviewer (2 for production)
- Reviewer must be different from author
- Reviews completed within 24 hours

### 2. Review Checklist
Reviewers must verify:
- [ ] Code follows corporate standards
- [ ] Tests are present and passing
- [ ] No security vulnerabilities
- [ ] No hardcoded secrets
- [ ] Documentation is updated
- [ ] Performance considerations addressed

### 3. Review Process
1. Developer creates pull request
2. Automated checks run (tests, linting, security)
3. Reviewer(s) assigned
4. Reviewer provides feedback
5. Developer addresses feedback
6. Reviewer approves
7. Code merged

### 4. Approval Requirements
- **Development**: 1 technical reviewer
- **Staging**: 1 technical + 1 QA reviewer
- **Production**: 2 technical + 1 security + 1 manager

### 5. Review Standards
- Be constructive and respectful
- Focus on code, not developer
- Provide specific, actionable feedback
- Explain reasoning
- Acknowledge good work

## Exceptions
Emergency hotfixes may bypass review with CISO approval, but must be reviewed post-deployment.

---
*For questions, contact engineering@acme.com*
