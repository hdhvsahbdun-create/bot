import discord
import requests

DISCORD_TOKEN = "MTU0Nzc0MjEzMDMyMjE1MzYzNA.GHCkeV.ArizRcam-70T0Fjz2E-qrJIAMTKC9InxEd1CnA"
OPENROUTER_API_KEY = "Sk-or-v1-d696cb9a9dce43732d22c0fae666622eddb18ee4c07c719fe5cc766704e0b7f7"

MODEL_ID = "mistralai/mistral-7b-instruct"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot ist online als {client.user}")

@client.event
async def on_message(message):
    # Eigene Nachrichten ignorieren
    if message.author == client.user:
        return

    # Reagiert auf Erwähnung (@Bot) oder Direktnachricht (DM)
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        async with message.channel.typing():
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": MODEL_ID,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if res.status_code == 200:
                answer = res.json()["choices"][0]["message"]["content"]
                for chunk in [answer[i:i+2000] for i in range(0, len(answer), 2000)]:
                    await message.reply(chunk)
            else:
                await message.reply("Fehler bei der API-Anfrage.")

client.run(DISCORD_TOKEN)
