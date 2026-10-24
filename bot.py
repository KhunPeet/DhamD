
            for link in found_links:
                clean_link = link.split('&')[0]
                pinned_links.append(clean_link)

        clean_input = url_input.strip().split('&')[0]

        if clean_input not in pinned_links:
            await ctx.send("⛔ **ไม่อนุญาตให้เล่นลิงก์นี้!** บอทอนุญาตให้เล่นเฉพาะลิงก์ YouTube ที่ถูก **ปักหมุด (Pin)** ไว้ในห้องแชทนี้เท่านั้น\n*(พิมพ์ `!listpins` เพื่อดูรายชื่อลิงก์ที่ได้รับอนุญาต)*")
            return

        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("❌ กรุณาเข้าห้องเสียงก่อนสั่งเปิดธรรมะครับ")
                return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        try:
            player = await YTDLSource.from_url(url_input, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            await ctx.send(f'🎧 กำลังเปิดฟังพุทธวจน (จากลิงก์ปักหมุด):\n**{player.title}**')
        except Exception as e:
            await ctx.send(f"⚠️ เกิดข้อผิดพลาดในการเล่นลิงก์นี้: {e}")

@bot.command(name='listpins', help='ดูรายชื่อลิงก์พุทธวจนที่ถูกปักหมุดไว้')
async def listpins(ctx):
    pins = await ctx.channel.pins()
    youtube_regex = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)\S+)'
    
    youtube_links = []
    for message in pins:
        found_links = re.findall(youtube_regex, message.content)
        for link in found_links:
            if link not in youtube_links:
                youtube_links.append(link)

    if not youtube_links:
        await ctx.send("📌 ไม่มีลิงก์ YouTube ในข้อความปักหมุดครับ")
        return

    response = "📌 **รายชื่อพุทธวจนจากข้อความปักหมุด (ที่สามารถใช้คำสั่ง `!play` ได้):**\n"
    for i, link in enumerate(youtube_links, 1):
        response += f"`{i}`. {link}\n"
    await ctx.send(response)

@bot.command(name='stop', help='หยุดเล่นและให้บอทออกจากห้อง')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องเสียงเรียบร้อยแล้วครับ สาธุ 🙏")
    else:
        await ctx.send("⚠️ บอทไม่ได้อยู่ในห้องเสียงครับ")

# ดึง Token จากระบบ Environment Variable ของ Render (ปลอดภัยและไม่ต้องเปิดเผย Token ในโค้ด)
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
