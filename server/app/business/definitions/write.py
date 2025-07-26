from app.core.database import get_db_manager
from app.config import DB_URL
from app.logger import AppLogger

logger = AppLogger().get_logger()

async def add_new_tenant(
    id: str,
    name: str,
    email: str,
    room_number: int,
    kyc: bool = False
):
    logger.info(f"Adding new tenant: {id}, {name}, {email}, {room_number}, KYC: {kyc}")
    query = """
        INSERT INTO master.tenants_dim (id, name, email, room_number, kyc) VALUES (
            :id, :name, :email, :room_number, :kyc
        )
    """
    params = {
        "id": id,
        "name": name,
        "email": email,
        "room_number": room_number,
        "kyc": kyc
    }
    
    db_manager = get_db_manager(DB_URL)
    
    try:
        result = await db_manager.execute(query, params, fetch="none", transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None


async def add_new_mealactivity(
    tenant_id: str,
    meal_type: str,
    room_number: int | None = None,
    timestamp: float | None = None,
    rating: int | None = None
):
    logger.info(f"Adding new meal activity for tenant {tenant_id}, room {room_number}, meal type {meal_type}, timestamp {timestamp}, rating {rating}")
    
    query = """
        INSERT INTO master.tenants_dim VALUES (
            :tenant_id, :room_number, :meal_type, CURRENT_TIMESTAMP(), NULL
        )
    """
    params = {
        "tenant_id": tenant_id,
        "room_number": room_number,
        "meal_type": meal_type,
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="none", transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None