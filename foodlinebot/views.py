from django.shortcuts import render

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from .scraper import IFoodie

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature) # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        food = IFoodie()
        food.init()
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print(event.message.text)
                food.update()
                rec = event.message.text.split(" ")
                mes = rec[0]
                food.get_close(mes)
                content = ""
                cur = food.link.tail
                link = []
                while cur != None:
                    link.append(cur.ind)
                    #print(cur.data, food.Data[cur.ind][4] * food.Data[cur.ind][5])
                    cur = cur.next
                if food.len == 8:
                    if(len(rec) > 1):
                        number = int(rec[1])
                        content += food.Data[link[7]][0] + "\n" + "當前號碼： " + str(food.Data[link[7]][3]) + "\n" + "預計等待時間： " + str((number - food.Data[link[7]][3]) * food.Data[link[7]][5]) + " 分鐘\n" + food.Data[link[7]][2] + "\nhttps://spot.line.me/search?q=" + food.Data[link[7]][0].replace(" ", "+") + "\n\n"
                        print(number, food.Data[link[7]][3])
                    if(len(rec) == 1):
                        content += food.Data[link[7]][0] + "\n" + "當前號碼： " + str(food.Data[link[7]][3]) + "\n" + "預計等待時間： " + str( food.Data[link[7]][3] * food.Data[link[7]][5]) + " 分鐘\n" + food.Data[link[7]][2] + "\nhttps://spot.line.me/search?q=" + food.Data[link[7]][0].replace(" ", "+") + "\n\n"
                    content += "以下為推薦的店家\n\n"
                    for i in range(6, -1, -1):
                        content += food.Data[link[i]][0] + "\n" + "評分： " + food.Data[link[i]][1] + "\n" + "目前候位人數： " + str(food.Data[link[i]][4]) + "人\n" + "預計等待時間： " + str(food.Data[link[i]][4] * food.Data[link[i]][5]) + " 分鐘\n" + food.Data[link[i]][2] + "\nhttps://spot.line.me/search?q=" + food.Data[link[i]][0].replace(" ", "+") + "\n"
                        if i != 0:
                            content += "\n"
                else:
                    content += "查無此店\n\n以下是您的搜尋結果\n\n"
                    for i in range(len(link) - 1, -1, -1):
                        content += food.Data[link[i]][0] + "\n" + "評分： " + food.Data[link[i]][1] + "\n" + "目前候位人數： " + str(food.Data[link[i]][4]) + " 人\n" + "預計等待時間： " + str(food.Data[link[i]][4] * food.Data[link[i]][5]) + " 分鐘\n" + food.Data[link[i]][2] + "\nhttps://spot.line.me/search?q=" + food.Data[link[i]][0].replace(" ", "+") + "\n"
                        if i != 0:
                            content += "\n"
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=content)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
