from pathlib import Path
import os
import logging
import re
from pypinyin import pinyin, lazy_pinyin, Style
from functools import reduce

class DataPreProcessor:
    def __init__(self,filePath):
        self.openSohuXmlFile(filePath)

    def openSohuXmlFile(self,filePath):
        os.chdir('.')
        pinyinMaps={}
        with open(filePath, "r",encoding='utf-8') as sohuXmlFile:
            with open("aaa.txt",'w',encoding='utf-8') as writeFile:
                for i in range(0,40000000):
                    a = sohuXmlFile.readline()
                    regxNewsContent=re.compile(r'<content>(\S+)</content>')
                    chineseSegments=re.compile(r'([\u4e00-\u9fef]+)')
                    aa=regxNewsContent.search(a)
                    if aa:
                        b=chineseSegments.findall(aa.groups()[0])
                        for seg in b:
                            if len(seg)>=2:
                                writeFile.write(seg+'\n')
        #                         py=lazy_pinyin(seg)
        #                         ppy=reduce((lambda x, y: x+y+' '),py,'')
        #                         for pi in py:
        #                             pinyinMaps.setdefault(pi,0)
        #                             pinyinMaps[pi]+=1
        #                         writeFile.write(seg+'\n'+ppy+'\n')
        # with open("b.txt",'w',encoding='utf-8') as writeFile:                            
        #     for k,v in pinyinMaps.items():
        #         writeFile.write('%5s: %d\n'%(k,v))




if __name__ == '__main__':
    dpp=DataPreProcessor('news_sohusite_xml_utf8.dat')