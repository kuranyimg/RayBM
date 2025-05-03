from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# قائمة الإيموتات مع المدة بالثواني لكل واحدة
emote_list: list[tuple[str, str, int]] = [
    ('1', 'dance-wrong', 10),
    ('98', 'idle-floorsleeping2', 8),
    ('99', 'idle-floorsleeping', 8),
    ('100', 'sit-open', 6),
    ('101', 'emote-shrink', 4),
    ('102', 'hcc-jetpack', 6),
    ('103', 'idle-hero', 5),
    # أكمل باقي الإيموتات بنفس النمط ...
    ('2', 'emote-fashionista', 7),
    ('3', 'emote-gravity', 6),
    ('4', 'dance-icecream', 10),
    ('5', 'idle-dance-casual', 6),
    ('6', 'emote-kiss', 5),
    ('7', 'emote-no', 4),
    ('8', 'emote-sad', 4),
    ('9', 'emote-yes', 4),
    ('10', 'emote-laughing', 6),
    # اختصرنا القائمة لتوضيح الفكرة
]

# تنفيذ التكرار
async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        duration = 8  # مدة افتراضية

        for emote in emote_list:
            if emote[0].lower() == emote_name.lower() or emote[1].lower() == emote_name.lower():
                emote_id = emote[1]
                duration = emote[2]
                break

        if emote_id == "":
            await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} Invalid emote name or ID. 🔄🚫")
            return

        await self.highrise.send_whisper(user.id, f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name}. Type 'stop' to cancel. 🔄👯🏻‍♂️")

        while True:
            print(f"Loop {emote_name} - {user.username}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.send_whisper(user.id, f"🚫🔄 {user.username} loop failed 🔄🚫")
                return
            await asyncio.sleep(duration)

    try:
        splited_message = message.strip().split(" ", 1)
        trigger = splited_message[0].lower()
        if trigger not in ["loop", "!loop", "-loop"]:
            return
        emote_name = splited_message[1].strip()
    except:
        await self.highrise.send_whisper(user.id, f"🚫 @{user.username}, please specify an emote name after 'loop'.")
        return
    else:
        taskgroup = self.highrise.tg
        task_list: list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
        taskgroup.create_task(coro=loop_emote(self, user, emote_name), name=user.username)

# لإيقاف التكرار عند كتابة stop أو Stop
async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    if message.strip().lower() != "stop":
        return
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅️ {user.username} loop stopped successfully.")
            return
    await self.highrise.send_whisper(user.id, f"ℹ️ {user.username} no active loop to stop.")
