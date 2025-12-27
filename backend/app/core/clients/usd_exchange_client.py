import httpx


class UsdExchangeClient:

    async def usd_to_ars(self, date_str: str) -> float:
        url = (
            "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@"
            f"{date_str}/v1/currencies/usd.json"
        )

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()

        usd = data.get("usd", {})
        ars = usd.get("ars")
        
        if ars is None:
            raise ValueError("ARS rate not found in usd exchange response")
        return float(ars)