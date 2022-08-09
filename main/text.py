class AllText:
    def __init__(self, first_name, user_id=None, last_name=None, phone_number=None, username=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username

    def start(self, lang='uz'):
        text = ''
        if lang == 'uz':
            text = f'Assalom alaykum {self.first_name} !\n' \
                   f'Botimizga xush kelibsiz!\n' \
                   f'Botdan foydalanishni boshlash uchun quyidagi tugmani bosing:'
        elif lang == 'ru':
            text = f'Привет {self.first_name}\n' \
                   f'Добро пожаловать в наш бот\n' \
                   f'Нажмите на кнопку ниже, чтобы начать использовать бота:'
        return text

    def step2(self, lang='uz'):
        text = ''
        if lang == 'uz':
            text = f'Bizda siz uchun ikkita bo`lim mavjud\n' \
                   f'Bot haqida qisqacha malumotni /help\n' \
                   f'buyrugi orqali bilishingiz mumkin.'
        elif lang == 'ru':
            text = f'У нас есть две категории\n' \
                   f'О нашем боте /help\n'
        return text
