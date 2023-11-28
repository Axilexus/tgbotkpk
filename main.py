import texts
from apply_schedule import *
from CreateSession import CreateSession, events
from DataBase import DataBase
import texts
import asyncio
from buttons import *
Bot = CreateSession("KPKBOT")
letter = {b'11A9': '1-1 А9', b'11B9': '1-1 Б9', b'11G9': '1-1 Г9', b'11P9': '1-1 П9', b'12P9': '1-2 П9', b'11S9': '1-1 С9', b'11R9': '1-1 Р9', b'12R9': '1-2 Р9', b'11S11': '1-1 С11', b'11P11': '1-1 П11', b'21A9': '2-1 А9', b'21B9': '2-1Б9', b'21T9': '2-1 Т9', b'21S9': '2-1С11', b'21P9': '2-1 П9', b'22P9': '2-2 П9', b'21P11': '2-1 П11', b'31A9': '3-1 А9', b'31G9': '3-1 Г9', b'31T9': '3-1 Т9', b'31S9': '3-1 С9', b'31S11': '3-1 С11', b'31B9': '3-1Б9', b'31P9': '3-1 П9', b'32P9': '3-2 П9', b'41A9': '4-1 А9', b'41G9': '4-1 Г9', b'41E9': '4-1 Э9', b'41S9': '4-1С9', b'41P9': '4-1 П9', b'42P9': '4-2 П9'}



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
@Bot.client.on(events.NewMessage(pattern='/h'))
async def homework_msg(event):
    await event.respond(texts.DENAY)
@Bot.client.on(events.NewMessage(pattern='/dwnld'))
async def download_schelude(event):
    if event.message.chat.id == 1051119325:
        url = event.message.text.split(' ', maxsplit=1)[1]
        down = Schedule()
        down.download(url)
        await event.respond("Успешно!")
    else:
        await event.respond(texts.DENAY)
@Bot.client.on(events.NewMessage(pattern='/deldoc'))
async def deldocs(event):
    if event.message.chat.id == 1051119325:
        docs = os.listdir()
        for doc in docs:
            if ".docx" in doc:
                os.remove(doc)
                await event.respond(f"Расписание {doc} было удалено")
    else:
        await event.respond(texts.DENAY)
@Bot.client.on(events.NewMessage(pattern='/r'))
async def schelude_msg(event):
    sender = Schedule()
    text = sender.send_schelude(event.message.chat.id)
    try:
        await event.respond(text)
    except:
        await event.respond("Похоже что то пошло не так... попробуйте ввести команду /groups и выбрать группу. Если не поможет, напишите создателю @axilexus")
@Bot.client.on(events.NewMessage(pattern='/sendall'))
async def sendall_msg(event):
    if event.message.chat.id == 1051119325:
        msg = event.message.text.split(" ", maxsplit=1)[1]
        chat_id = event.message.chat.id
        chats = DataBase('chats.db')
        chats_id = chats.select_data_all("chats")
        for chat in chats_id:
            print(chat[0], msg)
            await Bot.client.send_message(int(chat[0]), msg)
    else:
        await event.respond(texts.DENAY)


@Bot.client.on(events.NewMessage(pattern='/addh'))
async def add_homework_msg(event):
    await event.respond(texts.DENAY)
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
async def select_group_msg(event):
    await event.respond('Пожалуйста, выберите свой курс:', buttons=menu_group)
@Bot.client.on(events.NewMessage(pattern="/calls"))
async def calls_msg(event):
    await Bot.client.send_file(event.message.chat.id, file='images/calls.jpg', caption="Расписание звонков:")
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
            groups = DataBase('groups.db')
            groups.cur.execute("CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, group_name TEXT)")
            chat_id = event.chat.id
            group_name = letter[event.data]
            groups.cur.execute("SELECT * FROM groups WHERE chat_id=?", (chat_id,))
            existing_group = groups.cur.fetchone()
            if existing_group:
                # Если запись уже есть, обновляем название группы
                groups.cur.execute("UPDATE groups SET group_name=? WHERE chat_id=?", (group_name, chat_id))
                groups.conn.commit()
                await event.edit( f"Группа обновлена: {group_name}")
            else:
                # Если записи нет, добавляем новую запись
                groups.cur.execute("INSERT INTO groups VALUES (?, ?)", (chat_id, group_name))
                groups.conn.commit()
                await event.edit(chat_id, f"Группа добавлена: {group_name}")





Bot.start()
