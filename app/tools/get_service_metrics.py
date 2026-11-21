
from langchain.tools import tool


# Simulated metrics for local development.
# Later, we will replace this with a monitoring API.
SERVICE_METRICS = {
    "user-api": {
        "cpu_usage_percent": 78.5,
        "memory_usage_percent": 72.3,
        "request_rate_per_second": 145,
        "error_rate_percent": 8.2,
        "average_latency_ms": 420,
        "p95_latency_ms": 1250,
        "database_pool_size": 20,
        "database_max_overflow": 10,
        "database_connections_in_use": 30,
        "database_connections_available": 0,
    }
}


@tool
def get_service_metrics(service: str) -> dict:
    """
    Retrieve operational metrics for an application service.

    Use this tool when investigating service performance,
    high CPU or memory usage, increased latency, elevated
    error rates, or database connection pool utilization.

    This tool returns simulated metrics in the current
    development environment, not live production metrics.

    Args:
        service: Name of the application service,
                 for example user-api.
    """
    metrics = SERVICE_METRICS.get(service)

    if metrics is None:
        return {
            "status": "not_found",
            "service": service,
            "message": f"No metrics available for {service}",
        }

    return {
        "status": "success",
        "source": "simulated_metrics",
        "service": service,
        "metrics": metrics,
    }
