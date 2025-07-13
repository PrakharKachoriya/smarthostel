from app.core.database import get_db_manager
from app.config import DB_URL


async def add_new_tenant(
    id: int,
    name: str,
    email: str,
    room_number: int
):
    query = """
        INSERT INTO master.tenants_dim VALUES (
            :id, :name, :email, :room_number
        )
    """
    params = {
        id: id,
        name: name,
        email: email,
        room_number: room_number
    }
    
    db_manager = get_db_manager(DB_URL)
    
    try:
        result = await db_manager.execute(query, params, transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None


async def add_new_mealactivity(
    tenant_id: int,
    room_number: int,
    meal_type: str,
    timestamp: float | None = None,
    rating: int | None = None
):
    
    query = """
        INSERT INTO master.tenants_dim VALUES (
            :tenant_id, :room_number, :meal_type, CURRENT_TIMESTAMP(), NULL
        )
    """
    params = {
        tenant_id: tenant_id,
        room_number: room_number,
        meal_type: meal_type,
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None