# -*- encoding=utf8 -*-
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
__author__ = "panghu"

from math import fabs
from operator import index
from pickle import TRUE
# from tkinter.messagebox import NO
from airtest.core.api import *
import os
import platform
from airtest_util import get_child, get_item_type, get_random_result
from airtest.aircv import *

auto_setup(__file__)


poco = AndroidUiautomationPoco(
    use_airtest_input=True, screenshot_each_action=False)


class XHSScirpt:
    min_support = 100
    search_text = "Python"
    export_path = r'/Users/liangyi/Downloads/xhs_data'

    oblique = '/'
    content_list = []

    def __init__(self, min_support, search_text, export_path):
        self.min_support = min_support
        self.search_text = search_text
        self.export_path = export_path
        os_name = platform.system()
        if os_name == 'Windows':
            self.oblique = '\\'
        else:
            self.oblique = '/'

    def save_img(self, img_path, img_element):
        width, height = device().get_current_resolution()
        position_x, position_y = img_element.get_position()
        size_width, size_height = img_element.attr('size')
        img_size_width = width * size_width
        img_size_height = height * size_height
        img_center_x = position_x * width
        img_cneter_y = position_y * height
        img_x = 0
        img_y = img_cneter_y - (img_size_height / 2)
        screen = G.DEVICE.snapshot()
        screen = aircv.crop_image(
            screen, [img_x, img_y, img_size_width, img_size_height + img_y])
        pli_img = cv2_2_pil(screen)
        temp_path = r'{}{}{}.png'.format(
            self.export_path, self.oblique, img_path)
        pli_img.save(temp_path, quality=90, optimize=True)

    # 启动App
    def open_app(self):
        start_app('com.xingin.xhs')
        self.check_local_cache()

    # 检查本地缓存
    def check_local_cache(self):
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

        if os.path.exists(self.export_path + self.oblique + r'all_data.txt'):
            with open(self.export_path + self.oblique + r'all_data.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    self.content_list.append(line)
                f.close()
        print('原本缓存的数据:{}'.format(len(self.content_list)))
        print(self.content_list)

    # 获取首页搜索按钮
    def find_home_search_btn(self):
        try:
            home_item = poco("androidx.drawerlayout.widget.DrawerLayout")
            home_item.wait_for_appearance()
        except:
            print('寻找首页搜索按钮失败')
            return False
        top_item = home_item.child()[0]
        if top_item == None:
            print('寻找首页搜索按钮失败')
            return False
        top_index = 0
        result = False
        while not result and top_index != 12:
            temp_result = self.check_child(2, top_item)
            top_item = top_item.child()[0]
            if top_item == None:
                print('寻找首页搜索按钮失败')
                return False
            if temp_result:
                result = self.check_child(3, top_item)
            top_index += 1
        search_item = None
        for item in top_item.children():
            if item.attr('type') == 'android.widget.ImageView':
                search_item = item
        if search_item == None:
            print('寻找首页搜索按钮失败')
            return False
        search_item.click()
        return True

    def check_child(self, need_count, element_item):
        return element_item.children().__len__() == need_count

    # 检测搜索页面并搜索
    def find_search_input(self):
        try:
            item_list = poco(
                typeMatches="android.widget.TextView", textMatches="搜索")
            item_list.wait_for_appearance()
        except:
            print('进入搜索页面失败')
            return False
        for item in item_list:
           if get_item_type(item.parent()) != "android.widget.LinearLayout":
               search_btn = item
        if not search_btn:
            print('获取搜索按钮失败')
            return False

        input_item = search_btn.parent().child(typeMatches='android.widget.FrameLayout').child(
            typeMatches='android.widget.EditText')
        if input_item:
            input_item.set_text(self.search_text)
            sleep(1)
            search_btn.click()
            sleep(1)

            in_page = False
            index = 0
            while (not in_page) or index > 120:
                try:
                    pic_btn = poco(
                        typeMatches="android.widget.TextView", textMatches="图文")
                    pic_btn.wait_for_appearance(timeout=5)
                    if pic_btn.parent().child(typeMatches='android.widget.ImageView'):
                        in_page = True
                        pic_btn.parent().click()
                except:
                    print('获取图文按钮貌似出了问题')
                    return False
                finally:
                    index += 1
            if not in_page:
                print('搜索失败')
                return False

            return True
        else:
            print('获取输入框失败')
            return False

    # 获取列表数据
    def get_search_list(self):

        try:
            page_item = poco(type='androidx.viewpager.widget.ViewPager')
            page_item.wait_for_appearance()
            note_list_item = page_item.child(type='android.widget.FrameLayout').child(
                type="androidx.recyclerview.widget.RecyclerView").child(type='android.widget.FrameLayout')
        except:
            print('搜索失败')
            return

        for note_item in note_list_item:
            try:
                support_item = note_item.child(type='android.widget.RelativeLayout').child(
                    type='android.widget.FrameLayout')
            except:
                print('无效item')
                continue
            if support_item:
                if support_item.child(type='android.widget.ImageView') and support_item.child(type='android.widget.TextView'):
                    support_text = support_item.child(
                        type='android.widget.TextView').get_text()
                    if "万" in support_text:
                        support_number = float(
                            support_text.replace('万', "")) * 10000
                    else:
                        support_number = int(support_text)
                    if support_number > self.min_support:
                        note_item.click()
                        sleep(1)
                        note_data = self.get_note_detail()
                        if poco(name='com.xingin.xhs:id/noteContentLayout'):
                            sleep(2)
                            keyevent("BACK")
                        if note_data:
                            self.content_list.append(note_data.get('title'))
                            with open(self.export_path + self.oblique + r'all_data.txt', 'a+', encoding='utf-8') as f:
                                f.write('{}\n'.format(note_data['title']))
                                f.close()

                            print('采集到一篇图文笔记，现存:{}篇笔记'.format(
                                len(self.content_list)))

    # 获取笔记详情
    def get_note_detail(self):
        note_dict = {
            'type': '图文'
        }
        try:
            content_page_item = poco(
                name='com.xingin.xhs:id/noteContentLayout')
            content_page_item.wait_for_appearance(timeout=10)
        except:
            print('页面参数获取失败')
            return None

        try:
            searial_item = poco(name='com.xingin.xhs:id/noteContentLayout').child(typeMatches='android.widget.FrameLayout').child(
                type="android.widget.LinearLayout").child(typeMatches='android.widget.TextView')
            searial_text = searial_item.get_text()
            total_number = 0
            total_text_list = searial_text.split('/')
            if len(total_text_list):
                total_number = int(total_text_list[1])
            else:
                total_number = 1
        except:
            total_number = 1

        try:
            string_item_list = poco(name='com.xingin.xhs:id/noteContentLayout').child(
                typeMatches='android.widget.LinearLayout').child(typeMatches='android.widget.TextView')
        except:
            print('标题获取失败')
            return None

        index = 0
        for string_item in string_item_list:
            content_string = string_item.get_text()
            if index == 0:
                note_dict['title'] = content_string
            else:
                note_dict['desc'] = content_string
            index += 1

        if note_dict['title'] in self.content_list:
            print('笔记:{}已在本地,无需重新采集'.format(note_dict.get('title')))
            return None
        try:
            img_element = poco(name='com.xingin.xhs:id/noteContentLayout').child(
                typeMatches='android.widget.FrameLayout').child(typeMatches='androidx.recyclerview.widget.RecyclerView')
        except:
            print('图片获取失败')

        temp_path = self.export_path + self.oblique + note_dict['title']

        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        if img_element.exists():
            if total_number > 1:
                for index in range(0, total_number):
                    if index != 0:
                        img_element.swipe([-1, -0.0125], duration=0.25)
                        sleep(1)
                    self.save_img('{}{}{}'.format(
                        note_dict['title'], self.oblique, index+1), img_element)
            else:
                self.save_img('{}{}1'.format(
                    note_dict['title'], self.oblique), img_element)

        page_item = content_page_item.parent().parent().parent().parent()
        if page_item:
            try:
                bottom_item_list = page_item.child(type='android.widget.FrameLayout').child(type='android.view.ViewGroup').child(
                    type='android.view.ViewGroup').child(type='android.widget.LinearLayout').child(type='android.widget.TextView')
            except:
                print('底部参数获取失败')

            index = 0
            for bottom_text_item in bottom_item_list:
                bottom_text = bottom_text_item.get_text()
                if index == 0:
                    note_dict['support'] = bottom_text
                    if get_random_result():
                        try:
                            bottom_text_item.parent().click()
                        except:
                            print('笔记:{}点赞失败'.format(note_dict['title']))
                elif index == 1:
                    note_dict['collect'] = bottom_text
                    try:
                        bottom_text_item.parent().click()
                    except:
                        print('笔记:{}收藏失败'.format(note_dict['title']))
                else:
                    note_dict['comment'] = bottom_text
                index += 1

        author_item = poco(name='com.xingin.xhs:id/nickNameTV')
        if author_item:
            note_dict['author'] = author_item.get_text()
        else:
            note_dict['author'] = ""

        with open(r'{}{}result.txt'.format(temp_path, self.oblique), 'a+', encoding='utf-8') as f:
            f.write('标题:  {}\n'.format(note_dict['title']))
            f.write('作者:  {}\n'.format(note_dict['author']))
            f.write('类型:  {}'.format(note_dict['type']))
            f.write('点赞:{}  收藏:{}  评论:{}\n'.format(
                note_dict['support'], note_dict['collect'], note_dict['comment']))
            f.write('内容:\n{}'.format(note_dict['desc']))
            f.close()

        return note_dict

    # 滚动一下
    def to_next(self):
        sleep(0.5)
        poco.swipe([0.5, 0.9], [0.5, 0.1], duration=0.25)
        sleep(1)
        self.get_search_list()

    def start_scroll(self):
        while True:
            self.to_next()

    # 开始搜素任务
    def start_search(self):
        if not self.find_home_search_btn():
            return
        if not self.find_search_input():
            return
        self.get_search_list()
        self.start_scroll()


script = XHSScirpt(min_support=100, search_text='python',
                   export_path=r'/Users/liangyi/Downloads/xhs_data')

script.open_app()
script.start_search()
