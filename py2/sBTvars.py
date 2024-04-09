# -- basics py methods

import mf

from subprocess import Popen, PIPE, STDOUT,check_output
import os,sys,glob,time,getopt,copy,getpass,struct,errno
import inspect
import shelve
import cPickle as pickle
from socket import gethostname,getfqdn
import datetime

from time import time as timer
from time import sleep,mktime
from types import StringType,IntType,FloatType,ListType,DictType,TupleType
from math import atan2,atan,pi,fabs,cos,sin,log,tan,acos,sqrt
import array

import zipfile
import filecmp

# -- get local vars -- installation dependent
#
from sbtLocal import *

#sbtRootVer="%s/%s"%(sbtRoot,sbtVersion)
# -- root ver is the root in the v04 distro
sbtRootVer = sbtRoot

versionDev='v03'
versionBT=sbtVersion.lower()

# -- VVVVVVVV - sBT dirs & vars
#

bm3year=2007
em3year=2022
em3yearP1=em3year+1
 
sbtMeta='h-meta-sbt-%s-vars.csv'%(versionBT)
md3SumMeta='h-meta-md3-sum.csv'
md3VarsMeta='h-meta-md3-vars.csv'

sbtVerDirDat="%s/dat"%(sbtRootVer)

sbtDatDir="%s/dat"%(sbtRoot)
sbtProdDir='%s/products/tcdiag'%(sbtRoot)
sbtSrcDir="%s/src"%(sbtRoot)

sbtVerDirTcPrc="%s/%s"%(sbtRoot,versionDev)
sbtVerDir=sbtRootVer

sbtVerDirDatTcPrc="%s/dat"%(sbtVerDirTcPrc)
sbtPrcDirTcdiag="%s/prc/tcdiag"%(sbtVerDirTcPrc)
sbtPrcDirTctrk="%s/prc/tctrk"%(sbtVerDirTcPrc)

sbtGeogDatDir="%s/geog"%(sbtVerDirDatTcPrc)
sbtGslibDir="%s/gslib"%(sbtVerDirTcPrc)

tsbdbdir="%s/tcdiag"%(sbtDatDir)
adeckSdir="%s/adeck-dtg"%(sbtDatDir)
tmtrkbdir="%s/tmtrkN"%(sbtDatDir)
abdirStm='%s/adeck-stm'%(sbtDatDir)
abdirDtg='%s/adeck-dtg'%(sbtDatDir)

TcNamesDatDir="%s/tc/names"%(sbtVerDirDat)
TcVitalsDatDir="%s/tc/tcvitals"%(sbtDatDir)

W2BaseDirPrc="%s/prc/"%(sbtVerDirTcPrc)

# -- lsdiag
#
TcTcanalDatDir="%s/tcdiag"%(sbtDatDir)
TcDiagDatDir=TcTcanalDatDir

# -- wxmap2 dirs not part of repo
#
W2BaseDirDat='/data/w22/dat/'
Nwp2DataBdir='%s/nwp2'%(W2BaseDirDat)
era5bdir='%s/nwp2/w2flds/dat/era5'%(W2BaseDirDat)

# -- source data for pr
#
PrGsmapV6GProducts='%s/pr/pr_gsmapV6-Grev'%(W2BaseDirDat)
PrCmorphV10Products='%s/pr/pr_cmorph-v10'%(W2BaseDirDat)
PrCmorphVX0Products='%s/pr/pr_cmorph'%(W2BaseDirDat)
PrImergV06Products='%s/pr/pr_imerg'%(W2BaseDirDat)


W2plotXsize=900
W2plotAspect=3.0/4.0


# -- VVVVVVVV -- basic constants and settings
#

pi=4.0*atan2(1.0,1.0)
pi4=pi/4.0
pi2=pi/2.0

deg2rad=pi/180.0
rad2deg=1.0/deg2rad

# -- earth ~ flattened sheriod r=6335.4 -> 6399.6 km
# this values is mean GC distance
#
rearth=6371.0

km2nm=60.0/(2*pi*rearth/360.0)
nm2km=1.0/km2nm
deglat2km=((2.0*pi*rearth)/360.0)
deglat2nm=60.0
knots2ms=1000.0/(km2nm*3600.0)
ms2knots=1.0/knots2ms

# -- units 
#
tcunits='metric'
tcunits='english'

# -- epsilon
#
epsilon=1e-10
epsilonm5=1.0e-5

# --- wmo gravity
#
gravity=9.80665

# -- VVVVVVVV -- mfbase
#
MandatoryPressureLevels=[1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10]

# -- set units or 'metric'
#
units='english'

# -- 20030828 -- set calendar; can change by calendar='365day'
#
calendar='gregorian'

# -- new future w3 vars for moving to hopper.orc.gmu.edu
# -- funny place to put because of the many imports

ptmpBaseDir=os.getenv('PTMP')


# -- VVVVVVVV -- tcVM.py
#

# tc parameters/limits
#
TCvmin=25.0
#TCvmin=30.0

vmaxTS=35.0
vmaxTY=65.0

IPerror=15.0 # nmi

ddtgTrack=6

Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'H':'SH', # -- to handle both s and p for shem
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'T':'SA',
    'X':'XX',
}

Basin1toHemi = {
    'A':'nhem',
    'B':'nhem',
    'L':'nhem',
    'I':'nhem',
    'S':'shem',
    'P':'shem',
    'W':'nhem',
    'C':'nhem',
    'E':'nhem',
    'Q':'shem',
    'T':'shem',
    'H':'shem',
    'X':'XXXX',
}

Basin1toFullBasin = {
    'A':'nio',
    'B':'nio',
    'L':'lant',
    'I':'nio',
    'S':'shem',
    'H':'shem',
    'P':'shem',
    'W':'wpac',
    'C':'cpac',
    'E':'epac',
    'Q':'slant',
    'T':'slant',
    'X':'XXXXX',
}

Basin2toBasin1 = {
    'IO':'I',
    'SH':'P',
    'SH':'S',
    'SI':'S',
    'SP':'P',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AT':'L',
    'AL':'L',
    'NA':'L',
    'SL':'Q',
    'SA':'T',
    'BB':'B',
    'AS':'A',
    'AA':'A',
    'XX':'X',
    # -- default in gettrk_gen.x  how he handles 'I' storms...
    'HC':'I',
}


ClimoBasinsHemi = {
    'NHS':['nhem','wpac','epac','lant','nio','shem','global'],
    'SHS':['shem','sio','swpac','nhem','global'],
}

Basin2toBasin1Tpc = {
    'IO':'I',
    'SP':'P',
    'SL':'Q',
    'SI':'S',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AL':'L',
    'NA':'A',
    'BB':'B',
}


Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AT',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'H':'SH',
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'X':'XX',
}

Basin1toForecastCenter = {
    'A':'JTWC',
    'B':'JTWC',
    'L':'NHC',
    'I':'JTWC',
    'S':'JTWC',
    'P':'JTWC',
    'W':'JTWC',
    'C':'CPHC',
    'E':'NHC',
    'Q':'NHC',
    'X':'XHC',
}

Basin1toButtonStyle = {
    'A':'bnio',
    'B':'bnio',
    'L':'blant',
    'I':'bnio',
    'S':'bsio',
    'P':'bspac',
    'W':'bwpac',
    'C':'bcpac',
    'E':'bepac',
    'Q':'blant',
}

Basin1toButtonColor = {
    'A':'wheat',
    'B':'wheat',
    'L':'pink',
    'I':'wheat',
    'S':'#ADD8E6',
    'P':'#EE82EE',
    'W':'#EE82EE',
    'C':'lightgreen',
    'E':'lightgrey',
    'Q':'pink',
}

Basin1toBasinNumber = {
    'L':'1',
    'E':'2',
    'W':'3',
    'C':'4',
    'A':'5',
    'B':'6',
    'I':'7',
    'S':'8',
    'P':'9',
    'Q':'10',
}

Basin1toBasinName = {
    'A':'   ASEA - Arabian Sea',
    'B':'   BAYB - Bay of Bengal',
    'L':'   LANT - north Atlantic',
    'I':'    NIO - north Indian Ocean',
   'S':'    SIO - south Indian Ocean',
    'P':'  SPWAC - southwest Pacific',
    'W':'WESTPAC - western North Pacific',
    'C':'CENTPAC - central North Pacific',
    'E':'EASTPAC - eastern North Pacific',
    'Q':'  SLANT - south Atlantic'
}

Basin1toBasinNameShort = {
    'A':'ASEA',
    'B':'BAYB',
    'L':'LANT',
    'I':'NIO',
    'S':'SIO',
    'P':'SPWAC',
    'W':'WESTPAC',
    'C':'CENTPAC',
    'E':'EASTPAC',
    'Q':'SLANT'
}

Basin1toHemi1 = {
    'A':'N',
    'B':'N',
    'L':'N',
    'I':'N',
    'S':'S',
    'P':'S',
    'W':'N',
    'C':'N',
    'E':'N',
    'Q':'S',
}

Basin1toHemi3 = {
    'A':'NHS',
    'B':'NHS',
    'L':'NHS',
    'I':'NHS',
    'S':'SHS',
    'P':'SHS',
    'W':'NHS',
    'C':'NHS',
    'E':'NHS',
    'Q':'SHS',
}

Basin1toHemi4 = {
    'A':'nhem',
    'B':'nhem',
    'L':'nhem',
    'I':'nhem',
    'S':'shem',
    'P':'shem',
    'W':'nhem',
    'C':'nhem',
    'E':'nhem',
    'Q':'shem',
}

Basin1toBasin3 = {
    'A':'nio',
    'B':'nio',
    'I':'nio',
    'L':'atl',
    'S':'shm',
    'P':'shm',
    'W':'wpc',
    'C':'epc',
    'E':'epc',
    'Q':'slt',
    'T':'slt',
}


SuperBasins=['NHS','SHS','LTS','WPS','EPS','NIS']

Hemi1toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
}

Hemi3toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
}

Hemi3toHemiNameShort = {
    'NHS':'NHEM',
    'SHS':'SHEM',
    'LTS':'LANT SB',
    'WPS':'WPAC SB',
    'EPS':'EPAC SB',
    'NIS':'NIO  SB',
}

Hemi1toHemiVeriName = {
    'NHS':'nhem',
    'SHS':'shem',
    'LTS':'lant',
    'WPS':'wpac',
    'EPS':'epac',
    'NIS':'nio',
}

Hemi1toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
}

Hemi3toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
}

Hemi3toSuperBasins = {
    'NHS':('NHS','NIS','WPS','EPS','LTS'),
    'SHS':('SHS','S','P','Q'),
}

BasinsAll=['L','E','C','W','A','B','I','S','P','Q']


TcGenBasin2Area={
    'lant':'troplant',
    'epac':'tropepac',
    'wpac':'tropwpac',
    'shem':'tropshem',
    'nio':'tropnio',
}

TcGenBasin2PrwArea={
    'lant':'prwLant',
    'epac':'prwEpac',
    'cepac':'prwCEpac',
    'wpac':'prwWpac',
    'shem':'prwSpac',
    'nio':'prwIo',
}

TcGenBasin2B1ids={
    'lant':['l'],
    'epac':['c','e'],
    'wpac':['w'],
    'shem':['s','p'],
    'nio':['a','b'],
}

b1id2tcgenBasin={
    'w':'wpac',
    'e':'epac',
    'c':'epac',
    'l':'lant',
    's':'shem',
    'p':'shem',
    'a':'nio',
    'b':'nio',
    't':'lant',
    }


tdmin=25.0
tsmin=35.0
tymin=65.0
stymin=130.0

peakNhemMMDDHH='090100'
peakShemMMDDHH='021500'

#primeMeridianChk=60.0 -- too big for AS, e.g., 01A.12
primeMeridianChk=30.0

centerid='MFTC'
tcVcenterid='M2TC'

maxNNnum=49

tcVcenterid='M3TC'
global undef,taus,oPrsizMin,\
       radInfPrKm,radInfPrNM,\
       radInfPrKM,radkms,oPrpre

undef=-999.0
undefVar=1e20

taus=[0,12,24,48,72]
taus=[0,6,12,18,24]
taus=[6,12,18]
taus=[6,12]
# -- only using 6-h precip accumulations...
taus=[6]

oPrsizMin=0
radInfPrKm=[300,500,800]
radInfPrNM={}
radInfPrKM={}

def nint(f):
    if(f>=0.0): rc=int(f+0.5)
    if(f<=0.0): rc=int(f-0.5)
    return(rc)

for rad in radInfPrKm:
    radn=nint(rad*km2nm)*1.0
    radInfPrNM[rad]=radn
    radInfPrKM[radn]=rad
    
radkms=radInfPrNM.keys()
radkms.sort()

oPrpre='pr'
mname = {
'01':'January',
'02':'February',
'03':'March',
'04':'April',
'05':'May',
'06':'June',
'07':'July',
'08':'August',
'09':'September',
'10':'October',
'11':'November',
'12':'December'
}

mname3 = {
'01':'Jan',
'02':'Feb',
'03':'Mar',
'04':'Apr',
'05':'May',
'06':'Jun',
'07':'Jul',
'08':'Aug',
'09':'Sep',
'10':'Oct',
'11':'Nov',
'12':'Dec'
}

cname3 = {
'JAN':'01',
'FEB':'02',
'MAR':'03',
'APR':'04',
'MAY':'05',
'JUN':'06',
'JUL':'07',
'AUG':'08',
'SEP':'09',
'OCT':'10',
'NOV':'11',
'DEC':'12'
}



#
#  add 0 for indexing by month vice month-1
#
mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
aday=(1,32,60,91,121,152,182,213,244,274,305,335)
adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)


sec2hr=1/3600.0

sbtB1id2Basin={
    'e':'epac',
    'c':'cpac',
    'w':'wpac',
    'i':'io',
    'a':'io',
    'b':'io',
    's':'shem',
    'p':'shem',
    'h':'shem',
    'l':'lant',
}

# -- VVVVVVVVVVVVVVVV -- w2localvars
#
Nwp2ModelsNwp=   ['gfs2','fim8','ecm2','ukm2','ngp2','cmc2',
                  'ngpc','navg',
                  'ohc','ocn','ww3','gfsc','ukmc','jmac','ngpj']

Nwp2ModelsAll=   [
		 'gfs2','fim8','ecm2','ukm2',
         'cmc2','cgd2',
         'ngp2','navg',
		 'fv3e','fv3g','fv7e','fv7g',
		 'hwrf','era5','ecm5',
         'jgsm',
		 'ohc','ocn','ww3','gfsc','ukmc','jmac','ngpj','goes','gfsr','gfr1','ecmn','ecmg','ecmt','ecm4']

Nwp2ModelsActive=[
	'gfs2','ecm2','ukm2','cmc2','navg',
	'fv7e','fv7g',
	'hwrf',
    'era5',
	'ohc','ocn','ww3','gfsc','ukmc','jmac','ngpj','goes','ecm4','ecm5'
	] # -- 20180120 -- deprecate fim and nws ecmwf

# -- on tenki7
# -- 20211130 -- ecmt working now with vsmf2 .ecmwfapirc
Nwp2ModelsActive=[
	'gfs2','ecm5','navg','cgd2','jgsm','ecmt',
	] 

Nwp2ModelsActive0618=[
	'gfs2','navg','jgsm',
	] 

Nwp2ModelsActiveAll=copy.deepcopy(Nwp2ModelsActive)
try:
    Nwp2ModelsActiveAll.remove('goes')
except:
    None
	
Nwp2ModelsActiveW2flds=Nwp2ModelsActiveAll
Nwp2ModelsActW20012=Nwp2ModelsActiveAll
Nwp2ModelsActW20618=Nwp2ModelsActive0618



