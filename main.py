from machine import  Pin, ADC, PWM
import  time

pwm0 = PWM(Pin(21))
#p1 = Pin(4, Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(22))
while True:
    val = adc.read_uv()
    print(val)
    pwm0.duty(val/1000)
#    time.sleep_ms(1000)
