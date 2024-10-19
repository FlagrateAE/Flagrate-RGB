from serial import Serial
import time

class Arduino(Serial):
    def __init__(self, port: str):
        """Initialize serial connection to Arduino
        
        Parameters
        ----------
        port : str
            Serial port name (COM* for Windows, /dev/tty* for Linux)
        """
        
        super().__init__(port=port, baudrate=9600, bytesize=8, parity="N", stopbits=1)
        
        time.sleep(2)
        print("Arduino connected")
    
    def send(self, data: str):
        """Send text data to Arduino via serial
        
        Parameters
        ----------
        data : str
        Text data to be sent"""
        self.write(bytes(data, 'utf-8'))
    
    def receive(self):
        """
        This funcion is a stub
        """
        return self.readline()
    
