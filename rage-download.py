#!/usr/bin/python

import  sys, re,  requests

from lxml import html
#from django.utils.encoding import smart_str, smart_unicode 

def main(): 
        if len(sys.argv) > 1:
		URL=str(sys.argv[1])
		print str(sys.argv[1])
	print "<html>"
	print "<head><title>Rage Playlist extension</title></head>"
	print "<body>"
	print "<ul>"
	artist_list = []
	song_list = []
	time_list = []
	song_artist_time_list = []
	if len(sys.argv)>1:
		page = requests.get(str(sys.argv[1]))
	else:
		page = requests.get('http://www.alphastar.net.au/rage/rage.html')
        rendered = page.text.encode('ascii','ignore')
	getDate(rendered)
	tree = html.fromstring(rendered)
	for playlistTag in tree.xpath('//html/body//div[@class="abcLayoutFixed"]/div[@id="mainContent"]/div[@class="abcRow"]/div[@class="abcSpan9"]/div[@class="playlist"]'):

		timeTag = playlistTag.xpath('//p[@class="time"]')
		for t1 in timeTag:
			#print t1.text
			time_list.append(t1.text)

		listTag = playlistTag.xpath('//p[@class="list"]')	
		timeCtr = 0
                for lt in listTag:
			artistTag=lt.xpath('strong')
			for el1 in artistTag:
				#print el1.text
				artist_list.append(el1.text)
			
			songTag=lt.xpath('em')
			for el2 in songTag:
				#print el2.text
				song_list.append(el2.text)
				song_artist_time_list.append(timeCtr)
				#print "^^timeCtr = "+str(timeCtr)

			#print len(artist_list)
			#print len(song_list)

			timeCtr = timeCtr + 1

			checkLengths(artist_list, song_list)

			if (len(artist_list) <> len(song_list)):	
				print "trouble"
				exit(1)
			else:
				pass
				#print "song and artist list match up. As we expect :)"

		print str(len(song_artist_time_list))+" songs over" #84
		print str(len(time_list))+ " time periods" #13
		print "<P>"
		
		#exit(1)

		for x in range (0,len(artist_list)):
			#print "x is "+str(x)
			print "<li>"
			print "<a href='http://www.google.com/search?btnI=I&q=youtube+"
			print(artist_list[x]+song_list[x])
			print "'>["+time_list[song_artist_time_list[x]]+"]"+song_list[x]+" by "+artist_list[x]+"</a>"
			print "</li>"
		print "</ul>"
		print "</body>"

def getDate(pageText):
	#print pageText
	x = re.search("<p.*date.*p>",pageText)
	print "<b>"+x.group(0)+"</b>"

def checkLengths(artist_list, song_list):
	if (len(artist_list) <> len(song_list)):
		print "trouble"
		exit(1)
	else:
		pass
		#print "song and artist list match up. As we expect :)"

if __name__ == "__main__":
	main()
