#-------------------------------------------------------------
# Some settings
#-------------------------------------------------------------

#set -o nounset     # These  two options are useful for debugging.
#set -o xtrace
alias debug="set -o nounset; set -o xtrace"

ulimit -S -c 0      # Don't want coredumps.
set -o notify
set -o noclobber
set -o ignoreeof


# Enable options:
shopt -s cdspell
shopt -s cdable_vars
shopt -s checkhash
shopt -s checkwinsize
shopt -s sourcepath
shopt -s no_empty_cmd_completion
shopt -s cmdhist
shopt -s histappend histreedit histverify
shopt -s extglob       # Necessary for programmable completion.

# Disable options:
shopt -u mailwarn
unset MAILCHECK        # Don't want my shell to warn me of incoming mail.


#-------------------------------------------------------------
# File & strings related functions:
#-------------------------------------------------------------


# Find a file with a pattern in name:
function ff() { find . -type f -iname '*'"$*"'*' -ls ; }

# Find a file with pattern $1 in name and Execute $2 on it:
function fe() { find . -type f -iname '*'"${1:-}"'*' \
-exec ${2:-file} {} \;  ; }

#  Find a pattern in a set of files and highlight them:
#+ (needs a recent version of egrep).
function fstr()
{
    OPTIND=1
    local mycase=""
    local usage="fstr: find string in files. Usage: fstr [-i] \"pattern\" [\"filename pattern\"] "
    while getopts :it opt
    do
        case "$opt" in
           i) mycase="-i " ;;
           *) echo "$usage"; return ;;
        esac
    done
    shift $(( $OPTIND - 1 ))
    if [ "$#" -lt 1 ]; then
        echo "$usage"
        return;
    fi
    find . -type f -name "${2:-*}" -print0 | \
xargs -0 egrep --color=always -sn ${case} "$1" 2>&- | more

}




##### Resizer func
# Output sizes -
# Please note the format: each size is wrapped with quotes, width and height are separated with space.
output=( "200 240" "300 360" "400 480" "2000 2400" "800 600" "1024 768" "1152 864" "1280 960" "1280 1024" "1400 1050" "1440 960" "1600 1200" "1920 1440" "1024 600" "1366 768" "1440 900" "1600 900" "1680 1050" "1280 800" "1920 1080" "1920 1200" "2560 1440" "2560 1600" "2880 1800")

# If you frequently use the same source file (e.g. "~/Desktop/src.jpg"),
# set it in "default_src"
# default_src="src.jpg";

# If you frequently use the same destination
# (e.g. "~/Desktop/Some_folder/%.jpg"), set it in "default_dst"
# Destination must include "%", it will be replaced by output size, e.g. "800x600"
# default_dst="%.jpg";

# Add signature?
# default_sign='y'

# If you frequently use the same signature file (e.g. "~/Desktop/sig.png"),
# set it in "default_sig"
# default_sig="sig.png";

# Gravity is for cropping left/right edges for different proportions (center, east, west)
default_gravity="center"

# Output JPG quality: maximum is 100 (recommended)
quality=100

function math(){
    echo $(python -c "from __future__ import division; print $@")
    }


function save_resized(){

      # read target width and height from function parameters
      local dst_w=${1}
      local dst_h=${2}

      # calculate ratio
      local ratio=$(math $dst_w/$dst_h);

      # calculate "intermediate" width and height
      local inter_w=$(math "int(round($src_h*$ratio))")
      local inter_h=${src_h}

      # calculate best sharpness
      local sharp=$(math "round((1/$ratio)/4, 2)")

      # which size we're saving now
      local size="${dst_w}x${dst_h}"
      echo "Saving ${size}..."

      #crop intermediate image (with target ratio)
      convert ${src} -gravity ${gravity} -crop ${inter_w}x${inter_h}+0+0 +repage temp.psd

      # apply signature
      if [ "${sign}" == "y" ]; then
      convert temp.psd ${sig} -gravity southeast -geometry ${sig_w}x${sig_h}+24+48 -composite temp.psd
      fi

      # final convert! resize, sharpen, save
      convert temp.psd -interpolate bicubic -filter Lagrange -resize ${dst_w}x${dst_h} -unsharp 0x${sharp} +repage -density 72x72 +repage -quality ${quality} ${dst/%/${size}}
}

############

function swap()
{ # Swap 2 filenames around, if they exist (from Uzi's bashrc).
    local TMPFILE=tmp.$$

    [ $# -ne 2 ] && echo "swap: 2 arguments needed" && return 1
    [ ! -e $1 ] && echo "swap: $1 does not exist" && return 1
    [ ! -e $2 ] && echo "swap: $2 does not exist" && return 1

    mv "$1" $TMPFILE
    mv "$2" "$1"
    mv $TMPFILE "$2"
}

function extract()      # Handy Extract Program
{
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xvjf $1     ;;
            *.tar.gz)    tar xvzf $1     ;;
            *.bz2)       bunzip2 $1      ;;
            *.rar)       unrar x $1      ;;
            *.gz)        gunzip $1       ;;
            *.tar)       tar xvf $1      ;;
            *.tbz2)      tar xvjf $1     ;;
            *.tgz)       tar xvzf $1     ;;
            *.zip)       unzip $1        ;;
            *.Z)         uncompress $1   ;;
            *.7z)        7z x $1         ;;
            *)           echo "'$1' cannot be extracted via >extract<" ;;
        esac
    else
        echo "'$1' is not a valid file!"
    fi
}


# Creates an archive (*.tar.gz) from given directory.
function maketar() { tar cvzf "${1%%/}.tar.gz"  "${1%%/}/"; }

# Create a ZIP archive of a file or folder.
function makezip() { zip -r "${1%%/}.zip" "$1" ; }

# Make your directories and files access rights sane.
function sanitize() { chmod -R u=rwX,g=rX,o= "$@" ;}

#-------------------------------------------------------------
# Process/system related functions:
#-------------------------------------------------------------


function my_ps() { ps $@ -u $USER -o pid,%cpu,%mem,bsdtime,command ; }
function pp() { my_ps f | awk '!/awk/ && $0~var' var=${1:-".*"} ; }


function killps()   # kill by process name
{
    local pid pname sig="-TERM"   # default signal
    if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
        echo "Usage: killps [-SIGNAL] pattern"
        return;
    fi
    if [ $# = 2 ]; then sig=$1 ; fi
    for pid in $(my_ps| awk '!/awk/ && $0~pat { print $1 }' pat=${!#} )
    do
        pname=$(my_ps | awk '$1~var { print $5 }' var=$pid )
        if ask "Kill process $pid <$pname> with signal $sig?"
            then kill $sig $pid
        fi
    done
}

function mydf()         # Pretty-print of 'df' output.
{                       # Inspired by 'dfc' utility.
    for fs ; do

        if [ ! -d $fs ]
        then
          echo -e $fs" :No such file or directory" ; continue
        fi

        local info=( $(command df -P $fs | awk 'END{ print $2,$3,$5 }') )
        local free=( $(command df -Pkh $fs | awk 'END{ print $4 }') )
        local nbstars=$(( 20 * ${info[1]} / ${info[0]} ))
        local out="["
        for ((j=0;j<20;j++)); do
            if [ ${j} -lt ${nbstars} ]; then
               out=$out"*"
            else
               out=$out"-"
            fi
        done
        out=${info[2]}" "$out"] ("$free" free on "$fs")"
        echo -e $out
    done
}


function my_ip() # Get IP adress on ethernet.
{
    MY_IP=$(/sbin/ifconfig eth0 | awk '/inet/ { print $2 } ' |
      sed -e s/addr://)
    echo ${MY_IP:-"Not connected"}
}

function ii()   # Get current host related info.
{
    echo -e "\nYou are logged on ${BRed}$HOST"
    echo -e "\n${BRed}Additionnal information:$NC " ; uname -a
    echo -e "\n${BRed}Users logged on:$NC " ; w -hs |
             cut -d " " -f1 | sort | uniq
    echo -e "\n${BRed}Current date :$NC " ; date
    echo -e "\n${BRed}Machine stats :$NC " ; uptime
    echo -e "\n${BRed}Memory stats :$NC " ; free
    echo -e "\n${BRed}Diskspace :$NC " ; mydf / $HOME
    echo -e "\n${BRed}Local IP Address :$NC" ; my_ip
    echo -e "\n${BRed}Open connections :$NC "; netstat -pan --inet;
    echo
}

#-------------------------------------------------------------
# Misc utilities:
#-------------------------------------------------------------

function repeat()       # Repeat n times command.
{
    local i max
    max=$1; shift;
    for ((i=1; i <= max ; i++)); do  # --> C-like syntax
        eval "$@";
    done
}



#-------------------------------------------------------------
# Imagemagick and Http utilities:
#-------------------------------------------------------------

function get_content_length ()
    {
    url="$1"
    size=$(curl -A "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -sI "$url" | grep Content-Length | awk '{print $2}');

}


function download_url_curl ()
    {
    url="$1"
        {
        size=$(curl -A "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -O "$url");
        echo "$size";
    }
}



function download_multifile_curl ()
    {
    url="$1"
    $(curl -A "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -O "${url}".png -O "${url}"_m.jpg -O "${url}"_l.jpg);

}


function img_multithumb_file ()
    {
        f="$1"
        dname=$(dirname "$f")
        fname=$(basename "$f")
        outdir="${dname}/output"
        mkdir -m 775 "${outdir}" ;
        format=`echo "$fname" | awk -F'.' '{ print $NF}'`;
        convert -format "${format}" "${f}" \
          \( +clone -resize x480 -write "${outdir}"/"${fname}"_l.jpg +delete \) \
          \( +clone -resize x240 -write "${outdir}"/"${fname}"_big.jpg +delete \) \
          \( +clone -resize x240 -write "${outdir}"/"${fname}"_m.jpg +delete \) \
             -define png:preserve-colormap -define png:format\=png24 \
             -define png:compression-level\=N -define png:compression-strategy\=N \
             -define png:compression-filter\=N -format "%w%"png "${outdir}"/"${fname}" ;
    }



#####
function img_trim_set_aspectratio ()
    {
    f="$1"
    IFSD="$IFS";
    dname=$(dirname "$f")
    fname=$(basename "$f")
    outdir="${dname}/output"
    export IFS="\n"
    convert ${f} -format jpg -crop `convert ${f} -virtual-pixel edge -blur "0x15" -fuzz "1%" -trim -format "%wx%h%O" info:` -background white +repage -gravity center -resize "1800x2160" -background white +repage -extent "2000x2400" -density 72x72 +repage -strip -quality 100 ${f}_new.jpg ;
        ## echo "${f}"_new.jpg ;
    export IFS="$IFSD";
}


function img_trim_set_bfly_ratio ()
    {
    f="$1"
    convert "${f}" -format jpg -crop $(convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim -format '%wx%h%O' info:) -background white +repage -gravity center -resize '1800x2160' -background white +repage -extent '2000x2400' -colorspace sRGB -unsharp 50 -strip -quality 100 "${f//.jpg/.jpg}";
    echo "${f//.jpg/_Ratioed_.jpg}" ;
    }


function img_return_width ()
    {
    f="$1"
    dmenwidth=$\(identify -verbose "${f}" | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'\);
    echo "$dmenwidth";
}


function img_return_height ()
    {
    f="$1"
    dmenheight=$\(identify -verbose  "${f}" | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'\);
    echo "$dmenheight" ;
}


function img_return_domclr ()
    {
    f="$1"
    domclr=`convert "${f}" -posterize 3 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`;
    echo "$domclr" ;
}


function img_return_wxhdpi ()
{
    identify -units 'PixelsPerInch' -format '"%w x %h %x x %y"' "$1";
}


function cache_clear_dir ()
{
    for f in $(find "$1" -maxdepth 4 -iname \*.jpg -exec basename {} \;| cut -c 1-9 | sort -nru); do
    /usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py "$f";
    done ;
}


function cache_clear_dir_postapi ()
{
    for f in $(find "$1" -maxdepth 1 -iname \*.jpg -exec basename {} \;| cut -c 1-9 | sort -nru); do
    curl -u johnb:admin -d updated_by="$USER" -d colorstyle="${f}" -X PUT http://prodimages.ny.bluefly.com/image-update/;
    curl -u johnb:admin -d updated_by="$USER" -d colorstyle="${f}" -X POST http://prodimages.ny.bluefly.com/image-update/;
    #-H 'Authorization: Token fb49f24a29060a350628fd9e9fb08b3b9762abbd'
    #/usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py "$f";
    echo "${USER} updated ${f} "$(date)"" ;
    done ;
}


function listyles (){
        {
        echo $(find "$1" -maxdepth 1 -iname \*.jpg -exec basename {} \;| cut -c 1-9 | sort -nru) ;
    };
}



function profilePyScript ()
    {
    scriptin="$1"
    #scriptname=`basename "${scriptin}"`
    scriptargs="$2"
    altoutdir="/home/johnb/Share"
    graphtype="dot" ##"$4"
    runtime=`date +%H%M%S`
    graphdir=/home/johnb/Share/PRODIMAGES_OUTPUT/debug_graphs
    graphout="${graphdir}"/"${scriptin//.py}"_"${runtime}".png
    mkdir -p "${graphdir}" ;
    cd "${graphdir}" ;
    pycallgraph -s --output-file="${graphout}" --tool "${graphtype}" -- /usr/local/batchRunScripts/python/"${scriptin}" "${scriptargs}" ;
    chmod ugo+rw "${graphout}" ;
    echo Graph Created "${graphout}" ;
}


function compfile_to_basefile ()
    {
    testImage="$1"
    if [[ "$#" > 1 ]]; then
        baseImage="$2"
    else
        baseImage=/mnt/Post_Complete/Complete_Archive/.PDP/base_pdp_na_x700.jpg
    fi;
    bnameTest=$(basename "${testImage}")
    bnameBase=$(basename "${baseImage}")
    cd $(dirname "${baseImage}")
    diffpix=$(convert "${testImage}" "${baseImage}" -resize "400x300!" MIFF:- | compare -metric AE -fuzz "10%" - null: 2>&1) ;
    if [[ $diffpix > 0 ]]; then
        echo "File `basename ${testImage}` has $(echo \"$diffpix\") Different Pixels vs the base input file `basename \"${baseImage}\"`"
    else
        mkdir -p matches/"${bnameBase}"_matches
        cp $baseImage matches/
        cp $testImage matches/"${bnameBase}"_matches

    fi;
}

function env_parallel() {
    export parallel_bash_environment='() {
        '"$(echo "shopt -s expand_aliases 2>/dev/null"; alias;typeset -p | grep -vFf <(readonly; echo GROUPS; echo FUNCNAME; echo DIRSTACK; echo _; echo PIPESTATUS; echo USERNAME) | grep -v BASH_;typeset -f)"'
    }'
    # Run as: env_parallel parallel_bash_environment "2>/dev/null;" ...
    `which parallel` "$@"
    unset parallel_bash_environment
}

######### NExt 3 basically the same, last one recursive
function listyles (){
        {
        echo $(find "$1" -maxdepth 1 -type f -exec basename {} \;| cut -c 1-9 | sort -nru) ;
    };
}
function find_styles (){
        {
        echo $(find "$1" -maxdepth 1 -type f -exec basename {} \;| cut -c 1-9 | sort -nru) ;
    };
}

function find_styles_recurse (){
        {
        echo $(find "$1" -type f -exec basename {} \;| cut -c 1-9 | sort -nru) ;
    };
}

#### Collect Marketplacer and send to my drop folder for processing magickLoad.py
function send_to_johnb_drop (){
    jbupload=/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/JohnBragato/
    cp /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/*/*.jpg $jbupload ;
    count=`ls $jbupload | wc -1`
    echo "Finshed moving ${count} to ${jbupload}"
}
## Split arg $1 by delimiter $2, and return last delimited field, ie. -1/$NF
function splitdelimit() { echo $1 | awk -F"$2" '{print $NF}' ; }


## Color text/prompt func
function elite
{

local GRAY="\[\033[1;30m\]"
local LIGHT_GRAY="\[\033[0;37m\]"
local CYAN="\[\033[0;36m\]"
local LIGHT_CYAN="\[\033[1;36m\]"
local NO_COLOUR="\[\033[0m\]"

case $TERM in
    xterm*|rxvt*)
        local TITLEBAR='\[\033]0;\u@\h:\w\007\]'
        ;;
    *)
        local TITLEBAR=""
        ;;
esac

local temp=$(tty)
local GRAD1=${temp:5}
PS1="$TITLEBAR $GRAY-$CYAN-$LIGHT_CYAN($CYAN\u$GRAY@$CYAN\h\$DARK_BLUE)$CYAN-$LIGHT_CYAN($CYAN\#$GRAY/$CYAN$GRAD1\$LIGHT_CYAN)$CYAN-$LIGHT_CYAN($CYAN\$(date +%H%M)$GRAY/$CYAN\$(date +%d-%b-%y)$LIGHT_CYAN)$CYAN-$GRAY-$LIGHT_GRAY\n\$GRAY-$CYAN-$LIGHT_CYAN($CYAN\$$GRAY:$CYAN\w\$LIGHT_CYAN)$CYAN-$GRAY-$LIGHT_GRAY "
PS2="$LIGHT_CYAN-$CYAN-$GRAY-$NO_COLOUR "
}

function recent_styles_uploaded ()
    {
        {
        if [[ "$#" > 0 ]]; then MINUTESAGO=$1
        else MINUTESAGO=60
        fi;
        local QUERY=`echo -e "select distinct t1.colorstyle from www_django.image_update t1 join product_snapshot_live t2 on t1.colorstyle=t2.colorstyle where create_dt > date_sub(now(), interval $MINUTESAGO minute) and (t2.image_ready_dt is not null and t2.image_ready_dt != \"0000-00-00\");"` ;
        RESULT=`mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e "$QUERY" -D www_django`
        #echo $(echo -e "$QUERY")
        echo "${RESULT[@]}"
        }

        #for f in $RESULT; do echo "$f"; done
}

# Local Variables:
# mode:shell-script
# sh-shell:bash
# End:
