
from create_bot_and_conn import dp
from aiogram import executor
from screenshot import on_startup
from handlers import commands, find_another_report, language, no_filter, screen_with_filters, search_and_screen, set_selectors, add_favorite

commands.register_handlers_commands(dp)
language.register_handlers_language(dp)
search_and_screen.register_handlers_search_and_screen(dp)
add_favorite.register_handlers_search_and_screen(dp)
no_filter.register_handlers_no_filters(dp)
set_selectors.register_handlers_set_selectors(dp)
screen_with_filters.register_handlers_screen_with_filters(dp)
find_another_report.register_handlers_find_another_report(dp)

executor.start_polling(dp, on_startup=on_startup)
