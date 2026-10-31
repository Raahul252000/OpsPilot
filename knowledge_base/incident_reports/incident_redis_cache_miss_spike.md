# Historical Incident (Fictional): Redis Cache Miss Spike

## Summary
Cache hit ratio dropped and database read load increased, followed by elevated API latency.

## Impact
Read-heavy API paths became slower. Exact customer impact is not specified in this fictional report.

## Evidence observed
- Cache misses rose above the normal baseline.
- Redis remained reachable and command latency was near its usual range.
- Database read volume increased at approximately the same time.
- The change began after an application release.

## Investigation
The team compared cache-key formats, TTL settings, release changes, hit/miss metrics, and database load. A key-prefix change in the new release caused requests to use keys that did not match existing cache entries.

## Likely root cause
The cache-key format change was the strongest supported explanation for the miss spike.

## Resolution
The team corrected the key format through a reviewed application change and monitored cache behavior after deployment.

## Verification
Cache hit ratio improved, database read volume declined, and API latency returned toward baseline.

## Lessons learned
- Treat cache-key changes as compatibility-sensitive changes.
- Monitor hit ratio and downstream database load together.
- Do not flush a cache as a first-line response.

## Tags
redis, cache-miss, database-load, latency
