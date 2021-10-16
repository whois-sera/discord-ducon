import logging, json, random, requests, os, discord
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Ce bot est utile.

Oui.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='./', description=description, intents=intents)

def get_random_risibank_by_search(kw):
  try:
    url = 'https://api.risibank.fr/api/v0/search'
    myobj = {'search': kw}

    ret = requests.post(url, data = myobj)
    dict_stickers = json.loads(ret.text)
    stickers = list(filter(lambda like: like["likes"] > 1000, dict_stickers["stickers"]))
    if len(stickers) == 0:
      stickers = dict_stickers["stickers"]
    return random.choice(stickers)["risibank_link"]
  except:
    return "Aucun résultat !"

def get_random_1825():
  base_post_url = "https://www.jeuxvideo.com"
  html_dom = requests.get('https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm').text
  soup = BeautifulSoup(html_dom, "lxml")
  posts = soup.findAll(class_="topic-title", limit=25)
  del posts[0]
  post = random.choice(posts)
  return {
    "title": post["title"],
    "href": f"{base_post_url}{post['href']}"
  }

def get_best_1825_post():
  base_post_url = "https://www.jeuxvideo.com"
  html_text = requests.get('https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm').text
  soup = BeautifulSoup(html_text, "lxml")
  postlist = soup.find("ul", class_="topic-list topic-list-admin")
  posts = postlist.findAll("li")
  del posts[0]
  out = []
  for post in posts:
      if post.find("span", class_="topic-count") is not None:
          count = post.find("span", class_="topic-count").string
          count = count.replace(" ", "")
          count = count.replace("\n", "")
          count = count.replace("Nb", "0")
      else:
          count = 0
      if post.a is not None and 'href' in post.a.attrs:
          link = post.a["href"]
      else:
          link = ""
      if post.a is not None and 'title' in post.a.attrs:
          title = post.a["title"]
      else:
          title = ""
      out.append((int(count), link, title))
  out.sort(key=lambda x:x[0], reverse=True)
  return {
    "title":out[0][2],
    "href": f"{base_post_url}{out[0][1]}",
    "count":out[0][0],
  }

@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')

@bot.command()
async def ducon(ctx):
  msg = "I'LL MAKE THIS SERVER GREAT AGAIN"
  await ctx.send(msg)

@bot.command()
async def hello(ctx):
  msg = "Hello {0.mention} !".format(ctx.author)
  await ctx.send(msg)

@bot.command()
async def random1825(ctx):
  post = get_random_1825()
  embed = discord.Embed(
      type="rich",
      title=post["title"],
      color=discord.Color.blue(),
      url=post["href"]
  )
  await ctx.send(embed=embed)

@bot.command()
async def best1825(ctx):
  post = get_best_1825_post()
  embed = discord.Embed(
      type="rich",
      title=f'{post["title"]} ({post["count"]} réponses)',
      color=discord.Color.blue(),
      url=post["href"]
  )
  await ctx.send(embed=embed)

@bot.command()
async def paix(ctx):
  msg = "https://image.noelshack.com/fichiers/2021/05/7/1612738731-7484ae4516cs5420.jpg"
  await ctx.send(msg)

@bot.command()
async def risibank(ctx, needle = None):
  msg = "https://image.noelshack.com/fichiers/2021/05/7/1612738731-7484ae4516cs5420.jpg"
  if needle is not None:
    msg = get_random_risibank_by_search(needle)
  else:
    msg = "$ducon risibank [KHEYWORD]\nPoste un sitcker de Risibank en rapport avec la recherche."
  await ctx.send(msg)

bot.run(os.environ['token'])