from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# Combined emote list with names and emote IDs
emote_list: list[tuple[str, str]] = [
    ('1', 'dance-wrong'), ('98', 'idle-floorsleeping2'), ('99', 'idle-floorsleeping'), 
    ('100', 'sit-open'), ('101', 'emote-shrink'), ('102', 'hcc-jetpack'), 
    ('103', 'idle-hero'), ('104', 'emoji-halo'), ('105', 'sit-idle-cute'), 
    ('106', 'idle_layingdown'), ('107', 'emote-ghost-idle'), ('smooch', 'emote-kissing-bound'), 
    ('Relaxing', 'idle-floorsleeping2'), ('Cozy Nap', 'idle-floorsleeping'),
    ('Laid Back', 'sit-open'), ('Shrink', 'emote-shrink'), ('Ignition Boost', 'hcc-jetpack'), 
    ('Hero Pose', 'idle-hero'), ('Levitate', 'emoji-halo'), ('rest', 'sit-idle-cute'),
    ('attentive', 'idle_layingdown'), ('ghost', 'emote-ghost-idle'), ('fairyfloat', 'idle-floating'),
    ('fairytwirl', 'emote-looping'), ('kissing', 'emote-kissing-bound'), ('tiktok11', 'dance-tiktok11'),
    ('gottago', 'idle-toilet'), ('astronaut', 'emote-astronaut'), ('wrong', 'dance-wrong'),
    ('fashion', 'emote-fashionista'), ('gravity', 'emote-gravity'), ('icecream', 'dance-icecream'),
    ('casual', 'idle-dance-casual'), ('kiss', 'emote-kiss'), ('no', 'emote-no'), ('sad', 'emote-sad'),
    ('yes', 'emote-yes'), ('lau', 'emote-laughing'), ('hello', 'emote-hello'), ('wave', 'emote-wave'),
    ('shy', 'emote-shy'), ('tired', 'emote-tired'), ('flirt', 'emote-lust'), ('flirty', 'emote-lust'),
    ('model', 'emote-model'), ('bow', 'emote-bow'), ('curtsy', 'emote-curtsy'), 
    ('snowball', 'emote-snowball'), ('hot', 'emote-hot'), ('snowangel', 'emote-snowangel'),
    ('charging', 'emote-charging'), ('confused', 'emote-confused'), ('telekinesis', 'emote-telekinesis'),
    ('float', 'emote-float'), ('teleport', 'emote-teleporting'), ('maniac', 'emote-maniac'),
    ('energyball', 'emote-energyball'), ('snake', 'emote-snake'), ('frog', 'emote-frog'),
    ('superpose', 'emote-superpose'), ('cute', 'emote-cute'), ('pose7', 'emote-pose7'),
    ('pose8', 'emote-pose8'), ('pose1', 'emote-pose1'), ('pose5', 'emote-pose5'), 
    ('pose3', 'emote-pose3'), ('cutey', 'emote-cutey'), ('tik10', 'dance-tiktok10'),
    ('sing', 'idle_singing'), ('enthused', 'idle-enthusiastic'), ('shop', 'dance-shoppingcart'),
    ('russian', 'dance-russian'), ('pennywise', 'dance-pennywise'), ('tik2', 'dance-tiktok2'),
    ('blackpink', 'dance-blackpink'), ('celebrate', 'emoji-celebrate'), ('gagging', 'emoji-gagging'),
    ('flex', 'emoji-flex'), ('cursing', 'emoji-cursing'), ('thumbsup', 'emoji-thumbsup'),
    ('angry', 'emoji-angry'), ('punk', 'emote-punkguitar'), ('zombie', 'emote-zombierun'),
    ('sit', 'idle-loop-sitfloor'), ('fight', 'emote-swordfight'), ('ren', 'dance-macarena'),
    ('wei', 'dance-weird'), ('tik8', 'dance-tiktok8'), ('tik9', 'dance-tiktok9'),
    ('uwu', 'idle-uwu'), ('tik4', 'idle-dance-tiktok4'), ('star', 'emote-stargazer'),
    ('pose9', 'emote-pose9'), ('boxer', 'emote-boxer'), ('guitar', 'idle-guitar'),
    ('penguin', 'dance-pinguin'), ('anime', 'dance-anime'), ('creepy', 'dance-creepypuppet'),
    ('watch', 'emote-creepycute'), ('revelation', 'emote-headblowup'), ('bashful', 'emote-shy2'),
    ('pose10', 'emote-pose10'), ('party', 'emote-celebrate'), ('skating', 'emote-iceskating'),
    ('scritchy', 'idle-wild'), ('nervous', 'idle-nervous'), ('timejump', 'emote-timejump'),
    ('jingle', 'dance-jinglebell'), ('hyped', 'emote-hyped'), ('sleigh', 'emote-sleigh'),
    ('surprise', 'emote-pose6'), ('repose', 'sit-relaxed'), ('relaxed', 'sit-relaxed'),
    ('kawaii', 'dance-kawai'), ('touch', 'dance-touch'), ('gift', 'emote-gift'),
    ('pushit', 'dance-employee'), ('salute', 'emote-cutesalute'), ('launch', 'emote-launch')
]

# Main loop command
async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower():
                emote_id = emote[1]
                break
        if not emote_id:
            await self.highrise.send_whisper(user.id, f"❌ Emote not found: {emote_name}")
            return
        
        await self.highrise.send_whisper(user.id, f"🔁 @{user.username}, looping emote: {emote_name}")
        while True:
            try:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(10)
            except Exception:
                await self.highrise.send_whisper(user.id, f"❌ @{user.username} loop failed.")
                break

    # Check if the message is a loop command
    valid_prefixes = ["loop ", "Loop ", "!loop ", "-loop "]
    emote_name = None
    for prefix in valid_prefixes:
        if message.startswith(prefix):
            emote_name = message[len(prefix):].strip()
            break

    if not emote_name:
        return  # Ignore non-loop commands

    # Cancel previous loop if any
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()

    # Start new emote loop
    taskgroup.create_task(coro=loop_emote(self, user, emote_name), name=user.username)

# Stop loop command
async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    if message.lower() != "stop":
        return
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅ @{user.username}, loop stopped.")
            return
    await self.highrise.send_whisper(user.id, f"⚠️ @{user.username}, no loop to stop.")
