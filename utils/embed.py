import random
from time import sleep

import discord
from discord.ext import commands, tasks
from discord.utils import get

# from core.pundit.pundit import PUNDIT

client = commands.Bot(command_prefix=commands.when_mentioned_or(
    'j!'), description='Nah!!')

def hello():
    return createEmbed(
        name="Hello World!",
        value=10,
        description=
        """
        Write a python program to print the text `Hello World!`
        """,
        sampleoutput="Hello World!"
    )

def mapping():
    return createEmbed(
        name="Mapping",
        value=90,
        description=
        """
        Write a small python program to take a few numbers as input and make them print as a list
        """,
        sampleinput="1 22 33 44",
        sampleoutput="[1, 22, 33, 44]"
    )

def multiply():
    return createEmbed(
        name="Multiply",
        value=100,
        description=
        """
        Write a small python program to take a few <space> seperated numbers as input and make the product of those numbers
        """,
        sampleinput="10 20 30 100",
        sampleoutput="600000",
        explanation="""
Explanation:
10*20*30*100 = 600000
"""
    )


def Toget10():
    return createEmbed(
        name="Toget10",
        value=110,
        description=
        """
        You are given an integer array containing the grades you have received so far in a class. Each grade is between 0 and 10, inclusive. Assuming that you will receive a 10 on all future assignments, determine the minimum number of future assignments that are needed for you to receive a final grade of 10. You will receive a final grade of 10 if your average grade is 9.5 or higher.

        **Input:**
        First line is an integer showing number of previous assignment
        Second line is the space seperated array of integers containing the marks of previous assignment

        **Output:**
        The minimum number of future assignments required


        **This task should be implemented in C language**
        """,
        sampleinput=
"""
2
8 9
""",
        sampleoutput=
"""
4
"""
    )

CHALLS = [
    hello,
    mapping,
    multiply,
    Toget10,
]

async def sendchalls(client):
    taskChnl = get(
            get(
                client.get_guild(id=787331336813412353).categories, name='general'
            )
            .channels,
            name='tasks'
        )
    # taskChnl = client.get_channel(id = 760352099090432020)
    for task in CHALLS:
        await taskChnl.send(
            embed=task()
        )
    return

def createEmbed(name="", value="", description="", category="", sampleinput="", sampleoutput="", explanation="", image_url=""):
    challenge = discord.Embed(
        title=name+"\n"+f"Points: {value}",
        description=description,
        color=0xff0000
    )
    if(sampleinput):
        challenge.add_field(
            name="Sample Input",
            value='```'+sampleinput+'```',
        )
    if(sampleoutput):
        challenge.add_field(
            name="Sample Output",
            value='```'+sampleoutput+'```',
        )
    if(category):
        challenge.add_field(
            name="Category",
            value=category,
        )
    if(explanation):
        challenge.set_footer(
            text=explanation
        )
    if(image_url):
        challenge.set_image(url=image_url)
    return challenge

@client.event
async def on_ready():
    await sendchalls(client)
    exit(0)
client.run("Nzg3MzMxNDU3NTgzOTM5NTk0.X9TZjw.UTH5oa-1bzYTIJhb9VCR02-LBeY")
