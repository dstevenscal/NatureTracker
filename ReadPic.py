import PIL.Image
import PIL.ExifTags
import pandas
import os
import shutil
import datetime

AllFiles = os.listdir('NewPic')
err = open('ErrorLog.txt','a')
err.write('FileName, ErrorDesc,DateTime \n')
err.close()
data = open('PhotoLatLong.txt','a')
data.write('FileName,DateTaken,Lat,Long \n')

path1 = 'NewPic/'
path2 = 'OldPic/'
listing = os.listdir(path1)
for x in AllFiles:
    if x.endswith(".JPG"):
        img = PIL.Image.open(path1+x)
        exif_data = img._getexif()
        FileName = x
        if 306 not in exif_data.keys():
            print(str(Filename)+' has no datetime stamp')
            with open('ErrorLog.txt','a') as err:
                err.write(str(FileName+', No Date found,'+str(datetime.datetime.now()).split('.')[0]+'\n'))
                err.close()
        else:
            DateTaken =   exif_data[306]
        newval = exif_data.get(34853)
        if 2 not in newval:
            with open('ErrorLog.txt','a') as err:
                err.write(str(FileName+', GPS info not found,'+str(datetime.datetime.now()).split('.')[0]+'\n'))
                err.close()
        else:
            latdegs = exif_data[34853][2][0][0]
            latmins = exif_data[34853][2][1][0]
            latsecs = exif_data[34853][2][2][0]  / exif_data[34853][2][2][1]
            latcoords = latdegs + latmins/60 + latsecs/3600
            longdegs = exif_data[34853][4][0][0]
            longmins = exif_data[34853][4][1][0]
            longsecs = exif_data[34853][4][2][0]  / exif_data[34853][4][2][1]
            longcoords = longdegs + longmins/60 + longsecs/3600
            longcoords = longcoords * -1
        with open('PhotoLatLong.txt','a') as data:
           data.write(str(FileName+','+str(DateTaken)+','+str(latcoords)+','+str(longcoords)+'\n') )
           img.close()
           shutil.move(path1+x,path2+x)

           data.close()
