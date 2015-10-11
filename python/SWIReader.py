import csv,re
import cx_Oracle

filename='BlueFly-test.csv'
pipe_names = {}

BULLET1_MAPS = ['ARMS', 'BEZEL', 'BEZEL FUNCTION', 'BEZEL MATERIAL', 'BRACELET', 'BRACELET COLOR', 'BRACELET LENGTH', 'BRACELET MATERIAL', 'BRACELET WIDTH',] 
BULLET2_MAPS = ['CALENDAR', 'CASE', 'CASE BACK', 'CASE DIAMETER', 'CASE HEIGHT', 'CASE SHAPE', 'CASE THICKNESS', 'CASE WIDTH', 'CLASP', 'CLASP TYPE', 'CLOSURE', 'COLOR', 'CROWN', 'CRYSTAL',]
BULLET3_MAPS = ['DESCRIPTION', 'DIAL COLOR', 'DIAMOND CLARITY', 'DIAMOND COLOR', 'DIAMONDS', 'DIMENSION', 'DIMENSIONS', 'EXTERIOR', 'FEATURES', 'FINISH', 'FRAME', 'FRAME MATERIAL', 'FRAME STYLE',] 
BULLET4_MAPS = ['GENDER', 'HANDS', 'HINGE', 'INCLUDES', 'INTERIOR', 'LENS', 'LUMINOUS', 'MANUFACTURED', 'MARKERS', 'MATERIAL', 'MATERIALS', 'MODEL ALIAS', 'MODEL NUMBER', 'MOVEMENT', 'MULTI-FUNCTION',]
BULLET5_MAPS = ['NOSE BRIDGE', 'NOSE PADS', 'OTHER', 'PROTECTION', 'RIM', 'RX', 'SERIES', 'SIZE', 'STONES', 'STRAP', 'STRAP COLOR', 'STRAP LENGTH', 'STRAP MATERIAL', 'STRAP WIDTH', 'STYLE', 'SUBDIAL',]
BULLET6_MAPS = ['SUBDIALS', 'SWEEP SECOND HAND', 'TEMPLE', 'TEMPLES', 'WATER RESISTANT', 'WEIGHT']
LONG_DESCRIPTION_MAP = ['PRODUCT_DESCRIPTION']

connection = cx_Oracle.connect("pomgr", "j1mmych00", "BFYQA1201_QARAC201-VIP.QA.BLUEFLY.COM")
cursor = connection.cursor()



#cursor.execute("""
#          select sysdate from dual""",)
#for column_1, in cursor:
#    print "Values:", column_1


def update_watches(item):
    
    # Get ID, Product_ID

    cursor.execute("""
    select id,product_id
    from pomgr.product_color
    where vendor_style = :arg_1
    """, arg_1 = item['SWI_SKU'],)

    print "Checking: ", item['SWI_SKU']

    id = ''
    product_id = ''

    for id, product_id in cursor:
        print id,product_id
        item['ID'] = id
        item['PRODUCT_ID'] = product_id

    if id != '':
        print 'Found'
#        print sorted(item)

        # Update Material

        if 'CASE' in item:
            cursor.execute('update pomgr.product_detail set material = :item where product_id = :product_id', {'item': item['CASE'], 'product_id': str(item['PRODUCT_ID'])})


        b1_string = ""
        b2_string = ""
        b3_string = ""
        b4_string = ""
        b5_string = ""
        b6_string = ""

        for key in BULLET1_MAPS:
            if key in item:
                b1_string += key.title() + ': ' + item[key] + '<br>'

        for key in BULLET2_MAPS:
            if key in item:
                b2_string += key.title() + ': ' + item[key] + '<br>'

        for key in BULLET3_MAPS:
            if key in item:
                b3_string += key.title() + ': ' + item[key] + '<br>'

        for key in BULLET4_MAPS:
            if key in item:
                b4_string += key.title() + ': ' + item[key] + '<br>'

        for key in BULLET5_MAPS:
            if key in item:
                b5_string += key.title() + ': ' + item[key] + '<br>'

        for key in BULLET6_MAPS:
            if key in item:
                b6_string += key.title() + ': ' + item[key] + '<br>'


        cursor.execute("""update pomgr.product_color_detail 
set bullet_1 = :b1s ,  
    bullet_2 = :b2s ,
    bullet_3 = :b3s ,
    bullet_4 = :b4s ,  
    bullet_5 = :b5s ,  
    bullet_6 = :b6s ,
    long_description = :prod_desc
where product_color_id = :id 
""", { 'b1s': b1_string, 
        'b2s': b2_string, 
        'b3s': b3_string, 
        'b4s': b4_string, 
        'b5s': b5_string, 
        'b6s': b6_string,
        'prod_desc' : item['PRODUCT_DESCRIPTION'],
        'id' : item['ID']})

        connection.commit()


with open(filename, 'rb') as f:
    reader = csv.reader(f,quoting=csv.QUOTE_ALL,delimiter=',')
    headers = reader.next()
    swi = {}

    for index,item in enumerate(headers):
        swi[item] = index

    SWI_item = {}

    for row in reader:

        for key in swi:
            SWI_item[key] = row[swi[key]]

        pipe_out = re.split("\|",row[swi['FEATURES_PIPED']])

        field_name  = ""
        field_value = ""


        for pipe_index,pipe_value in enumerate(pipe_out):
            
            if pipe_index != 0:

                if pipe_index % 2:
                    field_name = pipe_value
                else:
                    field_value = pipe_value
                    # print '  ',field_name,':',field_value
                    SWI_item[field_name.upper()] = field_value
                    
        


        if SWI_item['STORE'] == 'Watches':
            update_watches(SWI_item)

