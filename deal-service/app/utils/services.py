import random

from app.database.models import Deal
from vkbottle import API


async def create_new_deal(payload: dict) -> str:
    deal = await Deal.create(**payload)
    return deal.__str__()


async def get_all_deals(limit: int) -> list[Deal]:
    deal_list = await Deal.all().limit(limit)
    return deal_list


async def send_vk_notification_employes(
        api_object: API,
        message: str
):
    employes_ids: set[int] = {169991712} # Например хранить vk ids можно в redis
    
    for empl_id in employes_ids:
        try:
            await api_object.messages.send(
                user_id=empl_id,
                message=message,
                random_id=int(random.random())
            )
        except Exception as e:
            print(f"VK user id: {empl_id} ", e)