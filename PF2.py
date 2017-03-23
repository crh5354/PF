#!/usr/bin/env python
#-*- coding:utf-8 -*-  
#-- Author: Crh
#----------------

import json
import os
import shutil
import xlrd
import sys
import Tkinter
import tkMessageBox
import tkFileDialog 
from Tkinter import *
import Image  
import sys
import ImageDraw, ImageFont, ImageFilter
import string
import re

# 数据处理器
class DataHandlers(object):
    # 构造函数
    def __init__( self ):
        pass

    # 析构函数
    def __del__( self ):
        pass

    #搜索png路径
    def search_file( self, str1, paths ):
        Target_Path = paths
        imgfiles = []
        for path, dirs, files in os.walk(Target_Path):
            imgfiles.extend([os.path.join(path, f) for f in files if f.endswith(str1)])
        return imgfiles

    #中文转unicode
    def getStrToUnicode( self, str1 ):
        # print str1
        return repr(unicode(str1, "utf-8"))

    # 十六进制转十进制
    def getUnicode16To10( self, unicodes ):
        # print unicodes
        if len( unicodes ) == 1:
            return ord( unicodes )
        unicodes = unicodes[:-1]
        unicodes = unicodes[-4:]
        return int( unicodes, 16 )

    def getImageData( self, files ):
        width = 0
        height = 0
        tempw = 0
        array = []
        keyarray = {}
        maxWidth = 0
        maxHeight = 0
        for x in range(len(files)):
            img = Image.open(files[ x ])
            w, h = img.size
            if w > maxWidth:
                maxWidth = w
            if h > maxHeight:
                maxHeight = h

        for x in range(len(files)):
            img = Image.open(files[ x ])
            w, h = img.size
            if height == 0:
                height = maxHeight
            if width + maxWidth > 1024:
                tempw = 1024
                width = 0
                height = height + maxHeight
            # print files[ x ]
            array.append( [ files[ x ], width, height - maxHeight, (w, maxHeight), ( w, h ) ] )
            width = width + w
        if tempw == 0:
            tempw = width
        keyarray["width"] = tempw
        keyarray["height"] = height
        keyarray["data"] = array
        return keyarray

    def drawImage( self, files, paths ):
        keyarray = self.getImageData( files )
        imgs = Image.new('RGBA', (keyarray['width'], keyarray["height"]), (0, 0, 0, 0))
        # print keyarray["data"]
        for x in range( len( keyarray["data"] ) ):
            im = Image.open( keyarray["data"][x][0] ) 
            imgs.paste(im, (keyarray["data"][x][1], keyarray["data"][x][2]))
        imgs.save( paths, "png")

    def getStringData( self, strs ):
        exp=re.compile('.*_(.*)\.')
        results=exp.findall(strs)[0]
        if results == "00":
            results = "\\"
        elif results == "01":
            results = "/"
        elif results == "02":
            results = ":"
        elif results == "03":
            results = "?"
        elif results == "04":
            results = '"'
        elif results == "05":
            results = "<"
        elif results == "06":
            results = ">"
        elif results == "07":
            results = "."
        elif results == "08":
            results = "|"
        elif results == "09":
            results = "_"
        return results
        # num = strs.find(".png")
        # strss = strs
        # ss = ""
        # for i in range(num-1, 0, -1):
        #     if strs[i] == '_':
        #         # print -(len(strs) - num)
        #         strss = strs[i+1:]
        #         strss = strss[:-4]
        #         return strss
        #         break
        # return ""

     
    def writeFNT( self, numVar, paths, resPath, fntPath, state ):
        keyarray = self.getImageData( self.search_file(".png", paths) )
        line1 = 'info face="crh--GBK1-0" size={0} bold=0 italic=0 charset="" unicode=0 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=1,1 \n'.format(32) 
        line2 = 'common lineHeight={0} base=28 scaleW={1} scaleH={2} pages=1 packed=0 \n'.format(keyarray["data"][0][3][1], keyarray["data"][0][3][0], keyarray["data"][0][3][1]) 
        line3 = 'page id=0 file="{0}" \n'.format( resPath + ".png" ) 
        line4 = 'chars count={0} \n'.format(len( keyarray["data"] )) 
        line  = 'char id={0} x={1} y={2} width={3} height={4} xoffset={5} yoffset={6} xadvance={7} page={8} chnl={9} letter="{10}" \n'
        # line  = 'char id=[0] x=[1] y=[2] width=[3] height=[4] xoffset=[5] yoffset=[6] xadvance=[7] page=[8] chnl=[9] letter="[10]" \n'
        f=file( fntPath, "w+" )
        
        num = 0.0
        try:
           num = string.atof(numVar)
        except:
            num = 0

        f.writelines( line1 )
        f.writelines( line2 )
        f.writelines( line3 )
        f.writelines( line4 )

        # 第一个字符编码为32,也就是空格，位置为0,0,宽高为0,0, 绘制到屏幕的相应位置时，像素偏移（0，28），绘制完后相应位置的x往后移15像素再画下一个字符，字的图块在第1页上
        # char id=32  x=0     y=0     width=0    height=0     xoffset=0     yoffset=28    xadvance=15     page=0 chnl=0
        # print keyarray["data"]
        for x in range( len( keyarray["data"] ) ):
            letter = self.getStringData( keyarray["data"][x][0] )
            cid = 0
            if len(letter) != 1:
                uid = self.getStrToUnicode( letter )
                cid = self.getUnicode16To10( uid )
            else:
                cid = ord( letter )

            print keyarray["data"][x]
            picSize = keyarray["data"][x][4]
            xx = keyarray["data"][x][1]
            yy = keyarray["data"][x][2]
            width = keyarray["data"][x][3][0]
            height = keyarray["data"][x][3][1]
            xoffset = 0  
            yoffset = 0
            if state == 1:
                pass
            elif state == 2:
                xoffset= (width - picSize[0])/2  
                yoffset= (height - picSize[1])/2
            elif state == 3:
                xoffset= width - picSize[0]  
                yoffset= height - picSize[1]
            xadvance = width + num
            page=0 
            chnl=0

            print letter, cid
            # print '\n'
            # strline = line.format(  )
            print cid, xx, yy, width, height, xoffset, yoffset, xadvance, page, chnl, letter
            pp = [ cid, xx, yy, width, height, xoffset, yoffset, xadvance, page, chnl, letter ]
            f.writelines( line.format( cid, xx, yy, width, height, xoffset, yoffset, xadvance, page, chnl, letter ) )
        
        f.close()



# 界面管理器
class Interface(object):
    # 私有变量
    __root = None
    __var1 = None
    __var2 = None
    __var3 = None
    __var4 = None
    __IntVar = None
    __DataHandlers = None
    # 构造函数
    def __init__( self ):
        pass

    # 析构函数
    def __del__( self ):
        pass

    def choiceDirectory( self ):
        filename = tkFileDialog.askdirectory(parent=self.__root,initialdir="/",title='Pick a directory')
        self.__var1.set( filename )


    def saveDirectory( self ):
        filename = tkFileDialog.askdirectory(parent=self.__root,initialdir="/",title='Pick a directory')
        self.__var2.set( filename )

    def exportResource( self ):
        if self.getTargetPath() == "/" or self.getSavePath() == "/":
            tkMessageBox.showinfo( "路径错误", "路径错误或者不存在")
            return
        if not os.path.exists( self.getTargetPath() ) or not os.path.exists( self.getSavePath() ) :
            tkMessageBox.showinfo( "路径错误", "路径错误或者不存在")
            return
        self.__DataHandlers.drawImage( self.__DataHandlers.search_file(".png", self.getTargetPath()), self.getSavePngPath() )
        self.__DataHandlers.writeFNT( self.__var4.get(), self.getTargetPath(), self.getResourceName(), self.getFntPath(), self.__IntVar.get() )
        tkMessageBox.showinfo( "PF提示", "导出完美成功，请点赞！")

    def explainCallback( self ):
        strs = "本工具具备小图合并为大图并生成对应的fnt文件功能\n"
        strs = strs + "1、资源图片命名规则必须是XXX_?.png， XXX使用中随意，？代表就是这图片上的字体\n"
        strs = strs + "如：单个小图片是的是个9，那么资源图片的命名就是XXX_9.png；单个小图片是的是个中，那么资源图片的命名就是XXX_中.png；\n"
        strs = strs + "2、注意路径别带中文路径\n"
        strs = strs + "3、注意某些图片是压缩过，导致图片部分信息丢失，会导致本工具不能使用或者带有瑕疵，建议先使用完本工具处理完再去压缩\n"
        strs = strs + '4、特殊符号对应说明 例如 XXX_01.png = XXX_/.png 对应表 : \n'
        strs = strs + '00=\\ \n01=/ \n02=: \n03=? \n04=" \n05=< \n06=> \n07=. \n08=| \n09=_ \n'
        strs = strs + "5、make in crh"
        tkMessageBox.showinfo( "PF说明", strs)

    def getTargetPath( self ):
        print self.__var1.get() + "/"
        return self.__var1.get() + "/"

    def getSavePath( self ):
        print self.__var2.get() + "/"
        return self.__var2.get() + "/"

    def getResourceName( self ):
        print self.__var3.get()
        return self.__var3.get()

    def getFntPath( self ):
        print self.getSavePath() + self.getResourceName() + ".fnt"
        return self.getSavePath() + self.getResourceName() + ".fnt"

    def getSavePngPath( self ):
        print self.getSavePath() + self.getResourceName() + ".png"
        return self.getSavePath() + self.getResourceName() + ".png"

    # 初始化界面
    def initUI( self ):
        self.__DataHandlers = DataHandlers()

        self.__root = Tkinter.Tk()
        self.__var1 = StringVar()
        self.__var2 = StringVar()
        self.__var3 = StringVar()
        self.__var4 = StringVar()
        self.__IntVar = IntVar()

        self.__root.title("Png To Fnt")
        self.__root.geometry('400x300')
        self.__root.resizable(width=False, height=False)

        # -------------------
        btns1 = Tkinter.Button(self.__root, text ="选择目标资源文件夹", command = self.choiceDirectory)
        btns1.grid(column=1, row=1)
        E1 = Entry(self.__root, bd =5, textvariable=self.__var1)
        E1.grid(column=4, row=1)
        self.__var1.set("")
    
        # -------------------
        btns2 = Tkinter.Button(self.__root, text ="选择保存资源文件夹", command = self.saveDirectory)
        btns2.grid(column=1, row=2)
        E2 = Entry(self.__root, bd =5, textvariable=self.__var2)
        E2.grid(column=4, row=2)
        self.__var2.set("")

        

        # -------------------
        label3 = Tkinter.Label( self.__root, text = "导出资源名字" )
        label3.grid( column=1, row=3 )

        E3 = Entry(self.__root, bd =5, textvariable=self.__var3)
        E3.grid(column=4, row=3)
        self.__var3.set("test")

        # -------------------
        label4 = Tkinter.Label( self.__root, text = "字体偏移参数" )
        label4.grid( column=1, row=4 )

        E4 = Entry(self.__root, bd =5, textvariable=self.__var4)
        E4.grid(column=4, row=4)
        self.__var4.set("0")

        # -------------------
        btns3 = Tkinter.Button(self.__root, text ="导出", command = self.exportResource, width = 20, height = 2)
        btns3.grid(column=4, row=11)

        btns9 = Tkinter.Button(self.__root, text ="说明", command = self.explainCallback, width = 20, height = 2)
        btns9.grid(column=1, row=11)


        self.__IntVar = IntVar()
        self.__IntVar.set(2)

        label9 = Tkinter.Label( self.__root, text = "对齐方式：" )
        label9.grid( column=1, row=7 )

        r1 = Tkinter.Radiobutton(self.__root, text="顶端", variable=self.__IntVar, value=1)
        r2 = Tkinter.Radiobutton(self.__root, text="居中", variable=self.__IntVar, value=2)
        r3 = Tkinter.Radiobutton(self.__root, text="底部", variable=self.__IntVar, value=3)
        r1.grid(column=4, row=7)
        r2.grid(column=4, row=8)
        r3.grid(column=4, row=9)
    
        self.__root.mainloop()

# 主函数 -------------------------------------
if __name__ == '__main__': 
    # 初始化ui对象
    ui = Interface()
    ui.initUI()