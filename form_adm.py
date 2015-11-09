import os
import re
import subprocess
import time
#put in a timestamp print here
import datetime
ts1 = time.time()
st1 = datetime.datetime.now().time()

fo = open("l4.json","r+")
strfile = fo.read()
fo.close()
print "ADM file creation started."
str2 = strfile.replace("[","{{")
str3 = str2.replace("]","}}")
str4 = str3.replace('"type":','"typee":')
str5 = str4.replace('s,"',',"')
print "Replacing analysed_sst"
str6 = str5.replace('}\n{"analysed_sst"',',"analysed_sst"')
print "Replacing analysed_error"
str7 = str6.replace('}\n{"analysis_error"',',"analysis_error"')
print "Replacing lat"
str8 = str7.replace('}\n{"lat"',',"lat"')
print "Replacing lon"
str9 = str8.replace('}\n{"lon"',',"lon"')
print "Replacing mask"
str10 = str9.replace('}\n{"mask"',',"mask"')
print "Replacing sea_ice_fraction"
str11 = str10.replace('}\n{"sea_ice_fraction"',',"sea_ice_fraction"')
print "Replacing time"
str12 = str11.replace('}\n{"time"',',"time"')
# check what we need to do for the closing braces of time

#str7 = str6.replace('}\n{"dimensions"','}}\n{"dimensions"') #this is to insert a closing brace for a record before the next dimension
print "uuid insertion underway"
sub = "{\"dimensions\":"
offset = 0
pos = str12.find(sub, offset)
while pos >= 0:
    #generating uuid
    p1 = subprocess.Popen(["uuidgen"], shell=False, stdout=subprocess.PIPE)
    output1 = p1.stdout.read()
    output1.replace('\n','')
    #print "stored1:::"
    #print output1
    str12 = str12[:pos+1]+"\"fid\": \""+output1+"\","+str12[pos+1:]
    pos = str12.find(sub, pos + 1)
    #print pos

str13 = str12.replace('\n",','",')
#print str13
print "Writing to adm file"
fadm = open("newfile.adm", "w")
fadm.write(str13)
fadm.close()

print "Giving timestamps"
#put in ending timestamp here
st2 = datetime.datetime.now().time()
ts2 = time.time()
print "start time:"
print st1
print "end time:"
print st2
print "Time elapsed:"
print ts2 - ts1
