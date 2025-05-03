from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# Emote list: (trigger name, emote ID, duration in seconds)
emote_list: list[tuple[str, str, int]] = [
    ('100', 'dance-wrong', 8), ('98', 'idle-floorsleeping2', 10), ('99', 'idle-floorsleeping', 10),
    ('1', 'sit-open', 6), ('101', 'emote-shrink', 5), ('102', 'hcc-jetpack', 7),
    ('smooch', 'emote-kissing-bound', 6), ('Relaxing', 'idle-floorsleeping2', 10),
    ('Levitate', 'emoji-halo', 6), ('tiktok11', 'dance-tiktok11', 12),
    ('icecream', 'dance-icecream', 9), ('hello', 'emote-hello', 5),
    ('wave', 'emote-wave', 5), ('sad', 'emote-sad', 4), ('kiss', 'emote-kiss', 6),
    # ... (add more with durations)
]

# Main loop command
async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_id: str, emote_name: str, duration: int) -> None:
        await self.highrise.send_whisper(user.id, f"🔁 @{user.username}, looping emote: {emote_name}")
        while True:
            try:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
            except Exception:
                await self.highrise.send_whisper(user.id, f"❌ @{user.username} loop failed.")
                break

    # Parse message and extract emote name
    message_lower = message.lower()
    valid_prefixes = ["loop ", "!loop ", "-loop "]
    emote_name = None
    for prefix in valid_prefixes:
        if message_lower.startswith(prefix):
            emote_name = message[len(prefix):].strip()
            break

    if not emote_name:
        return

    # Find emote ID and duration
    emote_id = ""
    duration = 10  # default fallback
    for emote in emote_list:
        if emote[0].lower() == emote_name.lower():
            emote_id = emote[1]
            duration = emote[2]
            break

    if not emote_id:
        await self.highrise.send_whisper(user.id, f"❌ Emote not found: {emote_name}")
        return

    print(f"Loop command triggered with emote: {emote_name} ({emote_id}) for {duration}s")

    # Cancel previous loop (if any)
    taskgroup = self.highrise.tg
    for task in list(taskgroup._tasks):
        if task.get_name() == user.username:
            task.cancel()

    # Start new loop
    taskgroup.create_task(
        coro=loop_emote(self, user, emote_id, emote_name, duration),
        name=user.username
    )

# Stop loop command
async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    if message.lower() != "stop":
        return
    taskgroup = self.highrise.tg
    for task in list(taskgroup._tasks):
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅ @{user.username}, loop stopped.")
            return
    await self.highrise.send_whisper(user.id, f"⚠️ @{user.username}, no loop to stop.")
