# -*- encoding=utf8 -*-
__author__ = "admin"

from os import name, popen
from airtest.core.api import *
from airtest.aircv import *
import random
import platform

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

min_support = 0
search_text = "Python"
export_path = r'F:\Code\PhoneCrawler\xhs.air\result'


osName = platform.system()
if(osName == 'Windows'):
    oblique = '\\'
else:
    oblique = '/'

content_dict_all = {}
content_list = []


def get_random_result():
    font_random = random.randint(0, 9)
    behind_random = random.randint(7, 12)
    result_random = random.randint(0, 12)
    return result_random > font_random and result_random < behind_random

def save_img(img_path,img_element):
    width, height = device().get_current_resolution()
    position_x,position_y = img_element.get_position()
    size_width, size_height = img_element.attr('size')
    img_size_width = width * size_width
    img_size_height = height * size_height
    img_center_x = position_x * width
    img_cneter_y = position_y * height
    img_x = 0
    img_y = img_cneter_y - (img_size_height / 2)
    screen = G.DEVICE.snapshot()
    screen = aircv.crop_image(screen, [img_x, img_y, img_size_width, img_size_height + img_y])
    pli_img = cv2_2_pil(screen)
    temp_path = r'{}{}{}.png'.format(export_path, oblique, img_path)
    pli_img.save(temp_path, quality=90, optimize=True)

def get_target_item(content_item, name_list):
    temp_item = content_item
    for index in range(0, len(name_list)):
        name = name_list[index]
        if temp_item.child(name).exists():
            temp_item = temp_item.child(name)
        else:
            return None
    return temp_item

def get_target_text(target_item, placeholder):
    return target_item.get_text() if target_item.exists() else placeholder

def get_poco_text(name,placeholder):
    return poco(name).get_text() if poco(name).exists() else placeholder

def get_page_note():
    list_item = poco("com.xingin.xhs:id/cwq")
    list_item.wait_for_appearance()
    element_list = poco("com.xingin.xhs:id/cwq").children()
    for element_item in element_list:
        if element_item.child('android.widget.RelativeLayout').exists():
            support_item = get_target_item(content_item=element_item, name_list=[
                'android.widget.RelativeLayout',
                'com.xingin.xhs:id/cb4',
                'com.xingin.xhs:id/cus'
            ])
            if support_item:
                try:
                    support_number = int(support_item.get_text())
                    if support_number > min_support:
                        element_item.click()
                        sleep(1.0)
                        content_data = get_detail()
                        if not poco("com.xingin.xhs:id/cwq").exists():
                            keyevent("BACK")
                        sleep(1.0)
                        if content_data:
                            content_dict_all[content_data.get('title')] = content_data
                            content_list.append(content_data.get('title'))
                            print('采集到一篇图文笔记，现存:{}篇笔记'.format(len(content_list)))
                except:
                    print('无效item')
        

def get_detail():
    try:
        page_item = poco('com.xingin.xhs:id/bi')
        page_item.wait_for_appearance()
        data_dict = None
        if poco('com.xingin.xhs:id/dfo').exists():
            data_dict = get_detail_video()
        else:
            data_dict = get_dateil_text()
        return data_dict
    except:
        return None


def get_dateil_text():
    title_item = poco('com.xingin.xhs:id/dgo')
    title_item.wait_for_appearance(timeout=20)
    if not title_item.exists():
        return None

    searial_item = poco('com.xingin.xhs:id/bu4')
    if searial_item.exists():
        searial_text = searial_item.get_text()
        total_number = 0
        total_text_list = searial_text.split('/')
        if len(total_text_list):
            total_number = int(total_text_list[1])
        else:
            total_number = 1
    else:
        total_number = 0

    content_dcit = {}
    content_dcit['title'] = get_poco_text('com.xingin.xhs:id/dgo', '无')
    content_dcit['desc'] = get_poco_text('com.xingin.xhs:id/bu3', '无')
    content_dcit['type'] = '图文'
    content_dcit['collect'] = get_poco_text('com.xingin.xhs:id/dg4', '0')
    content_dcit['support'] = get_poco_text('com.xingin.xhs:id/dey', '0')
    content_dcit['comment'] = get_poco_text('com.xingin.xhs:id/df4', '0')
    content_dcit['author'] = get_poco_text(name='com.xingin.xhs:id/nickNameTV', placeholder='无')

    if content_dcit['title'] in content_list:
        return None

    collect_item = poco('com.xingin.xhs:id/dg3')
    if collect_item.exists() and get_random_result():
        collect_item.click()

    support_item = poco('com.xingin.xhs:id/dex')
    if support_item.exists() and get_random_result():
        support_item.click()

    temp_path = export_path + oblique + content_dcit['title']

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    with open(r'{}{}result.txt'.format(temp_path, oblique), 'a+', encoding='utf-8') as f:
        f.write('标题:  {}\n'.format(content_dcit['title']))
        f.write('作者:  {}\n'.format(content_dcit['author']))
        f.write('类型:  {}'.format(content_dcit['type']))
        f.write('点赞:{}  收藏:{}  评论:{}\n'.format(content_dcit['support'],content_dcit['collect'],content_dcit['comment']))
        f.write('内容:\n{}'.format(content_dcit['desc']))
        f.close()

    if total_number > 0:
        img_element = poco('com.xingin.xhs:id/dp4')
        if img_element.exists():
            if total_number > 1:
                for index in range(0, total_number):
                    if index != 0:
                        poco("com.xingin.xhs:id/btx").swipe([-1, -0.0125], duration=0.25)
                        sleep(1)
                    save_img('{}{}{}'.format(
                        content_dcit['title'], oblique, index), img_element)
            else:
                save_img('{}{}1'.format(
                    content_dcit['title'], oblique), img_element)

    sleep(2)
    with open(export_path + oblique + r'all_data.txt', 'a+', encoding='utf-8') as f:
        f.write('{}\n'.format(content_dcit['title']))
        f.close()

    return content_dcit

def get_detail_video():
    return None
    poco('com.xingin.xhs:id/bu4').click()
    desc_item = poco('com.xingin.xhs:id/dfq')
    if not desc_item.exists():
        return None
    data_dict = {}
    data_dict['type'] = '视频'
    desc_text_item = get_target_item(desc_item, name_list=['com.xingin.xhs:id/df7', 'com.xingin.xhs:id/dfp'])
    data_dict['title'] = desc_text_item.get_text() if desc_text_item else "无"
    data_dict['time'] = get_poco_text(name='com.xingin.xhs:id/f4g', placeholder='无')
    data_dict['author'] = get_poco_text(name='com.xingin.xhs:id/matrixNickNameView', placeholder='无')
    if poco('com.xingin.xhs:id/fu0').exists():
        poco('com.xingin.xhs:id/fu0').click()
    
    data_dict['collect'] = get_poco_text('com.xingin.xhs:id/d21', '0')
    data_dict['support'] = get_poco_text('com.xingin.xhs:id/d25', '0')
    data_dict['comment'] = get_poco_text('com.xingin.xhs:id/d23', '0')
    return data_dict

def open_app():  
    start_app('com.xingin.xhs')
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    
    if os.path.exists(export_path + oblique + r'all_data.txt'):
        with open(export_path + oblique + r'all_data.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip('\n')
                content_list.append(line)
            f.close()



# 开启搜索
def start_search():
    search_element = poco('com.xingin.xhs:id/ege')
    search_element.wait_for_appearance()
    search_element.click()
    sleep(1.0)
    # 输入内容并搜索
    input_element = poco('com.xingin.xhs:id/cx3')
    input_element.wait_for_appearance()
    input_element.set_text(search_text)
    poco('com.xingin.xhs:id/cx7').click()

# 获取页面信息
def get_page():
    get_page_note()

def to_next():
   sleep(0.5)
   poco.swipe([0.5, 0.9],[0.5,0.1], duration=0.25)
   sleep(1)
   get_page_note()

# 滑动
def start_scroll():
    while True:
        to_next()
        
        
open_app()
start_search()
get_page()
start_scroll()








