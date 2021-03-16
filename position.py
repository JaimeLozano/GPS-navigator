import os
import io
import pynmea2
import serial

def cls():
    os.system('cls' if os.name =='nt' else 'clear')
    
class Position:
    def __init__(self):
        self.timestamp = 0
        self.datetime = 0
        self.status = 0
        self.latitude = 0
        self.longitude = 0
        self.lon_dir = 0
        self.spd_over_grnd = 0
        self.mag_variation = 0
        self.mag_var_dir = 0
        self.num_sv_in_view = 0
        self.sv_prn_num_1 = 0
        self.altitud = 0
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1.0)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    def updatePosition(pos):
        try:
            line = pos.sio.readline()
            msg = pynmea2.parse(line)
            
            if (msg.sentence_type == 'RMC'):
                pos.timestamp = msg.timestamp
                pos.datetime = msg.datetime
                pos.status = msg.status
                pos.latitude = msg.latitude
                pos.longitude = msg.longitude
                pos.lon_dir = msg.lon_dir
                pos.spd_over_grnd = msg.spd_over_grnd
                pos.mag_variation = msg.mag_variation
                pos.mag_var_dir = msg.mag_var_dir
                return True
                
            if (msg.sentence_type == 'GSV'):
                pos.num_sv_in_view = msg.num_sv_in_view
                pos.sv_prn_num_1 = msg.sv_prn_num_1

            if (msg.sentence_type == 'GGA'):
                pos.altitud = msg.altitude
                    
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
        except AttributeError as e:
            print('Attribute error: {}'.format(e))
    
    def printData(pos):
        # Clear screen
        cls()
        print(str('UTC: ') + str(pos.timestamp))
        print(str('Fecha: ') + str(pos.datetime))
        print(str('Position status: ') + str(pos.status))
        print(str('Latitud: ') + str(pos.latitude))
        print(str('Longitud: ') + str(pos.longitude))
        print(str('Dirección de la Lat y Lon: ') + str(pos.lon_dir))
        print(str('Speed over ground: ') + str(pos.spd_over_grnd))
        print(str('Declinación magnética: ') + str(pos.mag_variation))
        print(str('Dirección de la dec.mag.: ') + str(pos.mag_var_dir))
        print(str('Nº satélites recibidos: ') + str(pos.num_sv_in_view))
        print(str('PRN1: ') + str(pos.sv_prn_num_1))
        print(str('Altitud: ') + str(pos.altitud))
