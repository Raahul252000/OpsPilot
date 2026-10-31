
APPLICATION_LOGS = [
    {
        "timestamp": "2026-10-25T10:00:01.120Z",
        "service": "user-api",
        "level": "INFO",
        "logger": "app.startup",
        "message": "User API application started successfully",
        "request_id": None,
    },
    {
        "timestamp": "2026-10-25T10:00:03.241Z",
        "service": "user-api",
        "level": "INFO",
        "logger": "app.database",
        "message": "Database connection pool initialized",
        "request_id": None,
        "metadata": {
            "pool_size": 20,
            "max_overflow": 10,
            "pool_timeout_seconds": 5,
        },
    },
    {
        "timestamp": "2026-10-25T10:01:12.450Z",
        "service": "user-api",
        "level": "INFO",
        "logger": "app.middleware",
        "message": "Request completed successfully",
        "request_id": "req-1001",
        "metadata": {
            "method": "GET",
            "path": "/api/users/101",
            "status_code": 200,
            "duration_ms": 42,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:18.910Z",
        "service": "user-api",
        "level": "WARNING",
        "logger": "app.database",
        "message": "Database connection acquisition taking longer than expected",
        "request_id": "req-1002",
        "metadata": {
            "pool_checked_out": 24,
            "pool_size": 20,
            "max_overflow": 10,
            "wait_time_ms": 1200,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:21.182Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "Database connection timeout while acquiring connection from pool",
        "request_id": "req-1003",
        "metadata": {
            "pool_checked_out": 30,
            "pool_size": 20,
            "max_overflow": 10,
            "timeout_seconds": 5,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:21.185Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.middleware",
        "message": "Request failed with database connection timeout",
        "request_id": "req-1003",
        "metadata": {
            "method": "GET",
            "path": "/api/users/205",
            "status_code": 500,
            "duration_ms": 5012,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:24.310Z",
        "service": "user-api",
        "level": "WARNING",
        "logger": "app.database",
        "message": "Database connection pool utilization reached maximum capacity",
        "request_id": "req-1004",
        "metadata": {
            "pool_checked_out": 30,
            "pool_size": 20,
            "max_overflow": 10,
            "pool_available": 0,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:27.612Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "Database connection acquisition failed after timeout",
        "request_id": "req-1005",
        "metadata": {
            "timeout_seconds": 5,
            "pool_available": 0,
            "exception": "TimeoutError",
        },
    },
    {
        "timestamp": "2026-10-25T10:02:29.011Z",
        "service": "user-api",
        "level": "WARNING",
        "logger": "app.database",
        "message": "Slow database query detected",
        "request_id": "req-1006",
        "metadata": {
            "query_type": "SELECT",
            "table": "users",
            "duration_ms": 4200,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:31.820Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "PostgreSQL connection reset during query execution",
        "request_id": "req-1007",
        "metadata": {
            "exception": "OperationalError",
            "sql_state": "08006",
        },
    },
    {
        "timestamp": "2026-10-25T10:02:35.100Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.middleware",
        "message": "Request failed while retrieving user profile",
        "request_id": "req-1008",
        "metadata": {
            "method": "GET",
            "path": "/api/users/301",
            "status_code": 500,
            "duration_ms": 5031,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:38.740Z",
        "service": "user-api",
        "level": "WARNING",
        "logger": "app.database",
        "message": "Database connection retry scheduled",
        "request_id": "req-1009",
        "metadata": {
            "attempt": 1,
            "max_attempts": 3,
            "retry_delay_ms": 500,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:39.251Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "Database connection retry failed",
        "request_id": "req-1009",
        "metadata": {
            "attempt": 2,
            "max_attempts": 3,
            "exception": "TimeoutError",
        },
    },
    {
        "timestamp": "2026-10-25T10:02:41.450Z",
        "service": "user-api",
        "level": "INFO",
        "logger": "app.middleware",
        "message": "Request completed successfully",
        "request_id": "req-1010",
        "metadata": {
            "method": "GET",
            "path": "/api/health",
            "status_code": 200,
            "duration_ms": 15,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:44.220Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "Database connection pool exhausted",
        "request_id": "req-1011",
        "metadata": {
            "pool_checked_out": 30,
            "pool_available": 0,
            "pool_size": 20,
            "max_overflow": 10,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:48.900Z",
        "service": "user-api",
        "level": "WARNING",
        "logger": "app.database",
        "message": "Database connection hold duration exceeded threshold",
        "request_id": "req-1012",
        "metadata": {
            "connection_hold_time_ms": 8500,
            "threshold_ms": 5000,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:52.140Z",
        "service": "user-api",
        "level": "ERROR",
        "logger": "app.middleware",
        "message": "Request failed due to database connection acquisition timeout",
        "request_id": "req-1013",
        "metadata": {
            "method": "POST",
            "path": "/api/users",
            "status_code": 500,
            "duration_ms": 5020,
        },
    },
    {
        "timestamp": "2026-10-25T10:02:55.010Z",
        "service": "user-api",
        "level": "INFO",
        "logger": "app.middleware",
        "message": "Request completed successfully",
        "request_id": "req-1014",
        "metadata": {
            "method": "GET",
            "path": "/api/users/102",
            "status_code": 200,
            "duration_ms": 38,
        },
    },
    {
        "timestamp": "2026-10-25T10:03:01.880Z",
        "service": "payment-api",
        "level": "ERROR",
        "logger": "app.database",
        "message": "Payment database connection failed",
        "request_id": "pay-2001",
        "metadata": {
            "exception": "OperationalError",
            "status_code": 503,
        },
    },
]



from langchain.tools import tool

@tool
def search_application_logs(
    service: str,
    keyword: str,
) -> list[dict]:
    """
    Search application logs by service and keyword.
    """

    matching_logs = []

    for log in APPLICATION_LOGS:

        if log["service"] != service:
            continue

        if keyword.lower() in log["message"].lower():
            matching_logs.append(log)

    return matching_logs