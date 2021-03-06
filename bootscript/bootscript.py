#!/usr/bin/python
import os, re, subprocess, sys, urllib, string, Tac, EntityManager
sys.stdout

# This points to the ZTP server, change the IP address to match the server
# This address is using the HTTP Protocol
configUrl = "http://30.0.0.3/%s/%s"
swiUrl = "http://30.0.0.3/swi/%s"
request_swiversion="4.12.5.1"
swiversion = ''

# Look at the boot-config file and get the currently set EOS version
fd = open("/etc/swi-version", "r")
for item in fd:
   if "SWI_VERSION=" in item:
      swiversion = item.strip('SWI_VERSION=|\n')
fd.close()

#This allows output to the console during boot time
def printLog( logmsg ):
    print logmsg
    os.system( '/usr/bin/logger -p local4.crit -t ZeroTouch %s' % logmsg )


def mountEntity( sysdb, *args, **kwargs ):
   mg = sysdb.mountGroup()
   entity = mg.mount( *args, **kwargs )
   mg.close( blocking=True )
   return entity

# Mount lldpStatus from sysdb
def mountSysdb():
   global lldpStatus
   sysname = os.environ.get( "SYSNAME", "ar" )
   sysdb = EntityManager.Sysdb( sysname=sysname )
   try:
      swiVersionSplit = map(int, swiversion.split( '.' ))
      #Added this check to account for Sysdb change in 4.12.0
      if swiVersionSplit[0] == 4 and swiVersionSplit[1] > 11:
         lldpStatus = mountEntity( sysdb, 
					   "l2discovery/lldp/status/all",
					   "Lldp::AllStatus", "r" )
      elif swiVersionSplit[0] == 4 and swiVersionSplit[1] < 12:
          lldpStatus = mountEntity( sysdb, 
					   "l2discovery/lldp/status",
					   "Lldp::Status", "r" )
   except e:
		printLog ('Failed to mount lldpStatus, Sysdb may have changed structure')
		sys.exit( 1 )
		
   if not lldpStatus:
         printLog( 'Failed to mount lldpStatus' )
         sys.exit( 1 )

def escapedString( origString ):
   """Return the origString with all non-printable characters escaped
   with the exception of a null byte terminator, which is stripped"""
   # we strip terminating NUL characters because some buggy 
   # D-Link switches transmit them
   s = []
   for char in origString.rstrip( '\0' ):
      if char in string.printable:
         s.append( char )
      else:
         s.append( "\\x%02x" % ord( char ) )
   return ''.join( s )

def getNeighPortDescription( intf ):   
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.portId:
         return escapedString( obj.portId )
   return None


def getNeighPortName( intf ):
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.portDesc:
         return escapedString( obj.portDesc )
   return None

   
def getNeighDeviceDescription( intf ):   
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.sysName:
         return escapedString( obj.sysName )
   return None
   
mountSysdb()
# Get neighbor device and portid for Ma1
neighDevice = getNeighDeviceDescription('Management1')
neighPort = getNeighPortDescription('Management1')
neighPortifname = getNeighPortName('Management1')

# Parse the Data from LLDP values
mgmtDevice=neighDevice.split(r".")[0]
mgmtPortDesc=neighPort.split()[0]

# Create the get config URL in the form http://ztp-server/config/vEOSMGMT/Ethernet1
parsedUrl = configUrl % (mgmtDevice, mgmtPortDesc)
printLog ( '[ ejun logger ] config down parsedUrl is %s' % (parsedUrl))

# Download the config to flash
# Check if the switch is in the database.
if not urllib.urlopen( parsedUrl ).read() == "Device not found":
	urllib.urlretrieve(parsedUrl, '/mnt/flash/startup-config')
else:
	printLog( "Device not in the database, exiting" ) 
	sys.exit( 1 )

# Build the URL that sends the current switch version
parsedUrl = swiUrl % (request_swiversion)
printLog ( '[ ejun logger ] swi down parsedUrl is %s' % (parsedUrl))

#Download the new EOS if we need it.
downlad_status=False
if request_swiversion == swiversion:
 download_status=False
else:
 download_status=True

eosFilename = None
ret = urllib.urlopen(parsedUrl)
updateBootConfig = True
err = 0

#if ret.geturl() == parsedUrl:
if not download_status:
   printLog('No Update Required')
   updateBootConfig = False
else:
	eosFilename = ret.geturl().rsplit("/")[-1]
	printLog('Update Required - Getting %s' % eosFilename)
	try:
		download = True
		#Check if the file is on the server to download
		#if ret.info()['content-type'] == 'text/html':
		if int(ret.info()['content-length']) < 1024 :
			printLog('EOS File %s not present on ZTP server, upload to /usr/share/autoprovision/media' % eosFilename)
			printLog('ZTP Exiting')
			updateBootConfig = False
			err = 1
		#elif ret.info()['content-type'] == 'application/octet-stream':
                else:
			#Check if the file already exists.
			if not os.path.isfile('/mnt/flash/%s' % eosFilename):
				download = True
			#It doesn't exist locally
			else:
				# Get the size of the file on the server and locally
				swiSize = ret.info()['content-length']
				localFileSize = str(os.stat('/mnt/flash/%s' % eosFilename).st_size)
				if swiSize == localFileSize:
					printLog ('EOS file already exists, no download required.')
					download = False
			# Do we need to download the EOS Image
			if download == True:
				# Get the size of the file on the server
				swiSize = ret.info()['content-length']
				urllib.urlretrieve(parsedUrl, '/mnt/flash/%s' % eosFilename)
	                        printLog('download url = %s' % parsedUrl)
				# After it has downloaded, get the size on flash
				localFileSize = str(os.stat('/mnt/flash/%s' % eosFilename).st_size)
				# If the sizes don't match, restart.
				if swiSize == localFileSize:
					printLog ('Downloaded %s' % eosFilename)
				else:
					printLog ('Download failed, exiting')
					updateBootConfig = False
					err = 1
	except (IOError, urllib.ContentTooShortError):
		printLog ('Download Failed')
		updateBootConfig = False
		err = 1
	
# Change the boot-config file to new version
if updateBootConfig:
    fd = open("/mnt/flash/boot-config", "w")
    fd.write("SWI=flash:%s\n\n" % eosFilename)
    fd.close()

sys.exit( err )

