import texts
from CreateSession import CreateSession, events
from DataBase import DataBase
import texts
import asyncio
from buttons import *
Bot = CreateSession("KPKBOT")



@Bot.client.on(events.NewMessage(pattern='/start'))
async def start_msg(event):
    chat_id = event.message.chat.id
    chats = DataBase('chats.db')
    chats.create_base("chats", "chat")
    chats.insert_data("chats", chat_id)

    await event.respond(texts.GREETINGS)

@Bot.client.on(events.NewMessage(pattern='/help'))
async def help_msg(event):
    await event.respond(texts.HELP)


@Bot.client.on(events.NewMessage(pattern='/chats'))
async def chats_msg(event):
    if event.message.chat.id == 1051119325:
        chats = DataBase('chats.db')
        chats.create_base("chats", "chat")
        chats_id = chats.select_data_all("chats")
        text = texts.CHATS_TEXT
        for chat in chats_id:
            text += f"```{chat[0]}```\n"

        await event.respond(text)
    else:
        await event.respond(texts.DENAY)

@Bot.client.on(events.NewMessage(pattern='/group'))
async def test_msg(event):
    await event.respond('Пожалуйста, выберите свой курс:', buttons=menu_group)

@Bot.client.on(events.CallbackQuery())
async def callback_handler(event):
    match event.data:
        case b'1_course':
            await event.edit("Выберите группу первого курса:", buttons=menu_1_course)
        case b'2_course':
            await event.edit("Выберите группу второго курса:", buttons=menu_2_course)
        case b'3_course':
            await event.edit("Выберите группу третьего курса:", buttons=menu_3_course)
        case b'4_course':
            await event.edit("Выберите группу четвертого курса:", buttons=menu_4_course)
        case b'back':
            await event.edit('Пожалуйста, выберите свой курс:', buttons=menu_group)
        case _:
            await event.edit("Еще не готово :(")





Bot.start()
