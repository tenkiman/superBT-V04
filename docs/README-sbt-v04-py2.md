<div align="center">

<h1>The .py(2) interface</h1>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 10 May 2024 </b>
</div>

I know python2 has been long deprecated, but as an old-guy, long-time python
user, and the availability of both in [anaconda.org](https://anaconda.org
"https://anconda.org") distros, decided to leave it up to modern users to the
convert to python3 and/or convert to run on either.

### Table of Contents

- [Installation](#installation)
- [Four Applications](#four-applications)
- [Command-line interface](#command-line-interface)
  * [TC codes in the `-S` option and the md3 track files](#tc-codes-in-the--s-option-and-the-md3-track-files)
  * [TCs are labelled/numbered using the NNB.YYYY format](#tcs-are-labellednumbered-using-the-nnbyyyy-format)
  * [Application Documentation](#application-documentation)
- [p-md3-ls.py - list positions by DTG or storm](#p-md3-lspy---list-positions-by-dtg-or-storm)
- [p-md3-stm-anl.py - analyze 9Xdev v 9Xnon](#p-md3-stm-anlpy---analyze-9xdev-v-9xnon)
- [p-sbt-v04-anl-ts.py - analyze time series of sBT variables](#p-sbt-v04-anl-tspy---analyze-time-series-of-sbt-variables)
- [p-sbt-v04-anl-var.py - list/analyze sBT variables (under development)](#p-sbt-v04-anl-varpy---listanalyze-sbt-variables-under-development)

## Installation

The `py2/` directory comes with two examaple `sbtLocal.py` files

- `sbtLocal.py-mac` (used on my macbook)
- `sbtLocal.py-mike5` (on my openSuse virtual machine)

create a sbtLocal.py in the (full path) directory you installed, e.g., if in

`/home/user1/superBT/`

then the `sbtLocal.py` file would be:

```
# -- full path with local installation directories
#
sbtRoot='/home/user1/superBT/'
sbtVersion='V04'
```

The `sbtRoot` python variable tells the applications where the dat/ and py2/
are located

Here is the ['mike5' openSuse computer environment](README-sbt-mike5.md).

## Four Applications

The main applications are:

To list and analyze the md3 data:

- [p-md3-ls.py](../py2/p-md3-ls.py)  list positions by DTG or storm
- [p-md3-stm-anl.py](../py2/p-md3-stm-anl.py) analyze 9Xdev v 9Xnon

To list and analyze the sBT data:

- [p-sbt-v04-anl-ts.py](../py2/p-sbt-v04-anl-ts.py)  analyze time series of sBT variables
- [p-sbt-v04-anl-var.py](../py2/p-sbt-v04-anl-var.py) list/analyze sBT variables (under development)


## Command-line interface

The four applications provided are run using a command-line interface. Data are accessed/sliced with two basic options:

- ```-S``` by 'S'torm

For example, `-S w.07` would pull all WPAC storms from 2007

- ```-d``` by date-time using the 'DTG' (Date-Time-Group) **`YYYYMMDDHH`**

For example, 12 UTC 1 July 2022 would be coded as `2022070112` NB: sometimes the HH can be dropped to indicate the date only


### TC codes in the `-S` option and the md3 track files

[NHEMcodes]: ## "
B - Bay of Bengal
A - Arabian Sea
I - North Indian Ocean (NIO) both B & A
W - Western north PACific (WPAC)
C - Central north PACific (CPAC)
E - Eastern north PACific (EPAC)
L - north atLANTic (LANT)
"

[SHEMcodes]: ## "
S - South Indian Ocean (SIO)
P - southwest Pacific ocean
H - SHEM S & P 
"

[TCs]: ## "
TD  - Tropical Depression : Vmax < 35 kts
TS  - Tropical Storm      : Vmax >=35 & Vmax < 64 kts
HU  - Hurricane           : Vmax >=65kts
STY - Super Typhoon       : Vmax >= 130 kts
SD  - Subtropical Depression : Vmax < 35 kts
SS  - Subtropical Storm      : Vmax >=35 & Vmax < 64 kts
"


- three TC types [**NN**][TCs] (mouse over) ; **9Xdev** ; **9Xnon**
  - **NN** - [a numbered/named TC in the JTWC/NHC BT files][TCs] (mouse over)
  - **9Xdev** - the pre/potential TC (pTC or 9X) disturbance that developed into an **NN** TC
  - **9Xnon** - pTC that did ***not develop*** into an **NN** TC

- **TC type code**
  - LO,DB,WV,MT,TD,TS,TY,ST,SD,SS,XT

- **pre TC (9Xdev and 9Xnon)**

  - LO	low
  - DB	disturbance
  - WV	wave
  - MT	monsoon trough

- **TC**

  - TD	tropical depression
  - TS	tropical storm
  - TY	hurricane/typhoon
  - ST 	super typhoon (Vmax >= 130 kts)

- **sub-tropical TC**

  - SD	subtropical depression
  - SS	subtropical storm

- **eXtra-tropical TC**

  - XT	eXtra-tropical cyclone


### TCs are labelled/numbered using the NNB.YYYY format

- NN : storm number
- B  : basin code for [NHEM][NHEMcodes] & [SHEM][SHEMcodes] (mouse over for a list)
- YYYY : basin season year, NB: the SHEM season starts 1 July YYYY-1 and ends on 30 June YYYY, e.g., the 2023 SHEM season ran from 20220701 - 20230630

- **NN** storms nn = 01-50

- **9X** storms An = A = a,b,c,...z and n = 0-9

  - first 90X would be a0X, second b0X


- **B** subbasin code
  - **w** - WPAC  western N Pacific
  - **c** - CPAC (180W-140W) central N Pacific
  - **e** - EPAC (140W-)     eastern N Pacific
  - **l** - LANT 	       north Atlantic
  - **a** - Arabian Sea
  - **b** - Bay of Bengal
  - **i** - IO - Indian Ocean both(**a**&**b**)

  - **s** - southern IO
  - **p** - SWPAC southwest Pacific
  - **h**  SHEM - souther Hemisphere (both s&p)

- **[A-Z]nB** -- for INVESTs or 9X storms

  - C8W --> 3rd 98W of season

- **JTWC** basins

  w,i,a,b,h,s,p

- **NHC** basins

  c,e,l

- **CPHC/NHC** basins

  c

### Application Documentation

All my .py apps are run using the command line. Documentation of the options
and examples are given by running the app with no options.



## p-md3-ls.py - list positions by DTG or storm

Use the p-md3-ls.py app to list storms/posits.  Here is what is output when
running with no options:

```
p-md3-ls.py  [ -a -B -D -v -b -9 -m -d -O -S -s -V -Y ]

plain args:

switches:
  -a :: anlType=[None] anlType: time2gen|
  -B :: doBT=[0] only display best track info
  -D :: doNNand9X=[1] do NOT list 9X that developed into NN
  -v :: doVitals=[0] make tcvitals for tracker
  -b :: dobt=[0] dobt for both get stmid and trk
  -9 :: dofilt9x=[0] only do 9X
  -m :: domiss=[0] out stmids with missing dtg
  -d :: dtgopt=[None]  dtgopt
  -O :: override=[0] override
  -S :: stmopt=[None]  stmid target
  -s :: sumonly=[0] list stmids only
  -V :: verb=[0] verb=1 is verbose
  -Y :: yearOpt=[None] yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py

Purpose:
an 'ls' or listing app for 'mdeck3' data two filter options are available:
-S by storm
-d by dtg or date-time-group or YYYYMMDDHH

Example(s):
p-md3-ls.py -S w.19 -s       # list just the summary for ALL WPAC storms in 2019 including 9Xdev and 9Xnon and NN
p-md3-ls.py -S w.19 -s -B    # list the summary for only numbered or NN WPAC storms in 2019 w/o summary of 9Xdev
p-md3-ls.py -S 20w.19        # list all posits for supertyphoon HAGIBIS -- the largest TC to hit Tokyo
p-md3-ls.py -S l.18-22 -s -B # list all atLANTic storms 2018-2022


The Current DTG: 2024051012  Time: 17:51:10 UTC 10 May, 2024
```

## p-md3-stm-anl.py - analyze 9Xdev v 9Xnon

```
p-md3-stm-anl.py  [ -b -9 -x -f -O -N -S -s -V -Y ]

plain args:

switches:
  -b :: dobt=[0] dobt for both get stmid and trk
  -9 :: dofilt9x=[0] only do 9X
  -x :: doshow=[1] do NOT show in pltHist
  -f :: filtopt=[None] 
            
FF.TT.NN
FF: all|season|dev
TT: latb|latmn|stmlife|time2gen|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1          

  -O :: override=[0] override
  -N :: ropt=[]  norun is norun
  -S :: stmopt=[None]  stmid target
  -s :: sumonly=[0] list stmids only
  -V :: verb=[0] verb=1 is verbose
  -Y :: yearOpt=[None] yearOpt

Purpose:
analyze 9Xdev v 9Xnon and plot histograms

Example(s):
p-md3-stm-anl.py -S w.18-22 -f all.9xlife.0  # histogram of 9Xdev v 9Xnon lifetime for WPAC 2018-2022

The Current DTG: 2024051012  Time: 17:53:50 UTC 10 May, 2024
```

## p-sbt-v04-anl-ts.py - analyze time series of sBT variables

```
p-sbt-v04-anl-ts.py  [ -P -X -b -9 -L -O -N -S -V ]

plain args:

switches:
  -P :: doPlot=[None]  plot ivars -- ivar0,ivars1...
  -X :: doXv=[0] do xv of plot if doPlot != None
  -b :: dobt=[0] dobt for both get stmid and trk
  -9 :: dofilt9x=[0] only do 9X
  -L :: lsVars=[0]  list variable/descriptions
  -O :: override=[0] override
  -N :: ropt=[]  norun is norun
  -S :: stmopt=[None]  stmid target
  -V :: verb=[0] verb=1 is verbose

Purpose:
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin

Example(s):
p-sbt-v04-anl-ts.py 2019

The Current DTG: 2024051012  Time: 17:54:56 UTC 10 May, 2024
```


## p-sbt-v04-anl-var.py - list/analyze sBT variables (under development)

```
p-sbt-v04-anl-var.py  [ -P -b -C -d -l -n -L -m -O -N -S -V ]

plain args:

switches:
  -P :: csvPath=[None] set the path for the .csv output files
  -b :: doBt=[0] do bt or NN only
  -C :: doCsv=[0] ls in .csv format
  -d :: doDev=[0] do Dev 9X only
  -l :: doLs=[None]  only list a var1,var2
  -n :: doNon=[0] do NonDev 9X only
  -L :: lsVars=[0]  list variable/descriptions
  -m :: mdtgOpt=[None]  filter dtgs in range mdtgOpt
  -O :: override=[0] override
  -N :: ropt=[]  norun is norun
  -S :: stmopt=[None]  stmid target
  -V :: verb=[0] verb=1 is verbose

Purpose:
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin

Example(s):
p-sbt-v04-anl-var.py -S w.07 -l bvmax,mvmax 
p-sbt-v04-anl-var.py -S w.07-09 -m 0701.0901 -d # get Dev 9X for july/aug 

The Current DTG: 2024051012  Time: 17:55:38 UTC 10 May, 2024
```
