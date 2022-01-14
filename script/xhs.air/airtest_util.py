# from tkinter.messagebox import NO
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.aircv import *
from airtest.core.api import *
import random


def get_random_result():
    font_random = random.randint(0, 9)
    behind_random = random.randint(7, 12)
    result_random = random.randint(0, 12)
    return result_random > font_random and result_random < behind_random

def get_offspring(element_item):
    try:
        if element_item.offspring().exists():
            return element_item.offspring()
        return None
    except:
        return None


def get_offspring(element_item, hierarchy=1):
    temp_item = element_item
    for _ in range(0, hierarchy):
        if get_offspring(temp_item):
            temp_item = get_offspring(temp_item)
        else:
            return None
    return temp_item


def get_child(element_item, child_list):
    temp_item = element_item
    for child_index in child_list:
        try:
            if temp_item.child()[child_index]:
                temp_item = temp_item.child()[child_index]
        except:
            return None
    return temp_item


def get_parent(element_item, count):
    temp_item = element_item
    for _ in range(count):
        try:
            if temp_item.parent():
                temp_item = temp_item.parent()
            else:
                return None
        except:
            return None

def get_item_type(item):
    return item.attr('type')


def save_img(img_path, img_element, export_path, oblique):
    width, height = device().get_current_resolution()
    position_y = img_element.get_position()
    size_width, size_height = img_element.attr('size')
    img_size_width = width * size_width
    img_size_height = height * size_height
    img_cneter_y = position_y * height
    img_x = 0
    img_y = img_cneter_y - (img_size_height / 2)
    screen = G.DEVICE.snapshot()
    screen = aircv.crop_image(
        screen, [img_x, img_y, img_size_width, img_size_height + img_y])
    pli_img = cv2_2_pil(screen)
    temp_path = r'{}{}{}.png'.format(export_path, oblique, img_path)
    pli_img.save(temp_path, quality=90, optimize=True)
