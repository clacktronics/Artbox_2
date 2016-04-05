from pyb import UART, millis
from pwm import ledpwm
from time import sleep
from seq_reader import sequence

adc1 = pyb.ADC('X22')

GreenF = 150
step = 0


hi = 400
mid = 100
bass = 50
kick = 25

pin = [

  	ledpwm('Y1',8,1,kick),
	ledpwm('Y6',1,1,hi), #inv
 	ledpwm('Y2',8,2,mid),
 	ledpwm('Y12',1,3,bass),
 	ledpwm('X3',9,1,kick),
 	ledpwm('X6',0,0,hi),
	ledpwm('X5',0,0,mid),
 	ledpwm('Y11',1,2,bass) #inv
]


def allPWM(value):
	for led in pin:
		led.pwm(value)

def setPWM(input):
    global trigcheck
    global trig_time

    for i,val in enumerate(input):
        out = int(val) * 10
        if out == 90: out = 100
        pin[i].pwm(out)

        # As its slow check for more triggers whilst writing pins
        if adc1.read() > 50 and (millis() - trig_time) >= 500:
            trigcheck = True
            print('blip')
            trig_time = millis()
            return

allPWM(0)
i = 1
loop_strt = 0
onLoop = True
loop = -1
loopCount = 0
played = 0
sname = 'not set'

step_time = millis()
trig_time = millis()
wait_for_trig = True
trigcheck = False

if __name__ == "__main__":

    start = pyb.micros()

    seq = sequence()

    while True:

        if adc1.read() > 50 and (millis() - trig_time) >= 600 or trigcheck:
            wait_for_trig = False

            loopCount+=1

            if loopCount >= loop:
                onLoop = False
                loopCount = 0

            if onLoop:
                i = loop_strt+1
                print("%d of %d" % (loopCount+1, loop))
            else:
                step = seq.getStep(i).replace(' ','')[:-1]
                print('x', end="")
                while step[:3] != "seq":
                    i+=1
                    step = seq.getStep(i).replace(' ','')[:-1]
                    #print('seek',i)
                sname = step
                loop_strt = i
                onLoop = True
                i+=1
                print(sname)

            trigcheck = False
            trig_time = millis()


        if pyb.elapsed_micros(start) >= 55700 and not wait_for_trig:

            step = seq.getStep(i).replace(' ','')[:-1]

            if step[:3] == "seq":
                wait_for_trig = True
                #sname = step
                continue

            elif step[:4] == "loop":
                loop = int(step[5:])
                i += 1
                continue

            else:
                #print(i,loop,sname,step)
                setPWM(step)
                i += 1
                start = pyb.micros()
