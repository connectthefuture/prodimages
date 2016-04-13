MERGE
   INTO  target_table tgt
   USING source_table src
   ON  ( src.column1 = tgt.column1 and
         src.column2 = tgt.column2)
WHEN MATCHED
THEN
   UPDATE
   SET   tgt.column3= src.column3,
         tgt.column4 = src.coulmn4
   WHERE tgt.column3 IN (val1, val2)
WHEN NOT MATCHED
   THEN
INSERT ( tgt.column1,
         tgt.column2,
         tgt.column3,
         tgt.column4 )
VALUES ( src.coulmn1,
         src.coulmn2,
         src.coulmn3,
         src.coulmn4);
