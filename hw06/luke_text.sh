# Here's how to use imagemagick to display text
# Make a blank image
SIZE=320x240
TMP_FILE=/tmp/frame.png

# From: http://www.imagemagick.org/Usage/text/
convert -texture tux.png -fill blue -font Times-Roman -pointsize 24 \
      -size $SIZE \
      label:"Luke's BeagleBone Blue" \
      -draw "text 0,200 'Bottom of Display'" \
      $TMP_FILE

sudo fbi -noverbose -T 1 $TMP_FILE

# convert -list font
