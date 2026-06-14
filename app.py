import os
import asyncio
import aiohttp
from microsoft_teams.apps import App, ActivityContext
from microsoft_teams.api import MessageActivity

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://soc-ai-rulebot-agent.livelyocean-c3150e2c.swedencentral.azurecontainerapps.io/message"
).strip()

PORT = int(os.getenv("PORT", "8000"))

app = App()

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    user_input = ctx.activity.text or ""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                BACKEND_URL,
                json={"text": user_input},
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                data = await resp.json()

        reply = data.get("reply") or data.get("message") or "No response from backend."
        await ctx.send(reply)

    except Exception as e:
        await ctx.send(f"Error calling backend: {str(e)}")


if __name__ == "__main__":
    asyncio.run(app.start())