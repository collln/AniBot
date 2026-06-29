import discord, os, random
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from post import userQuery
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


@tree.command(
    name="animequery",
    description="Check whether an anime has an upcoming release scheduled",
    guild=GUILD,
)
@app_commands.describe(title="The title of the anime you want to check")
async def animequery(interaction: discord.Interaction, title: str):
    # Acknowledge the interaction first so Discord doesn't time out
    # while the (blocking) AniList request runs.
    await interaction.response.defer()

    anime_title, air_date = userQuery(title)

    if anime_title is None:
        await interaction.followup.send(f'Could not find an anime titled "{title}".')
        return

    if air_date:
        message = f"**{anime_title}** has an upcoming release at: {air_date}"
    else:
        message = f"There is no upcoming release scheduled for **{anime_title}**."

    await interaction.followup.send(message)


client.run(token)