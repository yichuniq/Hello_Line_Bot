import os
import sys
import time
from datetime import datetime


from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationSendMessage,
    TemplateSendMessage, ButtonsTemplate, 
    CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn,
    MessageAction, PostbackAction, URIAction,
    PostbackEvent, QuickReply, QuickReplyButton,
)

from linebot.models.emojis import Emojis

from msgHelper import (
    isHi, IntroHelper,
    newTextSendMessage
)



app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

Intro = IntroHelper()
quick_reply_tepmplate = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="相關專案", text="Projects")
        ),
        QuickReplyButton(
            action=MessageAction(label="特質", text="Traits")
        ),
        QuickReplyButton(
            action=MessageAction(label="其他", text="Others")
        ),
        QuickReplyButton(
            action=PostbackAction(label="取消", data="cancel")
        ),
    ]
)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if isHi(text):
        line_bot_api.reply_message(
            event.reply_token,
            newTextSendMessage(
                text="嗨嗨! $", 
                emojis=[
                    Emojis(
                        index=4, 
                        length=6,
                        product_id='5ac1de17040ab15980c9b438', 
                        emoji_id='193'
                    )
                ]
            )
        )
    elif text == 'Brief Intro':
        try:
            line_bot_api.push_message(
                to=event.source.user_id,
                messages=TextSendMessage(text=Intro.brief1))

            time.sleep(3.5) 

            line_bot_api.push_message(
                to=event.source.user_id,
                messages=TextSendMessage(text=Intro.brief2))

            time.sleep(5) 

            line_bot_api.push_message(
                to=event.source.user_id,
                messages=TextSendMessage(
                    text=Intro.brief3,
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="了解更多", text="More Info")
                            )
                        ]
                    )
                )
            )

        except LineBotApiError as e:
            raise e

    elif text == 'More Info':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
            text=f'選擇想了解的項目 {chr(0x10005E)}',quick_reply=quick_reply_tepmplate))
    elif text == 'Projects':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                text='Python. Spring 2020', title='Data Science Courseworks', actions=[
                    PostbackAction(label='Intro', data='Intro-DS'),
                    URIAction(label='Go to repository', uri='https://github.com/yichuniq/Data-Science')
                ]),
            CarouselColumn(
                text='React/Node.js/AWS. Spring 2020', title='WeatherMood', actions=[
                    PostbackAction(label='Intro', data='Intro-WeatherMood'),
                    URIAction(label='Go to page', uri='http://as5-db-dev.us-east-1.elasticbeanstalk.com')
                ]),
            CarouselColumn(
                text='PySpark. Fall 2021', title='Massive Data Analysis', actions=[
                    PostbackAction(label='Intro', data='Intro-MDA'),
                    URIAction(label='Go to repository', uri='https://github.com/yichuniq/Massive-Data-Analysis')
                ]),
            CarouselColumn(
                text='Game written in C++. Spring 2018', title='Doodle Jump', actions=[
                    PostbackAction(label='Intro', data='Intro-Doodle'),
                    URIAction(label='Go to demo video', uri='https://www.youtube.com/watch?v=kHv_C8zjW5c')
                ]),
            CarouselColumn(text='Computer Graphics, Embedded systems, .etc', title='See more on GitHub', actions=[
                URIAction(label='@yichuniq', uri='https://github.com/yichuniq'),
                PostbackAction(label='上一步', data='More-Info')
            ])
        ])
        template_message = TemplateSendMessage(alt_text='Projs', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

        line_bot_api.push_message(
            to=event.source.user_id,
            messages=TextSendMessage(
                text="滑至最右按'上一步'或按以下回到選單",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(
                            action=PostbackAction(label='選單', data='More-Info'))]
                )
            )
        )

    elif text == 'Traits':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/NZYTsTK.jpg',
                text='點擊分項了解更多', title='Carl的個人特質', actions=[
                PostbackAction(label='Responsibe', data='Triats-Resp'),
                PostbackAction(label='Open-minded', data='Triats-Open'),
                PostbackAction(label='上一步', data='More-Info')
            ])
        ])
        template_message = TemplateSendMessage(alt_text='Traits', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Others':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='點擊分項展開內容', title='其他Carl剛好想分享的', actions=[
                PostbackAction(label='推一首歌', data='Music'),
                PostbackAction(label='開頭的照面在哪拍的', data='Location'),
                PostbackAction(label='寶可夢', data='Poke'),
            ])
        ])
        template_message = TemplateSendMessage(alt_text='Traits', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)


        line_bot_api.push_message(
            to=event.source.user_id,
            messages=TextSendMessage(
                text="回到選單或輸入Bye結束聊天",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(
                            action=PostbackAction(label='選單', data='More-Info'))]
                )
            )
        )
    elif text == 'Help':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=Intro.help))
    elif text == 'Bye':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=Intro.bye))
    else:
        reply = f"抱歉目前無法回應：({text})，可以輸入 Help 取得使用細節！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'Intro-DS':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.ds))
    elif event.postback.data == 'Intro-MDA':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.mda))
    elif event.postback.data == 'Intro-WeatherMood':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.wm))
    elif event.postback.data == 'Intro-Doodle':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.dj))
    elif event.postback.data == 'Triats-Resp':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.traits_resp))
    elif event.postback.data == 'Triats-Open':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.traits_open))
    elif event.postback.data == 'More-Info':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
            text='選擇想了解的項目',quick_reply=quick_reply_tepmplate))
    elif event.postback.data == 'Music':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="Chvrches-Forever"))
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://i.imgur.com/7w0cpRn.jpg',action=
                                URIAction(
                                    label='Listen!',
                                    uri='https://www.youtube.com/watch?v=CRDruiv08_4')),
        ])
        template_message = TemplateSendMessage(alt_text='Image-music', template=image_carousel_template)
        line_bot_api.push_message(event.source.user_id, template_message)

        time.sleep(1) 

        line_bot_api.push_message(
            event.source.user_id, TextSendMessage(text="A song that get you out of depression."))
    elif event.postback.data == 'Location':
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title='清華大學 梅園', address='新竹市東區光復路二段101號',
                latitude=24.7928700, longitude=120.9908193))
    elif event.postback.data == 'Poke':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=Intro.poke))
    



if __name__ == "__main__":
    app.run()