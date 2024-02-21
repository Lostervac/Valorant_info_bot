import discord
from discord.ext import commands
from bot_token import token
from img_class import get_class
from character_descriptions import character_descriptions

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
    activity = discord.Activity(type=discord.ActivityType.custom, name="!help")
    await bot.change_presence(activity=activity)

@bot.command()
async def gethelp(ctx):
    await ctx.send(
        "```"
        "!gethelp\n"
        "!hello\n"
        "!info komutuyla valorant karakteri hakkında bilgi alabilirsin. Örnek kullanım: !info Jett\n"
        "Eğer görsel atarak bilgi almak istiyorsan !check yazdıktan sonra ek kısmına bir valorant karakteri fotoğrafı atman yeterli\n"
        "```"
    )

    

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba {bot.user}! Ben bir botum!')

@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

@bot.command()
async def info(ctx, cn):
    if len(cn) > 0:
        character_name = cn[0].upper() + cn[1:]
    else:
        character_name = cn
    
    if character_name in character_descriptions:
        await ctx.send(character_descriptions[character_name])
    
@bot.command()
async def check(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            img_path = f"img/{file_name}"
            await attachment.save(img_path)

        class_name, score = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=img_path)
        await ctx.send(f"Bu {class_name.strip()} karakteridir.")
        
        if class_name.strip() in character_descriptions:
            await ctx.send(character_descriptions[class_name.strip()])
    else:
        await ctx.send("Resim göndermediniz. Resim göndermek için !check komutunu yazdıktan sonra ek kısmına görsel atmalısınız")

bot.run(token)
