import os
import re
import subprocess
import time
#put in a timestamp print here
import datetime
ts1 = time.time()
st1 = datetime.datetime.now().time()


path = "/Users/malarout/Desktop/sample/5/"
for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith(".nc"):
            #print "root:::"
            #print root
            file_path = root+"/"+name
            print file_path
            ncdump_cmd1 = "ncdump-json -j -h "+file_path+" >> l4.json"
            ncdump_cmd2 = "ncdump-json -j -v analysed_sst  "+file_path+" >> l4.json"
            ncdump_cmd3 = "ncdump-json -j -v analysis_error  "+file_path+" >> l4.json"
            ncdump_cmd4 = "ncdump-json -j -v lat "+file_path+" >> l4.json"
            ncdump_cmd5 = "ncdump-json -j -v lon "+file_path+" >> l4.json"
            ncdump_cmd6 = "ncdump-json -j -v mask "+file_path+" >> l4.json"
            ncdump_cmd7 = "ncdump-json -j -v sea_ice_fraction "+file_path+" >> l4.json"
            ncdump_cmd8 = "ncdump-json -j -v time "+file_path+" >> l4.json"
            os.system(ncdump_cmd1)
            os.system(ncdump_cmd2)
            os.system(ncdump_cmd3)
            os.system(ncdump_cmd4)
            os.system(ncdump_cmd5)
            os.system(ncdump_cmd6)
            os.system(ncdump_cmd7)
            os.system(ncdump_cmd8)           

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
