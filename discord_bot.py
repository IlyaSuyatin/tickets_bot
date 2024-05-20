import discord as dsc
from anylise import analyse_input, check_date, convert_date, nlp
from selenium_utils import get_tickets

TOKEN = "MTIyOTQ5NDIzNDU2MjgyMjI1NQ.GkDXLC.HVBVo10gY2NyzX1RhjRG7uSQqTe6QgVCnGKucs"
intents = dsc.Intents.default()
intents.message_content = True
client = dsc.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot Online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        try:
            analysis_result = analyse_input(message.content, nlp)
            cities, time = analysis_result
            if cities and time:
                date_status = check_date(time)
                converted_date = convert_date(time).strftime("%d.%m.%Y")
                tickets = get_tickets(converted_date, cities[0], cities[1])
                print(tickets)
                await message.channel.send(f"Departure city: {cities[0]};\nDestination city: {cities[1]};\nDeparture date: {converted_date};\nDate Status: {date_status}")
            else:
                await message.channel.send("Sorry, I couldn't understand the request.")
        except TypeError:
                await message.channel.send("Sorry, I couldn't understand the request.")
client.run(TOKEN)