import serial
import os
import stopit

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
    # Stopit is required here as there may be multiple lines.
    str = ''
    while True:
        with stopit.ThreadingTimeout(0.4) as timer:
            assert timer.state == timer.EXECUTING
            response = ser.readlines().decode()
        if timer.state == timer.EXECUTED:
            str += response
        else:
            break
    
    if str:
        print(f"Response: \n{str}")
