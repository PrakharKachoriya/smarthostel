from fastapi import Depends

from app.dependencies.auth import verify_pg_id

async def get_context(pg_id = Depends(verify_pg_id)):
    return {"pg_id": pg_id}