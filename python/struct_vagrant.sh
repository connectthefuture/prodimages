#!/bin/bash

. ~/.bash_profile

## if [[ $1 ]];
## then;
rootdir=$1;
## else;
##   rootdir='django_home'
## fi;

# Create "$rootdir" directory in our home directory
mkdir ~/"$rootdir"

# Change into the newly created ~/"$rootdir" directory
cd ~/"$rootdir"

# Create a place for the Chef cookbooks
mkdir ~/"$rootdir"/cookbooks

# Change into the newly created ~/"$rootdir"/cookbooks directory
cd ~/"$rootdir"/cookbooks

# Clone the Chef cookbooks repositories as needed (we will use the following cookbooks in this guide)
git clone git://github.com/opscode-cookbooks/apache2.git
git clone git://github.com/opscode-cookbooks/apt.git
git clone git://github.com/opscode-cookbooks/build-essential.git
git clone git://github.com/opscode-cookbooks/git.git
git clone git://github.com/opscode-cookbooks/vim.git
git clone git://github.com/opscode-cookbooks/python.git
git clone git://github.com/opscode-cookbooks/pip.git

