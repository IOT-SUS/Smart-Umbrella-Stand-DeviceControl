#!/usr/bin/python

import time
import logging
import datetime
import RPi.GPIO as GPIO

from dateutil import parser

from lib.ip    import get_ip_and_wifi
from lib.servo import Servo
from lib.sonar import Sonar
from lib.MFRC522.rfid  import Rfid

from api.device import deviceAPI

MIN_DISTANCE = 40

class rentControl():
    @staticmethod
    def run(data):
        status, tagType = Main.myRfid.scanCard()
        if Main.myRfid.checkIsOk(status):
            logging.info('Card detected')

        status, rfid = Main.myRfid.getUID()
        if Main.myRfid.checkIsOk(status):
                    
            rrs_id  = data['public_id']
            user_id = data['user_id']

            data = {
                'rrs_id' : rrs_id, 
                'user_id': user_id,
                'rfid'   : rfid
            }
            logging.info(data)
            return deviceAPI.rentSuccess(data, rentControl.rentSucc, rentControl.rentFaild)
        return False

    @staticmethod
    def rentSucc(res):
        logging.info('Rent umbrella successfully.')
        return True

    @staticmethod
    def rentFaild(res):
        logging.info('Wrong umbrella RFID!')
        return False

    @staticmethod
    def pollingSucc(res):
        logging.info('Someone is renting umbrella :>')
        data = res.json()['data']

        expire_time = data['expire_time']
        expire_time = parser.parse(expire_time)

        # open door
        Main.myServo.open()
        # start rent control
        while datetime.datetime.now() < expire_time and rentControl.run(data) == False:
            time.sleep(0.5) 
        # close door
        Main.myServo.close()
        return True

    @staticmethod
    def pollingFaild(res):
        logging.info('Waiting someone to rent umbrella :D')
        return False

class returnControl():
    pre_distance = 1000

    @staticmethod
    def run(data):
        status, distance = Main.mySonar.getDistance()
        logging.info('distance: {}'.format(distance))
        if returnControl.pre_distance < MIN_DISTANCE and distance < MIN_DISTANCE:
            rrs_id = data['public_id']
            rfid   = returnControl.rfid

            data = {
                'rrs_id' : rrs_id,
                'rfid'   : rfid
            }
            logging.info(data)
            return deviceAPI.returnSuccess(data, returnControl.returnSucc, returnControl.returnFaild)
        
        # update pre distance
        returnControl.pre_distance = distance
        return False
    
    @staticmethod
    def returnSucc(res):
        logging.info('Return umbrella Successfully.')
        return True

    @staticmethod
    def returnFaild(res):
        logging.info('Return umbrella Faild.')
        return False

    @staticmethod
    def polling():
        status, tagType = Main.myRfid.scanCard()
        if Main.myRfid.checkIsOk(status):
            logging.info('Card detected')

        status, rfid = Main.myRfid.getUID()
        returnControl.rfid = rfid
        if Main.myRfid.checkIsOk(status):
            data = {'rfid': rfid}
            logging.info(data)
            deviceAPI.ureturn(data, returnControl.ureturnSucc, returnControl.ureturnFaild)
        
        logging.info('Waiting someone to return umbrella : (')
        return False

    @staticmethod
    def ureturnSucc(res):
        logging.info('Someone is returning umbrella :>')

        data = res.json()['data']
        
        expire_time = data['expire_time']
        expire_time = parser.parse(expire_time)

        # open door
        Main.myServo.open()
        # de noisy
        returnControl.pre_distance = 10000
        # start rent control
        while datetime.datetime.now() < expire_time and returnControl.run(data) == False:
            time.sleep(0.1)
        # close door
        Main.myServo.close()
        return True

    @staticmethod
    def ureturnFaild(res):
        logging.info('Worng RFID!!!')
        return False

class Main():
    @staticmethod
    def init():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        Main.myServo = Servo()
        Main.myRfid  = Rfid()
        Main.mySonar = Sonar()

    @staticmethod
    def updateDeviceStatus():
        data = get_ip_and_wifi()
        deviceAPI.updateDeviceStatus(data, Main.updateDeviceStatusSucc, Main.updateDeviceStatusFaild)
        return True
    
    @staticmethod
    def updateDeviceStatusSucc(res):
        return True

    @staticmethod
    def updateDeviceStatusFaild(res):
        return False

    @staticmethod
    def run():
        # Update Device Status
        Main.updateDeviceStatus()

        # Rent
        deviceAPI.polling(rentControl.pollingSucc, rentControl.pollingFaild)        

        # Retrun
        returnControl.polling()

if __name__ == '__main__':
    logging.basicConfig(
        level    = logging.INFO, 
        filemode = 'w',
        filename = 'log.txt',
        format   = '[%(asctime)s %(levelname)-8s] %(message)s',
        datefmt  = '%Y%m%d %H:%M:%S',
	)
    
    try:
        Main.init()
        while True:
            Main.run()
    except Exception as e:
        GPIO.cleanup()
        logging.info('Good Bye! :{}'.format(e))
