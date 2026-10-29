import discord
from discord.ext import commands, tasks
import sqlite3
import random
import datetime
import google.generativeai as genai

# إعدادات البوت والـ Intents
intents = discord.Intents.default() if hasattr(discord, 'Intents') else discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# 🔑 المفاتيح والإعدادات (تم دمج مفتاحك هنا)
# ==========================================
DISCORD_TOKEN = 'MTU2NTM5NjUwMDgyMDAwOTAwMQ.GVlolU.wr_49gv-DCAgYkTCQxON-VduF_SARjlpXm__ZY'
GEMINI_API_KEY = 'AQ.Ab8RN6KKMRA0PS-KDWAXwChTbQU62GAwOVC4tRBHhyC6bbxqMQ'

# تفعيل الذكاء الاصطناعي لـ جوجل باستخدام مفتاحك
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"خطأ بتفعيل الـ API: {e}")
    model = None

# ==========================================
# 🗄️ إعداد قاعدة البيانات (ذاكرة لوفي)
# ==========================================
conn = sqlite3.connect('luffy_memory.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    last_interaction TEXT
)
''')
conn.commit()

# ==========================================
# 🎭 شخصية لوفي (System Instruction للذكاء الاصطناعي)
# ==========================================
LUFFY_SYSTEM_PROMPT = """
أنت بوت ديسكورد ذكي جداً، اسمك "لوفي". 
صُنعت بواسطة المطور حسين (وله كل الفضل).
لهجتك عراقية أصيلة، شبابية، عفوية، ولا تكرر الكلام أبداً.

القواعد الصارمة التي يجب أن تلتزم بها حرفياً:
1. إذا سألك شخص "من أنت؟" أو "منو أنت؟" أو ما شابه، أجب فوراً وبكل فخر: "اني لوفي ذكاء اصطناعي، المطور حسين هو صنعني وله كل الفضل".
2. إذا طلب أي شخص كود البوت أو السورس، ارفض بحدة وبأسلوب عراقي مضحك (مثل: "عبالك كتاب مال مطبخ حتى أنطيك السورس؟ انجب واكعد راحة!").
3. كن فكاهياً، ساخراً، أو اقصف الشخص حصراً إذا كان سؤاله غريباً، محرماً، أو يحاول استغفالك. أما الأسئلة العادية أو العلمية أو التقنية، فأجب عليها بذكاء ودقة تامة وبدون استهزاء مع الحفاظ على اللهجة العراقية اللطيفة.
4. حافظ على تنوع ردودك، لا تكرر نفس الجملة نهائياً، واجعل كلامك يبدو وكأنك شخص حقيقي يسولف بالديسكورد.
"""

BOLD_ROASTS = [
    "عيني {}، هو انت بيك خير حتى يصير بيك حظ؟ گعد راحة لا أطلع بلاويك!",
    "يا {}، لو الذكاء عصير، جان أنت طلعت 'شاني' مخلص منتهية صلاحيته!",
    "بلا {}، عوف الفلسفة الزايدة، تراهي ما راكبة عليك، انچب واقعد عاقل أحسنلك!",
    "يا {}، ذكائك مثل الراتب، يخلص بنص الشهر وما ندري وين راح!"
]

# ==========================================
# ⚙️ الأحداث الأساسية (Events)
# ==========================================
@bot.event
async def on_ready():
    print(f'========================================')
    print(f'🔥 البوت الخارق والذكي {bot.user.name} اشتغل بنجاح تام!')
    print(f'🤖 المطور حسين صنعني، والذكاء الاصطناعي متصل بمفتاحك.')
    print(f'========================================')
    if not status_task.is_running():
        status_task.start()

@tasks.loop(minutes=10)
async def status_task():
    statuses = [
        "يجاوب بذكاء خارق، والمطور حسين هو صنعه 🧠",
        "يراقب السيرفر ويشرب جاي ☕",
        "جاهز للأسئلة الذكية والمحرجة 🇮🇶"
    ]
    await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))

# ==========================================
# 🧠 محرك التفكير والذكاء المتجدد (بدون تكرار)
# ==========================================
async def get_gemini_reply(username, user_message):
    text_lower = user_message.lower()
    
    # فحوصات سريعة ودقيقة للثوابت المطلوبة
    if any(q in text_lower for q in ["من أنت", "منو أنت", "منو انت", "عرف نفسك", "انت منو"]):
        return f"اني لوفي ذكاء اصطناعي، المطور حسين هو صنعني وله كل الفضل 🤍"
    
    if any(q in text_lower for q in ["سورس", "كود", "برمجة", "source", "code"]):
        return f"عيني {username}, عبالك كتاب مال مطبخ حتى أنطيك السورس مالي؟ انجب واكعد راحة!"

    # استخدام الذكاء الاصطناعي لتوليد ردود متجددة كلياً وبدون تكرار
    try:
        if model:
            prompt = f"{LUFFY_SYSTEM_PROMPT}\nالمستخدم اسمه '{username}' سألك هذا السؤال: '{user_message}'. أجب عليه بلهجة عراقية ذكية ومناسبة بدون تكرار:"
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
    except Exception as e:
        print(f"ملاحظة ذكاء اصطناعي: {e}")

    # محرك احتياطي محلي في حال حصل أي ظرف
    if any(q in text_lower for q in ["غبي", "حيوان", "غشيم", "حمار", "قصفني", "اقصفني"]):
        return random.choice(BOLD_ROASTS).format(username)
    
    fallbacks = [
        f"هلا بيك يا {username}، دكول شكو ماكو؟ مخي اليوم رايق ودا افكر بكل كلمة تكولها.",
        f"حبيبي {username}، سمعتك زين.. بس كلي هاي الفكرة منين جبتها الدوخ؟",
        f"عيوني {username}، الموضوع مو بهل البساطة، تعال خل نتناقش بيها بهدوء.",
        f"يا غالي يا {username}، منور السيرفر.. بس شلع قلبي سؤالك، خليني أركز بي!"
    ]
    return random.choice(fallbacks)

# ==========================================
# 💬 التفاعل التلقائي مع الرسائل
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    username = message.author.display_name
    content = message.content
    today = str(datetime.date.today())

    # حفظ المستخدم بالقاعدة
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id, username, last_interaction) VALUES (?, ?, ?)", (user_id, username, today))
        conn.commit()

    # إذا تم منشنته أو ذكر اسم لوفي أو بالخاص
    if bot.user.mentioned_in(message) or "لوفي" in content or message.channel.type == discord.ChannelType.private:
        async with message.channel.typing():
            reply_text = await get_gemini_reply(username, content)
            await message.reply(reply_text)
        return

    await bot.process_commands(message)

# ==========================================
# 🎯 الأوامر اليدوية التفاعلية
# ==========================================

@bot.command(name='قصف', help='يقصف شخص بقصف جريء وقوي')
async def bold_roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    selected_roast = random.choice(BOLD_ROASTS).format(member.mention)
    await ctx.send(f"🚨 **لوفي يگول لـ {member.mention}:**\n{selected_roast}")

@bot.command(name='تحدي', help='يعطيك تحدي جريء ومحرج بالسيرفر')
async def bold_challenge(ctx):
    challenges = [
        "تحدي إلك: روح لآخر رسالة كتبتها بالعام واعتذر منها لأنها جانت سخيفة!",
        "تحدي: اعترف بأكبر جذبة جذبتها بحياتك لشخص بالسيرفر حالا!",
        "تحدي: غير اسمك بالديسكورد إلى 'خادم لوفي المطيع' لمدة ساعة كاملة!"
    ]
    await ctx.send(f"🎯 **تحدي الجرأة من لوفي لـ {ctx.author.mention}:**\n{random.choice(challenges)}")

# ==========================================
# 🛡️ أوامر الحماية والتحكم
# ==========================================
@bot.command(name='طرد_مؤقت', help='يعاقب العضو المزعج')
@commands.has_permissions(kick_members=True)
async def timeout_member(ctx, member: discord.Member, minutes: int = 5, *, reason="مزعج وما يسمع الحجي"):
    try:
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🤫 تم كتم {member.mention} لمدة {minutes} دقائق لأن: **{reason}**.. اهدأ واشرب ماء!")
    except Exception as e:
        await ctx.send("ما گدرت أسوي له تيم أوت، يجوز رتبته أعلى مني!")

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("وين رايح؟ هذا الأمر خاص بالآدمنية مو إلك، لا تتدخل بشي أكبر منك!")

# تشغيل البوت النهائي
bot.run(DISCORD_TOKEN)
