
import machine
import utime as time
import micropython
micropython.alloc_emergency_exception_buf(100)

AEHA_FREQ = 38000
AEHA_HDR_MARK  = 3500
AEHA_HDR_SPACE = 1700
AEHA_MARK = 450
AEHA_ONE_SPACE  = 1300
AEHA_ZERO_SPACE = 400

class Transmitter:
    def __init__(self, pin=21):
        self._pin = machine.Pin(pin, machine.Pin.OUT)
        self._pwm = machine.PWM(self._pin, freq=AEHA_FREQ, duty=0)

    def _mark(self, us):
        self._pwm.duty(50)
        time.sleep_us(us)

    def _space(self, us):
        self._pwm.duty(0)
        time.sleep_us(us)

    def send(self, data):
        self._mark(AEHA_HDR_MARK)
        self._space(AEHA_HDR_SPACE)
        for octet in data:
            mask = 1 << 7
            while mask:
                if octet & mask :
                    self._mark(AEHA_MARK)
                    self._space(AEHA_ONE_SPACE)
                else:
                    self._mark(AEHA_MARK)
                    self._space(AEHA_ZERO_SPACE)
                mask >>= 1
        self._mark(AEHA_MARK)
        self._space(AEHA_ZERO_SPACE)
