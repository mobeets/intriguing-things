import json
import urllib2
import datetime
from time import mktime
from dateutil import parser
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://tinyletter.com/intriguingthings/letters/'
EXAMPLE_URL =  'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-146'
START_URL = 'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-like-a-dog-in-an-mri-machine'

def read(url):
    response = urllib2.urlopen(url)
    return response.read()

def parse(html):
    obj = BeautifulSoup(html).body
    dt = parser.parse(obj.find('div', attrs={'class': 'date'}).text.strip())
    contents = obj.find('div', attrs={'class': 'message-body'})
    next_url = obj.find('div', attrs={'class': 'paging'}).a.get('href')
    return dt, contents, next_url

class Thing:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.ps = []

    def __str__(self):
        ps = u'\n<br>'.join([p.decode('utf-8') for p in self.ps])
        return u'<a href="{0}">{1}</a>: {2}'.format(self.url, self.title, ps)

def things(obj):
    i = 1
    thing = None
    items = []
    has_number = lambda i, val: val.startswith('{0}.'.format(i))
    for p in obj.findChildren('p'):
        if p.text is not None and ((p.strong is not None and has_number(i, p.strong.text)) or has_number(i, p.text)):
            thing = Thing(p.a.text if p.a is not None else p.text.partition('. ')[-1], p.a.get('href') if (p.a is not None and p.a.has_key('href')) else '#')
        elif thing is not None and p.text == u'&nbsp;':
            items.append(thing)
            thing = None
            i += 1
            if i == 6:
                break
        elif thing is not None and p.text:
            thing.ps.append(str(p))
    if thing is not None:
        items.append(thing)
    return items

def fix_2014_06_06(html):
    html = html.replace('<div class="message-body">', '<div class="message-body"><p>')
    html = html.replace('<p>"Eating too fast', '</p><p>"Eating too fast')
    return parse(html)[1]

def load(url=EXAMPLE_URL):
    dt, contents, next_url = parse(read(url))
    if dt.strftime('%Y-%m-%d') == '2014-06-06':
        contents = fix_2014_06_06(read(url))
    return (dt, things(contents)), next_url

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        elif isinstance(obj, Thing):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

def write(T, outfile):
    with open(outfile, 'w') as f:
        json.dump(T, f, cls=MyEncoder)

def main(starturl=START_URL, outfile='tmp.json'):
    """
    * also want all hrefs in the entire html contents probably
    """
    T = []
    next_url = starturl
    while next_url and next_url != 'javascript:void(0)':
        next_url = BASE_URL + next_url.split('letters/')[1]
        print next_url
        ts, next_url = load(next_url)
        if len(ts) == 0 and dt.strftime('%Y-%m-%d') not in ['2014-06-06']:
            print 'ERROR: {0}'.format(dt)
        T.append(ts)
    write(T, outfile)

def tmp_main(outfile='tmp.json'):
    import glob
    import os.path
    T = []
    for infile in glob.glob('int_things_raw/*'):
        html = open(infile).read()
        dt, contents, next_url = parse(html)
        ts = things(contents)
        if len(ts) == 0:
            if dt.strftime('%Y-%m-%d') == '2013-12-17':
                ts = things(fix_2014_06_06(html))
            elif dt.strftime('%Y-%m-%d') == '2014-06-06':
                1/0 # pass
            else:
                print 'ERROR: {0}'.format(dt)
        T.append((dt, ts))
    write(T, outfile)

if __name__ == '__main__':
    tmp_main()
    # main()
