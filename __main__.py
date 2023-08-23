import asyncio
import logging
import genshin
import os

accountsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "accounts.txt")

def getAccount():
    infos = []
    with open(accountsFile, "r") as f:
        lines = f.readlines()
        
        i = 0
        for line in lines:
            if i != 0:
                infos.append(line.strip().split(" "))
            i += 1
    return infos
            

def getLogger():
    logger = logging.getLogger("genshin daily rewards")
    logger.setLevel(logging.INFO)
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "genshin_daily_rewards.log")
    if not os.path.isfile(file):
        with open(file, "w") as f:
            pass
    handler = logging.FileHandler(filename=file, encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s %(message)s'))
    logger.addHandler(handler)
    return logger

async def collect(ltuid, ltoken, logger: logging.Logger, user="not specify"):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies, game=genshin.Game.GENSHIN)

    try:
        reward = await client.claim_daily_reward()
        logger.info("{} was {} collected for {}".format(reward.amount, reward.name, user))
    except genshin.AlreadyClaimed:
        logger.info("Already collected for {}".format(user))
    except Exception as e:
        logger.warning("Error for {}. {}".format(user, e))
    
async def main():
    logger = getLogger()
    if not os.path.isfile(accountsFile):
        raise Exception("No accounts file !")
    while True :
        accounts = getAccount()
        for account in accounts:
            await collect(account[0], account[1], logger, account[2])
        await asyncio.sleep(60 * 60 * 6) # Every 6 hours
        
        
asyncio.run(main())

