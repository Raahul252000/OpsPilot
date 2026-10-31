# Runbook: Redis Cache Issues

## Purpose
Investigate cache timeouts, elevated cache latency, or a sudden rise in cache misses.

## Symptoms
- Cache commands time out or return errors.
- Cache hit ratio drops below its normal baseline.
- Database load rises as cache misses increase.
- API latency increases on cache-dependent paths.

## Possible causes
- Redis service is unavailable or overloaded.
- Network latency between application and Redis.
- Key expiration or eviction patterns changed.
- Cache key format or application behavior changed after deployment.
- Hot keys or large values cause uneven load.

## Initial checks
1. Confirm whether failures affect all cache operations or specific keys/commands.
2. Check Redis health, latency, memory use, evictions, and connection counts.
3. Compare hit/miss ratio and database load with the normal baseline.
4. Check recent deployments, key-prefix changes, TTL changes, and traffic shifts.
5. Inspect application logs for timeouts and retry behavior.

## Safe response
- Preserve metrics and timestamps before making changes.
- Do not flush the cache as a generic troubleshooting step.
- Do not change TTLs, evict keys manually, or restart Redis without authorization.
- If cache bypass is supported, use only the documented, approved procedure because bypass can increase database load.

## Verification
- Redis latency and error rate recover.
- Cache hit ratio trends toward baseline.
- Database load and API latency stabilize.
