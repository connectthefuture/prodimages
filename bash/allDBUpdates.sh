#!/bin/bash

. ~/.bash_profile

## Import to local Mysql from DSSPRD1
## import uno
/usr/local/batchRunScripts/bash/importPoUpcomingStatuses.sh &
/usr/local/batchRunScripts/bash/importEventStyleStatusImgCpy.sh &
/usr/local/batchRunScripts/bash/importEventStyleStatus.sh &
/usr/local/batchRunScripts/bash/import_prodsnapshot_livedata.sh & \; 

## 2nd dssprd1 import
/usr/local/batchRunScripts/bash/importEventStyleInfoPMA.sh &
/usr/local/batchRunScripts/bash/sampleAgingImportpma.sh &
/usr/local/batchRunScripts/bash/importSampleVendorStyle_pma.sh &
/usr/local/batchRunScripts/bash/import_prodsnapshot.sh &
/usr/local/batchRunScripts/bash/importSKUToPhpMyAdmin.sh & \;


### Get and Import the File7 Dir hierarchy
/usr/local/batchRunScripts/bash/styleStringTestMakerPushed.sh &
/usr/local/batchRunScripts/bash/styleStringZimagesPro.sh & \;

/usr/local/batchRunScripts/bash/styleStringImportPma.sh \;



## Regenerate the Lavender Report with updates
/usr/local/batchRunScripts/bash/morningEventMail.sh \;
