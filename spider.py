from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


fwrite = open("test",'w')

'''def WriteToXml(smoviedetails):
    movdetails = {}
    if('Banner' in smoviedetails):
        smoviedetails = filter(lambda a: a != ' ' and a != ', ',smoviedetails)
        i = 0
        length = len(smoviedetails)
        while(i< length):
            if(i+1 < length):
                smoviedetails[i+1] = smoviedetails[i+1].replace('\n','')
                smoviedetails[i+1] = smoviedetails[i+1].replace(':','')

            if('banner' == smoviedetails[i].lower()):
                movdetails['banner'] = smoviedetails[i+1]
            if('starring' == smoviedetails[i].lower()):
                movdetails['starring'] = []
                i = i+1
                while(smoviedetails[i].lower() != 'producer'):
                    movdetails['starring'].append(smoviedetails[i])
                    i = i+1
                i = i-1
            if('producer' == smoviedetails[i].lower()):
                movdetails['producer'] = smoviedetails[i+1]
            if('director' == smoviedetails[i].lower()):
                movdetails['director'] = smoviedetails[i+1]
            if('story' == smoviedetails[i].lower()):
                movdetails['story'] = smoviedetails[i+1]
            if('screenplay' == smoviedetails[i].lower()):
                movdetails['screenplay'] = smoviedetails[i+1]
            if('dialogues' == smoviedetails[i].lower()):
                movdetails['dialogues'] = smoviedetails[i+1]
            if('music director' == smoviedetails[i].lower()):
                movdetails['music director'] = smoviedetails[i+1]
            if('cinematographer' == smoviedetails[i].lower()):
                movdetails['cinematographer'] = smoviedetails[i+1]
            if('choreographer' == smoviedetails[i].lower()):
                movdetails['choreographer'] = smoviedetails[i+1]
            if('art director' == smoviedetails[i].lower()):
                movdetails['art director'] = smoviedetails[i+1]
            if('stunts' == smoviedetails[i].lower()):
                movdetails['stunts'] = smoviedetails[i+1]
            if('editor' == smoviedetails[i].lower()):
                movdetails['editor'] = smoviedetails[i+1]
            if('singers' == smoviedetails[i].lower()):
                movdetails['singers'] = smoviedetails[i+1]
            if('lyrics' == smoviedetails[i].lower()):
                movdetails['lyrics'] = smoviedetails[i+1]
            if('audio' == smoviedetails[i].lower()):
                movdetails['audio'] = smoviedetails[i+1]
            if('release date' == smoviedetails[i].lower()):
                movdetails['release date'] = smoviedetails[i+1]
            i = i + 1

        print movdetails
        #smoviedetails.remove(", ")
        #smoviedetails.remove(' ')
        #print len(smoviedetails)
        #fwrite.write(smoviedetails)
    fwrite.write("\n")'''
def GetElement(smoviedetails,movdetails,current,next):
        length = len(smoviedetails)
        i = 0
        try:
            while(i< length):
                if(current == smoviedetails[i].lower()):
                    movdetails[current] = []
                    if(next == ''):
                        movdetails[current].append(smoviedetails[i+1])
                        return
                    i = i+1
                    while(smoviedetails[i].lower() != next):
                        movdetails[current].append(smoviedetails[i])
                        i = i + 1
                    return
                i = i + 1
        except (RuntimeError, TypeError, IndexError):
            return

def WriteToXml(smoviedetails,filename):
    movdetails = {}

    fwritetext = open('2000/'+filename,'w')

    if('Banner' in smoviedetails):
        smoviedetails = filter(lambda a: a != ' ' and a != ', ',smoviedetails)
        GetElement(smoviedetails,movdetails,'banner','starring')
        GetElement(smoviedetails,movdetails,'starring','producer')
        GetElement(smoviedetails,movdetails,'producer','director')
        GetElement(smoviedetails,movdetails,'director','story')
        GetElement(smoviedetails,movdetails,'story','screenplay')
        GetElement(smoviedetails,movdetails,'screenplay','dialogues')
        GetElement(smoviedetails,movdetails,'dialogues','music director')
        GetElement(smoviedetails,movdetails,'music director','cinematographer')
        GetElement(smoviedetails,movdetails,'cinematographer','choreographer')
        GetElement(smoviedetails,movdetails,'choreographer','art director')
        GetElement(smoviedetails,movdetails,'art director','stunts')
        GetElement(smoviedetails,movdetails,'stunts','editor')
        GetElement(smoviedetails,movdetails,'editor','singers')
        GetElement(smoviedetails,movdetails,'singers','lyrics')
        GetElement(smoviedetails,movdetails,'lyrics','audio')
        GetElement(smoviedetails,movdetails,'audio','release date')
        GetElement(smoviedetails,movdetails,'release date','')
        #print movdetails
    for key in movdetails:
        #print key
        fwritetext.write(key)
        fwritetext.write(':\t')
        templist = movdetails[key]
        for tlist in templist:
            tlist = tlist.replace(':','')
            tlist = tlist.replace('\n','')
            fwritetext.write(tlist)
        fwritetext.write('\n')

    fwritetext.close()

class ImdbSpider(BaseSpider):
    name = "imdbcrawler"
    allowed_domains = ["telugupedia.com"]
    start_urls = ['http://www.telugupedia.com/wiki/index.php?title=Films_Released_in_2000']#["http://www.telugupedia.com/wiki/index.php?title=Bumper_Offer_Telugu_Movie"]
    '''rules = (
            Rule(SgmlLinkExtractor(allow=''),callback='parse',cb_kwargs={'depth':0},follow=True,),
            );'''

    def parse_movie(self,response,filename):
    	hxs = HtmlXPathSelector(response)
        ulist = hxs.select('//ul')
    	WriteToXml(ulist[0].select('li//text()').extract(),filename)
            #break
    def parse(self,response):
        hxs = HtmlXPathSelector(response)        
        ulist = hxs.select('//ol')
        #for ul in ulist:
        links = ulist.select('li/a/@href').extract()
        filenamelist = ulist.select('li/a/text()').extract()
        print filenamelist
        i = 0
        for link in links:
            templink = 'http://www.telugupedia.com'+link
            filename = filenamelist[i]
            yield Request(templink,callback = lambda r,filename=filename:self.parse_movie(r,filename))
            i = i+1
            #print text
#fwrite.close()
