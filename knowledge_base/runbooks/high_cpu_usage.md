# Runbook: High CPU Usage

## Purpose
Guide investigation when a service or host reports sustained high CPU utilization.

## Symptoms
- CPU utilization remains above its normal baseline.
- Request latency or queue depth increases.
- Health checks become slow or fail.
- Monitoring reports CPU saturation.

## Possible causes
- Traffic spike or unexpected workload.
- Expensive query or inefficient code path.
- Tight loop, excessive retries, or background job backlog.
- Resource limits are too restrictive.
- A recent deployment introduced a regression.

## Initial checks
1. Identify the affected host, container, or service and exact time window.
2. Compare CPU usage with the service's normal baseline.
3. Check request rate, latency, error rate, and queue depth.
4. Inspect process/container CPU metrics if available.
5. Review logs for repeated errors or retry loops.
6. Compare symptom onset with deployments, scheduled jobs, and traffic changes.

## Interpretation
- CPU rising with request volume may indicate load-related pressure.
- CPU rising while traffic is stable may indicate a regression, retry loop, or background task.
- CPU pressure alongside high latency is correlated evidence, not proof of root cause.

## Safe response
- Collect relevant metrics and logs before restarting or scaling.
- If a specific job is suspected, confirm ownership and impact before pausing it.
- Scaling, killing processes, or rolling back deployments requires an approved change or incident procedure.

## Verification
- CPU returns toward the expected baseline.
- Latency and error rate improve.
- Queue depth stops growing and drains normally.
- The improvement persists during the monitoring window.

## Escalation
Escalate if saturation persists, customer impact grows, or no clear workload or deployment correlation is found.
