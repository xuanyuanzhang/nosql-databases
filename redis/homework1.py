import urllib2
url = "https://api.nasa.gov/planetary/apod?api_key=o71eOeRUuccZPqz5hvmRV1vLN5tE9SdIuH0Vl1Cc&date=2017-09-08"
content = urllib2.urlopen(url).read()
begin_ind = content.find('"url"')+8
end_ind = content[begin_ind:].find('"')
print content[begin_ind: begin_ind+end_ind]
