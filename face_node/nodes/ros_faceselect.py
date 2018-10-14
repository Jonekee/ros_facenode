#!/usr/bin/env python
#-*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Int32

import time#导入python的time模块

import numpy as np  #导入python的numpy模块并更名为np
import cv2  #导入python的opencv模块

import os#导入python的os模块
command="fswebcam -d /dev/video0 -r 600*600 /home/pi/Desktop/photo.jpeg"
photo = "/home/pi/Desktop/photo.jpeg"
compare_photo =  "/home/pi/catkin_ws/src/face_node/photo/photo_compare.jpeg"
hf_alt2_xml = "/home/pi/catkin_ws/src/face_node/haarcascade_frontalface_alt2.xml"

# 您需要先注册一个App，并将得到的API key和API secret写在这里。
# You need to register your App first, and enter you API key/secret.
API_KEY = "yJL5Mw02ZohjfElqG9BUXVDftC2AS8lw"
API_SECRET = "whXnDdVyiu0V6hL3lgWJfw0nFDiADLRX"
# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat

def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))
	
# First import the API class from the SDK
# 首先，导入SDK中的API类
from face_node.facepp import API, File
#创建一个API对象，如果你是国际版用户，代码为：api = API(API_KEY, API_SECRET, srv=api_server_international)
#Create a API object, if you are an international user,code: api = API(API_KEY, API_SECRET, srv=api_server_international)
api = API(API_KEY, API_SECRET)

rospy.init_node('opencv_face_node')

pub = rospy.Publisher('topic_face', Int32, queue_size=3)

#下面进入拍照循环
while not rospy.is_shutdown():
    os.system(command)#执行command所代表的指令，即拍照
    time.sleep(2)#等待2s
	#下面是用opencv进行人脸识别，识别出有人脸才进行下一步人脸比较，否则一直拍照
    face_cascade = cv2.CascadeClassifier(hf_alt2_xml)
    # read image读取图像
    img = cv2.imread(photo)
    # Convert to grayscale转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect face Multiscale 检测面尺度
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  
    if faces!=():
        #利用face++的detectAPI识别刚刚拍摄的照片中的人脸，其实这句调试时能看到不少信息，方便些，可以省略
        detectresult=api.detect(api_key=API_KEY,api_secret=API_SECRET,image_file=File(photo))
        #将结果输出到打印到命令行界面上
        print_result('Detect result:', detectresult)
	#调用face++的compareAPI将拍到的照片与本地权限者照片做比较，confidence表示拍到的照片与本地权限者照片是同一人的置信度
        comparation=api.compare(api_key=API_KEY,api_secret=API_SECRET,image_file1=File(compare_photo),image_file2=File(photo))
        confidence=comparation['confidence']
        if confidence >= 70:
            pub.publish(1)
        else:
            pub.publish(2)
    else:
        print "No one"
		
