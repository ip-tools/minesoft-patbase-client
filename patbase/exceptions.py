# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>

class PatBaseException(Exception):
    pass

class PatBaseRequestError(PatBaseException):
    pass

class PatBaseLoginError(PatBaseException):
    pass

class PatBaseQueryError(PatBaseException):
    pass

class PatBaseResultError(PatBaseException):
    pass
