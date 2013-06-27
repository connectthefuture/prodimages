import os,re


#def regex_filepath():
#pattern = r''
filepath = '/Users/johnb/2013-03-25_write.csv'

def regex_compile_pattern(pattern):
    regex = re.compile(pattern)
    return(regex)
    
    
def regex_search_string(regex, searchstring):
    #for matchObj in searchstring:
    searchstring = str(searchstring)
    match = re.search(regex, searchstring)
    if match:
        print searchstring
    else:
        print "Regex Not Found in String"
        
        
        
def csv_reader(filepath,delim):
    import csv
    f = open(filepath, "rb")
    reader = csv.reader(f, delimiter=delim)
    all_lines = []
    
    for line in reader:
                    
        all_lines.append(line)
            #print all_lines
        #print returnline
    f.close()
    return (all_lines)        
#def csv_reader(filepath,delim):
#    import csv
#    with open(filepath) as f:
#        reader = csv.reader(f, delimiter=delim)
#        all_lines = []
#        for line in reader:
#            for row in line:
#                
#                all_lines.append(row)
#                #print all_lines
#            #print returnline
#        return all_lines

#fields = my_csv.next()
searchstring = "exiftool -'IPTC:SimilarityIndex=Scanned In at Bluefly' /mnt/Post_Ready/aPhotoPush/032213_CH/323548201/323548201_2.jpg"
csvlines = csv_reader(filepath, ",")
#print csvlines
pattern = re.compile(".")
regex = regex_compile_pattern(pattern)
#try:
#        
#    for line in csvlines:
#        print line
#        regex_search_string(regex, line)
#except TypeError:
#    print "end"
   
for line in csvlines:
    #enumerate(line)
    print csvlines[1]
    regex_search_string(pattern, line)
    
#result = regex_search_string(regex, searchstring)
    
