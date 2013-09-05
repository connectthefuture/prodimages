# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""
<<<<<<< HEAD
=======

### Get the Cat ID of an Event from an event ID. For adding to url and going to B&C URL to scrape img urls
>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
def get_catid_from_eventid(eventid):
    if len(eventid) == 4:
        import sqlalchemy
        orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
        connection = orcl_engine.connect()
        eventid = str(eventid)
        eventid_tocatid_query = "SELECT DISTINCT POMGR.EVENT.CATEGORY FROM POMGR.EVENT WHERE POMGR.EVENT.ID = '" + eventid + "'"
    #print eventid_tocatid_query
        for row in connection.execute(eventid_tocatid_query):
            catid = row['category']
    else:
        catid = eventid
    if catid:
        return catid
    else:
        print "Event {0} has not been pushed to ATG yet".format(eventid)


<<<<<<< HEAD
=======
######
########## Queries That accept Either a single style number or a difffield and/or another var, AKA ponum,file
######

###########
########### Return Dict of Colorstyle -- with sku value -- Inputing sku
###
def sqlQuerySkuColorstyleConvert(sku):
    import sqlalchemy
    #sku = str(sku)
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()

    querymake_consig_stylefix="SELECT Distinct POMGR_SNP.SKU.PRODUCT_COLOR_ID AS colorstyle, POMGR_SNP.SKU.SKU_CODE AS sku FROM POMGR_SNP.SKU WHERE POMGR_SNP.SKU.SKU_CODE LIKE '" + sku + "' ORDER by POMGR_SNP.SKU.PRODUCT_COLOR_ID ASC"

    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['sku']] = consigstyle

    #print consigstyles
    connection.close()
    return consigstyles

########### Return Dict of PO -key -- with colorstyle value -- Inputing PO
###
def sqlQueryReturnStylesbyPO(ponum):
    import sqlalchemy
    ponum = str(ponum)
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_ponum_to_colorstyle="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    result = connection.execute(querymake_ponum_to_colorstyle)
    #result = result.__iter__()
    connection.close()
    colorstyle_po_ret = {}
    for key, value in result.iteritems():
        ret = {}
        ret['colorstyle'] = value['colorstyle']
        colorstyle_po_ret[value['po_hdr']] = ret
    return colorstyle_po_ret

####### METADATA QUERIES FOR TAGGING
#### Metadata for RAW Files
def sqlQueryMetatagsRaw(style,f):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_metatags="""SELECT DISTINCT
      POMGR_SNP.PRODUCT_COLOR.ID                  AS colorstyle,
      POMGR_SNP.BRAND.NAME                        AS brand,
      POMGR_SNP.COLOR_GROUP.DESCRIPTION           AS color_group,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent,
      POMGR_SNP.PRODUCT_FOLDER.LABEL              AS category_sub,
      MAX(ATG_SNP.EVENT.ID)                       AS event_id,
      ATG_SNP.EVENT.EVENT_DESCRIPTION             AS event_title,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.PATH  AS product_path,
      ATG_SNP.EVENT.SHOT_LIST_DATE                AS shot_list_dt,
      ATG_SNP.EVENT.BRAND_EDITORIAL               AS brand_editorial,
      ATG_SNP.EVENT.CATEGORY                      AS cat_id,
      POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE        AS vendor_style,
      POMGR_SNP.LK_PRODUCT_STATUS.NAME            AS production_status
    FROM
      POMGR_SNP.PRODUCT_COLOR
    LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR
    ON
      POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID
    LEFT JOIN POMGR_SNP.LK_PRODUCT_STATUS
    ON
      POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
    LEFT JOIN ATG_SNP.EVENT
    ON
      ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID
    LEFT JOIN POMGR_SNP.PRODUCT
    ON
      POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID
    LEFT JOIN POMGR_SNP.PRODUCT_FOLDER
    ON
      POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID
    LEFT JOIN POMGR_SNP.BRAND
    ON
      POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID
    LEFT JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED
    ON
      POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID =
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID
    LEFT JOIN POMGR_SNP.COLOR_GROUP
    ON
      POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID = POMGR_SNP.COLOR_GROUP.ID
    WHERE
      POMGR_SNP.PRODUCT_COLOR.ID = COLORSTYLESEARCH
    GROUP BY
      POMGR_SNP.PRODUCT_COLOR.ID,
      POMGR_SNP.BRAND.NAME,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL,
      POMGR_SNP.PRODUCT_FOLDER.LABEL,
      ATG_SNP.EVENT.EVENT_DESCRIPTION,
      POMGR_SNP.COLOR_GROUP.DESCRIPTION,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.PATH,
      POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE,
      ATG_SNP.EVENT.SHOT_LIST_DATE,
      ATG_SNP.EVENT.BRAND_EDITORIAL,
      ATG_SNP.EVENT.CATEGORY,
      POMGR_SNP.LK_PRODUCT_STATUS.NAME
    ORDER BY
      POMGR_SNP.PRODUCT_COLOR.ID DESC"""
##########
##   --RENAME INPUT VARIABLE PRIOR TO QUERY
##########
    querymake_metatags = querymake_metatags.replace('COLORSTYLESEARCH', str(style))
    result = connection.execute(querymake_metatags)

    metatags = {}
    for row in result:
        metatag = {}
#        metatag['colorstyle'] = row['colorstyle']
#        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        metatag['IPTC:Brand'] = row['brand']
        metatag['XMP:Genre'] = row['color_group']
        metatag['IPTC:ProductType'] = row['category_sub']
        metatag['EventID'] = row['event_id']
        try:
            metatag['XMP:Album'] = "EventID " + str(row['event_id'])
        except:
            pass
        metatag['IPTC:Credit'] = row['product_path']
        metatag['IPTC:CopyrightNotice'] = row['brand']
        metatag['IPTC:SpecialInstructions'] = row['production_status']
        metatag['Keywords'] = row['category_parent']
        metatag['IPTC:Source'] = row['shot_list_dt']
#        metatag['IPTC:SpecialInstructions'] = '{:%Y-%m-%d}'.format(metatag['brand_editorial'])
#        metatag['IPTC:SampleStatusDate'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = row['sample_dt']
#        metatag['SourceFile'] = f
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag

    connection.close()
    return metatags

#### Daily Tags
def sqlQueryMetatagsSelects(style,f):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()

    querymake_metatags="SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.BRAND.NAME AS brand, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') AS copy_dt, POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent, POMGR_SNP.PRODUCT_FOLDER.LABEL AS category_sub, MAX(ATG_SNP.EVENT.ID) AS event_id, POMGR_SNP.LK_PRODUCT_STATUS.NAME AS production_status, MAX(ATG_SNP.EVENT.EVENT_DESCRIPTION) AS event_title, MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS sample_dt, MAX(POMGR_SNP.LK_SAMPLE_STATUS.NAME) AS sample_status, MAX(POMGR_SNP.PO_LINE.PO_HDR_ID) AS po_num, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style FROM POMGR_SNP.PRODUCT_COLOR LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID LEFT JOIN ATG_SNP.EVENT ON ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID INNER JOIN POMGR_SNP.PRODUCT ON POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER ON POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID INNER JOIN POMGR_SNP.BRAND ON POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED ON POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID LEFT JOIN POMGR_SNP.SAMPLE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.SAMPLE.PRODUCT_COLOR_ID LEFT JOIN POMGR_SNP.SAMPLE_TRACKING ON POMGR_SNP.SAMPLE.ID = POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR_SNP.LK_SAMPLE_STATUS ON POMGR_SNP.SAMPLE_TRACKING.STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.ID = '" + style + "' GROUP BY POMGR_SNP.PRODUCT_COLOR.ID, POMGR_SNP.BRAND.NAME, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD'), POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL, POMGR_SNP.PRODUCT_FOLDER.LABEL, POMGR_SNP.LK_PRODUCT_STATUS.NAME, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE ORDER BY POMGR_SNP.PRODUCT_COLOR.ID DESC"

    result = connection.execute(querymake_metatags)
    metatags = {}
    for row in result:
        metatag = {}
#        metatag['colorstyle'] = row['colorstyle']
        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        metatag['IPTC:Brand'] = row['brand']
        metatag['Keywords'] = row['brand']
        metatag['XMP:Genre'] = row['category_parent']
        metatag['IPTC:ProductType'] = row['category_sub']
        metatag['EventID'] = row['event_id']
        try:
            metatag['XMP:Album'] = "EventID " + str(row['event_id'])
        except:
            pass
        metatag['IPTC:Credit'] = row['event_title']
        metatag['IPTC:CopyrightNotice'] = row['production_status']
#        metatag['IPTC:SpecialInstructions'] = '{:%d-%m-%Y}'.format(row['copy_dt'])
#        metatag['IPTC:SpecialInstructions'] = row['copy_dt']
        metatag['IPTC:SimilarityIndex'] = row['sample_status']
#        metatag['IPTC:SampleStatusDate'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:SampleStatusDate'] = row['sample_dt']
#        metatag['IPTC:Source'] = row['sample_dt']
#        metatag['SourceFile'] = f
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag

    connection.close()
    return metatags
##########
## HELPER FUNCTION FOR ABOVE QUERIES
def get_dbinfo_for_metatags_singlefile(f):
    import os
    metafield_dict = {}
    listed = []
    stylefile = os.path.basename(f)
    style = stylefile.split('_')[0]
    #print style, f
    ### string = key/val as k=filepath, val=all metadata as k/v pairs
    exiftoolstring = sqlQueryMetatagsSelects(style,f)

    ## Uncomment below for Raw tags, Only Select tagger set currently
    ##exiftoolstring = sqlQueryMetatagsRaw(style,f)
    ##  exiftoolstring = sqlQueryMetatagsRaw(style,f)
    #pairs = zip(exiftoolstring.values(), exiftoolstring.keys())

    for k,v in exiftoolstring.iteritems():
        tmpd = {}
        for val in v:
            tmpd[val] = v[val]
            listed.append(tmpd)
        metafield_dict[k] = tmpd

    return metafield_dict
    #return listed

#########
############### No Variables Just Returns a dict of Results mostly based on date - some # of days
##########

>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    querymake_eventscal = 'select distinct POMGR.event.id as "event_id", POMGR.event.start_date as "ev_start", POMGR.event.end_date as "ev_end", POMGR.event.event_description as "event_title" from POMGR.event where POMGR.event.start_date >= trunc(sysdate) order by start_date desc'
    result = connection.execute(querymake_eventscal)
    events = {}
    for row in result:
        event = {}
        event['event_id'] = row['event_id']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']
        event['event_title'] = row['event_title']
        events[row['event_id']] = event

    print events
    connection.close()
    return events


def sqlQueryEventsStylesUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT POMGR.EVENT.ID AS "event_id", POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", POMGR.EVENT.EVENT_DESCRIPTION AS "event_title", POMGR.EVENT.START_DATE AS "ev_start", POMGR.EVENT.END_DATE AS "ev_end", POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM POMGR.EVENT INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY ON POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN POMGR.EVENT_PRODUCT_COLOR ON POMGR.EVENT.ID = POMGR.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN POMGR.PRODUCT_COLOR ON POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE POMGR.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY POMGR.EVENT.ID DESC, POMGR.EVENT.START_DATE DESC Nulls Last'
    result = connection.execute(querymake_eventscal)

    eventsStyles = {}
    for row in result:
        eventsStyle = {}
        eventsStyle['event_id'] = row['event_id']
        eventsStyle['category'] = row['category']
        eventsStyle['event_title'] = row['event_title']
        eventsStyle['ev_start'] = row['ev_start']
        eventsStyle['ev_end'] = row['ev_end']
        eventsStyle['colorstyle'] = row['colorstyle']
        eventsStyle['production_status'] = row['production_status']
        eventsStyles[row['colorstyle']] = eventsStyle

    print eventsStyles
    connection.close()
    return eventsStyles
<<<<<<< HEAD
=======


def sqlQuerylivesnapshot():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_livesnapshot="SELECT DISTINCT MAX(POMGR.PRODUCT_COLOR.ID) AS colorstyle,POMGR.BRAND.NAME AS brand,POMGR.LK_PRODUCT_STATUS.NAME AS production_status,MAX(POMGR.PO_LINE.PO_HDR_ID) AS po_number,MAX(POMGR.LK_SAMPLE_STATUS.NAME) AS sample_status,MAX(POMGR.SAMPLE_TRACKING.CREATE_DT) AS status_dt,POMGR.PRODUCT_COLOR.COPY_READY_DT AS copy_ready_dt,POMGR.PRODUCT_COLOR.IMAGE_READY_DT AS image_ready_dt,POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT AS production_complete_dt,POMGR.PRODUCT_COLOR.START_DATE AS start_dt,POMGR.PRODUCT_COLOR.ORIGINAL_START_DATE AS orig_start_dt,POMGR.LK_DEPT.NAME AS gender,POMGR.BUYER_PRODUCT_LINE.NAME AS category,MAX(POMGR.CATEGORY.NAME) AS product_type,POMGR.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE AS sample_image_dt,POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style,POMGR.COLOR_GROUP.DESCRIPTION AS color,MAX(POMGR.PRODUCT_FOLDER.LABEL) AS product_subtype,MAX(POMGR.SAMPLE_TRACKING_NUMBER.SAMPLE_ID) AS sample_id,MAX(POMGR.SKU.SKU_CODE) AS sku,MAX(POMGR.TRACKING_NUMBER.REF_NUMBER) AS track_number,MAX(POMGR.TRACKING_NUMBER.CREATE_DT) AS track_dt,MAX(POMGR.LK_SAMPLE_LOCATION.NAME)AS sample_location,MAX(POMGR.USERS.USERNAME) AS track_user,POMGR.LK_PO_TYPE.NAME AS po_type FROM POMGR.PRODUCT_COLOR LEFT JOIN POMGR.COLOR_GROUP ON POMGR.PRODUCT_COLOR.COLOR_GROUP_ID = POMGR.COLOR_GROUP.ID LEFT JOIN POMGR.LK_PRODUCT_STATUS ON POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID LEFT JOIN POMGR.SKU ON POMGR.PRODUCT_COLOR.ID = POMGR.SKU.PRODUCT_COLOR_ID LEFT JOIN POMGR.PO_SKU ON POMGR.SKU.ID = POMGR.PO_SKU.SKU_ID LEFT JOIN POMGR.SAMPLE ON POMGR.SAMPLE.PO_SKU_ID = POMGR.PO_SKU.ID LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR.USERS ON POMGR.SAMPLE_TRACKING.USER_ID = POMGR.USERS.ID LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR.SAMPLE_TRACKING_NUMBER ON POMGR.SAMPLE_TRACKING.SAMPLE_ID = POMGR.SAMPLE_TRACKING_NUMBER.SAMPLE_ID LEFT JOIN POMGR.TRACKING_NUMBER ON POMGR.SAMPLE_TRACKING_NUMBER.TRACKING_NUMBER_ID = POMGR.TRACKING_NUMBER.ID LEFT JOIN POMGR.LK_SAMPLE_LOCATION ON POMGR.SAMPLE_TRACKING.LOCATION_ID = POMGR.LK_SAMPLE_LOCATION.ID LEFT JOIN POMGR.PO_LINE ON POMGR.PO_SKU.PO_LINE_ID = POMGR.PO_LINE.ID LEFT JOIN POMGR.PO_HDR ON POMGR.PO_LINE.PO_HDR_ID = POMGR.PO_HDR.ID LEFT JOIN POMGR.LK_PO_STATUS ON POMGR.PO_HDR.PO_STATUS_ID = POMGR.LK_PO_STATUS.ID LEFT JOIN POMGR.LK_PO_TYPE ON POMGR.PO_HDR.PO_TYPE_ID = POMGR.LK_PO_TYPE.ID LEFT JOIN POMGR.PRODUCT ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT.ID INNER JOIN POMGR.BRAND ON POMGR.PRODUCT.BRAND_ID = POMGR.BRAND.ID INNER JOIN POMGR.PRODUCT_FOLDER ON POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRODUCT_FOLDER.ID LEFT JOIN POMGR.PRD_FDR_CAT_REL ON POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRD_FDR_CAT_REL.FOLDER_ID LEFT JOIN POMGR.CATEGORY ON POMGR.CATEGORY.ID = POMGR.PRD_FDR_CAT_REL.CATEGORY_ID LEFT JOIN POMGR.BUYER_PRODUCT_LINE ON POMGR.PRODUCT.BUYER_PRODUCT_LINE_ID = POMGR.BUYER_PRODUCT_LINE.ID LEFT JOIN POMGR.LK_DEPT ON POMGR.LK_DEPT.ID = POMGR.BUYER_PRODUCT_LINE.DEPT_ID WHERE POMGR.SAMPLE_TRACKING.CREATE_DT >= TRUNC(SysDate - 365) GROUP BY POMGR.BRAND.NAME,POMGR.LK_PRODUCT_STATUS.NAME,POMGR.PRODUCT_COLOR.COPY_READY_DT,POMGR.PRODUCT_COLOR.IMAGE_READY_DT,POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT,POMGR.PRODUCT_COLOR.START_DATE,POMGR.PRODUCT_COLOR.ORIGINAL_START_DATE,POMGR.LK_DEPT.NAME,POMGR.BUYER_PRODUCT_LINE.NAME,POMGR.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE,POMGR.PRODUCT_COLOR.VENDOR_STYLE,POMGR.COLOR_GROUP.DESCRIPTION,POMGR.LK_PO_TYPE.NAME,POMGR.PRODUCT.BRAND_ID ORDER by MAX(POMGR.PRODUCT_COLOR.ID) ASC"
    result = connection.execute(querymake_livesnapshot)
    snapshot = {}
    for row in result:
        snapshot_tmp = {}
        snapshot_tmp['colorstyle'] = row['colorstyle']
        snapshot_tmp['brand'] = row['brand']
        snapshot_tmp['production_status'] = row['production_status']
        snapshot_tmp['po_number'] = row['po_number']
        snapshot_tmp['sample_status'] = row['sample_status']
        snapshot_tmp['status_dt'] = row['status_dt']
        snapshot_tmp['copy_ready_dt'] = row['copy_ready_dt']
        snapshot_tmp['image_ready_dt'] = row['image_ready_dt']
        snapshot_tmp['production_complete_dt'] = row['production_complete_dt']
        snapshot_tmp['start_dt'] = row['start_dt']
        snapshot_tmp['orig_start_dt'] = row['orig_start_dt']
        snapshot_tmp['gender'] = row['gender']
        snapshot_tmp['category'] = row['category']
        snapshot_tmp['product_type'] = row['product_type']
        snapshot_tmp['sample_image_dt'] = row['sample_image_dt']
        snapshot_tmp['vendor_style'] = row['vendor_style']
        snapshot_tmp['color'] = row['color']
        snapshot_tmp['product_subtype'] = row['product_subtype']
        snapshot_tmp['sample_id'] = row['sample_id']
        snapshot_tmp['sku'] = row['sku']
        snapshot_tmp['track_number'] = row['track_number']
        snapshot_tmp['track_dt'] = row['track_dt']
        snapshot_tmp['sample_location'] = row['sample_location']
        snapshot_tmp['track_user'] = row['track_user']
        snapshot_tmp['po_type'] = row['po_type']

        ## colorstyle as dict KEY
        snapshot[row['colorstyle']] = snapshot_tmp

    connection.close()
    return snapshot


##############################
    #####################
    ## WEB APP QUERIES ##
    #####################
##############################
>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
