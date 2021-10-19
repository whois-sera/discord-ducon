import logging, json, random, requests, os, discord
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

rootDir = os.path.abspath(os.path.dirname(__file__))
rDir = os.path.join(rootDir, "ressources")

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
  """Return a Risibank sticker corresponding to the given keyword"""

  try:
    url = 'https://api.risibank.fr/api/v0/search'
    myobj = {'search': kw}

    ret = requests.post(url, data = myobj)
    dict_stickers = json.loads(ret.text)
    stickers = list(filter(lambda like: like["likes"] > 500, dict_stickers["stickers"]))
    if len(stickers) == 0:
      stickers = dict_stickers["stickers"]
    return random.choice(stickers)["risibank_link"]
  except:
    return "Aucun résultat !"

def get_random_1825():
  """Retrun a random 18-25 post from the first page"""

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
  """Return the most popular post in the first page of 18-25"""

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
  """Display when the bot is up and running"""

  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')

@bot.command()
async def ducon(ctx):
  """Affiche la raison d'etre du bot"""

  msg = "I'LL MAKE THIS SERVER GREAT AGAIN"
  await ctx.send(msg)

@bot.command()
async def gambate(ctx):
  """Encourage chaudement"""

  imgs = os.listdir(os.path.join(rDir, "gambate"))
  rand = random.choice(imgs)
  file = os.path.join(rDir, "gambate", rand)
  img = discord.File(file)
  await ctx.send(file=img)

@bot.command()
async def random1825(ctx):
  """Envoi un post 18-25 random parmis les 25 premiers"""

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
  """Envoi le post 18-25 avec le plus de réponse, en 1ere page"""

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
  """J'ai la flemme de documenter cette merde"""

  msg = "https://image.noelshack.com/fichiers/2021/05/7/1612738731-7484ae4516cs5420.jpg"
  await ctx.send(msg)

@bot.command()
async def risibank(ctx, needle = None):
  """Envoi un sticker Risibank suivant le theme donné
  
  ./risibank <theme>
  """

  msg = "https://image.noelshack.com/fichiers/2021/05/7/1612738731-7484ae4516cs5420.jpg"
  if needle is not None:
    msg = get_random_risibank_by_search(needle)
  else:
    msg = "$ducon risibank [KHEYWORD]\nPoste un sitcker de Risibank en rapport avec la recherche."
  await ctx.send(msg)

@bot.command()
async def isUp(ctx):
  """S'assurer que le bot est up"""

  await ctx.send("I'M UP MOTHERFUCKER !!")

bot.run(os.environ['token'])
