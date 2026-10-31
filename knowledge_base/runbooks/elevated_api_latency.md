# Runbook: Elevated API Latency

## Purpose
Investigate increased API response times while distinguishing application, database, network, and dependency causes.

## Symptoms
- p95 or p99 response latency rises above the service baseline.
- Requests time out while the service may still be reachable.
- Queue depth or in-flight request count increases.
- Users report slow operations.

## Initial checks
1. Confirm affected endpoints, regions, and time window.
2. Compare p50, p95, and p99 latency with the normal baseline.
3. Check request volume, error rate, saturation, and queue depth.
4. Inspect traces or logs for slow dependency calls.
5. Check database query duration, connection pool utilization, and lock waits.
6. Check recent deployments and external dependency health.

## Diagnostic clues
- One endpoint affected: investigate endpoint-specific code and dependencies.
- Many endpoints affected: investigate shared resources such as database, network, or worker capacity.
- Latency rises with pool saturation: investigate slow queries, lock waits, or connection leaks.
- Latency rises after a release: compare changed code and configuration, but verify with evidence.

## Safe response
- Gather trace IDs, timestamps, affected endpoints, and metric snapshots.
- Avoid increasing timeouts as the first response; this can hide symptoms or increase resource pressure.
- Scaling, changing timeout values, or rolling back requires approval under the applicable procedure.

## Verification
- p95/p99 latency returns near baseline.
- Error rate and queue depth recover.
- A sample of affected endpoints completes successfully.
- Improvement persists for the agreed observation window.
