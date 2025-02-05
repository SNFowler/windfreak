class TestWindfreak:
    """
    A class for interfacing directly with the Windfreak

    @TODO convert commands to 
    """
    COMMANDS = {
    "channel":            "C",   # Control Channel (A(0) or B(1))
    "rf_frequency":       "f",   # RF Frequency Now (MHz)
    "rf_power":           "W",   # RF Power (dBm)
    "rf_calibration":     "V",   # RF Calibration success?
    "temp_comp_mode":     "Z",   # Temperature Comp (0=none, 1=on set, 2=1sec, 3=10sec)
    "vga_dac":            "a",   # VGA DAC Setting [0,45000]
    "rf_phase_step":      "~",   # RF Phase Step (degrees)
    "rf_high_low":        "h",   # RF High (1) or Low (0) Power
    "pa":                 "r",   # PA On (1) or Off (0)
    "pll_chip_en":        "E",   # PLL Chip Enable On (1) or Off (0)
    "pll_output_power":   "I",   # PLL Output Power
    "pll_charge_pump":    "U",   # PLL Charge Pump Current
    "pll_mute":           "d",   # PLL Mute Till LD
    "muxout":             "m",   # Muxout function
    "autocal":            "T",   # Autocal On (1) or Off (0)
    "feedback_select":    "b",   # Feedback Select Fundamental (1) or Divided (0)
    "channel_spacing":    "i",   # Channel Spacing (Hz)
    "show_version":       "v",   # Show version (0=firmware, 1=hardware)
    "write_settings":     "e",   # Write all settings to EEPROM
    "reference":          "x",   # Reference (external=0, internal 27MHz=1, internal 10MHz=2)
    "trigger":            "w",   # Enable Trigger (0=software, 1=sweep, 2=step, 3=hold all)
    "sweep_lower":        "l",   # Sweep Lower Frequency (MHz)
    "sweep_upper":        "u",   # Sweep Upper Frequency (MHz)
    "sweep_step_size":    "s",   # Sweep Step Size (MHz)
    "sweep_step_time":    "t",   # Sweep Step Time (mS)
    "sweep_amp_low":      "[",   # Sweep Amplitude Low (dBm)
    "sweep_amp_high":     "]",   # Sweep Amplitude High (dBm)
    "sweep_direction":    "^",   # Sweep Direction (up=1, down=0)
    "sweep_diff_sep":     "k",   # Sweep Differential Frequency Separation (MHz)
    "sweep_diff":         "n",   # Sweep Differential (0=off, 1=ChA-DiffFreq, 2=ChA+DiffFreq)
    "sweep_type":         "X",   # Sweep Type (linear=0, tabular=1)
    "sweep_run":          "g",   # Sweep Run (on=1, off=0)
    "sweep_continuous":   "c",   # Sweep Set Continuous Mode
    "am_step_time":       "F",   # AM Step Time in microseconds
    "am_cycles":          "q",   # AM Number of Cycle Repetitions
    "am_run":             "A",   # AM Run Continuous (on=1, off=0)
    "am_lookup":          "@",   # Program AM Lookup Table
    "pulse_on":           "P",   # Pulse On Time (us)
    "pulse_off":          "O",   # Pulse Off Time (us)
    "pulse_repetitions":  "R",   # Pulse Number of Repetitions
    "pulse_invert":       ":",   # Pulse Invert Signal (on=1, off=0)
    "pulse_run":          "G",   # Pulse Run One Burst
    "pulse_continuous":   "j",   # Pulse Continuous Mode
    "pulse_dual":         "D",   # Pulse Dual Channel Mode
    "fm_frequency":       "<",   # FM Frequency (Hz)
    "fm_deviation":       ">",   # FM Deviation (Hz)
    "fm_repetitions":     ",",   # FM Number of Repetitions
    "fm_type":            ";",   # FM Type (sinusoid=1, chirp=0)
    "fm_continuous":      "/",   # FM Continuous Mode
    "phase_lock":         "p",   # Phase Lock Status (lock=1, unlock=0)
    "temperature":        "z",   # Temperature in degrees C
    "pll_reference":      "*",   # PLL Reference Frequency (MHz)
    "model_type":         "+",   # Model Type
    "serial_number":      "-",   # Serial Number
    "help":               "?"    # Help
    }

    def __getattr__(self, command):
        try:
            code = self.COMMANDS[command]
            return code+"?"
        except:
            Exception("invalid recieve command")

    def __setattr__(self, command, value):
        try:
            code = self.COMMANDS[command]
            return code+str(value)
        except:
            Exception("invalid command")

if __name__ == "__main__":
    test = TestWindfreak()

    print("Testing __getattr__ (receiving commands):")
    for command in TestWindfreak.COMMANDS:
        try:
            # Access the attribute to simulate a "get" operation
            result = test.command()
            print(f"{command} -> {result}")
        except Exception as e:
            print(f"Error retrieving {command}: {e}")

    print("\nTesting __setattr__ (sending commands):")
    # For testing, we'll simulate setting each command to a sample value (e.g., 123)
    for command in TestWindfreak.COMMANDS:
        try:
            # __setattr__ in this test class doesn't actually store a value;
            # it simply returns the formatted command string.
            result = test.__setattr__(command, 123)
            print(f"Setting {command} to 123 -> {result}")
        except Exception as e:
            print(f"Error setting {command}: {e}")
