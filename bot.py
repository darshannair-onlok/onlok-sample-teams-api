from botbuilder.core import ActivityHandler, TurnContext

class HelloBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("Hello! How can I help you today?")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hi! I am your bot. How can I help?")