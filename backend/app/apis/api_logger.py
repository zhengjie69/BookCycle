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


    bufferSize = 64 * 1024
    with open("record.log", "rb") as fIn:
        with open("record.log.encrypted", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, str(key, 'utf-8'), bufferSize)

    logging.shutdown()
    #remove('record.log')

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

    #prints security logs
    now = datetime.now()
    timeformat = now.strftime("%Y-%m-%d %H:%M:%S")

    txt = "\nWhen: {}\nWhat: {}\nWhere: {}\nWho: {}\nResult: {}\n".format(timeformat,actionDescription,functionCalled,ipAddress,result)
    #txt = "What: {}".format(ipAddress)

    userModel = User()

    key = userModel.get_key()

    if os.path.exists('record.log.encrypted'):
        # if key is not None:
        decrypt(key)
        with open("record.log", "a") as file_to_write:
            file_to_write.write(txt)
        encrypt(key)


    else:
        with open("record.log", "a") as file_to_write:
            file_to_write.write(txt)
        encrypt(key)

    # checks if the result is an error result
    #prints app.logging.error
    if type(result) == str and "Error" in result:
        return(jsonify(result), 401)

    # checks if the result is a exception
    elif type(result) == str and "Exception" in actionDescription:


        # # checks if the encrypted record exists before logging
        if os.path.exists('record.log.encrypted'):
            # if key is not None:
            decrypt(key)
            app.logger.error(txt)
            encrypt(key)


        else:
            app.logger.error(txt)
            encrypt(key)

            # f = open("record.log.encrypted", "r")
            # encrypted = f.read()
            # f.close()

        return(jsonify(result), 401)

    else:



        return(jsonify(result), 201) 