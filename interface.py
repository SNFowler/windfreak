import serial
import os

# Open the serial port manually
ser = serial.Serial('/dev/ttyACM0', timeout = 0.5)
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
    response = ser.readline()
    if response:
        print("Recieved:")
        while response:
            print(f"{response.decode()[:-1]}")
            response = ser.readline()
