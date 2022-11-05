import re

def data_cleaning_without_space(userTextInput):

    # matches and replaces anything that's not alphanumeric without a space
    cleanString = re.sub(r'[^a-zA-Z0-9]+', '', userTextInput)
    return cleanString

def data_cleaning_with_space(userTextInput):

    # matches and replaces anything that's not alphanumeric with a space
    cleanString = re.sub(r'[^a-zA-Z0-9]+', ' ', userTextInput)
    return cleanString

def isstring(userTextInput):
    try:
        str(userTextInput)
        if userTextInput == "":
            return False

        return True
    except ValueError:
        return False

def isemail(email):

    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def isvalidpassword(password):

    # Make a regular expression
    # for validating password
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*?[#?!@$%^&*-])(?!.* ).{8,25}$"
    
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, password)):
        return True
    else:
        return False

def isvalidcontactnumber(contactNumber):

    if isstring(contactNumber):
        if isint(contactNumber):
            if len(str(contactNumber)) == 8:

                contactNumberStartingNumber = int(str(contactNumber)[0])
                if contactNumberStartingNumber == 9 or contactNumberStartingNumber == 8 or contactNumberStartingNumber == 6:
                    return True
    
    return False
    
def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

def isint(num):
        try:
            int(num)
            return True
        except ValueError:
            return False