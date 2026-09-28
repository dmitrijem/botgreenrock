from aiogram import Bot, Dispatcher, F, types, fsm
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import markup
import models
from aiogram.types import InlineKeyboardButton, Message
from aiogram.filters import Command
import asyncio
import re
import json

BOT_TOKEN = "8099964645:AAETF1WUdtUWRbmUL1DX6spjBUWA4WsNNlY"
ADMIN = 940369449
message_ids = []

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    inn = State()
    name = State()
    pay = State()
    user_id = State()
    user_money = State()
    am_cost = State()
    cost = State()
    am_cost_buy = State()
    div = State()
    order_am = State()
    order_cos = State()
    order_buy_am = State()
    order_buy_cost = State()
    order_id = State()
    am_cost_cr = State()
    cost_cr = State()
    name_cr = State()
    am_cost_buy_cr = State()

timer_events = {}

def edit_money(message: Message,edmoney, edpayme, user_id):
    with models.SessionLocal() as session:
        money = float(edmoney)
        payme = float(edpayme)
        new_money = str(money+payme)
        user = session.query(models.User).filter(models.User.user_id == user_id).first()
        if not user:
            return None
        user.money = str(new_money)
        session.commit()
        return new_money
def user_invest(callback_query: types.CallbackQuery, inn, name):
    with models.SessionLocal() as session:
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        firstname = callback_query.from_user.full_name
        status = "Инвестор"
        money = 0
        cost = 0
        new_user_invest = models.User(user_id=user_id,firstname=firstname, username=username, status=status, inn=inn, name=name, money=money, costs_on_birge=cost, crypto_on_birge=0)
        session.add(new_user_invest)
        session.commit()
def user_invest2(user_id, firstname, usrname, inn, name):
    with models.SessionLocal() as session:
        user_id = user_id
        username = usrname
        firstname = firstname
        status = "Инвестор"
        money = 0
        cost = 0
        new_user_invest = models.User(user_id=user_id,firstname=firstname, username=username, status=status, inn=inn, name=name, money=money, costs_on_birge=cost, crypto_on_birge=0)
        session.add(new_user_invest)
        session.commit()
def user_comp(callback_query: types.CallbackQuery, inn, name):
    with models.SessionLocal() as session:
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        firstname = callback_query.from_user.first_name
        status = "Компания"
        money = 0
        cost = 0
        new_user_comp = models.User(user_id=user_id,firstname=firstname, username=username, status=status, inn=inn, name=name, money=money, costs_on_birge=cost, crypto_on_birge=0)
        session.add(new_user_comp)
        session.commit()
def user_comp2(user_id, firstname, usrname, inn, name):
    with models.SessionLocal() as session:
        user_id = user_id
        username = usrname
        firstname = firstname
        status = "Компания"
        money = 0
        cost = 0
        new_user_comp = models.User(user_id=user_id,firstname=firstname, username=username, status=status, inn=inn, name=name, money=money, costs_on_birge=cost, crypto_on_birge=0)
        session.add(new_user_comp)
        session.commit()
def pay(message: Message, payme):
    with models.SessionLocal() as session:
        user_id = message.from_user.id
        inn_from = "Наличные рудлы"
        Operation = "Пополнение счета"
        inn_to = models.get_user_inn(user_id)
        costs = "-"
        new_pay = models.oper(user_id=user_id, inn_from=inn_from, operation=Operation,payme=payme, inn_to=inn_to, costs=costs)
        session.add(new_pay)
        session.commit()
def place(message: Message, costs, pay, pays):
    with models.SessionLocal() as session:
        user_id = message.from_user.id
        inn_from = models.get_user_inn(user_id)
        operation = "Размещение акиций на биржу!"
        inn_to = "Биржа"
        new_place = models.oper(user_id=user_id, inn_from=inn_from, operation=operation, payme=pay,one_cost=pays, costs=costs, inn_to=inn_to)
        session.add(new_place)
        session.commit()
async def delete_message_after_delay(event: asyncio.Event, order_index: int, user_id: int, am_buy: int, order_id: int):
    try:
        await asyncio.wait_for(event.wait(), timeout=24*3600)
    except asyncio.TimeoutError:
        print(1)
        pass
    a = int(am_buy)
    with models.SessionLocal() as session:
            userid = session.query(models.User).filter(models.User.user_id == user_id).first()
            user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
            order = session.query(models.orders).filter(models.orders.id == order_id).first()
            if order.st_order == "Продажа":
                list = json.loads(user.have_cost)
                letter = "".join(re.findall(r"[^\d]", list[order_index]))
                num = "".join(re.findall(r"\d", list[order_index]))
                list[order_index] = f"{letter}{int(num)+a}"
                user.have_cost = json.dumps(list, ensure_ascii=False)
                session.query(models.orders).filter(models.orders.id == order_id).delete()
                session.commit()
            elif order.st_order == "Покупка":
                session.query(models.orders).filter(models.orders.id == order_id).delete()
                session.commit()
    await bot.send_message(user_id, text="Ваш оредер истек!")
    timer_events.pop(order_id, None)


    
@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if models.user_exist(user_id):
        if models.get_user_status(user_id) == "Компания":
            msg = await message.answer("Вы уже зарегестрировали Компанию", reply_markup=markup.but2)
        elif models.get_user_status(user_id) == "Инвестор":
            msg = await message.answer("Вы уже зарегестрировались как Инвестор", reply_markup=markup.but4)
    elif not models.user_exist(user_id):
        msg = await message.answer("Привет(по всем вопросам писать @neverminderrr)! Напиши номер своего ИНН")
        await state.set_state(Form.inn)
@dp.message(F.text, Form.inn)
async def cap_name(message: Message, state: FSMContext):
        if len(message.text) != 4:
            await message.answer("Вы ввели неккоректный ИНН, попробуйте еще раз!(ИНН - 4 цифры)")
            return
        await state.update_data(inn=message.text)
        await message.answer("Введите название вашей компании или ИП!(цифры в названии не писать!!!)")

        await state.set_state(Form.name)
@dp.message(F.text, Form.name)
async def test(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        data = await state.get_data()
        inn = data.get('inn')
        name = data.get('name')
        await message.answer(f'Отлично вот твои данные:\n'
                             f'ИНН: {inn}\n' 
                             f'Название: {name}\n' 
                             'Твое колличество рудлов: 0\n' 
                             'Если все верно нажми дальше\n' 
                             'Если ты хочешь изменить еще раз! ',reply_markup=markup.but7)
@dp.callback_query(F.data == 'again')
async def again(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.reply("Напиши еще раз команду /start!")
@dp.callback_query(F.data == 'next')
async def next(callback_query: types.CallbackQuery):
    msg = await callback_query.message.reply("Выберите ветку игры!", reply_markup=markup.but3)

@dp.callback_query(F.data == "role_company")
async def comp(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Заявка на регистрацию отправлена!")
    user_id = callback_query.from_user.id
    firstname = callback_query.from_user.first_name
    usrname = callback_query.from_user.username
    data = await state.get_data()
    inn = data.get('inn')
    name = data.get('name')
    await bot.send_message(ADMIN, f"Заявка на регистрацию\n"
                                    f"ИНН - {inn}\n"
                                    f"Имя - {name}", reply_markup=markup.but29)
    @dp.callback_query(F.data == "agree_reg_cmp")
    async def reg_agr(callback_query: types.CallbackQuery, state: FSMContext):
        await bot.send_message(user_id, "Заявка одобрена! Вы зарегестрировали компанию!", reply_markup=markup.but2)
        
        user_comp2(user_id, firstname, usrname, inn, name)
        await state.clear()
    @dp.callback_query(F.data == "disagree_reg_cmp")
    async def reg_disagr(callback_query: types.CallbackQuery, state: FSMContext):
        await bot.send_message(user_id,"Заявка отклонена попробуйте еще раз! (/start)")
@dp.callback_query(F.data == 'role_investor')
async def inv(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Заявка на регистрацию отправлена!")
    user_id = callback_query.from_user.id
    firstname = callback_query.from_user.first_name
    usrname = callback_query.from_user.username
    data = await state.get_data()
    inn = data.get('inn')
    name = data.get('name')
    await bot.send_message(ADMIN, f"Заявка на регистрацию\n"
                                    f"ИНН - {inn}\n"
                                    f"Имя - {name}", reply_markup=markup.but30)
    @dp.callback_query(F.data == "agree_reg_inv")
    async def reg_agri(callback_query: types.CallbackQuery, state: FSMContext):
        print(name, inn)
        await bot.send_message(user_id, "Заявка одобрена! Вы зарегестрировались как инвестор!", reply_markup=markup.but4)
        user_invest2(user_id, firstname,usrname, inn, name)
        with models.SessionLocal() as session:
            user = session.query(models.User).filter(models.User.user_id == user_id).first()
            new_costs = models.costs(invest_name = user.name, have_cost = "[]")
            session.add(new_costs)
            new_crypto = models.crypto(invest_name= user.name, have_crypto="[]")
            session.add(new_crypto)
            session.commit()
        await state.clear()
    @dp.callback_query(F.data == "disagree_reg_inv")
    async def reg_disagri(callback_query: types.CallbackQuery, state: FSMContext):
        await bot.send_message(user_id, "Заявка отклонена попробуйте еще раз! (/start)")
@dp.callback_query(F.data == 'profile_company')
async def pfofile_comp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    firstname = models.get_user_first(user_id)
    name = models.get_user_name(user_id)
    money = models.get_user_money(user_id)
    inn = models.get_user_inn(user_id)
    await callback_query.message.reply(f"Вот данные твоей Компании:\n"
                                       f"Имя: {firstname}\n"
                                       f"Название компании: {name}\n"
                                       f"Колличество рудолов: {money}\n"
                                       f"ИНН: {inn}", reply_markup=markup.but10)
@dp.callback_query(F.data == 'profile_investor')
async def inv_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    firstname = models.get_user_first(user_id)
    name = models.get_user_name(user_id)
    money = models.get_user_money(user_id)
    inn = models.get_user_inn(user_id)
    await callback_query.message.reply(f"Вот данные твоего профиля:\n"
                                       f"Имя: {firstname}\n"
                                       f"Название ИП: {name}\n"
                                       f"Колличество рудолов: {money}\n"
                                       f"ИНН: {inn}", reply_markup=markup.but10)
@dp.callback_query(F.data == "my_shares_investor")
async def my_costs_comp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
    markup.but15.inline_keyboard.clear()
    markup.but15.inline_keyboard.append([InlineKeyboardButton(text=f"Акции - Колличество",callback_data=f"stock")])
    if user:
        list = json.loads(user.have_cost)
        for i in list:
            letter = "".join(re.findall(r"[^\d]", i))
            num = "".join(re.findall(r"\d", i))
            if int(num) != 0:
                markup.but15.inline_keyboard.append([InlineKeyboardButton(text=f"{letter} - {num}",callback_data=f"stock_")])
    markup.but15.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Ваши акции:", reply_markup=markup.but15)

@dp.callback_query(F.data == "my_shares_company")
async def my_costs_comp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
    await callback_query.message.reply(f"У вас на бирже {userid.costs_on_birge} акций!", reply_markup=markup.but8)
    




@dp.callback_query(F.data == "payment_company")
async def pay_company(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.reply("Введи колличество рудолов, которые ты хочешь положить на счет!", reply_markup=markup.but9)
    await state.set_state(Form.pay)
    @dp.message(F.text, Form.pay)
    async def pays(message: Message, state: FSMContext):
        if message.text.isnumeric():
            await state.update_data(pay=message.text)
            data = await state.get_data()
            payme = data.get('pay')
            user_id = message.from_user.id
            pay(message, payme)
            await message.reply(f"<b>Заявка оставлена!</b>\n"
                            f"Вы хотите пополнить свой счет <b>{models.get_inn_log(user_id)}</b> на <b>{payme}</b>\n"
                            f"Чтобы мы подтвердили транзакцию, вам нужно сделать перевод на <b>ИНН биржи</b> на сайте <b>Ньюландии</b>\n"
                            f"<b>ИНН биржи: XXXX</b>", reply_markup=markup.but8, parse_mode="HTML")
            await bot.send_message(940369449, f"Новая заявка от пользователя {models.get_inn_log(user_id)} на {payme}\n!", reply_markup=markup.but11)
        else:
            await message.reply("Вы ввели неккректное число, введите число еще раз!")
            return
        @dp.callback_query(F.data == "agree")
        async def agree(message: Message, state: FSMContext):
            edpaym = models.get_user_payme(user_id)
            user_to = models.get_user_logi_id()
            with models.SessionLocal() as session:
                session.query(models.User).filter(models.User.user_id == user_to).update({models.User.money: models.User.money + edpaym})
                user_st = session.query(models.User).order_by(models.User.user_id == user_to).first()
                user = session.query(models.oper).order_by(models.oper.id.desc()).first()
                user.status = "Принята"
                session.commit()
            await bot.send_message(user_to, f"Заявка одобрена!")
            await bot.send_message(ADMIN, "Вы одобрили заявку!")
        @dp.callback_query(F.data == "disagree")
        async def diagree(message: Message):
            with models.SessionLocal() as session:
                user = session.query(models.oper).order_by(models.oper.id.desc()).first()
                user.status = "Отклонена"
                session.commit()
            user_to = models.get_user_logi_id(user_id)
            await bot.send_message(user_to, f"Заявка отклонена!", reply_markup=markup.but2)

@dp.callback_query(F.data == "place_shares")
async def place_share(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.reply("Введите колличество акций которые вы хотите разместить на бирже!")
    await state.set_state(Form.am_cost)
    @dp.message(F.text, Form.am_cost)
    async def am_cost(message: Message, state: FSMContext):
        if message.text.isnumeric():
            await state.update_data(am_cost=message.text)
            await message.reply("Введите цену за одну акцию!")
            await state.set_state(Form.cost)
        else:
            await message.reply("Вы ввели некоректное число, попробуйте еще раз!")
            return
    @dp.message(F.text, Form.cost)
    async def cost(message: Message, state: FSMContext):
        if message.text.isnumeric():
            user_id = message.from_user.id
            await state.update_data(cost=message.text)
            data = await state.get_data()
            user_id = message.from_user.id
            costs = int(data.get('am_cost'))
            pays = int(data.get('cost'))
            pay = costs*pays
            with models.SessionLocal() as session:
                money = session.query(models.User).filter(models.User.user_id == user_id).first()
            await message.reply(f"Заявка на размещение акций оставлен\nВы хотите разместить: {data.get('am_cost')} акций\nПо {data.get('cost')} рудолов за штуку!")
            await bot.send_message(940369449, f"Компания с ИНН: {models.get_user_inn(user_id)}\nХочет разместить: {data.get('am_cost')} акций\nПо {data.get('cost')} рудолов за штуку!", reply_markup=markup.but12)
            place(message, costs, pay, pays)
        else:
            await message.reply("Вы ввели некоректное число, попробуйте еще раз!")
            return
        @dp.callback_query(F.data == "agreee_place")
        async def agreeeee_place(callback_query: types.CallbackQuery):
            print(1)
            data = await state.get_data()
            costs = int(data.get('am_cost'))
            print(costs)
            with models.SessionLocal() as session:
                user = session.query(models.oper).order_by(models.oper.id.desc()).first()
                user.status = "Принята"
                session.commit()          
            user_to = models.get_user_logi_id()
            if money.status == "Компания":
                await bot.send_message(user_to, "Ваши акции размещены на бирже!", reply_markup=markup.but2)
            elif money.status == "Инвестор":
                await bot.send_message(user_to, "Ваши акции размещены на бирже!", reply_markup=markup.but4)
            await bot.send_message(ADMIN, "Вы одобрили заявку на размещение!")
            data.clear()
            markup.but13.inline_keyboard.clear()
            with models.SessionLocal() as session:
                userid = session.query(models.User).filter(models.User.user_id == user_id).first()
                userid.costs_on_birge = userid.costs_on_birge+int(costs)
                inn_from = models.get_user_inn(user_to)
                name = models.get_user_name(user_to)
                costs = models.get_logi_costs()
                payme = pay
                one_cost = models.get_logi_one_costs()
                new_pay = models.birge(name=name,user_id=user_id, inn_from=inn_from,one_cost = one_cost, payme=payme, costs=costs, type="cost")
                session.add(new_pay)
                session.commit()
            stocks = models.get_last_costs()
            markup.but13.inline_keyboard.append([InlineKeyboardButton(text=f"Компания - ИНН - Стоимость одной акции - Колличество акций",callback_data=f"stock")])
            for stock in stocks:
                markup.but13.inline_keyboard.append([InlineKeyboardButton(text=f"{stock.name} - {stock.inn_from} - {stock.one_cost}$ - {stock.costs}",callback_data=f"stock_{stock.id}")])
            markup.but13.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
            await callback_query.message.reply("Акции на бирже:", reply_markup=markup.but13)

@dp.callback_query(F.data == "place_crypto")
async def place_share(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.reply("Введите название для вашей монеты! (стоимость размещения 10.000 рудолов)")
    await state.set_state(Form.name_cr)
    @dp.message(F.text, Form.name_cr)
    async def name_cr(message: Message, state: FSMContext):
        if len(message.text) <= 10 and len(message.text) >= 3:
            await state.update_data(name_cr=message.text)
            await callback_query.message.reply("Введите колличество криптовалюты которые вы хотите разместить на бирже!")
            await state.set_state(Form.am_cost_cr)
        else:
            await message.reply("Вы ввели неккоректное название, попробуйте еще раз!")
            return            
    @dp.message(F.text, Form.am_cost_cr)
    async def am_cost(message: Message, state: FSMContext):
        if message.text.isnumeric():
            await state.update_data(am_cost_cr=message.text)
            await message.reply("Введите цену за одну монету!")
            await state.set_state(Form.cost_cr)
        else:
            await message.reply("Вы ввели некоректное число, попробуйте еще раз!")
            return
    @dp.message(F.text, Form.cost_cr)
    async def cost(message: Message, state: FSMContext):
        user_id = message.from_user.id
        with models.SessionLocal() as session:
            userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        moneyx = int(userid.money)
        if message.text.isnumeric():
            if moneyx > 10000:
                user_id = message.from_user.id
                await state.update_data(cost_cr=message.text)
                data = await state.get_data()
                user_id = message.from_user.id
                costs = int(data.get('am_cost_cr'))
                pays = int(data.get('cost_cr'))
                pay = costs*pays
                with models.SessionLocal() as session:
                    money = session.query(models.User).filter(models.User.user_id == user_id).first()
                await message.reply(f"Заявка на размещение акций оставлен\nВы хотите разместить: {data.get('am_cost_cr')} монет\nПо {data.get('cost_cr')} рудолов за штуку!")
                await bot.send_message(940369449, f"Компания с ИНН: {models.get_user_inn(user_id)}\nХочет разместить: {data.get('am_cost_cr')} монет\nПо {data.get('cost_cr')} рудолов за штуку!", reply_markup=markup.but28)
                place(message, costs, pay, pays)
            else:
                await message.reply("У вас недостаточно средств (10.000), попробуйте еще раз!")
        else:
            await message.reply("Вы ввели некоректное число, попробуйте еще раз!")
            return
        @dp.callback_query(F.data == "agreee_cr")
        async def agr_place(callback_query: types.CallbackQuery):
            print(1)
            data = await state.get_data()
            costs = int(data.get('am_cost_cr'))
            print(costs)         
            user_to = models.get_user_logi_id()
            if money.status == "Компания":
                await bot.send_message(user_to, "Ваши монеты размещены на бирже!", reply_markup=markup.but2)
            await bot.send_message(ADMIN, "Вы одобрили заявку на размещение!")
            name = str(data.get('name_cr'))
            markup.but25.inline_keyboard.clear()
            with models.SessionLocal() as session:
                userid = session.query(models.User).filter(models.User.user_id == user_id).first()
                userid.money = int(userid.money)-10000
                userid.crypto_on_birge = userid.crypto_on_birge+int(costs)
                inn_from = models.get_user_inn(user_to)
                print(name)
                costs = models.get_logi_costs()
                payme = pay
                one_cost = models.get_logi_one_costs()
                new_pay = models.birge(name=name,user_id=user_id, inn_from=inn_from,one_cost = one_cost, payme=payme, costs=costs, type="crypto")
                session.add(new_pay)
                session.commit()
            data.clear()
            stocks = models.get_last_crypto()
            markup.but25.inline_keyboard.append([InlineKeyboardButton(text=f"Название - Стоимость - Колличество",callback_data=f"fsdfdsf")])
            for stock in stocks:
                markup.but25.inline_keyboard.append([InlineKeyboardButton(text=f"{stock.name} - {stock.inn_from} - {stock.one_cost}$ - {stock.costs}",callback_data=f"stock_{stock.id}")])
            markup.but25.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
            await callback_query.message.reply("Криптовалюта на бирже:", reply_markup=markup.but25)

        @dp.callback_query(F.data == "disagree_cr")
        async def disagree(message: Message):
            if money.status == "Компания":
                await callback_query.message.reply("Ваши монеты не будут размещены на бирже", reply_markup=markup.but2)
            await bot.send_message(ADMIN, "Вы отклонили заявку на размещение!")
@dp.callback_query(F.data == "exchange_company")
async def birge(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Выберите:",reply_markup=markup.but24)
@dp.callback_query(F.data == "costs")
async def costs(callback_query: types.CallbackQuery):
    markup.but13.inline_keyboard.clear()
    stocks = models.get_last_costs()
    markup.but13.inline_keyboard.append([InlineKeyboardButton(text=f"Компания - ИНН - Стоимость акции - Кол. акций",callback_data=f"stock")])
    for stock in stocks:
        markup.but13.inline_keyboard.append([InlineKeyboardButton(text=f"{stock.name} - {stock.inn_from} - {stock.one_cost}$ - {stock.costs}",callback_data=f"stock_{stock.id}")])
    markup.but13.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Актуальные акции компаний!", reply_markup=markup.but13)
@dp.callback_query(F.data == "crypto")
async def crypto(callback_query: types.CallbackQuery):
    markup.but25.inline_keyboard.clear()
    stocks = models.get_last_crypto()
    markup.but25.inline_keyboard.append([InlineKeyboardButton(text=f"Название - Стоимость - Колличество",callback_data=f"fdsfsdfdsfdsfds")])
    for stock in stocks:
        markup.but25.inline_keyboard.append([InlineKeyboardButton(text=f"{stock.name} - {stock.inn_from} - {stock.one_cost}$ - {stock.costs}",callback_data=f"crypto_{stock.id}")])
    markup.but25.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Актуальная криптовалюта!", reply_markup=markup.but25)

@dp.callback_query(F.data.startswith("crypto_"))
async def birge_crypto(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    stat = models.get_user_status(user_id)
    if stat != "Компания":
        stock_id = int(callback_query.data.split("_")[1])
        with models.SessionLocal() as session:
            stock = session.query(models.birge).filter_by(id=stock_id).first()
            user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()
        if stock:
            await callback_query.message.answer(
                f"Вы выбрали:\n"
                f"Название: {stock.name}\n"
                f"Цена: {stock.one_cost}$\n"
                f"Количество: {stock.costs} шт.", reply_markup=markup.but26)
            stock=stock.name
        else:
            await callback_query.message.answer("Акция не найдена.")
    else:
        await callback_query.message.reply("Компания не может покупать акции!")    
    @dp.callback_query(F.data == "buy_crypto")
    async def buy_crypto(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.reply("Введите колличество монет, которые вы хотите купить!")
        await state.set_state(Form.am_cost_buy_cr)
        @dp.message(F.text, Form.am_cost_buy_cr)
        async def buy_cryptor(message: Message, state: FSMContext):
            with models.SessionLocal() as session:
                stock = session.query(models.birge).filter_by(id=stock_id).first()
                user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()          
            user_id = message.from_user.id
            await state.update_data(am_cost_buy_cr=message.text)
            data = await state.get_data()
            am_buy = data.get("am_cost_buy_cr")
            if int(am_buy) > int(models.get_birge_costs()):
                await message.reply("Нет столько монет на бирже!!")
                return
            elif int(am_buy) < 1:
                await message.reply("Дурак нахуя тебе отрицательное число акций?")
                return
            else:
                datas = False
                await message.reply(f"Вы купили {am_buy} ыы по цене - {models.get_birge_one_costs()}$")
                await bot.send_message(user.user_id, f"У вас купили {int(am_buy)} по цене {stock.one_cost}")
                with models.SessionLocal() as session:
                    userc = session.query(models.birge).filter(models.birge.name == stock.name).first()
                    user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()
                    userr = session.query(models.User).filter(models.User.user_id == user_id).first()
                    userr.money = userr.money-(int(am_buy)*int(stock.one_cost))
                    user.money = user.money+(int(am_buy)*int(stock.one_cost))
                    userid = session.query(models.User).filter(models.User.user_id == user_id).first()
                    user = session.query(models.crypto).filter(models.crypto.invest_name == userid.name).first()
                    if user:
                        data = json.loads(user.have_crypto)
                        for i in data:
                            letter = "".join(re.findall(r"[^\d]", i))
                            num = "".join(re.findall(r"\d", i))
                            index = data.index(i)
                            if str(letter) == str(stock.name):
                                datas = True
                                data[index] = f"{letter}{int(num)+int(am_buy)}"
                                json_data = json.dumps(data, ensure_ascii=False)
                                user.have_crypto = json_data
                                session.commit()
                        if datas == False:
                            data.append(f"{stock.name}{am_buy}")
                            json_data = json.dumps(data, ensure_ascii=False)
                            user.have_crypto = json_data
                            session.commit()
                    userc.costs = userc.costs - int(am_buy)
                    session.commit()
                    if userc.costs == 0:
                        session.delete(userc)
                    session.commit()

@dp.callback_query(F.data.startswith("stock_"))
async def birge_but(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    stat = models.get_user_status(user_id)
    if stat != "Компания":
        stock_id = int(callback_query.data.split("_")[1])
        with models.SessionLocal() as session:
            stock = session.query(models.birge).filter_by(id=stock_id).first()
            user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()
        if stock:
            await callback_query.message.answer(
                f"Вы выбрали:\n"
                f"Название: {stock.name}\n"
                f"Цена: {stock.one_cost}$\n"
                f"Количество: {stock.costs} шт.", reply_markup=markup.but14)
            stock=stock.name
        else:
            await callback_query.message.answer("Акция не найдена.")
    else:
        await callback_query.message.reply("Компания не может покупать акции!")
    @dp.callback_query(F.data == "buy_stock")
    async def buy_cost(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.reply("Введите колличество акций, которые вы хотите купить!")
        await state.set_state(Form.am_cost_buy)
        @dp.message(F.text, Form.am_cost_buy)
        async def buy_costs(message: Message, state: FSMContext):
            with models.SessionLocal() as session:
                stock = session.query(models.birge).filter_by(id=stock_id).first()
                user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()
            user_id = message.from_user.id
            await state.update_data(am_cost_buy=message.text)
            data = await state.get_data()
            am_buy = data.get("am_cost_buy")
            if int(am_buy) > int(models.get_birge_costs()):
                await message.reply("Нет столько акций на бирже!!")
                return
            elif int(am_buy) < 1:
                await message.reply("Дурак нахуя тебе отрицательное число акций?")
                return
            else:
                datas = False
                await message.reply(f"Вы купили {am_buy} акций по цене - {models.get_birge_one_costs()}$")
                await bot.send_message(user.user_id, f"У вас купили {int(am_buy)} по цене {stock.one_cost}")
                with models.SessionLocal() as session:
                    userc = session.query(models.birge).filter(models.birge.name == stock.name).first()
                    user = session.query(models.User).filter(models.User.user_id == stock.user_id).first()
                    user.money = user.money+(int(stock.one_cost)*int(stock.costs))
                    userid = session.query(models.User).filter(models.User.user_id == user_id).first()
                    user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
                    if user:
                        data = json.loads(user.have_cost)
                        for i in data:
                            letter = "".join(re.findall(r"[^\d]", i))
                            num = "".join(re.findall(r"\d", i))
                            index = data.index(i)
                            if str(letter) == str(stock.name):
                                datas = True
                                data[index] = f"{letter}{int(num)+int(am_buy)}"
                                json_data = json.dumps(data, ensure_ascii=False)
                                user.have_cost = json_data
                                session.commit()
                        if datas == False:
                            data.append(f"{stock.name}{am_buy}")
                            json_data = json.dumps(data, ensure_ascii=False)
                            user.have_cost = json_data
                            session.commit()
                    userc.costs = userc.costs - int(am_buy)
                    session.commit()
                    if userc.costs == 0:
                        session.delete(userc)
                    session.commit()
@dp.callback_query(F.data=="dividents")
async def divedents(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.reply("Введите колличество рудлов которое вы хотите выплатить каждому держателю акций:")
    await state.set_state(Form.div)
    user_id = callback_query.from_user.id
    stmt = models.select(models.costs.have_cost, models.costs.invest_name)
    merged_list = []
    with models.SessionLocal() as session:
        comp_name = session.query(models.User).filter(models.User.user_id == user_id).first()
    company_name = comp_name.name
    for letter_list, name in session.execute(stmt):
        letter = json.loads(letter_list)
        for i in letter:
            if str(i).startswith(company_name):
                merged_list.append(name)
    print(merged_list)
        
    @dp.message(F.text, Form.div)
    async def div(message: Message, state: FSMContext):
        if message.text.isnumeric():
            await state.update_data(div=message.text)
            data = await state.get_data()
            costs = int(data.get('div'))
            if int(len(merged_list))*costs < int(comp_name.money):
                await message.reply(f"Заявка на выплату каждому держателю акций по {costs} рудолов оставлена!")
                await bot.send_message(ADMIN, f"Компания с ИНН: {models.get_user_inn(user_id)}\n Хочет выплатить по {data.get('div')} рудолово каждому держателю акций!", reply_markup=markup.but27)
            else:
                await message.reply("У вас недостаточно рудолов для выплаты дивидендов!")
                await message.reply("Введите колличество рудлов которое вы хотите выплатить каждому держателю акций:")
                return
        else:
            await message.reply("Вы ввели некоректное число, попробуйте еще раз!")
            return
        @dp.callback_query(F.data == "agree_div", Form.div)
        async def agree_div(message: Message):
            await callback_query.message.reply("Ваша заявка на выплату дивидендов была принята!", reply_markup=markup.but2)
            us = models.select(models.User.name)
            for i in models.session.execute(us):
                print(i[0])
                if i[0] in merged_list:
                    with models.SessionLocal() as session:
                        comp_name = session.query(models.User).filter(models.User.user_id == user_id).first()
                        comp_name.money = int((comp_name.money) - int(costs))
                        name = session.query(models.User).filter(models.User.name == i[0]).first()
                        name.money += int(costs)
                        session.commit()
        @dp.callback_query(F.data == "disagree_div")
        async def disagree(message: Message):
            await message.reply("Ваши дивиденды не будут выплачены", reply_markup=markup.but2)
            await bot.send_message(ADMIN, "Вы отклонили заявку на размещение!")
@dp.callback_query(F.data == "orders")
async def order(callback_query: types.CallbackQuery):
    markup.but16.inline_keyboard.clear()
    markup.but16.inline_keyboard.append([InlineKeyboardButton(text=f"Акции - цена - колличество - покупка/продажа",callback_data=f"stock")])
    with models.SessionLocal() as session:
        orders = session.query(models.orders).all()
    for i in orders:
        markup.but16.inline_keyboard.append([InlineKeyboardButton(text=f"{i.cost_company_name} - {i.money_one_cost} - {i.num_cost} - {i.st_order}", callback_data=f"ordede_{i.id}")])
    markup.but16.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Ордера", reply_markup=markup.but16)

@dp.callback_query(F.data.startswith("ordede_"))
async def ordede(callback_query: types.CallbackQuery, state: FSMContext):
    order_id = int(callback_query.data.split("_")[1])
    await state.set_state(Form.order_id )
    await state.update_data(order_id=order_id)  
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        ord = session.query(models.orders).filter(models.orders.id == order_id).first()
    if ord:
        if user_id == ord.user_id:
            if ord.st_order == "Покупка":
                sent_message = await callback_query.message.answer(f"Ваш ордер на покупку!\n"
                                            f"Акции компании: {ord.cost_company_name}\n"
                                            f"Колличество: {ord.num_cost}\n"
                                            f"Цена за 1 шт: {ord.money_one_cost}",reply_markup=markup.but21)
            else:
                sent_message = await callback_query.message.answer(f"Ваш ордер на продажу!\n"
                                            f"Акции компании: {ord.cost_company_name}\n"
                                            f"Колличество: {ord.num_cost}\n"
                                            f"Цена за 1 шт: {ord.money_one_cost}",reply_markup=markup.but21)
        else:
            if ord.st_order == "Покупка":
                sent_message = await callback_query.message.answer(f"Ордер на покупку\n"
                                        f"Акции компании: {ord.cost_company_name}\n"
                                        f"Колличество: {ord.num_cost}\n"
                                        f"Цена за 1 шт: {ord.money_one_cost}",reply_markup=markup.but23)
            else:
                sent_message = await callback_query.message.answer(f"Ордер на продажу\n"
                                        f"Акции компании: {ord.cost_company_name}\n"
                                        f"Колличество: {ord.num_cost}\n"
                                        f"Цена за 1 шт: {ord.money_one_cost}",reply_markup=markup.but20)
                
    @dp.callback_query(F.data == "buy_sell_ordede", Form.order_id)
    async def buy_buy_ordede(callback_query: types.CallbackQuery, state: FSMContext):
        datas = False
        user_id = callback_query.from_user.id
        data = await state.get_data()
        order_id = data.get("order_id")
        with models.SessionLocal() as session:
            ord = session.query(models.orders).filter(models.orders.id == order_id).first()
            user_sell = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
            user_buy = session.query(models.User).filter(models.User.user_id == user_id).first()
            cost_buy = session.query(models.costs).filter(models.costs.invest_name == user_buy.name).first()
        if ord.st_order == "Продажа":
            print(1)
            if cost_buy.have_cost:
                if user_buy.money >= ((ord.num_cost)*(ord.money_one_cost)):
                    print(1)
                    lists = json.loads(cost_buy.have_cost)
                    print(type(lists))
                    if not(not lists):
                        print(2)
                        for i in lists:
                            print(i)
                            letter = "".join(re.findall(r"[^\d]", i))
                            num = "".join(re.findall(r"\d", i))
                            index = lists.index(i)
                            if ord.cost_company_name == str(letter):
                                with models.SessionLocal() as session:
                                    orr = session.query(models.orders).filter(models.orders.id == order_id).first()
                                    user_sel = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
                                    user_bu = session.query(models.User).filter(models.User.user_id == user_id).first()
                                    cost_bu = session.query(models.costs).filter(models.costs.invest_name == user_buy.name).first()

                                    lists[index] = f"{letter}{int(num)+int(orr.num_cost)}"
                                    a = json.dumps(lists, ensure_ascii=False)
                                    user_bu.money = (user_bu.money-(int(orr.num_cost)*int(orr.money_one_cost)))
                                    user_sel.money = (user_sel.money+(int(orr.num_cost)*int(orr.money_one_cost)))
                                    cost_bu.have_cost = a
                                    print(1)
                                    print(cost_bu.have_cost)
                                    orr = session.query(models.orders).filter(models.orders.id == order_id).delete()
                                    session.commit()
                                    session.close()
                            else:
                                datas = True
                                print(343)
                            if datas == True:
                                print(2)
                                print(lists)
                                with models.SessionLocal() as session:
                                    orr = session.query(models.orders).filter(models.orders.id == order_id).first()
                                    user_sel = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
                                    user_bu = session.query(models.User).filter(models.User.user_id == user_id).first()
                                    cost_bu = session.query(models.costs).filter(models.costs.invest_name == user_buy.name).first()
                                    lists.append(f"{orr.cost_company_name}{orr.num_cost*orr.money_one_cost}")
                                    cost_bu.have_cost = json.dumps(lists, ensure_ascii=False)
                                    user_bu.money = (user_bu.money-(int(orr.num_cost)*int(orr.money_one_cost)))
                                    user_sel.money = (user_sel.money+(int(orr.num_cost)*int(orr.money_one_cost)))
                                    orr = session.query(models.orders).filter(models.orders.id == order_id).delete()
                                    session.commit()
                                    session.close()
                    else:
                        with models.SessionLocal() as session:
                            orr = session.query(models.orders).filter(models.orders.id == order_id).first()
                            user_sel = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
                            user_bu = session.query(models.User).filter(models.User.user_id == user_id).first()
                            cost_bu = session.query(models.costs).filter(models.costs.invest_name == user_buy.name).first()
                            lists.append(f"{orr.cost_company_name}{orr.num_cost*orr.money_one_cost}")
                            cost_bu.have_cost = json.dumps(lists, ensure_ascii=False)
                            user_bu.money = (user_bu.money-(int(orr.num_cost)*int(orr.money_one_cost)))
                            user_sel.money = (user_sel.money+(int(orr.num_cost)*int(orr.money_one_cost)))
                            orr = session.query(models.orders).filter(models.orders.id == order_id).delete()
                            session.commit()
                            session.close()
                    print(user_sell.money)
                    await callback_query.message.reply("Вы купили ордер!",reply_markup=markup.but4)
                else:
                    return await callback_query.message.reply("У вас недостаточно средств!")







    @dp.callback_query(F.data == "buy_buy_ordede", Form.order_id)
    async def buy_buy_ordede(callback_query: types.CallbackQuery, state: FSMContext):
        lists = False
        user_id = callback_query.from_user.id
        data = await state.get_data()
        order_id = data.get("order_id")
        with models.SessionLocal() as session:
            ord = session.query(models.orders).filter(models.orders.id == order_id).first()
            user_sell = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
            user_buy = session.query(models.User).filter(models.User.user_id == user_id).first()
            cost_sell = session.query(models.costs).filter(models.costs.invest_name == user_sell.name).first()
            cost_buy = session.query(models.costs).filter(models.costs.invest_name == user_buy.name).first()
            if ord.st_order == "Покупка":
                lists = False
                if cost_buy.have_cost:
                    list = json.loads(cost_buy.have_cost)
                    for i in list:
                        letter = "".join(re.findall(r"[^\d]", i))
                        num = "".join(re.findall(r"\d", i))
                        index = list.index(i)
                        if str(letter) == ord.cost_company_name and int(num) >= ord.num_cost:
                            list[index] = f"{letter}{int(num)-int(ord.num_cost)}"
                            cost_buy.have_cost = json.dumps(list, ensure_ascii=False)
                            user_buy.money = int(user_buy.money)+(int(ord.num_cost)*int(ord.money_one_cost))
                            print(123)
                        else:
                            return await callback_query.message.reply("У вас нет такого колличества акций!", reply_markup=markup.but4)
                    print(1)
                    list2 = json.loads(cost_sell.have_cost)
                    print(len(list2))
                    if len(list2) == 0:
                        lists = True
                    for i in list2:
                        print(2321312312)
                        letter = "".join(re.findall(r"[^\d]", i))
                        num = "".join(re.findall(r"\d", i))
                        index = list2.index(i)
                        print(i)
                        print(1)
                        if str(letter) == ord.cost_company_name:
                            print(2)
                            list2[index] = f"{letter}{int(num)+int(ord.num_cost)}"
                            cost_sell.have_cost = json.dumps(list2, ensure_ascii=False)
                            user_sell.money = int(user_sell.money)-(int(ord.num_cost)*int(ord.money_one_cost))
                            ord = session.query(models.orders).filter(models.orders.id == order_id).delete()
                            session.commit()
                            lists = False
                            await callback_query.message.reply("Вы купили ордер!")
                            session.commit()
                        else:
                            lists = True
                            print(3)
                            print(lists)
                    if lists == True:
                        print(4)
                        list2.append(f"{ord.cost_company_name}{int(ord.num_cost)}")
                        cost_sell.have_cost = json.dumps(list2, ensure_ascii=False)
                        ord = session.query(models.orders).filter(models.orders.id == order_id).delete()
                        session.commit()
                        await callback_query.message.delete(chat_id = sent_message.chat.id, message_id = sent_message.message_id)
                        await callback_query.message.reply("Вы купили ордер!")
            session.commit()



        

    @dp.callback_query(F.data == "del_ordede", Form.order_id)
    async def del_ordede(callback_query: types.CallbackQuery, state: FSMContext):
                    data = await state.get_data()
                    order_id = data.get("order_id")
                    with models.SessionLocal() as session:
                        ord = session.query(models.orders).filter(models.orders.id == order_id).first()
                        user = session.query(models.User).filter(models.User.user_id == ord.user_id).first()
                        cost = session.query(models.costs).filter(models.costs.invest_name == user.name).first()
                        print(ord.id)
                        print(" ")
                        if ord.st_order == "Покупка":
                                session.query(models.orders).filter(models.orders.id == ord.id).delete()
                                session.commit()
                                await callback_query.message.delete(chat_id = sent_message.chat.id, message_id = sent_message.message_id)
                                await callback_query.message.reply("Вы удалили ордер!", reply_markup=markup.but4)
                        elif ord.st_order == "Продажа":
                                list = json.loads(cost.have_cost)
                                print(list)
                                for i in list:
                                    letter = "".join(re.findall(r"[^\d]", i))
                                    if letter == ord.cost_company_name:
                                        index = list.index(i)
                                        letter = "".join(re.findall(r"[^\d]", i))
                                        num = "".join(re.findall(r"\d", i))
                                        list[index] = f"{letter}{int(num)+int(ord.num_cost)}"
                                print(list)
                                print(cost.have_cost)
                                cost.have_cost = json.dumps(list, ensure_ascii=False)
                                print(cost.have_cost)
                                session.query(models.orders).filter(models.orders.id == ord.id).delete()
                                session.commit()
                                await callback_query.message.delete(chat_id = sent_message.chat.id, message_id = sent_message.message_id)
                                await callback_query.message.reply("Вы удалили ордер!", reply_markup=markup.but4)
                        if ord.id in timer_events:
                            print(timer_events)
                            task, event = timer_events[order_id]
                            event.set()
                            task.cancel()
                            timer_events.pop(order_id, None)
                            print(timer_events)
            

        

@dp.callback_query(F.data == "back_ord")
async def back_ord(callback_query: types.CallbackQuery):
    markup.but16.inline_keyboard.clear()
    markup.but16.inline_keyboard.append([InlineKeyboardButton(text=f"Акции - цена - колличество - покупка/продажа",callback_data=f"stock")])
    with models.SessionLocal() as session:
        orders = session.query(models.orders).all()
    for i in orders:
        markup.but16.inline_keyboard.append([InlineKeyboardButton(text=f"{i.cost_company_name} - {i.money_one_cost} - {i.num_cost} - {i.st_order}", callback_data=f"ordede_{i.id}")])
    markup.but16.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Ордера", reply_markup=markup.but16)

@dp.callback_query(F.data == "my_orders")
async def order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    markup.but17.inline_keyboard.clear()
    markup.but17.inline_keyboard.append([InlineKeyboardButton(text=f"Акции - цена - колличество - покупка/продажа",callback_data=f"stock")])
    with models.SessionLocal() as session:
        orders = session.query(models.orders).filter(models.orders.user_id == user_id).all()
    for i in orders:
        markup.but17.inline_keyboard.append([InlineKeyboardButton(text=f"{i.cost_company_name} - {i.money_one_cost} - {i.num_cost} - {i.st_order}", callback_data=f"my_ordede_{i.id}")])
    markup.but17.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Мои Ордера", reply_markup=markup.but17)

@dp.callback_query(F.data == "place_orders")
async def order(callback_query: types.CallbackQuery):    
    await callback_query.message.reply("Выберите какой ордер вы хотите разместить!", reply_markup=markup.but18)

@dp.callback_query(F.data == "sell_ord")
async def order(callback_query: types.CallbackQuery):   
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
    markup.but15.inline_keyboard.clear()
    markup.but15.inline_keyboard.append([InlineKeyboardButton(text=f"Акции - Колличество",callback_data=f"stock")])
    if user:
        list = json.loads(user.have_cost)
        for i in list:
            letter = "".join(re.findall(r"[^\d]", i))
            num = "".join(re.findall(r"\d", i))
            if int(num) != 0:
                markup.but15.inline_keyboard.append([InlineKeyboardButton(text=f"{letter} - {num}",callback_data=f"mystock_{list.index(i)}")])
    markup.but15.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Выберите акции которые вы хотите продать!:", reply_markup=markup.but15)

@dp.callback_query(F.data == "buy_ord")
async def order(callback_query: types.CallbackQuery):   
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
        companys = session.query(models.User).filter(models.User.costs_on_birge > 0).all()
    markup.but22.inline_keyboard.clear()
    markup.but22.inline_keyboard.append([InlineKeyboardButton(text=f"Акции компании",callback_data=f"stock")])
    if userid:
        for i in companys:
            markup.but22.inline_keyboard.append([InlineKeyboardButton(text=f"{i.name}",callback_data=f"stockcompan_{i.id}")])
    markup.but22.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])
    await callback_query.message.reply("Выберите акции которые вы хотите купить!:", reply_markup=markup.but22)

@dp.callback_query(F.data.startswith("stockcompan_"))
async def order_buy(callback_query: types.CallbackQuery, state: FSMContext): 
    order_cost = 0
    order_index = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        company = session.query(models.User).filter(models.User.id == order_index).first()
    if userid:
        await callback_query.message.reply("Введите колличество акций которое вы хотите купить!")
        await state.set_state(Form.order_buy_am)
    @dp.message(F.text, Form.order_buy_am)
    async def order_amm(message: Message, state: FSMContext):
        await state.update_data(order_buy_am=message.text)
        data = await state.get_data()
        order_buy_am = data.get("order_buy_am")
        if "".join(re.findall(r"\d", order_buy_am)):
            if company.costs_on_birge > int(order_buy_am):
                await callback_query.message.reply("Введите стоимость одной акции за шт!")      
                await state.set_state(Form.order_buy_cost)
            else:
                await callback_query.message.answer("Слишком много акций! Попробуйте еще раз!")
                return
        else:
            await callback_query.message.answer("Вы ввели неккректное число! Попробуйте еще раз!")
            return
    @dp.message(F.text, Form.order_buy_cost)
    async def order_costt(message: Message, state: FSMContext):
        await state.update_data(order_buy_cost=message.text)
        data = await state.get_data()
        order_cost = data.get("order_buy_cost")
        order_buy_am = data.get("order_buy_am")
        if "".join(re.findall(r"\d", order_cost)):
            if int(order_cost) * int(order_buy_am) <= userid.money:
                sent_message = await message.reply("Вы хотите разместить ордер на покупку!\n"
                                                        f"Акции компании:  {company.name}\n"
                                                        f"Колличество:  {order_buy_am}\n"
                                                        f"Цена за 1 шт:  {order_cost}",reply_markup=markup.but19)
            elif int(order_cost) * int(order_buy_am) > userid.money:
                await callback_query.message.answer("У вас недостаточно средств! Попробуйте еще раз!")
                return
        else:
            await callback_query.message.answer("Вы ввели неккректное число! Попробуйте еще раз!")
            return
    @dp.callback_query(F.data == "place_ord")
    async def place_buy_ord(callback_query: types.CallbackQuery):
            data = await state.get_data()
            order_cost = data.get("order_buy_cost")
            order_buy_am = data.get("order_buy_am")
            with models.SessionLocal() as session:
                                            user_id = callback_query.from_user.id
                                            user = session.query(models.User).filter(models.User.user_id == user_id).first()
                                            new_ord = models.orders(user_id=user_id, invest_name = user.name, cost_company_name=company.name, money_one_cost=int(order_cost), num_cost=int(order_buy_am), st_order="Покупка")
                                            session.add(new_ord)
                                            session.commit()
                                            order_id = new_ord.id
            event = asyncio.Event()
            task = asyncio.create_task(delete_message_after_delay(event,order_index,user_id,int(order_buy_am), order_id))
            timer_events[order_id] = (task, event)
            await callback_query.message.answer("Вы разместили ордер успешно!", reply_markup=markup.but4)




@dp.callback_query(F.data.startswith("mystock_"))
async def order(callback_query: types.CallbackQuery, state: FSMContext): 
    order_index = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        userid = session.query(models.User).filter(models.User.user_id == user_id).first()
        user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
    if user:
        list = json.loads(user.have_cost)
        letter = "".join(re.findall(r"[^\d]", list[order_index]))
        num = "".join(re.findall(r"\d", list[order_index]))
    if letter and num:
        await callback_query.message.reply("Введите колличество акций которое вы хотите разместить!")
        await state.set_state(Form.order_am)
    @dp.message(F.text, Form.order_am)
    async def order_am(message: Message, state: FSMContext):
        await state.update_data(order_am=message.text)
        data = await state.get_data()
        am_buy = data.get("order_am")
        if "".join(re.findall(r"\d", am_buy)):
            if int(am_buy) <= int(num):
                await message.reply("Введите стоимость одной акции, которые вы выставите!")
                await state.set_state(Form.order_cos)
            elif int(am_buy) > int(num):
                await message.reply("Вы хотите продать больше акций чем вы имеете! Попробуйте еще раз!")
                return
        else:
            await message.reply("Вы ввели неккректное число! Попробуйте еще раз!")
            return
    @dp.message(F.text, Form.order_cos)
    async def order_cos(message: Message, state: FSMContext):
        await state.update_data(order_cos=message.text)
        data = await state.get_data()
        am_buy = data.get("order_am")
        order_cos = data.get("order_cos")
        if "".join(re.findall(r"\d", order_cos)):
            sent_message = await message.reply("Вы хотите разместить ордер на продажу!\n"
                                                    f"Акции компании:  {letter}\n"
                                                    f"Колличество:  {am_buy}\n"
                                                    f"Цена за 1 шт:  {order_cos}",reply_markup=markup.but19)
        else:
            await message.reply("Вы ввели неккректное число! Попробуйте еще раз!")
            return
    @dp.callback_query(F.data == "place_ord")
    async def place_ord(callback_query: types.CallbackQuery):
        data = await state.get_data()
        am_buy = data.get("order_am")
        order_cos = data.get("order_cos")
        event = asyncio.Event()
        with models.SessionLocal() as session:
                    user_id = callback_query.from_user.id
                    user = models.User()
                    userid = session.query(models.User).filter(models.User.user_id == user_id).first()
                    user = session.query(models.costs).filter(models.costs.invest_name == userid.name).first()
                    cost = session.query(models.costs).filter(models.costs.invest_name == user.invest_name).first()
                    list = json.loads(cost.have_cost)
                    letter = "".join(re.findall(r"[^\d]", list[order_index]))
                    num = "".join(re.findall(r"\d", list[order_index]))
                    list[order_index] = f"{letter}{int(num)-int(am_buy)}"
                    new_ord = models.orders(user_id=user_id, invest_name = user.invest_name, cost_company_name=str(letter),money_one_cost=int(order_cos), num_cost=int(am_buy), st_order="Продажа")
                    session.add(new_ord)
                    user.have_cost = json.dumps(list, ensure_ascii=False)
                    session.commit()
                    order_id = new_ord.id
        task = asyncio.create_task(delete_message_after_delay(event,order_index,user_id,int(am_buy), order_id))
        timer_events[order_id] = (task, event)
        await callback_query.message.answer("Вы разместили ордер успешно!", reply_markup=markup.but4)

    
    

    

@dp.callback_query(F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    with models.SessionLocal() as session:
        user = session.query(models.User).filter(models.User.user_id == user_id).first()
    if user.status == "Инвестор":
        await callback_query.message.reply("Инвестор",reply_markup=markup.but4)
    else:
        await callback_query.message.reply("Компания",reply_markup=markup.but2)





    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    models.init_db()
    import asyncio
    asyncio.run(main())