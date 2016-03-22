from pyb import UART, micros
from pwm import ledpwm
from time import sleep
from seq_reader import sequence

adc1 = pyb.ADC('X22')

GreenF = 150
step = 0

pin = [

  	ledpwm('Y1',8,1,GreenF),
	ledpwm('Y6',1,1,GreenF), #inv
 	ledpwm('Y2',8,2,GreenF),
 	ledpwm('Y12',1,3,GreenF),
 	ledpwm('X3',9,1,GreenF),
 	ledpwm('X6',0,0,GreenF),
	ledpwm('X5',0,0,GreenF),
 	ledpwm('Y11',1,2,GreenF) #inv
]


def allPWM(value):
	for led in pin:
		led.pwm(value)

def setPWM(input):
    assert len(input) == 8

    for i,val in enumerate(input):
        out = val * 10
        if out == 90: out = 100
        pin[i].pwm(out)

allPWM(0)
i = 1
loop_strt = 0
onLoop = False
loop = -1
loopCount = 0

step_time = micros()
wait_for_trig = True

if __name__ == "__main__":

    seq = sequence()

    while True:
        if adc1.read() > 600:
            wait_for_trig = False
        if (micros() - step_time) >= 54000 and not wait_for_trig:
        #sleep( 0.054)
            step = seq.getStep(i).strip().replace(' ','')
            if step[:3] == "seq":
                if not onLoop:
                    loop_strt = i
                    onLoop = True
                    loopCount = 0
                elif onLoop:
                    i = loop_strt
                    loopCount += 1
                    if loopCount >= loop-1:
                        onLoop = False
                    wait_for_trig = True
            elif step[:4] == "loop":
                loop = int(step[5:])
            else:
                step = [int(pin) for pin in step]
                setPWM(step)
            print(loopCount, step)
            i += 1
            step_time = micros()
