from django import template
from django.utils.safestring import mark_safe #安全字符

#register的名字是固定的,不可改变
register = template.Library()   


# 过滤器只能传两个参数，可以写在控制语句中
#@register.filter
#def multi_xxxx(x,y):
    #return x*y
 

# 自定义的标签可以传多个参数，不能写在控制语句中
#@register.simple_tag
#def my_input(id,arg):
#　　 result = "<input type='text' id='%s' class='%s' />" %(id,arg,)
#　　 return mark_safe(result)


'''
django 关于英汉混编的标题按指定长度显示的方法
在用django使用模板语法加过滤器渲染标题时，经常会出现想要按指定的文字长度显示标题的部分文字，在超出长度后用"..."来表示未完全显示的这样一个效果。

这时我们一般会用到三个过滤器：

truncatechars:按字符数省略，包括后面的"..."三个点。（中文和英文都算一个字符）

truncatewords:按字的个数省略，不包括后面的"..."三个点。(但只能用于英文)

slice:取N个字符，可以用于中文。（中文和英文都算一个字符，与truncatechars差不多，只是没有"..."三个点）

那么这三个过滤器都没有办法来处理英文和中文混排的标题长度不一致的问题。在网上也看到些方法，但我觉得有些难理解。
我想利用utf-8编码格式的中文占三个字节这个属性，来区分汉字和其他字符，并通过它来获得标题所占的字节宽度。
然后截取想要显示的按汉字宽度来设定的题目所需宽度的标题文字。达到格式化标题英文汉字混排的统一长度省略的效果。

'''



#判断字符串是否包含中文，包含中文返回True
def is_chinese(check_char):
    if u'\u4e00' <= check_char <= u'\u9fff':
        return True

#计算字符串s的html实际长度
def get_real_len(s):
    '''
    计算字符串实际的长度，
    汉字显示的长度与英文的不同
    一个汉字等于2个英文的长度
    '''
    n = 0 
    for char in s:
        if is_chinese(char):
            n+=2
        else:
            n+=1
    #print('real_len_is',n)
    return n


# 过滤器 
@register.filter
def truncate_by_len(s, require_size):
    s_size = get_real_len(s)
    #如果字符宽度已经满足要求，直接返回字符
    if s_size <= require_size:
        return mark_safe(s)

    #从index 处开始截取字符...
    #截取字符后需要增加三个. 代表省略号
    require_size -= 4
    index = 0

    while(get_real_len(s[:index]) < require_size):
        #print(index)
        index += 1
    s = mark_safe((s[:index]+'...'))
    return s


if __name__ == '__main__':
    s = 'a中华人民共和国waaaa水'
    r = truncate_by_len(s,10)
    print(r)
