 
 
'''
非Django相关部分
需要在本地直接运行

'''


from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message, create_reply
from wechatpy.replies import BaseReply
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth
from wechatpy.replies import TextReply 

WECHAT_TOKEN = 'dhs789520'
AppID = 'wxd638d1da36c53aac'
AppSecret = '90969c6c2ec38a521b9a3b9637fe3d91'
 

from wechatpy import WeChatClient
client = WeChatClient(AppID,AppSecret)


#获取用户列表，需要认证
def get_followers():
    followers = client.user.get_followers()
    print(followers)


#自定义菜单，需要认证
def menu():
    '''
    以下为自定义菜单接口
    '''
    client.menu.update({
        "button":[
            {
                "type":"click",
                "name":"今日歌曲",
                "key":"V1001_TODAY_MUSIC"
            },
            {
                "type":"click",
                "name":"歌手简介",
                "key":"V1001_TODAY_SINGER"
            },
            {
                "name":"咬文嚼字",
                "sub_button":[
                    {
                        "type":"view",
                        "name":"质控",
                        "url":"http://linux.zicp.vip/icu/qc/"
                    },
                    {
                        "type":"view",
                        "name":"知识广场",
                        "url":"http://linux.zicp.vip/"
                    },
                    {
                        "type":"click",
                        "name":"赞一下我们",
                        "key":"V1001_GOOD"
                    }
                ]
            }
        ]
    })

if __name__ == "__main__":
    get_followers()
