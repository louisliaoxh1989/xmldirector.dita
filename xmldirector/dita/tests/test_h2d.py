# -*- coding: utf-8 -*-

################################################################
# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from xmldirector.dita.html2dita import html2dita_lxml
from xmldirector.dita.html2dita import html2dita_saxon


def test_html2dita_lxml():
    html = u'<div><h1>Überschrift üöäß</h1></div>'
    output = html2dita_lxml(html)
    assert u'Überschrift üöäß' in output

def test_html2dita_saxon():
    html = u'<div><h1>Überschrift üöäß</h1></div>'
    output = html2dita_saxon(html)
    assert u'Überschrift üöäß' in output

