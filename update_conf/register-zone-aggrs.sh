#! /usr/bin/env bash

WORKING_DIR=`pwd`
AGGR_LIB=$WORKING_DIR/aggr-lib
CONF_LIB=$WORKING_DIR/conf-lib

#### Define the Input Variables to Register the AGGR switch......
#
if [[ $# != 8 ]]
then
 echo "[ error ] $0 command is required like below"
 echo "$0"
 echo "     [   PLATFORM   ] : cloudstack or openstack"
 echo "     [   ZONE_NAME  ] : zone name such as epc, ktis and dmz"
 echo "     [   POD_TYPE   ] : product type such as prod, tb, dev"
 echo "     [   AGG_TYPE   ] : service or storage"
 echo "     [  AGGR1_NAME  ] : first aggregation switch name"
 echo "     [   AGGR1_LO   ] : first aggregation loopback ip address"
 echo "     [  AGGR2_NAME  ] : second aggregation switch name"
 echo "     [   AGGR2_LO   ] : second aggregation loopback ip address"
 exit
fi

PLATFORM=$1
ZONE_NAME=$2
POD_TYPE=$3
AGG_TYPE=$4
AGGR1_NAME=$5
AGGR1_LO=$6
AGGR2_NAME=$7
AGGR2_LO=$8

#### Loopback IP address Confirmation.......
#
AGGR1_LO_MASK=`echo $AGGR1_LO | awk -F'[/]' '{print $2}'`
if [[ $AGGR1_LO_MASK ]]
then
 if [[ $AGGR1_LO_MASK != 32 ]]
 then
  echo "$AGGR1_LO is wroing subnet [32bit]......"
  exit
 else
  AGGR1_LO=`echo $AGGR1_LO | awk -F'[/]' '{print $1}'`
 fi
fi

AGGR2_LO_MASK=`echo $AGGR2_LO | awk -F'[/]' '{print $2}'`
if [[ $AGGR2_LO_MASK ]]
then
 if [[ $AGGR2_LO_MASK != 32 ]]
 then
  echo "$AGGR2_LO is wroing subnet [32bit]......"
  exit
 else
  AGGR2_LO=`echo $AGGR2_LO | awk -F'[/]' '{print $1}'`
 fi
fi

#### Create the AGGR Environment files......
#
AGGR_CONF_FILE=$AGGR_LIB/$PLATFORM.$ZONE_NAME.$POD_TYPE.$AGG_TYPE-aggrs
if [[ -f $AGGR_CONF_FILE ]]
then
 echo "$AGGR_CONF_FILE has been already existed....."
 exit
fi
touch $AGGR_CONF_FILE
chmod 777 $AGGR_CONF_FILE
echo "${AGG_TYPE^^}""_AGGR1_NAME=$AGGR1_NAME" > $AGGR_CONF_FILE
echo "${AGG_TYPE^^}""_AGGR1_LO=$AGGR1_LO" >> $AGGR_CONF_FILE
echo "${AGG_TYPE^^}""_AGGR2_NAME=$AGGR2_NAME" >> $AGGR_CONF_FILE
echo "${AGG_TYPE^^}""_AGGR2_LO=$AGGR2_LO" >> $AGGR_CONF_FILE

### run status print
echo "completed"
