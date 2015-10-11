
#testinserts = [('Bul-63R17','73766','63R17','Watches',"Women\'s",'Quartz', 'Accutron by Bulova',"Women\'s Diamond Black Leather Cuff",'0','1',"With a touch of class, this stunning Accutron by Bulova quartz timepiece will add a distinguished look to a woman\'s wardrobe. Accutron is Bulova\'s Elite All Swiss Made Collection",'895','223.75','167.81','http://admin.swisswatchintl.com/H/63R17(L).jpg', "|Model Number|63R17|Style|Casual|Size|Women's|Case|Stainless steel|Dial Color|Black mother of pearl dial with silver tone hands, hour markers and arabic numerals|Strap|Black leather cuff strap|Movement|Swiss made quartz|Crystal|Sapphire|Bezel Material|38 black diamonds set on bezel|Case Width|24 mm|Case Height|32 mm|Case Thickness|8 mm|Strap Width|29 mm|Strap Length|7.0 inches|Material|Leather|Clasp Type|Buckle")]
csvfile = open('datafeedSAMPLE2.csv')

 
import sqlite3
 
conn = sqlite3.connect("swi_prodinfo.db")
 
cursor = conn.cursor()

conn.execute("""DROP TABLE IF EXISTS SWI_Prodinfo""")
 
   
cursor.execute("""CREATE TABLE SWI_Prodinfo
                  (SWI_SKU text, BO_VARIANCE_ID text, STYLE text, STORE text, CATEGORY text, SUBCATEGORY text, BRAND_NAME text, TITLE text, QOH text, WEIGHT text, PRODUCT_DESCRIPTION text, MSRP text, SELL_PRICE text, YOUR_COST text, IMAGE text, FEATURES_PIPED text)
               """)

cursor.executemany("INSERT INTO SWI_Prodinfo VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", testinserts)
conn.commit()

 
print "\nHere's a listing of all the records in the table:\n"
rowlist = {}
for row in cursor.execute("SELECT rowid, * FROM SWI_Prodinfo ORDER BY rowid"):
    count = 1
    pipelist = row[-1]
    pipelist = pipelist.split('|')
    while len(pipelist) > 0: 
    #for  in range(1,len(pipelist)):
    	#if len(pipelist) > 0:
    	try:
    		print len(pipelist)
    		value = pipelist.pop()
    		key = pipelist.pop()
    		rowlist[key] = value
    	except IndexError:
    		print rowlist
    		#rowlist[count] = subrow
    	#rowlist.append(count)
    	#rowlist.append(subrow)
    		#count += 1
    	#print row[-1][1]
 
#print cursor.fetchall()
#splitkeys  = []
splitvals  = []

#for k,v in rowlist.iteritems():
	
	
#	try:
		#if k == (k/2)/(2/k):
#		if k > 1:
#			print k,v
			#splitkeys.append(k)
			#splitvals.append(v)
#	except:
#		print 'error ' + str(k)
	
#pairedpipe = zip(splitkeys,splitvals)

#for item in pairedpipe:
	

print rowlist
