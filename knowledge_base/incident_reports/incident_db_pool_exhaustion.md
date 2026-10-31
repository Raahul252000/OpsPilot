# Historical Incident (Fictional): Database Connection Pool Exhaustion

## Summary
The API experienced intermittent request failures and elevated latency. Application logs showed connection pool acquisition timeouts.

## Impact
Some requests failed or completed slowly during the incident window. Exact customer impact was not measured in this example.

## Evidence observed
- Pool utilization was near its configured maximum.
- The database health check remained successful.
- Several requests waited longer than usual for a connection.
- The incident began during increased request volume.

## Investigation
The team compared request volume, pool utilization, query duration, and connection lifecycle metrics. A subset of requests held connections longer than expected. This evidence suggested connection contention, but did not alone prove a connection leak.

## Likely contributing factor
Long connection hold times combined with elevated request volume reduced available pool capacity.

## Resolution
The team optimized slow operations and corrected connection handling in a reviewed change. No destructive database action was taken.

## Verification
Pool utilization and acquisition wait time returned toward baseline. API timeout errors declined and representative requests succeeded.

## Lessons learned
- Track pool wait time as well as active connection count.
- Ensure connections are returned in all code paths.
- Correlate application and database metrics before changing pool size.

## Tags
database, connection-pool, latency, timeout
