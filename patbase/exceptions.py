# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>

class PatBaseException(Exception):
    pass

class PatBaseInvalidRequest(PatBaseException):
    pass

class PatBaseLoginFailed(PatBaseException):
    pass

class PatBaseInvalidFormat(PatBaseException):
    pass
