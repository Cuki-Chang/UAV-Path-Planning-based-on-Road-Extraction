import cv2
from PIL import Image as ImagePIL
from PIL import Image
im = ImagePIL.open('I.JPG')
print(im)
print(type(im))
im = cv2.imread('I.JPG')

#image = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))  #格式转换，bgr转rgb
#image.save('qq1.jpg',quality=95,dpi=(1024.0,1024.0))    #调整图像的分辨率为300,dpi可以更改

#pic = im[0:1024,0:1024,:]
pic = im[0:1024,0:1024,:]

image = Image.fromarray(cv2.cvtColor(pic,cv2.COLOR_BGR2RGB))

#image.save('M.JPG')

image.save('out1024.JPG',quality=95,dpi=(72.0,72.0))    #调整图像的分辨率
