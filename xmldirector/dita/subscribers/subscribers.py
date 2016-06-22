# -*- coding: utf-8 -*-

################################################################
# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from xmldirector.dita.html2dita import html2dita_lxml


def dita_modified(obj, event):
    language = obj.Language() or 'en'
    html = obj.body.raw
    obj.xml_set('xml_body', html2dita_lxml(
        html=html, 
        infotype=obj.infotype,
        lang=language))

