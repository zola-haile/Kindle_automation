import serial
import time
portName='/dev/tty.usbmodem2101'
def moveServo(portName):

    # Establish a connection with the Arduino (adjust 'COM3' to your port)
    arduino = serial.Serial(port=portName, baudrate=9600, timeout=1)

    def send_angle(angle):
        # Send the angle to Arduino as a string
        arduino.write(f'{angle}\n'.encode())


    time.sleep(2)  # Give time for the serial connection to initialize

    # Send 90 degrees to the Arduino
    send_angle(90)
    time.sleep(1)  # Wait for the servo to move

    # Send 180 degrees to the Arduino
    send_angle(180)
    time.sleep(1)  # Wait for the servo to move

    # Close the serial connection
    arduino.close()
