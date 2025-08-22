import re
import discord
from discord.ext import commands

TOKEN = "TON_TOKEN_ICI"

intents = discord.Intents.default()
intents.members = True  # Nécessaire pour surveiller les nouveaux membres
bot = commands.Bot(command_prefix="!", intents=intents)

# Regex : "Prénom Nom | prenom"
pattern = re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+ \| [A-Za-z]+$")

@bot.event
async def on_ready():
    print(f"✅ Bot connecté comme {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    """Vérifie automatiquement le pseudo à l’arrivée"""
    if not pattern.match(member.display_name):
        try:
            await member.send(
                "⚠️ Ton pseudo ne respecte pas la règle de **La Patrie** !\n\n"
                "👉 Format obligatoire : **Prénom Nom | vrai prenom**\n"
                "Exemple : `Ivan Petrov | Thomas`\n\n"
                "Merci de le corriger immédiatement camarade."
            )
            print(f"❌ {member.display_name} n'a pas respecté la règle, MP envoyé.")
        except discord.Forbidden:
            print(f"Impossible d’envoyer un MP à {member.display_name} (DM fermés).")

@bot.command()
async def verifier(ctx, member: discord.Member = None):
    """Commande manuelle pour vérifier un membre"""
    if not member:
        member = ctx.author  # Si pas de mention, on vérifie l'auteur

    if pattern.match(member.display_name):
        await ctx.send(f"✅ {member.display_name} respecte bien la règle.")
    else:
        await ctx.send(
            f"❌ {member.display_name} ne respecte PAS la règle.\n"
            "Format attendu : `Prénom Nom | vrai prenom`"
        )
        try:
            await member.send(
                "⚠️ Après vérification, ton pseudo ne respecte pas la règle !\n\n"
                "👉 Format obligatoire : **Prénom Nom | vrai prenom**\n"
                "Exemple : `Ivan Petrov | Thomas`\n\n"
                "Merci de le corriger immédiatement camarade."
            )
            print(f"DM envoyé à {member.display_name} suite à la commande !verifier.")
        except discord.Forbidden:
            print(f"Impossible d’envoyer un DM à {member.display_name} (DM fermés).")

bot.run(os.getenv("MTQwODU3MjEyMzYwNTI0MTkwOQ.GhEBIr.Yg0Cxh1R69YZqdqF3vx-HFKp7z-xhLQGn1JjL4"))


