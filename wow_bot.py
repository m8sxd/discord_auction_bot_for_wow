import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.find('div', {'data-slot': 'card-title'})
            if price_element:
                price_text = price_element.get_text(strip=True).replace(",", "")
                return float(price_text)
    except Exception as e:
        print(f"Chyba u {url}: {e}")
    return 0.0

def calculate_profits():
    urls_void = [
        "https://wowpricehub.com/eu/drak'thul/item/Ace%20of%20Void-245838",
        "https://wowpricehub.com/eu/drak'thul/item/Two%20of%20Void-245839",
        "https://wowpricehub.com/eu/drak'thul/item/Three%20of%20Void-245840",
        "https://wowpricehub.com/eu/drak'thul/item/Four%20of%20Void-245841",
        "https://wowpricehub.com/eu/drak'thul/item/Five%20of%20Void-245842",
        "https://wowpricehub.com/eu/drak'thul/item/Six%20of%20Void-245843",
        "https://wowpricehub.com/eu/drak'thul/item/Seven%20of%20Void-245844",
        "https://wowpricehub.com/eu/drak'thul/item/Eight%20of%20Void-245845",
        "https://wowpricehub.com/eu/drak'thul/item/Darkmoon%20Deck:%20Void-245750"
    ]

    urls_blood = [
        "https://wowpricehub.com/eu/drak'thul/item/Ace%20of%20Blood-245856",
        "https://wowpricehub.com/eu/drak'thul/item/Two%20of%20Blood-245857",
        "https://wowpricehub.com/eu/drak'thul/item/Three%20of%20Blood-245858",
        "https://wowpricehub.com/eu/drak'thul/item/Four%20of%20Blood-245859",
        "https://wowpricehub.com/eu/drak'thul/item/Five%20of%20Blood-245860",
        "https://wowpricehub.com/eu/drak'thul/item/Six%20of%20Blood-245861",
        "https://wowpricehub.com/eu/drak'thul/item/Seven%20of%20Blood-245862",
        "https://wowpricehub.com/eu/drak'thul/item/Eight%20of%20Blood-245863",
        "https://wowpricehub.com/eu/drak'thul/item/Darkmoon%20Deck:%20Blood-245855"
    ]

    all_urls = urls_void + urls_blood

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_price, all_urls))

    void_profit = round(results[8] - sum(results[0:8]))
    blood_profit = round(results[17] - sum(results[9:17]))
    
    return void_profit, blood_profit

# Úprava oprávnění pro starší verzi discord.py
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot se úspěšně přihlásil jako {bot.user}')

@bot.command()
async def profit(ctx):
    await ctx.send("Počítám aktuální ceny, chvilku strpení... ⏳")
    
    # Úprava asynchronního spouštění pro Python 3.6
    void_profit, blood_profit = await bot.loop.run_in_executor(None, calculate_profits)
    
    zprava = (
        f":bar_chart: **Aktuální profit na Drak'thulu:**\n"
        f":black_joker: **Deck of Void:** `{void_profit}` goldů\n"
        f":drop_of_blood: **Deck of Blood:** `{blood_profit}` goldů"
    )
    await ctx.send(zprava)

# SEM VLOŽ SVŮJ TOKEN Z DISCORD DEVELOPER PORTALU
with open("token.txt", "r") as file:
    TOKEN = file.read().strip()
    
if __name__ == "__main__":
    bot.run(TOKEN)