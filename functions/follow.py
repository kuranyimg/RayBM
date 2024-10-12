from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

async def follow(self: BaseBot, user: User, message: str) -> None:
    # Extract user ID from the message (format: !follow@username)
    if not message.startswith("!follow@"):
        await self.highrise.chat("Invalid command, use !follow@username")
        return

    # Extract username after !follow@
    try:
        target_username = message.split("@")[1].strip()
    except IndexError:
        await self.highrise.chat("Please use the correct format: !follow@username")
        return

    async def following_loop(self: BaseBot, target_username: str) -> None:
        while True:
            # Get the user position
            room_users = (await self.highrise.get_room_users()).content
            user_position = None
            for room_user, position in room_users:
                if room_user.username == target_username:
                    user_position = position
                    break

            if user_position is None:
                await self.highrise.chat(f"User with username {target_username} not found in the room.")
                return

            # Move towards the user if their position is an AnchorPosition
            if isinstance(user_position, AnchorPosition):
                await self.highrise.walk_to(Position(user_position.x + 1, user_position.y, user_position.z))
            await asyncio.sleep(0.5)

    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            await self.highrise.chat("I am already following someone. Stop first with /stop.")
            return

    # Create the follow task
    taskgroup.create_task(coro=following_loop(self, target_username))
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_coro().__name__ == "following_loop":
            task.set_name("following_loop")

    await self.highrise.chat(f"Following the user with username {target_username} 🚶‍♂️")

async def stop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            task.cancel()
            await self.highrise.chat(f"Stopped following 🛑")
            return
    await self.highrise.chat("I am not following anyone at the moment.")
