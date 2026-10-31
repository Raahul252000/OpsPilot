# Runbook: Memory Pressure

## Purpose
Investigate rising memory use, out-of-memory events, or container restarts.

## Symptoms
- Resident memory steadily increases.
- Containers are terminated or restarted.
- Garbage collection activity or latency rises.
- The operating system or orchestrator reports memory pressure.

## Possible causes
- Memory leak or unbounded in-process cache.
- Large payloads or unexpectedly large batches.
- Queue backlog causing work to accumulate.
- Concurrency increased without corresponding resource capacity.
- Memory limits are too low for the workload.

## Initial checks
1. Identify the affected process/container and start time.
2. Compare current memory use with baseline and configured limits.
3. Check restart history and out-of-memory events.
4. Review request size, batch size, queue depth, and concurrency metrics.
5. Compare symptoms with recent deployments and traffic changes.
6. Review logs for repeated allocation failures or unusually large payloads.

## Safe response
- Capture memory trends and relevant workload details.
- Avoid restarting repeatedly without collecting evidence; restarts can erase useful diagnostic state.
- Do not change memory limits or disable safety limits without approval.
- If availability is at immediate risk, follow the established incident escalation procedure.

## Verification
- Memory growth stabilizes.
- Restart/OOM events stop.
- Latency and error rates return to expected levels.
- Observe long enough to detect recurring growth.
