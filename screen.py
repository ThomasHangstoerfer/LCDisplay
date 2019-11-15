# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#


class Screen(object):
    """docstring for Screen"""
    def __init__(self):
        #super(Screen, self).__init__()
        #self.arg = arg
        self.isVisible_ = False
        pass

    def setVisible(self, visible):
        print("Screen.setVisible(%s)" % visible)
        self.isVisible_ = visible
        self.update()

    def isVisible(self):
        return self.isVisible_

    def update(self):
        pass

    def key(self, event):
        print("Screen.key() " % event)
