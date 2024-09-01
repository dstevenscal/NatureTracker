import PIL.Image
import PIL.ExifTags
import pandas
import os
import shutil
import json
import requests
import datetime
from datetime import datetime
from datetime import timedelta

api_token = 'addtokenhere'
api_url_base = 'https://api.darksky.net/forecast/'

AllFiles = os.listdir('NewPic')
err = open('ErrorLog.txt','a')
err.write('FileName, ErrorDesc,DateTime \n')
err.close()
data = open('PhotoLatLong.txt','a')
data.write('FileName,DateTaken,Lat,Long,precipIntensity,PrecipProbability,temperature,apparentTemperature,dewPoint,humidity,pressure,windSpeed,windGust,windBearing,CloudCover,uvIndex,visibility,nearest-station \n')
a = datetime(1970,1,1,0,1,1)

path1 = 'NewPic/'
path2 = 'OldPic/'
listing = os.listdir(path1)
CurDate = str(datetime.now()).split('.')[0]
for x in AllFiles:
    if x.endswith(".JPG"):
        img = PIL.Image.open(path1+x)
        exif_data = img._getexif()
        FileName = x
        if 306 not in exif_data.keys():
            print(str(Filename)+' has no datetime stamp')
            with open('ErrorLog.txt','a') as err:
                err.write(str(FileName+', No Date found,'+CurDate+'\n'))
                err.close()
        else:
            DateTaken =   exif_data[306]
            ApiDate = DateTaken[:4]+'-'+DateTaken[5:7]+'-'+DateTaken[8:10]+'T'+DateTaken[11:19]
            FileDate = DateTaken[:4]+'-'+DateTaken[5:7]+'-'+DateTaken[8:10]+' '+DateTaken[11:19]
            b = datetime(int(DateTaken[:4]),int(DateTaken[5:7]),int(DateTaken[8:10]),int(DateTaken[11:13]),int(DateTaken[14:16]),int(DateTaken[17:20]))           
        newval = exif_data.get(34853)
        if 2 not in newval:
            with open('ErrorLog.txt','a') as err:
                err.write(str(FileName+', GPS info not found,'+str(datetime.now()).split('.')[0]+'\n'))
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
            api_url_latlon = str(latcoords) +','+str(longcoords)
            time = ',' +ApiDate
            response = requests.get(api_url_base+api_token+'/'+api_url_latlon+time)
            dataapi = json.loads(response.content.decode('utf-8'))
            TT = (b-a).total_seconds()
            T1 = dataapi['hourly']['data'][0]['time']
            T2 = dataapi['hourly']['data'][1]['time']
            T3 = dataapi['hourly']['data'][2]['time']
            T4 = dataapi['hourly']['data'][3]['time']
            T5 = dataapi['hourly']['data'][4]['time']
            d = {0:TT-T1, 1:TT-T2, 2:TT-T3, 3:TT-T4, 4:TT-T5}
            k = min(d.items(),key=lambda x: x[1])
            pi = str(dataapi['hourly']['data'][k[0]]['precipIntensity'])
            pp = str(dataapi['hourly']['data'][k[0]]['precipProbability'])
            t = str(dataapi['hourly']['data'][k[0]]['temperature'])
            at = str(dataapi['hourly']['data'][k[0]]['apparentTemperature'])
            dp = str(dataapi['hourly']['data'][k[0]]['dewPoint'])
            hum = str(dataapi['hourly']['data'][k[0]]['humidity'])
            pr = str(dataapi['hourly']['data'][k[0]]['pressure'])
            ws = str(dataapi['hourly']['data'][k[0]]['windSpeed'])
            wg = str(dataapi['hourly']['data'][k[0]]['windGust'])
            wb = str(dataapi['hourly']['data'][k[0]]['windBearing'])
            cc = str(dataapi['hourly']['data'][k[0]]['cloudCover'])
            uv = str(dataapi['hourly']['data'][k[0]]['uvIndex'])
            vi = str(dataapi['hourly']['data'][k[0]]['visibility'])
        with open('PhotoLatLong.txt','a') as data:
           data.write(str(FileName+','+str(FileDate)+','+str(latcoords)+','+str(longcoords)+','+pi+','+pp+','+t+','+at+','+dp+','+hum+','+pr+','+ws+','+wb+','+cc+','+uv+','+vi+'\n') )
           img.close()
           shutil.move(path1+x,path2+x)

           data.close()
