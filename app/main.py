from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.dashboards.inflation.dashboard import dashboard as inflation_dashboard
from app.dashboards.mounts import dashboard_mounts, dashboards
from app.api.data.health import routes as health_routes
from app.api.data.cpi import routes as data_routes
from app.api.analytics.cpi import routes as analytics_routes

app = FastAPI(
    routes=dashboard_mounts(dashboards + [inflation_dashboard]),
)


@app.get("/")
async def index():
    return RedirectResponse(url=inflation_dashboard.get_relative_path("/"))


app.include_router(health_routes.router)
app.include_router(data_routes.router)
app.include_router(analytics_routes.router)
