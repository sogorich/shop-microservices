from app.database.models import Deal


async def create_new_deal(payload: dict) -> str:
    deal = await Deal.create(**payload)
    print(f"Created: {deal.__str__()}")

    return deal.__str__()


async def get_all_deals(limit: int) -> list[Deal]:
    deal_list = await Deal.all().limit(limit)
    return deal_list