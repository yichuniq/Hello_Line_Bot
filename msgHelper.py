
from linebot.models import TextSendMessage
from linebot.models.emojis import Emojis

# current version of line-bot-sdk-python can't send emoji via TextSendMessage
class newTextSendMessage(TextSendMessage):
    def __init__(self, text=None, emojis=None, quick_reply=None, **kwargs):

        super(newTextSendMessage, self).__init__(text=text, quick_reply=quick_reply, **kwargs)
        self.type = 'text'
        self.emojis = emojis


def isHi(text):
    Hi = ['hi', 'hello', 'hey', '嗨', '嗨嗨', '哈囉','安安']
    if text.replace(' ', '').lower() in Hi:
        return True
    return False


class IntroHelper:
    def __init__(self):
        self.brief1 = "\n".join((
            "Carl ，新竹人，目前就讀於清大資工系四年級",
            "紮實的課程中，培養了他解決問題的能力"
        ))
        
        self.brief2 = "\n".join((
            "對軟體開發充滿興趣的他，想透過實習，體驗軟體專案完整的開發流程，讓自己的開發能力更進一步。",
            f"而LINE TECH FRESH無疑是很棒的機會！ {chr(0x1000A4)}"
        ))

        self.brief3 = "更多資訊如Carl在\nData Science, Web Dev相關的專案，請輸入 More Info\n，或點擊以下按鈕來了解更多！"

        self.ds = "\n".join((
            "Varios topics including web crawler, prediction, optimization functions, compressing models.\n",
            "Learned: The key concept behind these algorithms and using them to solve real-world problems."
        ))

        self.mda = "\n".join((
            "Implemented impactful algortithms such as PageRank, Locality-Sensitive-Hashing via Pyspark.\n",
            "Learned: Manipulating large data in Map/Reduce concepts."
        ))

        self.wm = "\n".join((
            "A webpage for users to know the weather and leave their comments and mood. Currently held on AWS EBS.\n",
            "Learned: Useful technology stacks to build a modern web."
        ))

        self.dj = "\n".join((
            "A OOP project built with C++ and Allegro libraries, trying to remake the beloved game Doodle Jump.\n",
            "Strenghthen the knowledge of OOP design while having fun."
        ))

        self.help = "\n".join((
            "輸入：",
            "- Hi/Hello/嗨 :\n和Bot打招呼",
            "- Brief Intro :\n簡單介紹Carl",
            "- More Info :\n快速選單，了解Carl做的相關專案、個人特質等等",
            "- Bye:\n和Bot道別"
        ))

        self.bye = "\n".join((
            f"感謝你的時間！{chr(0x10005E)}",
            "想跟Carl本人聊聊，可以約他面試！"
        ))

        self.traits_resp = "\n".join((
            "Carl is a responsible person that took his work seriously.",
            "He not only finishes the tasks on time but also try hard to improve the quality.",
            "This is one of the reasons that he could get good grades in classes."
        ))

        self.traits_open = "\n".join((
            "Carl is open to learn and experience new things.",
            "For example, Besides studying several subfields in CS, he also took courses like Economics, Psychology, .etc,"
            " which enables him to think in different aspects."
        ))

        self.poke = "\n".join((
            "Need exp, gifts, and Raid inviatations!",
            "ID: 7232 5607 4773"
        ))

