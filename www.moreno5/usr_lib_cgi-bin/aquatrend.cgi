#!/bin/bash


## Strip HTML GET String into lcoal variables ##
STIME=`echo "$QUERY_STRING" | sed -n 's/^.*stime=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
ETIME=`echo "$QUERY_STRING" | sed -n 's/^.*etime=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
HIGHSCALE=`echo "$QUERY_STRING" | sed -n 's/^.*highscale=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
LOWSCALE=`echo "$QUERY_STRING" | sed -n 's/^.*lowscale=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
WIDTH=`echo "$QUERY_STRING" | sed -n 's/^.*width=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
HEIGHT=`echo "$QUERY_STRING" | sed -n 's/^.*height=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
TRENDTYPE=`echo "$QUERY_STRING" | sed -n 's/^.*ttype=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

case "$TRENDTYPE" in
'gauge1')

## Aquarium PH GRAPH ##
rrdtool graph /var/www/aqua.png --start $STIME --end $ETIME \
--upper-limit $HIGHSCALE --lower-limit $LOWSCALE --slope-mode --units-length 2 \
--interlaced \
--rigid \
--width $WIDTH --height 400 \
--vertical-label "pH\n" \
--color CANVAS#000000 \
--title "Aquarium pH" \
DEF:phv=/var/www/rrd/Marine.rrd:pnt_1:AVERAGE \
COMMENT:"\s" \
LINE1:phv#0000FF:"Ph=" \
VDEF:phlast=phv,LAST GPRINT:phlast:"%3.2lf%s" \
VDEF:phavg=phv,AVERAGE GPRINT:phavg:"avg=%3.2lf%spH \l" \
--watermark "Aquarium PH Graph">/dev/null
;;

'gauge2')
## Aquarium ORP GRAPH ##
rrdtool graph /var/www/aqua.png --start $STIME --end $ETIME \
--upper-limit $HIGHSCALE --lower-limit $LOWSCALE --slope-mode --units-length 2 \
--interlaced \
--rigid \
--width $WIDTH --height 400 \
--title "Aquarium ORP" \
--vertical-label "mV" \
--color CANVAS#000000 \
DEF:orp=/var/www/rrd/Marine.rrd:pnt_2:AVERAGE \
COMMENT:"\s" \
LINE1:orp#FF3D0D:"Orp=" \
VDEF:orplast=orp,LAST GPRINT:orplast:"%4.0lf%smV" \
VDEF:orpavg=orp,AVERAGE GPRINT:orpavg:"avg=%4.0lf%smV \l" \
--watermark "Aquarium ORP" >/dev/null
;;


'gauge3')
rrdtool graph /var/www/aqua.png --start $STIME --end $ETIME \
--upper-limit $HIGHSCALE --lower-limit 24 --slope-mode --units-length 2 \
--interlaced \
--rigid \
--width $WIDTH --height 400 \
--vertical-label "Degrees C" \
--color CANVAS#000000 \
--title "Aquarium Temperature" --vertical-label "Deg.C." \
DEF:degc1=/var/www/rrd/Marine.rrd:pnt_3:AVERAGE \
COMMENT:"\s" \
AREA:degc1#003366:"Aquariumm=" \
VDEF:degc1last=degc1,LAST GPRINT:degc1last:"%3.1lf%s" \
VDEF:degc1avg=degc1,AVERAGE GPRINT:degc1avg:"avg=%3.1lf%s \l" \
--watermark "Aquarium Temperature Graph" >/dev/null
;;


'gauge4')
## Temperature Profile ##
rrdtool graph /var/www/aqua.png --start $STIME --end $ETIME \
--upper-limit 35 --lower-limit 17 --slope-mode --units-length 2 \
--interlaced \
--rigid \
--width $WIDTH --height 400 \
--title "Tank Temperature Profile" --vertical-label "DegC" \
--color CANVAS#000000 \
COMMENT:"\s" \
COMMENT:"         Current  Average  Minimum  Maximum \l" \
COMMENT:"\s" \
DEF:degc2=/var/www/rrd/Marine.rrd:pnt_3:AVERAGE \
LINE1:degc2#FFFFFF:"Tank  " \
VDEF:degc2last=degc2,LAST GPRINT:degc2last:"%3.1lf%s" \
VDEF:degc2avg=degc2,AVERAGE GPRINT:degc2avg:" %3.1lf%s " \
VDEF:degc2min=degc2,MINIMUM GPRINT:degc2min:" %3.1lf%s "  \
VDEF:degc2max=degc2,MAXIMUM GPRINT:degc2max:"%3.1lf%sDegC \l"  \
DEF:degc5=/var/www/rrd/Marine.rrd:pnt_5:AVERAGE \
LINE1:degc5#0000FF:"Room  " \
VDEF:degc5last=degc5,LAST GPRINT:degc5last:"%3.1lf%s" \
VDEF:degc5avg=degc5,AVERAGE GPRINT:degc5avg:" %3.1lf%s " \
VDEF:degc5min=degc5,MINIMUM GPRINT:degc5min:" %3.1lf%s "  \
VDEF:degc5max=degc5,MAXIMUM GPRINT:degc5max:"%3.1lf%sDegC \l"  \
DEF:degc4=/var/www/rrd/Marine.rrd:pnt_4:AVERAGE \
COMMENT:"\s" \
LINE1:degc4#F555FF:"Heater" \
VDEF:degc4last=degc4,LAST GPRINT:degc4last:"%3.1lf%s" \
VDEF:degc4avg=degc4,AVERAGE GPRINT:degc4avg:" %3.1lf%s " \
VDEF:degc4min=degc4,MINIMUM GPRINT:degc4min:" %3.1lf%s "  \
VDEF:degc4max=degc4,MAXIMUM GPRINT:degc4max:"%3.1lf%sDegC \l"  \
--watermark "Reef Temperature Graph" >/dev/null
;;

'gauge5')
rrdtool graph /var/www/aqua.png --start $STIME --end $ETIME \
--upper-limit $HIGHSCALE --lower-limit $LOWSCALE --slope-mode --units-length 2 \
--interlaced \
--rigid \
--width $WIDTH --height $HEIGHT \
--slope-mode \
--title "Aquarium Spare" --vertical-label "XXXXX" \
--color CANVAS#000000 \
HRULE:25#FF0000: \
DEF:co21=/var/www/rrd/Marine1.rrd:pnt_5:AVERAGE \
AREA:co21#1DA237:"XXX" \
VDEF:co2last=co21,LAST GPRINT:co2last:"%4.1lf%sppm" \
VDEF:co2avg=co21,AVERAGE GPRINT:co2avg:"avg=%4.1lf%sppm      " \
--watermark "Aquarium Spare"  >/dev/null
;;

esac

## Send output to web page ##
echo Content-type: image/png
echo
cat /var/www/aqua.png
