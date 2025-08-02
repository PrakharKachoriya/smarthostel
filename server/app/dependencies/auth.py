from fastapi import Request, HTTPException

async def verify_pg_id(request: Request):
    pg_id = request.headers.get("pg_id", None)
    if not pg_id:
        raise HTTPException(status_code=401, detail="Missing pg_id in headers")

    return pg_id