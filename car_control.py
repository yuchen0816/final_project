import pyb, sensor, image, time, math
enable_lens_corr = False

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
   return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

min_degree = 0
max_degree = 179
start = 1
line = 1
line_over = 0
apriltag = 1

while(start):
   clock.tick()
   img = sensor.snapshot()

   if (line == 1):
    for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
          if (min_degree <= l.theta()) and (l.theta() <= max_degree):
              img.draw_line(l.line(), color = (255, 0, 0))
              print(l.theta())
              line = 0

              if(l.theta()>90): ##turn left
                turn_degree = l.theta() -90
                print("turn left")
                turn_time = (turn_degree/90) * 3
                uart.write("/turn/run -50 -0.1 \n".encode())
                time.sleep(turn_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(3.5)
                uart.write("/stop/run \n".encode())
                line_over = 1
                start = 0
                uart.write("/stage1/run \n".encode())
              elif(l.theta()<90): ##turn right
                turn_degree = 90 - l.theta()
                print("trun right")
                turn_time = (turn_degree/90) * 4
                uart.write("/turn/run -50 0.1 \n".encode())
                time.sleep(turn_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(3.5)
                uart.write("/stop/run \n".encode())
                line_over = 1
                start = 0
                uart.write("/stage1/run \n".encode())

while(line_over):
   clock.tick()
   img = sensor.snapshot()

   if(apriltag == 1):
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        print(degrees(tag.y_rotation()))
        apriltag = 0

        ##turn right and turn left degrees 0~90
        if(degrees(tag.y_rotation()) < 90):
                print("turn right")
                turn_right_time = (degrees(tag.y_rotation())/90) * 4
                turn_left_time = (degrees(tag.y_rotation())/90) * 7.5
                uart.write("/turn/run -50 0.1 \n".encode())
                time.sleep(turn_right_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(1)
                uart.write("/turn/run -50 -0.1 \n".encode())
                time.sleep(turn_left_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(2)
                uart.write("/stop/run \n".encode())
                uart.write("/stage2/run \n".encode())
                time.sleep(10)
                uart.write("/turn/run -20 -0.1 \n".encode())
                time.sleep(6)
                uart.write("/stop/run \n".encode())
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(8)
                uart.write("/stop/run \n".encode())
                uart.write("/stage3/run \n".encode())
        ##turn left and turn right degrees 270~360
        elif(degrees(tag.y_rotation()) > 270):
                print("turn left")
                turn_right_time = ((360-degrees(tag.y_rotation()))/90) * 7.5
                turn_left_time = ((360-degrees(tag.y_rotation()))/90) * 4
                uart.write("/turn/run -50 -0.1 \n".encode())
                time.sleep(turn_left_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(1)
                uart.write("/turn/run -50 0.1 \n".encode())
                time.sleep(turn_right_time)
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(2)
                uart.write("/stop/run \n".encode())
                uart.write("/stage2/run \n".encode())
                time.sleep(10)
                uart.write("/turn/run -20 -0.1 \n".encode())
                time.sleep(6)
                uart.write("/stop/run \n".encode())
                uart.write("/goStraight/run -50 \n".encode())
                time.sleep(8)
                uart.write("/stop/run \n".encode())
                uart.write("/stage3/run \n".encode())
