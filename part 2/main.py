from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# General setup
load_dotenv()
Token = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Tracking user sessions
user_sessions = {}


# Message func
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled ... prob)')
        return
    try:
        if message.author in user_sessions:
            correct_answer_tuple = user_sessions[message.author]['answer']
            choice, full_name = correct_answer_tuple
            if user_message.strip().upper() == choice:
                await message.channel.send(f"Correct answer! It was indeed: \n***{full_name}***")
            else:
                await message.channel.send(f"Wrong answer! The correct answer was: \n***{full_name}***")
            del user_sessions[message.author]  # Clear session after response
        else:
            # Get the response and expected answer if applicable
            response, answer_tuple = get_response(user_message)
            await message.channel.send(response)
            if answer_tuple:
                # Save session data if there's an answer to validate
                user_sessions[message.author] = {'answer': answer_tuple}
    except Exception as e:
        print(f'Exception has occurred: {e}')



# Bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# Handling messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


def main() -> None:
    client.run(Token)


if __name__ == '__main__':
    main()
