import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio

def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Najdeme cenu
            price_element = soup.find('div', {'data-slot': 'card-title'})
            price = 0.0
            if price_element:
                price_text = price_element.get_text(strip=True).replace(",", "")
                price = float(price_text)
            
            # Najdeme čas aktualizace (podle screenshotu)
            time_element = soup.find('p', class_='text-sm text-muted-foreground')
            time_text = time_element.get_text(strip=True) if time_element else "Unknown"
            
            return {"price": price, "time": time_text}
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return {"price": 0.0, "time": "Error"}

def calculate_all():
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
        results = list(executor.map(get_data, all_urls))

    # Výpočet profitů (používáme .get('price'))
    void_cards_sum = sum(r['price'] for r in results[0:8])
    void_deck_price = results[8]['price']
    void_profit = round(void_deck_price - void_cards_sum)

    blood_cards_sum = sum(r['price'] for r in results[9:17])
    blood_deck_price = results[17]['price']
    blood_profit = round(blood_deck_price - blood_cards_sum)
    
    # Vezmeme čas aktualizace z posledního staženého požadavku
    last_update = results[17]['time']
    
    return void_profit, blood_profit, last_update

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot successfully logged in as {bot.user}')

@bot.command()
async def profit(ctx):
    await ctx.send("Calculating current prices, please wait... ⏳")
    
    void_profit, blood_profit, last_update = await bot.loop.run_in_executor(None, calculate_all)
    
    message = (
        f":bar_chart: **Current profit on Drak'thul:**\n"
        f":black_joker: **Deck of Void:** `{void_profit}` gold\n"
        f":drop_of_blood: **Deck of Blood:** `{blood_profit}` gold\n\n"
        f"🕒 *{last_update}*"
    )
    await ctx.send(message)

with open("token.txt", "r") as file:
    TOKEN = file.read().strip()

if __name__ == "__main__":
    bot.run(TOKEN)