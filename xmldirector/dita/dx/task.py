# -*- coding: utf-8 -*-

# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
DITA Task
"""


from zope.interface import implements
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.app.textfield import RichText

from xmldirector.plonecore.i18n import MessageFactory as _
from xmldirector.plonecore.dx import dexterity_base
from xmldirector.plonecore.dx.xmltext_field import XMLText


class ITask(model.Schema):

    body = RichText(
        title=_(u'Task content')
    )

    xml_body = XMLText(
        title=_(u'XML Content'),
        required=False
    )


class Task(Item, dexterity_base.Mixin):

    implements(ITask)
