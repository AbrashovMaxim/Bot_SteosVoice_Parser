from aiogram import Bot, types, F, Router
from aiogram.types import URLInputFile
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.enums.chat_member_status import ChatMemberStatus
import aiohttp

from libs.config import config

router = Router()
scoup_player = []
ALPHABET = {"А́": "+А",
            "Е́": "+Е",
            "И́": "+И",
            "О́": "+О",
            "У́": "+У",
            "Ы́": "+Ы",
            "Э́": "+Э",
            "Ю́": "+Ю",
            "Я́": "+Я",
            "а́": "+а",
            "е́": "+е",
            "и́": "+и",
            "о́": "+о",
            "у́": "+у",
            "ы́": "+ы",
            "э́": "+э",
            "ю́": "+ю",
            "я́": "+я"}

class CheckSubscribe(CallbackData, prefix='subscribe'):
    page: int

async def checkStatus(check):
    if check.status == ChatMemberStatus.MEMBER or check.status == ChatMemberStatus.ADMINISTRATOR or check.status == ChatMemberStatus.CREATOR: return True
    else: return False

@router.message(Command('help'))
async def get_base_message(message: types.Message, command:CommandObject, bot: Bot):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": config.get_token_sv()}

    url = "https://api.voice.steos.io/v1/get/voices"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            result_arr = []
            result = ''
            for i in data['voices']:
                print(i)
                result += f'<b>{i["voice_id"]}</b> - {i["name"]["RU"]}\n'
                if len(result) > 3900: result_arr.append(result); result = ''
            result_arr.append(result)
            for i in result_arr: await message.answer(text=i)
            await message.delete()

@router.message(Command('start'))
async def command_start(message: types.Message, command:CommandObject, bot: Bot):
    data = command.args
    try:
        dataSplit = data.split(' ')
        dataInt = int(dataSplit[0])
        async with aiohttp.ClientSession() as session:
            url = "https://api.voice.steos.io/v1/get/tts"
            headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": config.get_token_sv()}
            bodyres = ' '.join(dataSplit[1:])
            for i,j in ALPHABET.items(): bodyres = bodyres.replace(i,j)
            body = {'voice_id': dataInt,
                    'text': bodyres,
                    'format': 'mp3'}
            async with session.post(url, headers=headers, json=body) as resp:
                data = await resp.json()
                file = URLInputFile(
                    data['audio_url'],
                    filename='audio_voice_'+str(dataInt)+'.mp3',
                )
                await bot.send_document(chat_id=message.chat.id, document=file, caption=f"<code>{message.text}</code>")
    except Exception as e:
        print(e)
        await message.answer(text="Неправильная команда!\n<code>/start VOICE_ID TEXT</code>")
        
    await message.delete()

@router.message(Command('scoup'))
async def command_scroupt(message: types.Message, command:CommandObject, bot: Bot):
    chat_id = message.chat.id
    if chat_id in scoup_player:
        scoup_player.remove(chat_id)
    else:
        scoup_player.append(chat_id)
    await message.answer(text="Теперь вы можете отправить сразу несколько команд /start")
    await message.delete()

@router.message(F.text)
async def get_base_message(message: types.Message, bot: Bot):
    print('1')
    chat_id = message.chat.id
    if chat_id in scoup_player:
        try:
            dataSplit = message.text.split("\n")
            for i in dataSplit:
                if i == "": continue
                splitData = i.split(' ')
                dataInt = int(splitData[0])
                async with aiohttp.ClientSession() as session:
                    url = "https://api.voice.steos.io/v1/get/tts"
                    headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": config.get_token_sv()}
                    bodyres = ' '.join(splitData[1:])
                    for j,k in ALPHABET.items(): bodyres = bodyres.replace(j,k)
                    body = {'voice_id': dataInt,
                            'text': bodyres,
                            'format': 'mp3'}
                    async with session.post(url, headers=headers, json=body) as resp:
                        data = await resp.json()
                        file = URLInputFile(
                            data['audio_url'],
                            filename='audio_voice_'+str(dataInt)+'.mp3',
                        )
                        await bot.send_document(chat_id=message.chat.id, document=file, caption=f"<code>{i}</code>")
        except Exception as e:
            print(e)
            await message.answer(text="Неправильная команда!\n<code>/start VOICE_ID TEXT</code>")
        
    await message.delete()