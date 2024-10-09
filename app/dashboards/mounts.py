from app.dashboards.inflation.dashboard import dashboard as inflation_dashboard
from fastapi.routing import Mount
from a2wsgi import WSGIMiddleware

dashboards = [
    inflation_dashboard
]


def dashboard_mounts(dashboards_to_mount: list):
    return [Mount(d.get_relative_path("/"), WSGIMiddleware(d.server)) for d in dashboards_to_mount]
