from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

emote_list: list[tuple[str, str]] = [
    ('smooch', 'emote-kissing-bound'), ('Relaxing', 'idle-floorsleeping2'),
    ('Cozy Nap', 'idle-floorsleeping'), ('Laid Back', 'sit-open'), 
    ('Shrink', 'emote-shrink'), ('Ignition Boost', 'hcc-jetpack'), 
    ('Hero Pose', 'idle-hero'), ('Levitate', 'emoji-halo'),
    ('rest', 'sit-idle-cute'), ('attentive', 'idle_layingdown'),
    # ... (rest of your emotes)
    ('launch', 'emote-launch')
]

# Command to loop emote
async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower():
                emote_id = emote[1]
                break
        if emote_id == "":
            await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} Invalid emote name.")
            return

        await self.highrise.send_whisper(user.id, f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name}. Type 'stop' to cancel. 🔄👯🏻‍♂️")

        while True:
            print(f"Loop {emote_name} - {user.username}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.send_whisper(user.id, f"⚠️ {user.username}, loop failed.")
                return
            await asyncio.sleep(10)

    try:
        splited_message = message.strip().split(" ", 1)
        trigger = splited_message[0].lower()
        if trigger not in ["loop", "!loop", "-loop"]:
            return
        emote_name = splited_message[1].strip()
    except:
        await self.highrise.send_whisper(user.id, f"🚫 @{user.username}, please specify an emote name.")
        return
    else:
        taskgroup = self.highrise.tg
        task_list: list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
        taskgroup.create_task(coro=loop_emote(self, user, emote_name), name=user.username)

# Command to stop loop with 'stop' or 'Stop'
async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    if message.strip().lower() != "stop":
        return
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅️ @{user.username} loop stopped successfully.")
            return
    await self.highrise.send_whisper(user.id, f"ℹ️ @{user.username} no active loop to stop.")
