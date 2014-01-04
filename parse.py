from HTMLParser import HTMLParser
import urllib2, sys, re

class WikipediaRacer(HTMLParser):
    
    allSeen = dict()
    nowSeen = set()
    endPage = ''
    getCount = 0

    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
            for attr in attrs:
                if (attr[0] == 'href'):
                    if (re.match('/wiki/(?!.*:|Main_Page)',attr[1])):
                        url = attr[1]
                        url = url.replace('/wiki/','')
                        self.nowSeen.add(url)
                        
    def startSearch(self, startPage, endPage):
        print "Search started for: " + startPage + " -> " + endPage
        thisRun = {startPage}
        self.allSeen[startPage] = 'root'
        nextRun = set()
        count = 1
        while (True):
            for runUrl in thisRun:
                self.getUrls(runUrl)
                print self.getPath(runUrl)
                for seenUrl in self.nowSeen:
                    if (seenUrl not in self.allSeen):
                        self.allSeen[seenUrl] = runUrl
                        if (seenUrl == endPage):
                            print str(len(self.allSeen))+' urls checked'
                            print self.getPath(seenUrl)
                            return
                        else:
                            nextRun.add(seenUrl)
            count = count+1
            thisRun = nextRun
            nextRun = set()
        
    def getUrls(self, pageName):
        url = 'http://en.wikipedia.org/wiki/'+pageName
        self.getCount = self.getCount+1
        print "Getting page #"+str(self.getCount)+": "+pageName
        resp = urllib2.urlopen(url)
        self.nowSeen = set()
        html = resp.read()
        html = html.decode('ascii',errors='ignore')
        self.feed(html)

    def getPath(self, pageName):
        if (pageName in self.allSeen):
            path = pageName
            parent = self.allSeen[pageName]
            while (parent != 'root'):
                path = parent+' -> '+path
                pageName = parent
                parent = self.allSeen[pageName]
        else:
            path = 'X -> '+pageName

        return path

if __name__ == '__main__':
    racer = WikipediaRacer()
    racer.startSearch(sys.argv[1], sys.argv[2])
