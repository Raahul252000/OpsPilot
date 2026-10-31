# Historical Incident (Fictional): Latency Increase After Deployment

## Summary
p95 API latency increased shortly after a release. The team investigated whether the deployment was responsible.

## Impact
A subset of API requests became slower. This example does not specify a real customer count or duration.

## Evidence observed
- p95 latency rose after the release.
- Request volume was close to its usual range.
- Traces showed increased duration in one database-backed endpoint.
- No broad service health failure was observed.

## Investigation
The team compared the release diff, endpoint traces, query duration, and database connection metrics. The changed endpoint issued an additional query for each returned item.

## Likely root cause
An N+1 query pattern introduced by the release was the strongest explanation supported by the trace evidence.

## Resolution
The team updated the data access path to fetch related records more efficiently and deployed the fix through the normal release process.

## Verification
Endpoint latency improved, p95 returned toward baseline, and error rate remained stable.

## Lessons learned
- Compare traces before and after a release.
- Check query count as well as query duration.
- Temporal correlation is a clue; use traces or other evidence to support causality.

## Tags
deployment, latency, database, n-plus-one
