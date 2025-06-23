import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your voice channel ID and category ID
VOICE_CHANNEL_ID = 854719692493029406  # replace with your actual voice channel ID
CATEGORY_ID = 894656267140870154      # replace with the category where temp text channels should go

# Keep track of the text channel created for a voice channel
vc_text_channels = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    for guild in bot.guilds:
        me = guild.get_member(bot.user.id)
        perms = me.guild_permissions
        print(f"🔍 Permissions in {guild.name}:")
        print(f"Manage Channels: {perms.manage_channels}")
        print(f"View Channels: {perms.view_channel}")
        print(f"Send Messages: {perms.send_messages}")

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    # When user joins a specific voice channel
    if after.channel and after.channel.id == VOICE_CHANNEL_ID:
        vc = after.channel

        if vc.id not in vc_text_channels:
            category = discord.utils.get(guild.categories, id=CATEGORY_ID)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_channels=True
                )
            }

            for m in vc.members:
                if m.bot:
                    continue
                overwrites[m] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                )

            category = discord.utils.get(guild.categories, id=CATEGORY_ID)

            text_channel = await guild.create_text_channel(
                name=f"{vc.name}-{member.name}-chat",
                overwrites=overwrites,
                category=category
            )

            vc_text_channels[vc.id] = text_channel

    # Check if someone left the monitored VC and it's now empty
    if before.channel and before.channel.id == VOICE_CHANNEL_ID:
        if len(before.channel.members) == 0 and before.channel.id in vc_text_channels:
            await vc_text_channels[before.channel.id].delete()
            del vc_text_channels[before.channel.id]

# Run the bot using your token
import os
bot.run(os.getenv("BOT_TOKEN"))
if token is None:
    raise ValueError("❌ BOT_TOKEN not found in environment variables.")

bot.run(token)