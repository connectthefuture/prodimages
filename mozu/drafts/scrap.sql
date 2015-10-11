
CREATE or REPLACE TRIGGER mozu_image_after_update
AFTER UPDATE OF MOZU_IMAGEID ON MOZU_IMAGE
FOR EACH ROW
DECLARE
    --set bf_imageid := new.MZ_IMAGEIDl;
    OLDUPDATED_COUNT NUMBER := :OLD.UPDATED_COUNT
    NEWUPDATED_COUNT NUMBER := ( OLDUPDATED_COUNT + 1);
BEGIN
    update MOZU_IMAGE
    SET MOZU_IMAGE.UPDATED_COUNT = :NEWUPDATED_COUNT
    WHERE :new.MZ_IMAGEID <> :old.MZ_IMAGEID
    AND :new.MD5CHECKSUM <> :old.MD5CHECKSUM;
    DBMS_OUTPUT.PUT_LINE('bf_imageid successfully updated into mozu_image_backup table');
END;



update MZIMG.MOZU_IMAGE 
	set UPDATED_COUNT = UPDATED_COUNT + 1 
	where MZ_IMAGEID = <somevalue> AND MD5CHECKSUM != <inserting record md5>;

MZIMG/password@qarac201-vip.qa.bluefly.com:1521/bfyqa1201


---- Auto Increment Oracle
DROP SEQUENCE MOZU_IMAGE_SEQ;
------------------------------
CREATE SEQUENCE MOZU_IMAGE_SEQ INCREMENT BY 1 START WITH 1 MAXVALUE 999999999999999999999999999 MINVALUE 1 CACHE 100;
------------------------------
CREATE OR REPLACE TRIGGER mozu_image_seq_trigger 
BEFORE INSERT ON mozu_image 
FOR EACH ROW
WHEN (new.id IS NULL)
BEGIN
  SELECT MOZU_IMAGE_SEQ.NEXTVAL
  INTO   :new.id
  FROM   dual;
  DBMS_OUTPUT.PUT_LINE('bf_imageid successfully updated into mozu_image_backup table' || :new.id); 
END;




def main(**kwargs):
    #insert_list = []
    # for f in sys.argv:
    #     insert_list.append(f)
    import os.path
    if kwargs.get('insert_list') and len(kwargs.get('insert_list')) > 1:
            insert_list = kwargs.get('insert_list')
    else:        
        src_filepath = kwargs.get('src_filepath')
        insert_list = src_filepath
    
    args_dict = {}
    for f in insert_list:
        l = []
        image_metadata = get_exif_all_data(f)
        mozu_image_table = mozu_image_table_instance()
        bf_imageid = os.path.basename(f)
        mz_imageid = kwargs.get(mz_imageid)
        if not kwargs.get('md5checksum'):
            md5checksum = md5_checksumer(f)
        l.append(dict(bf_imageid  = bf_imageid, 
                    mz_imageid  = mz_imageid, 
                    md5checksum = md5checksum,
                    image_metadata = get_exif_all_data(f)))
        args_dict[f] = l
    
    # Insert
    for k,v in args_dict:
        src_filepath = k
        args = v.items()
        try:
            mz_imageid, content_response = upload_productimgs_mozu(args)
            args['mz_imageid'] == mz_imageid
            insert_records = mozu_image_table.insert(**args)
            insert_records.execute()
            print 'Inserted --> ', args, ' <-- ', insert_records
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError ', args
            mz_imageid = mozu_image_table.select('mz_imageid', whereclause=mozu_image_table.c.bf_imageid==bf_imageid)
            updated_mz_imageid, content_response = upload_productimgs_mozu(arg, mz_imageid=mz_imageid)
            update_records = mozu_image_table.update(values=dict(**args),whereclause=mozu_image_table.c.bf_imageid==bf_imageid)
            res = update_records.execute()
            print res, 'Updated--> ', args, ' <-- ', update_records
            pass



            