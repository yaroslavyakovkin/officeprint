from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kbsett = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                            text='Цвет',
                            callback_data=f"print:color:clr"
            ),
            InlineKeyboardButton(
                            text='Черно-белое',
                            callback_data=f"print:color:bw"
            ) 
        ],
        [
            InlineKeyboardButton(
                            text='Убрать копию',
                            callback_data=f"print:copy:remove"
            ),
            InlineKeyboardButton(
                            text='Добавить копию',
                            callback_data=f"print:copy:add"
            )
        ],
        [
            InlineKeyboardButton(
                            text='Двусторонняя - переплет сверху',
                            callback_data=f"print:duplex:twoup"
            )
        ],
        [
            InlineKeyboardButton(
                            text='Односторонняя',
                            callback_data=f"print:duplex:oneside"
            )
        ],
        [
            InlineKeyboardButton(
                            text='Двусторонняя - переплет сбоку',
                            callback_data=f"print:duplex:twonear"
            )
        ],
        [
            InlineKeyboardButton(
                            text='В печать',
                            callback_data='print:print'
            )
        ],
        [
            InlineKeyboardButton(
                            text='Назад',
                            callback_data='print:back'
            )
        ]
    ]
)

kbmain = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                            text='Настройки',
                            callback_data=f"print:settings"
            )
        ],
        [
            InlineKeyboardButton(
                            text='В печать',
                            callback_data='print:print'
            )
        ],
        [
            InlineKeyboardButton(
                            text='Отменить',
                            callback_data='print:cancel'
            )
        ]
    ]
)