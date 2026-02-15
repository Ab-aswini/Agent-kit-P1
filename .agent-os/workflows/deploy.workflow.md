# Deploy Workflow

> Ship code to staging or production environments.

## Trigger
- All tests pass
- CTS-001 approves deployment
- Human Owner approves (for production)

## Agent Sequence

### Step 1: Pre-Deploy Verification
**Agent:** CTS-001
- Verify all tests pass
- Confirm no critical risks open
- Check deployment runbook is current

**Gate:** CTS-001 pre-deploy approval

### Step 2: Build
**Agent:** DO-001 (Docker Engineer)
- Build production Docker images
- Verify image health checks
- Tag with version

### Step 3: Database Migration
**Agent:** DB-002 (Migration Manager)
- Run pending migrations on staging first
- Verify data integrity
- Prepare rollback scripts

**Gate:** CTS-001 approves migration

### Step 4: Deploy to Staging
**Agent:** DO-003 (Deployment)
- Deploy to staging environment
- Run smoke tests
- Verify monitoring/logging

### Step 5: Staging Verification
**Agent:** QA-004 (E2E Test)
- Run E2E tests against staging
- Verify all critical flows
- Check performance metrics

**Gate:** Staging tests pass

### Step 6: Production Deploy
**Agent:** DO-003 (Deployment)
- Execute zero-downtime deployment
- Monitor for errors
- Verify health checks

**Gate:** Human Owner approves production deployment

### Step 7: Post-Deploy
**Agent:** DO-006 (Monitoring)
- Verify monitoring dashboards
- Confirm no error spikes
- Watch performance metrics

### Step 8: Memory Update
- Update deployment runbook
- Log deployment in decisions.md
- Update version in project-overview.md

## Rollback Procedure
1. DO-003 reverts to previous version
2. DB-002 runs down migrations if needed
3. Verify rollback success
4. Post-mortem with CTS-001

## Failure Handling
- Build failure → Fix and restart workflow
- Migration failure → Rollback and debug
- Staging failure → Fix and re-deploy staging
- Production error spike → Immediate rollback
