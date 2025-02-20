import serial
import serial.tools.list_ports

class PiUSB():
    def __init__(self, timeout = 0.5):
        self.ports = {}
        for port in serial.tools.list_ports.comports():
            self.ports[port.device] = (port.manufacturer, serial.Serial(port.device,timeout=timeout))
        
        print(self.ports)
    
    def list_devices(self):
        devices = {}
        for k,v in self.ports.items():
            print(f"{k}: {v[1]} {v[0]}")

    def write(self, device, encoded_msg):
        code = self.ports[device].write(encoded_msg)
        return code
    
    def read(self, device):
        return self.ports[device].readlines()

if __name__=="__main__":
    pi = PiUSB(timeout=0.5)
    print(pi.list_devices())
