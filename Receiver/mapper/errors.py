class WrongTrashField(Exception):
    info = 'Wrong trash fields setup.\nReturned data cannot be represented as list of dictionaries.'


class WrongContent(Exception):
    info = 'Unsupported input data format.'
