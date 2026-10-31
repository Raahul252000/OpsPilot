# Runbook: Database Connection Failures

## Purpose
Guide initial investigation when an application cannot establish or maintain database connections.

## Symptoms
- API requests fail with database connection timeout errors.
- Logs contain connection-refused, connection-timeout, or pool-acquisition-timeout messages.
- Database connection count approaches the configured limit.
- Requests slow down while waiting for a connection.

## Possible causes
- Application connection pool is exhausted.
- Connections are not returned to the pool after use.
- Database is unavailable, overloaded, or at its connection limit.
- Network connectivity or DNS resolution is failing.
- A recent deployment changed connection handling or concurrency.

## Initial checks
1. Identify the affected service, environment, and time window.
2. Check database service health using an approved monitoring source.
3. Inspect application logs for connection-related errors and timestamps.
4. Inspect active connections, pool utilization, and configured connection limits.
5. Check for long-running queries or sessions waiting on locks.
6. Compare symptom onset with recent deployments or traffic changes.

## Interpretation
- High pool utilization with a healthy database may indicate slow queries, leaked connections, or insufficient pool capacity.
- A database health failure suggests the issue may be downstream of the application.
- Errors beginning after a deployment make the change a useful lead, but not proof of causation.

## Safe response
- Gather evidence before changing pool sizes or restarting services.
- If long-running queries are present, capture query identifiers and durations for the database owner.
- Follow the approved database recovery procedure if the database itself is unhealthy.
- Do not terminate sessions, increase connection limits, or restart production services without authorization.

## Verification
- Confirm database health and pool utilization return to expected ranges.
- Confirm connection timeout errors decline.
- Confirm representative API requests succeed.
- Observe metrics for an agreed monitoring window.

## Escalation
Escalate to the database owner if connection limits are reached, locks persist, database health is degraded, or evidence is inconclusive.
