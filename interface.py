import serial
import os
import stopit

# A decorated read line function that won't run forever if there is no EOL character
@stopit.threading_timeoutable(default='')
def safe_read_line(serial_port):
    return serial_port.readline().decode()

# Open the serial port manually
ser = serial.Serial('/dev/ttyACM0')
print(f"Connected to {ser.name}")

# Start a loop
while True:
    user_input = input("Enter a string to send to the serial port (or 'q' to quit): ")

    if user_input.lower() == 'q':
        print("Port will be closed.")
        break  # Exit the loop

    # Write user input to the serial port
    ser.write(user_input.encode())  # .encode() to convert the string to bytes
    print(f"Sent: {user_input}")

    # Get the response from the serial port
    # readline will not stop reading until it encounters "\n" as the end of line character. This is a problem if there is nothing on the serial port.
    response = safe_read_line(ser, timeout=1)
    if response:
        print("Recieved:")
        while response != 'EOM.\n' and response != '':
            print("next line read\n")
            print(f"{response[:-1]}")
            response = safe_read_line(ser, timeout=1)
