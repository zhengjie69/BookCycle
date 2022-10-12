import re

def data_cleaning(userTextInput):

    # matches and replaces anything that's not alphanumeric or underscore
    cleanString = re.sub(r'[^\w]', '', userTextInput)
    return cleanString