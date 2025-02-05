import serial
import serial.tools.list_ports

class PiUSB():
    def __init__(self, timeout = 0.5):
        self.ports = {}
        for port in serial.tools.list_ports.comports():
            self.ports[port.device] = serial.Serial(port.device,timeout=timeout)
    
    def list_devices(self):
        devices = {}
        for port in self.ports:
            devices[port.device] = port.manufacturer

    def write(self, device, encoded_msg):
        code = self.ports[device].write(encoded_msg)
        return code
    
    def read(self, device):
        return self.ports[device].readlines()

if __name__=="__main__":
    pi = PiUSB()
    print(pi.list_devices())



        


