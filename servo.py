import RPi.GPIO as GPIO

# Set the GPIO pin numbers for the servos
pan_pin = 18
tilt_pin = 17

# Set the PWM frequency for the servos
pwm_freq = 50

# Set the duty cycle range for the servos
duty_min = 2.5
duty_max = 12.5

# Initialize the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(pan_pin, GPIO.OUT)
GPIO.setup(tilt_pin, GPIO.OUT)

# Initialize the PWM objects for the servos
pan_pwm = GPIO.PWM(pan_pin, pwm_freq)
tilt_pwm = GPIO.PWM(tilt_pin, pwm_freq)

# Start the PWM signals with 0% duty cycle
pan_pwm.start(0)
tilt_pwm.start(0)

# Define a function to set the servo position
def set_servo_position(pwm, position):
    duty = (position / 180.0) * (duty_max - duty_min) + duty_min
    pwm.ChangeDutyCycle(duty)
    GPIO.wait_for_edge(pwm_pin, GPIO.RISING)

# Move the pan servo to the left
set_servo_position(pan_pwm, 0)

# Move the pan servo to the center
set_servo_position(pan_pwm, 90)

# Move the pan servo to the right
set_servo_position(pan_pwm, 180)

# Move the tilt servo up
set_servo_position(tilt_pwm, 0)

# Move the tilt servo to the center
set_servo_position(tilt_pwm, 90)

# Move the tilt servo down
set_servo_position(tilt_pwm, 180)

# Stop the PWM signals
pan_pwm.stop()
tilt_pwm.stop()

# Clean up the GPIO pins
GPIO.cleanup()
