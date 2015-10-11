#!/usr/bin/env python
# -*- coding: utf-8 -*-
patterns = [r'^.*?/bc_jpg_makerDrop/(crop_fullsize_pad_center)/?.*?/(\d{9}(.*?))\.(.*?)$',
            r'^.*?/bc_jpg_makerDrop/(crop_fullsize_pad_anchor)/?.*?/(\d{9}(.*?))\.(.*?)$',
            r'^.*?/bfly_jpg_makerDrop/(crop_fullsize_center)/?.*?/(\d{9}(.*?))\.(.*?)$', 
            r'^.*?/bfly_jpg_makerDrop/(crop_fullsize_anchor)/?.*?/(\d{9}(.*?))\.(.*?)$']*10

strings = ["/mnt/Post_Complete/Complete_to_Load/nature_center/bc_jpg_makerDrop/crop_fullsize_pad_anchor/346470409.png", 
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bc_jpg_makerDrop/crop_fullsize_pad_center/346470408_1.jpg",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bc_jpg_makerDrop/crop_fullsize_pad_anchor/346470407_alt01.png",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bc_jpg_makerDrop/crop_fullsize_pad_center/346470406_1.png",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bfly_jpg_makerDrop/crop_fullsize_anchor/346880405.png",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bfly_jpg_makerDrop/crop_fullsize_center/346470404_1.jpg",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bfly_jpg_makerDrop/crop_fullsize_center/346470403.png",
            "/mnt/Post_Complete/Complete_to_Load/nature_center/bfly_jpg_makerDrop/crop_fullsize_anchor/336470402.jpg"]*10


def matches_pattern(str, patterns):
    for pattern in patterns:
        if pattern.match(str):
            return pattern.match(str), pattern
    return False



def regex_matcherator(strings,patterns):
    import re
    compiled_patterns = list(map(re.compile, patterns))
    for s in strings:
        if matches_pattern(s, compiled_patterns):
            print matches_pattern(s, compiled_patterns)[1].pattern
            print '--'.join(s.split('/')[-2:])
            print matches_pattern(s, compiled_patterns)[0].groups()
            print '\n'





r = regex_matcherator(strings,patterns)
#print r.next()