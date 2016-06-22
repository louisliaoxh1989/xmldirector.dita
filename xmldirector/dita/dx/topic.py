# -*- coding: utf-8 -*-

# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
DITA Topic
"""


from zope.interface import implements
from plone.dexterity.content import Item
from plone.supermodel import model

from xmldirector.plonecore.i18n import MessageFactory as _

from xmldirector.plonecore.dx import dexterity_base
from xmldirector.plonecore.dx.xmlbinary_field import XMLBinary
from xmldirector.plonecore.dx.xmlimage_field import XMLImage
from xmldirector.plonecore.dx.xmltext_field import XMLText
from xmldirector.plonecore.dx.xmlxpath_field import XMLXPath


class ITopic(model.Schema):

    xml_content = XMLText(
        title=_(u'XML Content'),
        required=False
    )

class Topic(Item, dexterity_base.Mixin):

    implements(ITopic)
