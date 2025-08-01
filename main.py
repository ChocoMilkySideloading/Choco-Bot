import os
import random
import discord
import openai
from discord.ext import commands
from discord.commands import slash_command, Option

# Load secrets
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    print("❌ ERROR: Missing DISCORD_TOKEN or OPENAI_API_KEY in environment variables.")
    exit(1)

# Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
openai.api_key = OPENAI_API_KEY

# /ask command using OpenAI
@slash_command(name="ask", description="Ask AI anything")
async def ask(ctx, question: Option(str, "What do you want to ask?")):
    await ctx.defer()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response["choices"][0]["message"]["content"]
        await ctx.respond(answer)
    except Exception as e:
        await ctx.respond(f"❌ Failed to get AI response: {e}")

# /dns
@slash_command(name="dns", description="Get the best DNS")
async def dns(ctx):
    await ctx.respond("Here is the best DNS by Choco Milky Sideloading:\nhttps://cdn.discordapp.com/attachments/1376994219649929388/1398794767084683274/Neb_DNS__Webclip.mobileconfig")

# /chocomilky
@slash_command(name="chocomilky", description="Get the Choco Milky app")
async def chocomilky(ctx):
    await ctx.respond("Here is the Choco Milky app for iOS 14 and over:\nhttps://cdn.discordapp.com/attachments/1373569891994697888/1378195101104476232/choco_milky_app.mobileconfig")

# /8ball
eight_ball_responses = [
    "Nah bruh", "Yea", "Looks like that's a yes", "Prolly bro",
    "Definitely", "Nope", "Ask again later", "Trust your gut",
    "Not a chance", "Maybe?", "Absolutely", "Try again"
]

@slash_command(name="8ball", description="Ask the magic 8 ball")
async def eight_ball(ctx, question: Option(str, "Ask your question")):
    response = random.choice(eight_ball_responses)
    await ctx.respond(f"🎱 {response}")

# /coinflip
@slash_command(name="coinflip", description="Flip a coin")
async def coinflip(ctx):
    await ctx.respond(f"🪙 You got **{random.choice(['Heads', 'Tails'])}**!")

# /roll
@slash_command(name="roll", description="Roll a 6-sided dice")
async def roll(ctx):
    await ctx.respond(f"🎲 You rolled a **{random.randint(1, 6)}**!")

# /joke
jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I told my computer I needed a break, and now it won’t stop sending me beach wallpapers.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

@slash_command(name="joke", description="Get a random joke")
async def joke(ctx):
    await ctx.respond(random.choice(jokes))

# /pfp
@slash_command(name="pfp", description="Get someone's profile picture")
async def pfp(ctx, user: Option(discord.User, "Mention a user")):
    await ctx.respond(f"{user.display_name}'s profile picture: {user.display_avatar.url}")

# /ban
@slash_command(name="ban", description="Ban a user (Admin only)")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.Member, "User to ban"), reason: Option(str, "Reason", default="No reason provided")):
    try:
        await member.ban(reason=reason)
        await ctx.respond(f"🔨 Banned **{member}** for: `{reason}`", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond("❌ I don't have permission to ban that member.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"❌ Error: {e}", ephemeral=True)

# /kick
@slash_command(name="kick", description="Kick a user (Admin only)")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, "User to kick"), reason: Option(str, "Reason", default="No reason provided")):
    try:
        await member.kick(reason=reason)
        await ctx.respond(f"👢 Kicked **{member}** for: `{reason}`", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond("❌ I don't have permission to kick that member.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"❌ Error: {e}", ephemeral=True)

# Ready
@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

# Start the bot
bot.run(DISCORD_TOKEN)
