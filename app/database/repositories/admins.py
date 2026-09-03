from app.database.client import get_client

TABLE = "admins"


def list_admin_ids() -> list[int]:
    response = get_client().table(TABLE).select("telegram_id").execute()
    return [row["telegram_id"] for row in response.data]
