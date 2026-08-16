import discord
from discord.ext import tasks
import datetime
import zoneinfo
import os

# ===== 설정 =====
TOKEN = os.environ.get("DISCORD_TOKEN", "여기에_봇_토큰_입력")
CHANNEL_ID = 123456789012345678  # 이 봇이 메시지를 보낼 채널 ID로 바꾸세요

MORNING_MESSAGE = "좋은 아침입니다! 오늘도 힘내세요 ☀️"
NIGHT_MESSAGE = "오늘 하루도 수고하셨습니다 🌙"
# =================

KST = zoneinfo.ZoneInfo("Asia/Seoul")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# 오늘 이미 보냈는지 기록 (중복 발송 방지)
sent_today = {"morning": None, "night": None}


@tasks.loop(seconds=30)
async def check_time():
    now = datetime.datetime.now(KST)
    today = now.date()

    # 매일 아침 7시
    if now.hour == 7 and now.minute == 0 and sent_today["morning"] != today:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(MORNING_MESSAGE)
        sent_today["morning"] = today

    # 매일 밤 9시
    if now.hour == 21 and now.minute == 0 and sent_today["night"] != today:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(NIGHT_MESSAGE)
        sent_today["night"] = today


@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료 (봇이 온라인 상태입니다)")
    if not check_time.is_running():
        check_time.start()


client.run(TOKEN)
