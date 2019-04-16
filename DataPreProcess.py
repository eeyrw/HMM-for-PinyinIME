from pathlib import Path
import os
import logging
import re,collections
from pypinyin import pinyin, lazy_pinyin, Style
from functools import reduce
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class DataPreProcessor:
    def __init__(self,filePath):
        self._dataFilePath_=filePath
        self._trainDsStatMap_=collections.OrderedDict()
        self._testDsStatMap_=collections.OrderedDict()

    def getChineseSegments(self,rawText):
        chineseSegments=re.compile(r'([\u4e00-\u9fef]+)')
        temp=[]
        for seg in chineseSegments.findall(rawText):
            if len(seg)>=2:
                temp.append(seg)
        return temp

    def printDsStatInfo(self):
        print(str.format('Train Data Set    Min length of segment: {0}, Max length of segment: {1}',list(self._trainDsStatMap_.keys())[0],list(self._trainDsStatMap_.keys())[-1]))
        trainSegLenList=[]
        testSegLenList=[]   
        for k,v in self._trainDsStatMap_.items():
            for i in range(v):
                trainSegLenList.append(k)
        for k,v in self._testDsStatMap_.items():
            for i in range(v):
                testSegLenList.append(k)   

        trainSegLenList = np.array(trainSegLenList)        
        testSegLenList = np.array(testSegLenList) 
        trainLen=trainSegLenList.size
        trainMean=np.mean(trainSegLenList)
        trainStd=np.std(trainSegLenList) 
        trainMax=np.max(trainSegLenList)
        trainMin=np.min(trainSegLenList)
        testMean=np.mean(testSegLenList)
        testStd=np.std(testSegLenList) 
        testMax=np.max(testSegLenList) 
        testMin=np.min(testSegLenList)

        testLen=testSegLenList.size             
        plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
        # Plot Histogram on x
        kwargs = dict(alpha=1,density=1, bins=50)
        plt.rcParams["figure.figsize"]=[8,3]
        plt.subplots_adjust(wspace=0.3)
        plt.figure(1)
        plt.subplot(121)
        plt.hist(trainSegLenList, **kwargs,color='r',label='训练集')
        plt.gca().set(title='训练集句子长度频率分布图', ylabel='频率')
        plt.subplot(122)
        plt.hist(testSegLenList, **kwargs,color='b',label='测试集')
        plt.gca().set(title='测试集长度频率分布图', ylabel='频率')
        #plt.show()
        plt.savefig("DataSetHistogram.pdf", dpi=150)
        with open('DataSetInfo.txt','w',encoding='utf-8') as f:
            f.write('TRA_LEN:%f\nT_MAX:%f\nT_MIN:%f\nT_MEAN:%f\nT_STD:%f\n'%(trainLen,trainMax,trainMin,trainMean,trainStd))
            f.write('\n\n')
            f.write('TST_LEN:%f\nT_MAX:%f\nT_MIN:%f\nT_MEAN:%f\nT_STD:%f\n'%(testLen,testMax,testMin,testMean,testStd))

    def generateTrainAndTestDataSet(self,trainDsFilePath,trainDsSize,testDsFilePath,testDsSize):
        os.chdir('.')
        trainDsSizeCount=0
        testDsSizeCount=0
        loopFlag=True
        regxNewsContent=re.compile(r'<content>(\S+)</content>')
        with open(self._dataFilePath_, "r",encoding='utf-8') as sohuXmlFile:
            print('Start generating training data set.')
            with open(trainDsFilePath,'w',encoding='utf-8') as writeFile:
                while loopFlag:
                    dataFileLine = sohuXmlFile.readline()
                    contentResult=regxNewsContent.search(dataFileLine)
                    if contentResult:
                        segments=self.getChineseSegments(contentResult.groups()[0])
                        for seg in segments:
                            if trainDsSizeCount>=trainDsSize:
                                loopFlag=False
                                break
                            segLen=len(seg)                                
                            self._trainDsStatMap_.setdefault(segLen,0)
                            self._trainDsStatMap_[segLen]+=1                         
                            trainDsSizeCount+=1
                            py=lazy_pinyin(seg)
                            ppy=reduce((lambda x, y: x+y+' '),py,'')
                            writeFile.write(seg+'\n'+ppy+'\n')

            loopFlag=True                        
            with open(testDsFilePath,'w',encoding='utf-8') as writeFile:
                print('Start generating testing data set.')            
                while loopFlag:
                    dataFileLine = sohuXmlFile.readline()
                    contentResult=regxNewsContent.search(dataFileLine)
                    if contentResult:
                        segments=self.getChineseSegments(contentResult.groups()[0])
                        for seg in segments:
                            if testDsSizeCount>=testDsSize:
                                loopFlag=False                                
                                break
                            segLen=len(seg)
                            self._testDsStatMap_.setdefault(segLen,0)
                            self._testDsStatMap_[segLen]+=1                           
                            testDsSizeCount+=1
                            py=lazy_pinyin(seg)
                            ppy=reduce((lambda x, y: x+y+' '),py,'')
                            writeFile.write(seg+'\n'+ppy+'\n')






if __name__ == '__main__':
    dpp=DataPreProcessor('news_sohusite_xml_utf8.dat')
    dpp.generateTrainAndTestDataSet('train.txt',40000000,'test.txt',400000)
    dpp.printDsStatInfo()