import discord, os, random
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
load_dotenv("secrets.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

token = os.getenv('TOKEN')

GUILD = discord.Object(id=932133337152254012)


@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print("Logged in as bot {0.user}".format(client))


# @client.event
# async def on_message(message):
#     username = str(message.author).split("#")[0]
#     channel = str(message.channel.name)
#     user_message = str(message.content)

#     print(f'Message {user_message} by {username} on {channel}')

#     if message.author == client.user:
#         return

#     if channel == "bot":
#         if user_message.lower() == "hello" or user_message.lower() == "hi":
#             await message.channel.send(f'Hello {username}')
#             return
#         elif user_message.lower() == "bye":
#             await message.channel.send(f'Bye {username}')
#         elif user_message.lower() == "tell me a joke":
#             jokes = [" Can someone please shed more\
#             light on how my lamp got stolen?",
#                      "Why is she called llene? She\
#                      stands on equal legs.",
#                      "What do you call a gazelle in a \
#                      lions territory? Denzel."]
#             await message.channel.send(random.choice(jokes))

@tree.command(
    name="test",
    description="My first application Command",
    guild=GUILD,
)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! This is my first slash command.")


client.run(token)