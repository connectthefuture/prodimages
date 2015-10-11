import csv,re

filename='BlueFly.csv'

pipe_names = {}


with open(filename, 'rb') as f:
    reader = csv.reader(f,quoting=csv.QUOTE_ALL,delimiter=',')
    headers = reader.next()
    swi = {}

    for index,item in enumerate(headers):
        swi[index] = item

    print '###Printing Headers###'

    print swi
    
    # row = reader.next()
    
    for row in reader:

        for row_index,row_value in enumerate(row):
        
            if row_index == 15 :
                pipe_out = re.split("\|",row[row_index])

                field_name  = ""
                field_value = ""
                for pipe_index,pipe_value in enumerate(pipe_out):

                    if pipe_index != 0:

                        if pipe_index % 2:
                            field_name = pipe_value
			    pipe_names[field_name] = ''
                        else:
                            field_value= pipe_value
                            print '  ',field_name,':',field_value
                    

            else:

                print row_index
                print swi[row_index],':',str(row_value)





print '####Printing Pipe Names'

print sorted(pipe_names)
                                            

