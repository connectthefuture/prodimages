#!/bin/bash

. ~/.bash_profile




/usr/local/batchRunScripts/bash/importPoUpcomingStatuses.sh & /usr/local/batchRunScripts/bash/importEventStyleStatusImgCpy.sh & /usr/local/batchRunScripts/bash/importEventStyleStatus.sh & /usr/local/batchRunScripts/bash/import_prodsnapshot_livedata.sh & 
/mnt/Post_Ready/zProd_Server/imageServer7/scripts/bash/importData/importEventStyleInfoPMA.sh & /mnt/Post_Ready/zProd_Server/imageServer7/scripts/bash/sampleAgingImportpma.sh & /usr/local/batchRunScripts/bash/importSampleVendorStyle_pma.sh & /usr/local/batchRunScripts/bash/import_prodsnapshot.sh &
/usr/local/batchRunScripts/bash/importSKUToPhpMyAdmin.sh & \;

