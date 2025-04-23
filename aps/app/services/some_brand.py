import httpx
from app.core.config import settings

# async def get_products(page: int = 1):
#     url = f"{settings.SB_URL}/api/products"
#     headers = {
#         "Authorization": f"{settings.SB_API_KEY}"
#     }
#     async with httpx.AsyncClient() as client:
#         res = await client.get(url, headers=headers)
#         print(res.json())
#         return res.json()

async def get_products(page: int = 1):
    url = f"{settings.SB_URL}/api/products?populate=images"
    headers = {
        "Authorization": f"Bearer {settings.SB_API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers)
        return res.json()