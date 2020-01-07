# coding:utf-8
import requests
import time
import re
import random
import hashlib
import json

# 使用自然语言处理模块来给英文段落分句
from nltk import tokenize
# import nltk
# nltk.download('punkt')
url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

appinfo = []
# appinfo.append(['20190308000275209','lim13WI3Ox5EJtzYZ1Gk']) #dhs789520
appinfo.append(['20190310000275705', 'hARGguTX0VqYYOyQtUbN'])  # dhs789522
# appinfo.append(['20190310000275711','P5NYYk0RsCIpPFezUcIo']) #dhs789523 超额不可用
appinfo.append(['20190310000275713', 'JwpVen_lkBpi5QjRp7yA'])  # dhs789525


# 判断字符串是否包含中文，包含中文返回True
def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True


# 使用百度翻译API进行翻译查询
def BDtranslate(q, fromLang, toLang, result):
    appid, secretKey = random.choice(appinfo)
    # 利用随机数生成sign
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = sign.encode('utf8')
    m1 = hashlib.md5()
    m1.update(sign)
    sign = m1.hexdigest()

    data = {
        'appid': appid,
        'q': q,
        'from': fromLang,
        'to': toLang,
        'salt': str(salt),
        'sign': sign
    }

    try:
        r = requests.post(url, data, timeout=10).text
        result_j = json.loads(r)
        result.append([q, ''])
        for r in result_j['trans_result']:
            result[-1][1] += r['dst'] + '\n'
        return None
    except Exception as error:
        return repr(error)


# 将英文段落拆分成句子的函数，但是我们在这里没有使用，替代方案是使用nltk
def split_into_sentences(text):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = r"(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|me|edu)"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)

    digits = "([0-9])"
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "e.g." in text:
        text = text.replace("e.g.", "e<prd>g<prd>")
    if "i.e." in text:
        text = text.replace("i.e.", "i<prd>e<prd>")
    text = re.sub(r"\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(
        alphabets +
        "[.]" +
        alphabets +
        "[.]" +
        alphabets +
        "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text)
    text = re.sub(
        alphabets +
        "[.]" +
        alphabets +
        "[.]",
        "\\1<prd>\\2<prd>",
        text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    if "..." in text:
        text = text.replace("...", "<prd><prd><prd>")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


# 逐句翻译，输入段落
def sbs(paragraph):
    result = []

    # 判断是中译英 还是英译中
    chinese = check_contain_chinese(paragraph)
    if chinese:
        fromLang = 'zh'
        toLang = 'en'

        # 中文化段为句
        sentences = re.split("([。\n！!；])", paragraph)
        sentences.append("")
        sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    else:
        fromLang = 'en'
        toLang = 'zh'

        # 英文化段为句
        sentences = tokenize.sent_tokenize(paragraph)
        #sentences =split_into_sentences(paragraph)

    # 对每一句进行翻译
    for sentence in sentences:
        # 去除空白行
        sentence = re.sub(r"^\s+", "", sentence)
        sentence = re.sub(r"\s+$", "", sentence)
        sentence = re.sub("^[ 　]+", "", sentence)
        sentence = re.sub("[ 　]+$", "", sentence)
        sentence = re.sub("\n+", "", sentence)
        if len(sentence) == 0:
            continue

        # 调用翻译器进行翻译
        error = BDtranslate(sentence, fromLang, toLang, result)
        if error:
            print('逐句翻译出错！%s' % error)

    # 返回翻译结果
    return result


# 整段翻译，输入段落
def para(paragraph):
    result = []

    # 判断是中译英 还是英译中
    chinese = check_contain_chinese(paragraph)
    if chinese:
        fromLang = 'zh'
        toLang = 'en'
    else:
        fromLang = 'en'
        toLang = 'zh'

    # 如果整段没有超过百度翻译字数限制,整段进行翻译
    if len(paragraph) < 4000:
        # 对整段再进行一次翻译
        error = BDtranslate(paragraph, fromLang, toLang, result)
        if error:
            print('整段翻译出错！%s' % error)
    else:
        result.append(['全部原文过长！', '暂不提供超过4000字的原文翻译'])

    # 返回翻译结果
    return result[0]


if __name__ == '__main__':

    # 判断文件编码所用
    import chardet

    filename = input('请输入要翻译的文本文件:\n')

    # 文件
    #q = open(filename,'r',encoding='utf-8').read()
    paragraph = open(filename, 'rb').read()
    # 判断编码，并解编码
    enc = chardet.detect(paragraph)['encoding']
    paragraph = paragraph.decode(enc)

    fd = open("翻译文件" + str(time.time()) + ".txt", "w", encoding='utf-8')

    # 调用 逐行翻译函数 sbs
    result = sbs(paragraph)
    # 调用 整段翻译函数 para
    result2 = para(paragraph)
    print("\n\n\n")

    for r in result:
        print("原文:%s\n译文:%s\n\n" % (r[0], r[1]))
        fd.write("原文:%s\n译文:%s\n\n" % (r[0], r[1]))

    fd.write("\n\n\n==============================\n\n\n")

    for r in result2:
        print("全部原文:%s\n全部译文:%s\n\n" % (r[0], r[1]))
        fd.write("全部原文:%s\n全部译文:%s\n\n" % (r[0], r[1]))

    fd.close()

    input("全部翻译完毕，回车后查看翻译结果文档")
