# coding: utf-8
class WrongInput(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class DuplicateValue(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class MissingParam(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
