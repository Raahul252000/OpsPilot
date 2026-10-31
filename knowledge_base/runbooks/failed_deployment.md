# Runbook: Failed Deployment

## Purpose
Guide investigation when a new application release fails to deploy or causes service degradation.

## Symptoms
- Deployment pipeline reports a failed stage.
- New instances fail readiness or liveness checks.
- Error rate or latency rises after a release.
- Application startup fails due to configuration, dependency, or migration errors.

## Initial checks
1. Record release identifier, environment, start time, and failed pipeline stage.
2. Read deployment and application startup logs.
3. Check readiness/liveness status and instance count.
4. Compare configuration and dependency changes with the previous known-good release.
5. Check whether a database migration or external dependency changed.
6. Compare service metrics before and after deployment.

## Possible causes
- Invalid configuration or missing secret.
- Dependency incompatibility.
- Application startup exception.
- Failed or incompatible database migration.
- Resource or health-check configuration mismatch.
- A code regression.

## Safe response
- Do not assume the deployment caused every symptom merely because timing overlaps.
- Preserve logs and release metadata for diagnosis.
- Rollback is a controlled change: verify rollback compatibility, especially with database migrations, and obtain required approval.
- Never expose secret values in incident notes or logs.

## Verification
- Deployment status is healthy.
- Instances pass readiness checks.
- Error rate and latency return to expected range.
- Key application workflows succeed.
- No new database or dependency errors appear.

## Escalation
Escalate to the release owner if rollback compatibility is uncertain, migrations are involved, or service health does not recover.
