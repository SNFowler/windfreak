import serial
import os

class Windfreak:
    """
    A class for interfacing directly with the Windfreak

    @TODO convert commands to 
    """
    WF_COMMANDS = {
    # public name           (code,  writable, independent)                  
    "channel":                  ("C", True,  False),  # Control Channel: writable; global (one channel selected)
    "rf_frequency":             ("f", True,  True),   # RF Frequency: writable; independent per channel
    "rf_power":                 ("W", True,  True),   # RF Power: writable; independent per channel
    "rf_calibration":           ("V", False, False),  # Amp Calibration success: read-only; global
    "temp_comp_mode":           ("Z", True,  True),   # Temperature Compensation: writable; independent per channel
    "vga_dac":                  ("a", True,  True),   # VGA DAC Setting: writable; independent per channel
    "rf_phase_step":            ("~", True,  True),   # RF Phase Step: writable; independent per channel
    "rf_high_low":              ("h", True,  True),   # RF High/Low Power: writable; independent per channel
    "pll_chip_en":              ("E", True,  True),   # PLL Chip Enable: writable; independent per channel
    "pll_charge_pump":          ("U", False, True),   # PLL Charge Pump Current: read-only; independent per channel
    "ref_doubler":              ("b", True,  True),   # REF Doubler: writable; independent per channel
    "channel_spacing":          ("i", True,  True),   # Channel Spacing: writable; independent per channel
    "reference":                ("x", True,  False),  # Reference: writable; global
    "pll_reference":            ("*", True,  False),  # PLL Reference Frequency: writable; global
    "sweep_lower":              ("l", True,  True),   # Sweep Lower Frequency: writable; independent per channel
    "sweep_upper":              ("u", True,  True),   # Sweep Upper Frequency: writable; independent per channel
    "sweep_step_size":          ("s", True,  True),   # Sweep Step Size: writable; independent per channel
    "sweep_step_time":          ("t", True,  True),   # Sweep Step Time: writable; independent per channel
    "sweep_amp_low":            ("[", True,  True),   # Sweep Amplitude Low: writable; independent per channel
    "sweep_amp_high":           ("]", True,  True),   # Sweep Amplitude High: writable; independent per channel
    "sweep_direction":          ("^", True,  True),   # Sweep Direction: writable; independent per channel
    "sweep_diff_sep":           ("k", True,  False),  # Sweep Differential Separation: writable; global
    "sweep_diff":               ("n", True,  False),  # Sweep Differential Method: writable; global
    "sweep_type":               ("X", True,  True),   # Sweep Type: writable; independent per channel
    "sweep_run":                ("g", True,  False),  # Sweep Run: writable; global
    "sweep_continuous":         ("c", True,  False),  # Sweep Continuous Mode: writable; global
    "trigger":                  ("w", True,  False),  # Trigger Connector Function: writable; global
    "trigger_polarity":         ("Y", True,  False),  # Trigger Polarity: writable; global
    "am_step_time":             ("F", True,  False),  # AM Step Time: writable; global
    "am_cycles":                ("q", True,  False),  # AM Cycle Repetitions: writable; global
    "am_run":                   ("A", True,  False),  # AM Run Continuous: writable; global
    "pulse_on":                 ("P", True,  True),   # Pulse On Time: writable; independent per channel
    "pulse_off":                ("O", True,  True),   # Pulse Off Time: writable; independent per channel
    "pulse_repetitions":        ("R", True,  True),   # Pulse Repetitions: writable; independent per channel
    "pulse_invert":             (":", True,  True),   # Pulse Invert Signal: writable; independent per channel
    "pulse_run":                ("G", True,  False),  # Pulse Run one burst: writable; global
    "pulse_continuous":         ("j", True,  False),  # Pulse Continuous Mode: writable; global
    "fm_frequency":             ("<", True,  True),   # FM Frequency: writable; independent per channel
    "fm_deviation":             (">", True,  True),   # FM Deviation: writable; independent per channel
    "fm_repetitions":           (",", True,  True),   # FM Repetitions: writable; independent per channel
    "fm_type":                  (";", True,  True),   # FM Modulation Type: writable; independent per channel
    "fm_continuous":            ("/", True,  False),  # FM Continuous Mode: writable; global
    "phase_lock":               ("p", False, True),   # PLL Phase Lock Status: read-only; independent per channel
    "trigger_digital_status":   ("I", False, False),  # Trigger Digital Status: read-only; global
    "temperature":              ("z", False, False),  # Temperature: read-only; global
    "automatic_comm_mode":      ("m", True,  False),  # Automatic Communication Mode: writable; global
    "test_message":             ("T", True,  False),  # Send Test Message: writable; global
    "show_version":             ("v", False, True),   # Show Version: read-only; independent per channel
    "model_type":               ("+", False, False),  # Model Type: read-only; global
    "serial_number":            ("-", False, False),  # Serial Number: read-only; global
    "write_settings":           ("e", True,  False),  # Write settings to EEPROM: writable; global
    "help":                   	("?", False, False)   # Help: read-only; global    }
    }

    def __init__(self, USB_ACM, timeout=0.5):
        # Open the serial port manually
        self.ser = serial.Serial(USB_ACM, timeout = 0.5)
        #get serial number of device
        self.device_id = self.query("-")[:-1]

        print(f"Connected to {self.device_id} via {self.ser.name}")

        self.settings = {}
    
    def read(self):
        # Get the response from the serial port
        response = ""
        current_line = self.ser.readline()

        # The windfreak can output multiple lines.
        # Loop ends when the latest line is blank
        while current_line:
                response += self.ser.readline()
        return response 
    
    def write(self, user_input):
        return self.ser.write(user_input.encode())

    def query(self, user_input):
        self.write(user_input)
        return self.read     

    def close(self):
        self.ser.close()  
    
    def interactive_mode(self):
        # For debugging and testing purposes
        while True:
            user_input = input(f"Enter a string to send to {self.device_id} (or 'q' to quit): ")

            if user_input.lower() == 'q':
                print("Port will be closed.")
                break  # Exit the loop

            # Write user input to the serial port
            self.ser.write(user_input)  # .encode() to convert the string to bytes
            print(f"{self.ser.read(user_input)}")
    
    def summary(self):
        status = self.query("-".encode())

    def set_settings(self, settings_dict):
        pass

    def get_settings(self):
        # iterate through commands and provide the settings for those that can be changed
        for key, triple in self.WF_COMMANDS.items():
            if triple[1] and 


    def __getattr__(self, command):
        try:
            code = self.WF_COMMANDS[command]
            return code+"?"
        except:
            Exception("invalid recieve command")

    def __setattr__(self, command, value):
        try:
            code = self.WF_COMMANDS[command]
            return code+str(value)
        except:
            Exception("invalid command")

    def __del__(self):
        self.close()

if __name__=="__main__":
    wf = Windfreak("/dev/ttyACM0")
    wf.interactive_mode()
