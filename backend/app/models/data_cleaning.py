import re

def data_cleaning(userTextInput):

    # matches and replaces anything that's not alphanumeric or underscore
    cleanString = re.sub(r'[^\w]', ' ', userTextInput)
    return cleanString


def isemail(email):

    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
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