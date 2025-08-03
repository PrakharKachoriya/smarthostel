import strawberry
from strawberry.types import Info

from app.graphql.db.types import (
    Pg, PgInput, Tenant, TenantInput, Staff, StaffInput,
    QRScanLog, QRScanLogInput
)
from app.business.definitions.read import get_table_row
from app.business.definitions.write import add_new_pg, add_new_tenant, add_new_staff, add_new_qr_scan_log
from app.business.ddl.methods import create_schema_if_not_exists, create_table_if_not_exists
from app.logger import AppLogger
from app.core.trigger_queue import get_trigger_queue

logger = AppLogger().get_logger()

trigger_queue = get_trigger_queue()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_pg(self, data: PgInput, info: Info) -> Pg | None:
        try:
            result = await add_new_pg(data.to_pydantic())
            return Pg(**result)
        except Exception as e:
            logger.error(f"Error adding new PG: {e}")
            return None
    
    @strawberry.mutation
    async def add_staff(self, data: StaffInput, info: Info) -> Staff | None:
        # print(data.__dict__)
        try:
            pg_id = info.context["pg_id"]
            result = await add_new_staff(data=data.to_pydantic(), pg_id=str(pg_id))
            return Staff(**result)
            
        except Exception as e:
            logger.error(e)
    
    @strawberry.mutation
    async def add_tenant(self, data: TenantInput, info: Info) -> Tenant | None:
        # print(data.__dict__)
        try:
            pg_id = info.context["pg_id"]
            # logger.info(f"Adding tenant to PG with ID: {pg_id}")
            result = await add_new_tenant(data=data.to_pydantic(), pg_id=str(pg_id))
            return Tenant(**result)
            
        except Exception as e:
            logger.error(e)
    
    @strawberry.mutation
    async def add_qr_scan_log(
        self,
        data: QRScanLogInput,
        info: Info
    ) -> QRScanLog | None:
        
        try:
            pg_id = info.context["pg_id"]
            tenant = await get_table_row(
                pg_id, "core", "tenant",
                and_filters = {
                    "id": data.tenant_id
                }
            )
            if not tenant:
                raise Exception('Tenant not registered in PG')

            tenant_has_scanned = await get_table_row(
                pg_id, "mess", "daily_scans",
                and_filters = {
                    "tenant_id": data.tenant_id,
                    "meal_type": data.meal_type
                }
            )

            if tenant_has_scanned:
                raise Exception('Tenant has already scanned')

            res = await add_new_qr_scan_log(data=data.to_pydantic(), pg_id=pg_id)
            
            trigger_payload = {
                "action": "qr scanned",
                "pg_key": pg_id,
                "meal_type": data.meal_type
            }
            
            await trigger_queue.enqueue(trigger_payload)

            return QRScanLog(**res)
        except Exception as e:
            logger.error(f"Error adding meal activity: {e}")
            return None
    
    @strawberry.mutation
    async def create_schema(self, schema_name: str, info: Info) -> None:
        """Create a new schema in the database."""
        
        try:
            await create_schema_if_not_exists(schema_name)
        except Exception as e:
            print(f"Error creating schema {schema_name}: {e}")
            return None

    @strawberry.mutation
    async def create_table(self, schema_name: str, table_name: str, columns: list[str], info: Info) -> None:
        """Create a new table in the specified schema."""
        
        try:
            # pg_id = info.context["pg_id"]
            # To be used for partitioning new table for pg id
            await create_table_if_not_exists(schema_name, table_name, columns)
        except Exception as e:
            print(f"Error creating table {schema_name}.{table_name}: {e}")
            return None