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
RESTART_URL = 'http://tinyletter.com/intriguingthings/letters/5-intriguing-things-like-a-dog-in-an-mri-machine'

class Thing:
    def __init__(self, number, title, url, src_url):
        self.number = number
        self.title = title
        self.url = url
        self.ps = []
        self.src_url = src_url

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
    breaks = ["""Subscribe to The Newsletter""", """1957 American English""", """Today's 1957""", """Tell Your Friends: Subscribe to 5 Intri""", """Did some good soul forward you this email?""", """Were you forwarded this email?""", """1957 English Usage""", """Subscribe to 5 Intriguing Things"""]
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
            thing = Thing(i, p.a.text if p.a is not None else p.text.partition('. ')[-1], p.a.get('href'), src_url)
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

def load(url):
    dt, contents, next_url = parse(read(url))
    if dt.strftime('%Y-%m-%d') == '2014-06-06':
        contents = fix_2014_06_06(read(url))
    return (dt, things(contents, url)), next_url

def write(T, Tp0, outfile):
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return int(mktime(obj.timetuple()))
            elif isinstance(obj, Thing):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)

    Tp_str = json.dumps(T, cls=MyEncoder)
    if Tp0:
        dts = [dt for dt, ts in Tp0]
        Tp = [(dt, ts) for dt, ts in json.loads(Tp_str) if dt not in dts]
        Tp_str = json.dumps(Tp0 + Tp, cls=MyEncoder)
    open(outfile, 'w').write(Tp_str)

def io(starturl, outfile, Tp0):
    T = []
    next_url = starturl
    while next_url and next_url != 'javascript:void(0)':
        next_url = BASE_URL + next_url.split('letters/')[1]
        print next_url
        ts, next_url = load(next_url)
        if len(ts) == 0 and dt.strftime('%Y-%m-%d') not in ['2014-06-06']:
            print 'ERROR: {0}'.format(dt)
        T.append(ts)
    write(T, Tp0, outfile)

def local_io(starturl, outfile, Tp0, srcdir):
    """
    use html files stored in srcdir, for testing locally
    """
    T = []
    url_to_filename = lambda url: os.path.join(srcdir, url.replace('/', '___'))
    filename_to_url = lambda fn: fn.replace('___', '/').replace(srcdir + '/', '')

    next_url = starturl
    while next_url and next_url != 'javascript:void(0)':
        next_url = BASE_URL + next_url.split('letters/')[1]
        infile = url_to_filename(next_url)
        print infile
        if 'int_things_raw/http:______tinyletter.com___intriguingthings___letters___5-intriguing-things-142' == infile:
            break
        html = open(infile).read()
        dt, contents, new_url = parse(html)
        ts = things(contents, next_url)
        if len(ts) == 0:
            if dt.strftime('%Y-%m-%d') == '2013-12-17':
                ts = things(fix_2014_06_06(html), next_url)
            elif dt.strftime('%Y-%m-%d') == '2014-06-06':
                pass
            else:
                print 'ERROR: {0}'.format(dt)
        T.append((dt, ts))
        next_url = new_url
    write(T, Tp0, outfile)

def load_old_and_start_url(infile):
    if os.path.exists(infile):
        with open(infile) as f:
            Tp0 = json.load(f)
            last_url = Tp0[-1][1][0].get('src_url', None)
            return Tp0, last_url
    return [], None

def main(infile, outfile, srcdir=None):
    Tp0, starturl = load_old_and_start_url(infile)
    if starturl is None:
        starturl = RESTART_URL
    if srcdir:
        local_io(starturl, outfile, Tp0, srcdir)
    else:
        io(starturl, outfile, Tp0)

"""
To do:

# https://github.com/ryandotsmith/null-buildpack

try to get 'heroku run ___' to work!

    1. heroku scheduler # https://devcenter.heroku.com/articles/scheduler
    2. heroku config vars to store key # http://stackoverflow.com/questions/14177039/how-to-store-private-key-on-heroku 
    3. paging, i.e. handling too much data (n.b. this will require adding search functionality)
"""
if __name__ == '__main__':
    psr = argparse.ArgumentParser()
    psr.add_argument('--infile', default='')
    psr.add_argument('--outfile', required=True, default='tmp.json')
    psr.add_argument('--srcdir', default=None)
    args = psr.parse_args()
    main(args.infile, args.outfile, args.srcdir)
