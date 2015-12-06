import numpy as np
def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


#c = np.arange(320000).reshape((400,800)) #auto generating the values

#getting dumped values from file
fadm = open("newfile.adm","r+")
filecontent = fadm.read()
fadm.close()
filecontent.replace('/n',"")
#print "length of file:",len(filecontent)
pos_uuid = filecontent.find("fid",0)
meta_content = ''
new_content = ''

while pos_uuid>=0:
    #finding the uuids, to process a record at a time in this loop
    pos_uuid_end = filecontent.find('",',pos_uuid)
    uuid = filecontent[pos_uuid+7:pos_uuid_end]
    #finding sst_data
    sst_start = filecontent.find('"analysed_sst":{{', pos_uuid)
    sst_end = filecontent.find('}}',sst_start)
    sst_data = filecontent[sst_start+17:sst_end]
    #finding analysis_error data
    err_start = filecontent.find('"analysis_error":{{', pos_uuid)
    err_end = filecontent.find('}}',err_start)
    err_data = filecontent[err_start+19:err_end]
    #finding sea ice fraction data
    sif_start = filecontent.find('"sea_ice_fraction":{{', 0)
    sif_end = filecontent.find('}}',sif_start)
    sif_data = filecontent[sif_start+21:sif_end]
    
    metadata = filecontent[pos_uuid:sst_start-1]
    file_meta = '{"'+metadata+'}'
    meta_content = meta_content+file_meta
    

    # put a for loop from 1 to 3, based on value assign the variable data either sst_data,err_data and sif_data
    for loop in range(1,3):
        if loop == 1:
            data = sst_data
            pos_start = sst_start+16
            pos_end = sst_end
            uuid_append = "_sst_"
            var_name = "analysed_sst"
            print "sst:"
        elif loop == 2:
            data = err_data
            pos_start = err_start+18
            pos_end = err_end
            uuid_append = "_err_"
            var_name = "analysis_error"
            print "err:"
        elif loop == 3:
            data = sif_data
            pos_start = sif_start+20
            pos_end = sif_end
            uuid_append = "_sif_"
            var_name = "sea_ice_fraction"
            print "sif:"
        i=1
        sub = ','
        s_temp = data
        print "length of s_temp file:",len(s_temp)
        pos = s_temp.rfind(',')
        
        # while loop to help find the position of comma of start of last 1800 values... basically to help seperate the 901th row of data
        while (i<1800):
            s_temp = s_temp[0:pos]
            pos = s_temp.rfind(',')
            i= i + 1
        
        #print data[0:pos] # 900x1800
        #print data[pos+1:] # last row of 1800

        json_data1 = '['+ data[0:pos] +']' # 900x1800
        json_data2 = '[' + data[pos+1:] +']' # last row of 1800
        
        print "count of commas"
        print json_data1.count(',')
        print json_data2.count(',')
        #print json_data1
        #print json_data2
        jarray1 = eval(json_data1)
        jarray2 = eval(json_data2)

        big_grid = np.reshape(jarray1,(900,1800))
        grid_row = np.reshape(jarray2,(1,1800))
        first_block = blockshaped(big_grid, 50, 50) #working with 50 rows 50 columns
        last_row = blockshaped(grid_row, 1, 50)
        
        new_file = ''
        
        for i in range(0,647):# interating over every chunk
            chunk_write = ''
            for j in range(0, 49):
                #print chunks[0][j]
                chunk_write = chunk_write + str(first_block[i][j])
            #conforming to adm format
            str_comma = chunk_write.replace(' ',',')
            str_comma = str_comma.replace(',,,',',')
            str_comma = str_comma.replace(',,',',')
            str_comma = str_comma.replace('[,','[')
            str_comma = str_comma.replace('[',',[')
            str_comma = '['+str_comma[1:]+']'
            #constructing new rec
            new_rec_chunk = '{"fid":"'+uuid+uuid_append+str(i)+'", "'+var_name+'":'+str_comma+'}'
            new_file = new_file + new_rec_chunk
            
        new_content = new_content + new_file

        # don't forget to advance to the next fid
    pos_uuid = filecontent.find("fid",pos_uuid+5)
    print pos_uuid

new_content = new_content + meta_content
print "writing to new file"
print new_content
finaladm =file("chunks.adm","w")
finaladm.write(new_content)
finaladm.close()
