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


def compact_source_label(source: str) -> str:
    if not source:
        return "Unknown source"

    # Official docs path
    if "/" in source or "\\" in source:
        return source.split("/")[-1].split("\\")[-1]

    # internal_note:client-a:title
    if source.startswith("internal_note:"):
        parts = source.split(":", 2)
        if len(parts) == 3:
            _, client_id, title = parts
            return f"Internal note ({client_id}): {title}"
        return source

    # case_memory:client-a:CASE-...
    if source.startswith("case_memory:"):
        parts = source.split(":", 2)
        if len(parts) == 3:
            _, client_id, title = parts
            return f"Case memory ({client_id}): {title}"
        return source

    # rule:165072:Some Rule Name
    if source.startswith("rule:"):
        parts = source.split(":", 2)
        if len(parts) == 3:
            _, rule_id, rule_name = parts
            return f"Rule {rule_id}: {rule_name}"
        return source

    return source


def build_sources_footer(context_sources: list, max_items: int = 3) -> str:
    if not context_sources:
        return ""

    seen = []
    for src in context_sources:
        label = compact_source_label(src)
        if label not in seen:
            seen.append(label)

    if not seen:
        return ""

    lines = ["", "Sources used:"]
    for label in seen[:max_items]:
        lines.append(f"- {label}")

    if len(seen) > max_items:
        lines.append(f"- +{len(seen) - max_items} more")

    return "\n".join(lines)


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
        context_sources = data.get("context_sources", [])

        sources_footer = build_sources_footer(context_sources, max_items=3)
        final_reply = f"{reply}\n{sources_footer}" if sources_footer else reply

        await ctx.send(final_reply)

    except Exception as e:
        await ctx.send(f"Error calling backend: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    asyncio.run(app.start(port=PORT))