# -*- coding: utf-8 -*-

# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
DITA Topic
"""


from zope.interface import implements
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.app.textfield import RichText

from xmldirector.plonecore.i18n import MessageFactory as _


class IContentFolder(model.Schema):
    pass


class ContentFolder(Container):
    implements(IContentFolder)
