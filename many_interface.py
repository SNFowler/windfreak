import serial
import serial.tools.list_ports
import os
import json


"""
@TODO write a generic settings file. Apply.
@TODO think about Send/Recieve. Do these need to be 2 functions or could the SCPI server code handle converting send/recieve commands and both of them be handled by the same method in this class? 
@TODO load and apply the settings file.

Ability to give windfreaks "nicknames" was removed for now, as it added a lot of code. 
"""

class windfreak_manager():
    def __init__(self, config_path = "config/default.json"):
        # load default settings
        #self.config_path = config_path    
        self.config = None
        self.windfreaks = {}
        
        # load settings
        #self.load_config()
        
        # Windfreak serials are indexed by static device ID (1182)
        self._refresh_wf_list()

        # apply settings   
        self.display_windfreaks()


        # things to summarise
        # Name, command
        self.summary_stats = {

        }

    def send(self, device_id, str_command):
        try:
            #send command to device, return the response (appears to usually just be a 1 or 0)
            ser = self.windfreaks[device_id]
            success_code = ser.write(user_input.encode())

        except:
            raise Exception(f"Invalid command: {device_id} -'{str_command}'")
    
    def recieve(self, device_id, str_command):
            self.send(device_id, str_command)
            # get the returned response as a single string.
            ser = self.windfreaks[device_id]
            response = ""
            current_line = ser.readline().decode()
            #Check for multiple return lines and add them to the response.
            if current_line:
                response += current_line
                current_line = ser.readline().decode()

            return response

    def recall(self, custompath=None):
        # loads the config file specified by the path. If no path is provided, the current previously used configpath is used.
        if custompath: self.configpath = custompath
        with open(self.configpath, 'r') as file:
            self.config = json.load(file)

    def store(self, custompath=None):
        # saves the current config to custompath. If no path is provided, the current config file is overriden
        if custompath: self.configpath = custompath
        with open(self.configpath, "w") as outfile:
            outfile.write(self.config)
    
    def load_config(self):
        assert self.config_path
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)

        except Exception as e:
            raise Exception("Loading config failed:") from e
        return config

    def _refresh_wf_list(self):
        # gets the currently connected windfreaks
        for port in serial.tools.list_ports.comports():
            # name of serial port
            name_ACM = port.device
            
            # open serial connection
            ser = serial.Serial(name_ACM, timeout = 0.5)
            
            # message the windfreak for its static ID
            ser.write("-".encode())
            device_id = ser.readline().decode()[:-1]
            self.windfreaks[device_id] = ser

            # if the windfreak was given a shorter name in settings, also add an entry for that shorter  
    
    def close_all(self):
        #closes everything
        for id in self.windfreaks.keys():
            self.windfreaks[id].close()

    def display_windfreaks(self):
        print("Current ports:")
        for id in sorted(self.windfreaks.keys()):
            print(f"{id} \t (via {self.windfreaks[id].port})")
    
    def status(self, verbose=False):
        for id in sorted(self.windfreaks.keys()):
            ser = self.windfreaks[id]
            # send a request to the windfreak for current status
            ser.write("?".encode())
            status = ""
            while True:
                # continue reading in until entire status is done.
                current = ser.readline().decode()

                # add recently read line to status.
                status += current
                if not current:
                    break

if __name__ == "__main__":        
    manager = windfreak_manager()

    # Start a loop
    while True:
        id          = input("Control which windfreak?")
        user_input  = input("Enter a string to send to the serial port (or 'q' to quit): ")

        if user_input.lower() == 'q':
            print("Exiting")
            break  # Exit the loop

        print(manager.recieve(id, user_input))

   
