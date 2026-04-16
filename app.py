import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import HelloBot

settings = BotFrameworkAdapterSettings(
    app_id=os.environ.get("MicrosoftAppId", ""),
    app_password=os.environ.get("MicrosoftAppPassword", ""),
    app_type=os.environ.get("MicrosoftAppType", ""),
    app_tenantid=os.environ.get("MicrosoftAppTenantId", "")
)

adapter = BotFrameworkAdapter(settings)
bot = HelloBot()

async def on_error(context, error):
    print(f"[Bot Error] {error}")
    await context.send_activity("Something went wrong. Please try again.")

adapter.on_turn_error = on_error

async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def call_bot(context):
        await bot.on_turn(context)

    await adapter.process_activity(activity, auth_header, call_bot)
    return web.Response(status=200)

async def health(req: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})

app = web.Application()
app.router.add_post("/api/messages", messages)
app.router.add_get("/health", health)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, host="0.0.0.0", port=port)