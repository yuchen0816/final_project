# final_project

## stage 1
這一階段是讓車子自行跟隨直線前進，

由openmv偵測地上的直線，

得知旋轉的角度後，

再將控制車子的訊號傳送到板子上，

到達定位後用車上的xbee傳送"stage 1 completed"到電腦上的xbee。
## stage 2
這一階段是偵測某處的apriltag控制車子朝向apriltag移動，

由openmv偵測斜前方的apriltag，

得知車子到apriltag上y方向的旋轉角度，

接著再傳送控制車子的訊號，

到達定位後用車上的xbee傳送"stage 2 completed"到電腦上的xbee。
## stage 3
這一階段是讓車子轉九十度後直線前進，

直到ping測量距離小於五公分後停下，

到達定位後用車上的xbee傳送"stage 3 completed"到電腦上的xbee。

