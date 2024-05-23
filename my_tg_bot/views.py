from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.vendors.telegram import Bot

from settings import TG_CHAT, TG_CHAT_BOT

@main_auth(on_cookies=True)
def main_view(request):
    but = request.bitrix_user_token

    if request.method == "POST":
        text = request.POST.get('text')
        bot = Bot(token=TG_CHAT_BOT)
        # Hello send image: https://i.imgur.com/tQ8Ryj1.png
        if "send image:" in text:
            text_before = text.split("send image:", 1)[0].strip()
            text_after = text.split("send image:", 1)[1].strip()
            if len(text_before) > 0:
                try:
                    bot.send_message(text=text_before, chat_id=TG_CHAT)
                except Exception as e:
                    print(e)
            if len(text_after) > 0:
                try:
                    bot.send_photo(photo=text_after, chat_id=TG_CHAT)
                except Exception as e:
                    bot.send_message(text=e, chat_id=TG_CHAT)

        else:
            bot.send_message(text=text, chat_id=TG_CHAT)

    return render(request, 'main_tg.html')
