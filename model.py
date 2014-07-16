import glob
import json
import os.path
import urllib2
import argparse
import datetime
from time import mktime
from dateutil import parser
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://tinyletter.com/intriguingthings/letters/'
EXAMPLE_URL =  'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-146'
RESTART_URL = 'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-like-a-dog-in-an-mri-machine'
NEXT_URL = 'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-like-a-dog-in-an-mri-machine'

class Thing:
    def __init__(self, number, title, url):
        self.number = number
        self.title = title
        self.url = url
        self.ps = []
        self.src_url = None

    def __str__(self):
        ps = u'\n<br>'.join([p.decode('utf-8') for p in self.ps])
        return u'<a href="{0}">{1}</a>: {2}'.format(self.url, self.title, ps)

def read(url):
    response = urllib2.urlopen(url)
    return response.read()

def parse(html):
    obj = BeautifulSoup(html).body
    dt = parser.parse(obj.find('div', attrs={'class': 'date'}).text.strip())
    contents = obj.find('div', attrs={'class': 'message-body'})
    next_url = obj.find('a', attrs={'class': 'paging-button prev'})
    next_url = next_url.get('href') if next_url is not None else next_url
    return dt, contents, next_url

def things(obj, src_url):
    breaks = ["""1957 American English""", """Today's 1957""", """Tell Your Friends: Subscribe to 5 Intri""", """Did some good soul forward you this email?""", """Were you forwarded this email?""", """1957 English Usage""", """Subscribe to 5 Intriguing Things"""]
    i = 1
    thing = None
    items = []
    found_number = lambda i, val: val.startswith('{0}.'.format(i))
    has_number = lambda i, p: (p.strong is not None and found_number(i, p.strong.text)) or found_number(i, p.text)
    has_url = lambda p: p.a is not None and p.a.has_key('href')
    for p in obj.findChildren('p'):
        if p.text is None:
            continue
        if any([has_number(j, p) for j in xrange(i, i+2)]) and has_url(p): # for various numbering errors
            if thing is not None:
                items.append(thing)
                thing = None
            thing = Thing(i, p.a.text if p.a is not None else p.text.partition('. ')[-1], p.a.get('href'))
            thing.src_url = src_url
            i += 1
        elif thing is not None:
            if [brk for brk in breaks if brk in p.text]:
                if thing is not None:
                    items.append(thing)
                    thing = None
            else:
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
    return (dt, things(contents, url)), next_url

def write(T, outfile, merge):
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return int(mktime(obj.timetuple()))
            elif isinstance(obj, Thing):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)

    out = json.dumps(T, cls=MyEncoder)
    if merge and os.path.exists(outfile):
        with open(outfile) as f:
            out_p = json.load(f)
        out_c = []
        for x,y in json.loads(out) + out_p:
            if x not in out_c:
                out_c.append((x,y))
        out = out_c
    open(outfile, 'w').write(out)

def main(starturl, outfile, merge):
    """
    * want to store source url 
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
    write(T, outfile, merge)

def tmp_main(starturl, outfile, merge):
    T = []
    for infile in glob.glob('int_things_raw/*'):
        html = open(infile).read()
        dt, contents, _ = parse(html)
        src_url = infile.replace('___', '/').replace('int_things_raw/', '')
        ts = things(contents, src_url)
        if len(ts) == 0:
            if dt.strftime('%Y-%m-%d') == '2013-12-17':
                ts = things(fix_2014_06_06(html), src_url)
            elif dt.strftime('%Y-%m-%d') == '2014-06-06':
                pass
            else:
                print 'ERROR: {0}'.format(dt)
        T.append((dt, ts))
    write(T, outfile, merge)

if __name__ == '__main__':
    psr = argparse.ArgumentParser()
    psr.add_argument('--outfile', default='tmp.json')
    psr.add_argument('--restart', action='store_true', default=False)
    psr.add_argument('--local', action='store_true', default=False)
    psr.add_argument('--merge', action='store_true', default=False)
    args = psr.parse_args()
    if args.local:
        tmp_main(RESTART_URL if args.restart else NEXT_URL, args.outfile, args.merge)
    else:
        main(RESTART_URL if args.restart else NEXT_URL, args.outfile, args.merge)
