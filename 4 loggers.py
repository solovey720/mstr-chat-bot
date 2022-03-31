import logging

# задаем единый формат сообщениям
formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')

#создаем логгеры под 4 блока, в кавычках название логгера, которое будет отражаться в лог-файле
scr_logger = logging.getLogger('screenshots')
base_logger = logging.getLogger('database')
connect_logger = logging.getLogger('mstr_connect')
tg_logger = logging.getLogger('tg bot')

#сюда можно впихнуть общие настройки, пока уровень логирования и формат сообщений
def log_settings(logger, handler):
    logger.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

scr_handler = logging.FileHandler('screenshots.log') #создаем лог-файл
scr_logger.addHandler(scr_handler) #соотносим лог-файл с логгером
log_settings(scr_logger, scr_handler) #задаем настройки

base_handler = logging.FileHandler('database.log')
base_logger.addHandler(base_handler)
log_settings(base_logger, base_handler) 

connect_handler = logging.FileHandler('mstr_connect.log')
connect_logger.addHandler(connect_handler)
log_settings(connect_logger, connect_handler) 

tg_handler = logging.FileHandler('tg bot.log')
tg_logger.addHandler(tg_handler)
log_settings(tg_logger, tg_handler) 

#раскидала сообщения по разным логгерам для примера
scr_logger.debug('debug message')
base_logger.info('info message')
connect_logger.warning('warn message')
tg_logger.error('error message')


#тут маленький пример, как можно вынести текст ошибки
vals = [1, 2]
try:
    print(vals[4])
except Exception:
    base_logger.error('error message', exc_info=True)
