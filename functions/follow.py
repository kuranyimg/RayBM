from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

async def follow(self: BaseBot, user: User, message: str) -> None:
    # Extract user ID from the message (format: !follow@user.id)
    if message.startswith("!follow@"):
        try:
            target_user_id = message.split("@")[1].strip()
        except IndexError:
            await self.highrise.chat("Please use the correct format: !follow@user.id")
            return
    else:
        await self.highrise.chat("Invalid command, use !follow@user.id")
        return

    async def following_loop(self: BaseBot, target_user_id: str) -> None:
        while True:
            # Get the user position
            room_users = (await self.highrise.get_room_users()).content
            user_position = None
            for room_user, position in room_users:
                if room_user.id == target_user_id:
                    user_position = position
                    break
            
            if user_position is None:
                await self.highrise.chat(f"User with ID {target_user_id} not found in the room.")
                return

            print(user_position)
            if type(user_position) != AnchorPosition:
                await self.highrise.walk_to(Position(user_position.x + 1, user_position.y, user_position.z))
            await asyncio.sleep(0.5)

    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            await self.highrise.chat("Already following someone.")
            return

    # Check if this function is already in the Highrise class tg (task group).
    taskgroup.create_task(coro=following_loop(self, target_user_id))
    task_list: list[Task] = list(taskgroup._tasks)
    # Sets the name of the task that has the following_loop function to "following_loop"
    for task in task_list:
        if task.get_coro().__name__ == "following_loop":
            task.set_name("following_loop")
    await self.highrise.chat(f"Coming 😍 to follow user ID {target_user_id} 🚶‍♂️")

async def stop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            task.cancel()
            await self.highrise.chat(f"Stopped following 🛑")
            return
    await self.highrise.chat("Not following anyone.")
    return
