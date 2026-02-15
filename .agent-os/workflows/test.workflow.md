# Test Workflow

> Run comprehensive test suites across the project.

## Trigger
- Before deployment
- After significant changes
- Scheduled test runs

## Agent Sequence

### Step 1: Unit Tests
**Agent:** QA-002 (Unit Test Generator)
- Run all unit tests
- Identify and fix gaps in coverage
- Report results

**Gate:** 80%+ coverage required

### Step 2: Integration Tests
**Agent:** QA-003 (Integration Test)
- Test API endpoints
- Verify database operations
- Test service interactions

### Step 3: End-to-End Tests
**Agent:** QA-004 (End-to-End Test)
- Run critical user journey tests
- Test across browsers/viewports
- Verify complete workflows

### Step 4: Performance Tests
**Agent:** QA-005 (Performance Testing)
- Run load tests
- Check response time SLAs
- Identify bottlenecks

### Step 5: Security Tests
**Agent:** QA-006 (Security Testing)
- Run OWASP checks
- Audit dependencies
- Test auth boundaries

### Step 6: Results Report
**Agent:** CTS-001
- Review all test results
- Approve or block deployment
- Update risk log if needed

## Memory Updates
- `memory/qa/test-coverage.md` — Updated coverage metrics
- `memory/qa/performance-benchmarks.md` — Updated benchmarks
- `memory/global/risk-log.md` — New risks if found

## Failure Handling
- Unit test failure → Return to relevant agent for fix
- Integration failure → Debug workflow for API issues
- Performance failure → Performance agent investigates
- Security failure → Risk agent escalates
