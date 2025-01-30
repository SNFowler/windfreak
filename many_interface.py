import serial
import serial.tools.list_ports
import os

class windfreak_manager():
    def __init__(self):
        self.windfreaks = {}
        self._refresh_wf_list()      
        self.display_windfreaks()

    def _refresh_wf_list(self):
        # Gets the currently connected windfreaks
        for port in serial.tools.list_ports.comports():
            # name of serial port
            name_ACM = port.device
            
            # open serial connection
            ser = serial.Serial(name_ACM, timeout = 0.5)
            
            # message the windfreak for its static ID
            ser.write("-".encode())
            device_id = ser.readline().decode()[:-1]
            self.windfreaks[device_id] = ser

    def display_windfreaks(self):
        print("Current ports:")
        for id in sorted(self.windfreaks.keys()):
            print(f"{id} \t (via {self.windfreaks[id].port})")
    
    def command(self, device_id, str_command):
        try:
            #send command to device, return the response
            ser = self.windfreaks[device_id]
            ser.write(user_input.encode()) 

            # get the returned response as a single string.
            response = ""
            current_line = ser.readline().decode()
            #Check for multiple return lines and add them to the response.
            if current_line:
                response += current_line
                current_line = ser.readline().decode()

            return response

        except:
            return f"Invalid command: {device_id}-'{str_command}'"
    
    def close_all(self):
        #closes everything
        for id in self.windfreaks.keys():
            self.windfreaks[id].close()
        

        
manager = windfreak_manager()
manager.display_windfreaks()

# Start a loop
while True:
    id          = input("Control which windfreak?")
    user_input  = input("Enter a string to send to the serial port (or 'q' to quit): ")

    if user_input.lower() == 'q':
        print("Exiting")
        break  # Exit the loop

    print(manager.command(id, user_input))

   
