# -*- coding: utf-8 -*-
import os
from utils.log import logging
from utils.requestshelper import RequestsHelper
from fontTools.ttLib import TTFont
from PIL import Image, ImageEnhance
from pytesseract import *

logger = logging.getLogger(__name__)


class WebFont(object):
    def __init__(self, plat_name):
        self.url = 'https://vfile.meituan.net/colorstone/2c8d9a8f5031f26f4e9fe924263e31ce2076.woff'
        self.plat_name = plat_name
        self.font_dict = dict()
        self.manual_dict = {
            'uniF3C5':  8,
            'uniEDEE':  6,
            'uniF38E':  2,
            'uniE824':  3,
            'uniE829':  5,
            'uniE851':  0,
            'uniEBCF':  1,
            'uniEE5A':  9,
            'uniEFFE':  4,
            'uniF35D':  7,
        }
        self.__init_font_map()

    def __init_font_map(self):
        """
        初始化猫眼的字符集模版,只在倒入模块时有构造方法调用一次
        """
        font_file = self.__save_font_file(self.url)
        font = TTFont(font_file)
        glyph_set = font.getGlyphSet()
        glyph_dict = glyph_set._glyphs.glyphs
        for k, v in self.manual_dict.items():
            self.font_dict[glyph_dict[k].data] = v

    def __save_font_file(self, url):
        filename = url.split('/')[-1]
        font_dir = "%s/%s" % (os.path.dirname(__file__), '../opt/fonts')
        # 判断文件是否存在
        if not os.path.exists("%s/%s" % (font_dir, filename)):
            if not os.path.exists(font_dir):
                os.mkdir(font_dir)
            try:
                response = RequestsHelper.get(url)
            except Exception:
                raise Exception()
            with open("%s/%s" % (font_dir, filename), 'wb') as fw:
                fw.write(response.content)
        return "%s/%s" % (font_dir, filename)

    def convert_to_num(self, series, url):
        """
        获取unicode的对应的数字
        :param series: int
        :param url: 字符集文件的地址
        :return: int，series对应数字
        """
        font_file = self.__save_font_file(url)
        font = TTFont(font_file)
        cmap = font.getBestCmap()
        num = cmap.get(series)
        glyph_set = font.getGlyphSet()

        return self.font_dict[glyph_set._glyphs.glyphs[num].data]


class FontManager(object):
    def __init__(self):
        self.fonts = dict()

    def add_font(self, plat_name):
        """
        倒入该模块时调用此方法初始化字符集模版
        :param plat_name: str 'maoyan'/
        """
        if plat_name == 'maoyan':
            self.fonts['maoyan'] = WebFont(plat_name)
        elif plat_name == 'douyin':
            pass
        else:
            raise Exception('平台：%s 暂不支持' % plat_name)

    def get_font(self, plat_name):
        try:
            return self.fonts[plat_name]
        except KeyError:
            raise Exception('请先调用get_font()来添加平台%s的字符集' % plat_name)

    def convert_to_num_ocr(self, fp):
        """
        获取unicode的对应的数字
        :param fp: 图片文件的路径或文件对象(必须byte方式打开)
        :return: 图片对应的数字, 如果不符合数字格式，则返回图片上的文本
        """
        im = Image.open(fp)
        enhancer = ImageEnhance.Contrast(im)
        image_enhancer = enhancer.enhance(4)
        im_orig = image_enhancer.resize((image_enhancer.size[0]*2, image_enhancer.size[1]*2), Image.BILINEAR)

        text = image_to_string(im_orig)
        try:
            return int(text)
        except ValueError:
            return text


fm = FontManager()
fm.add_font('maoyan')
maoyan_font = fm.get_font('maoyan')
logger.info(maoyan_font.convert_to_num(0xf8c3, 'https://vfile.meituan.net/colorstone/7986a5279399aeee3ef19fe37989a00d2088.woff'))

fp = open('/Users/apple/test/dolphin/opt/WX20180607-172930@2x.png', 'rb')
print(fm.convert_to_num_ocr(fp))