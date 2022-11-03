from datetime import datetime
from flask import jsonify
from flask import current_app as app
from ..models.user_model import User
from os import stat, remove
import os
import pyAesCrypt
import shutil
import logging
# function to log and return result
# note that all result that is an error should be a string containing the word "Error" at the start
# for ipAddress, if ngix is used for production, request.environ.get('HTTP_X_REAL_IP', request.remote_addr) should be used to get ip
# actionDescription will be used for logging purposes

def encrypt(key):

    #pyAesCrypt.encryptFile("recordc.log", "record.log.encrypted", key)
    #os.remove("record.log")
    #print("encrypting file")


    bufferSize = 64 * 1024
    with open("record.log", "rb") as fIn:
        with open("record.log.encrypted", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, str(key, 'utf-8'), bufferSize)

    logging.shutdown()
    remove('record.log')
def decrypt(key):
    #pyAesCrypt.decryptFile("record.log.encrypted", "recordc.log", key)

    bufferSize = 64 * 1024
    encFileSize = os.stat('record.log.encrypted').st_size


    with open("record.log.encrypted", "rb") as fIn:
        try:
            with open("record.log", "wb") as fOut:
                # decrypt file stream
                pyAesCrypt.decryptStream(fIn, fOut, str(key, 'utf-8'), bufferSize, encFileSize)
        except ValueError:
            # remove output file on error
            remove("record.log")


def return_result(ipAddress, actionDescription, functionCalled, result):
    
    print("----Log Test----")

    # who
    print("Who: {}".format(ipAddress))

    #what
    print("What: {}".format(actionDescription))

    #where
    print("Where: {}".format(functionCalled))

    #when
    now = datetime.now()
    print("When: {}".format(now))

    #result
    print("Result: {}".format(result))
    print("----------------")

    # checks if the result is an error result
    if type(result) == str and "Error" in result:
        return(jsonify(result), 401)

    # checks if the result is a exception
    elif type(result) == str and "Exception" in actionDescription:

        # loggerMessage = "{} ---- {} ---- {} ---- {}".format(ipAddress, actionDescription, functionCalled, result)
        
        # userModel = User()
        # # checks if the encrypted record exists before logging
        # if os.path.exists('record.log.encrypted'):
            

        #     if userModel.get_key() is not None:
        #         decrypt(userModel.get_key())
        #         app.logger.error(loggerMessage)
        #         encrypt(userModel.get_key())

        # else:
        #     app.logger.error(loggerMessage)
        #     encrypt(userModel.get_key())
        loggerMessage = "{} ---- {} ---- {} ---- {}".format(ipAddress, actionDescription, functionCalled, result)

        userModel = User()

        key = userModel.get_key()

        # # checks if the encrypted record exists before logging
        if os.path.exists('record.log.encrypted'):
            print("encrypt exist")

            # if key is not None:
            decrypt(key)
            app.logger.error(loggerMessage)
            encrypt(key)


        else:
            print("encrypt does not exist")
            app.logger.error(loggerMessage)

            # # Creates a new file
            # with open('recordc.log', 'w') as fp:
            #     pass
            # shutil.copyfile('record.log','recordc.log')

            encrypt(key)

            # f = open("record.log.encrypted", "r")
            # encrypted = f.read()
            # f.close()

            # f = open("record.log", "w")
            # f.write(encrypted)
            # f.close()
            # os.remove("record.log.encrypted")
            # os.remove("recordc.log")
        return(jsonify(result), 401)

    else:



        return(jsonify(result), 201) 