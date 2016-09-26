__author__ = 'MazeFX'

import xml.etree.ElementTree as Larch

larch = Larch.parse('resource.xml')
root = larch.getroot()

searchlist = []
searchstring = raw_input('What do you want to find?: ')

for child in root:
    code = child.get('ecode')
    if searchstring == code:
        print 'Supplement name: ' + code
        for name in child.findall('name'):
            nam = name.get('name')
            print 'Also known as: ' + nam

