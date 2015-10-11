 #!/usr/bin/python
 
 BaseName => {
            Require => {
                0 => 'FileName',
            },
            # remove the extension from FileName
            ValueConv => 'my $name=$val[0]; $name=~s/\..*?$//; $name',
        },
        # the following examples demonstrate simplifications which may be
        # used if only one tag is Require'd or Desire'd:
        # 1) the Require lookup may be replaced with a simple tag name
        # 2) "$val" may be used to represent "$val[0]" in the expression
        FileExtension => {
            Require => 'FileName',
            ValueConv => '$val=~/\.([^.]*)$/; $1',