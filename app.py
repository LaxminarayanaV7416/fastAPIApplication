from fastapi import FastAPI
import uvicorn
from routers import authorization_router
from utilities.data_base_connectivity_utils import SingletonDataBaseConnectivitySQLIte

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    SingletonDataBaseConnectivitySQLIte().base.metadata.create_all(bind = SingletonDataBaseConnectivitySQLIte.get_engine())

# ==== Adding all routers here ================
app.include_router(authorization_router.router)

# =============================================


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=5000, reload=True)