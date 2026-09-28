from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки для меню компании
but2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Профиль Компании", callback_data="profile_company")],
        [InlineKeyboardButton(text="Пополнить счет", callback_data="payment_company")],
        [InlineKeyboardButton(text="Разместить Акции", callback_data="place_shares")],
        [InlineKeyboardButton(text="Разместить Криптовалюту", callback_data="place_crypto")],
        [InlineKeyboardButton(text="Мои Акции", callback_data="my_shares_company")],
        [InlineKeyboardButton(text="Выплата дивидендов", callback_data="dividents")],
        [InlineKeyboardButton(text="Биржа", callback_data="exchange_company")],
    ]
)

# Кнопки для выбора роли
but3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Инвестор", callback_data="role_investor")],
        [InlineKeyboardButton(text="Компания", callback_data="role_company")],
    ]
)

but7 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Дальше✅", callback_data="next")],
        [InlineKeyboardButton(text="Еще раз❌", callback_data="again")],
    ]
)

but8 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад!", callback_data="cancel")],
    ]
)

but9 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернутся!", callback_data="cancel")],
    ]
)
but10 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернутся!", callback_data="cancel")],
    ]
)

but11 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agree")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree")]
    ]
)

but12 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agreee_place")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree_place")]
    ]
)

but27 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agree_div")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree_div")]
    ]
)

but28 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agreee_cr")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree_cr")]
    ]
)

but29 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agree_reg_cmp")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree_reg_cmp")]
    ]
)
but30 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить!", callback_data="agree_reg_inv")],
        [InlineKeyboardButton(text="Отказать!", callback_data="disagree_reg_inv")]
    ]
)

but13 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Имя - стоимость акции - колличество акций", callback_data="agree_place")]])

but15 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Имя - акции", callback_data="my_costs")]])

but16 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Акции - цена - колличество - покупка/продажа", callback_data="order")]])

but17 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Акции - цена - колличество - покупка/продажа", callback_data="my_order")]])

but14 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить!", callback_data="buy_stock")],
                                              [InlineKeyboardButton(text="Вернуться!", callback_data="back")],
                                              [InlineKeyboardButton(text="Назад", callback_data="cancel")]])

but18 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="На Продажу!", callback_data="sell_ord")],
                                              [InlineKeyboardButton(text="На Покупку!", callback_data="buy_ord")],
                                              [InlineKeyboardButton(text="Назад!",callback_data="cancel")]])

but19 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Разместить!",callback_data="place_ord")]])

but20 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить!", callback_data="buy_sell_ordede")],
                                              [InlineKeyboardButton(text="Назад!", callback_data="back_ord")]])

but23 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить!", callback_data="buy_buy_ordede")],
                                              [InlineKeyboardButton(text="Назад!", callback_data="back_ord")]])

but21 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Удалить!", callback_data="del_ordede")],
                                              [InlineKeyboardButton(text="Назад!", callback_data="back_ord")]])

but22 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Имя - акции", callback_data="my_costs")]])

but6 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать!", callback_data="role_start")]
        ]
)

but24 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Акции", callback_data="costs")],
                                              [InlineKeyboardButton(text="Криптовалюта", callback_data="crypto")]])

but25 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Название - Стоимость - Колличество", callback_data="fd")]])

but26 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить!", callback_data="buy_crypto")],
                                              [InlineKeyboardButton(text="Вернуться!", callback_data="back")],
                                              [InlineKeyboardButton(text="Назад", callback_data="cancel")]])

# Кнопки для меню инвестора
but4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Профиль Инвестора", callback_data="profile_investor")],
        [InlineKeyboardButton(text="Пополнить счет", callback_data="payment_company")],
        [InlineKeyboardButton(text="Разместить Ордер", callback_data="place_orders")],
        [InlineKeyboardButton(text="Мои Ордера", callback_data="my_orders")],
        [InlineKeyboardButton(text="Ордера", callback_data="orders")],
        [InlineKeyboardButton(text="Мои Акции", callback_data="my_shares_investor")],
        [InlineKeyboardButton(text="Моя Криптовалюта", callback_data="my_crypto_inv")],
        [InlineKeyboardButton(text="Биржа", callback_data="exchange_company")],
    ]
)
