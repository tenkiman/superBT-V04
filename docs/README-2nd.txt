      A super Best Track for Tropical Cyclone Forecasting and Reasearch
		       superBT-V04 --first beta version
				   20230115
				   20240110
				 Mike Fiorino
			       mfiorino@gmu.edu
(while a visiting professor at CCRS/AORI University of Tokyo 20220801-20221029)

0.  Intro
----------

While IBTRaCs and the final or post-season 'best tracks' from the two US
operational TC forecast centers are widely used in TC research and forecast
application development, there are three large deficiences that limit TC
research on longer time scales and on TC genesis and intensity change:

1) All TCs start as 'disturbances' with lower-level vorticity and organized
convection.  There are several sources of the disturbances that depend on the
basin.  As will be discussed later, the mean time between the first
identification of a disturbance or 'invest' in operations is 3 days.  Thus, TC
genesis studies are incomplete without a knowledge of which pre/potential TCs
(pTCs) develop and which do not.

2) A consistent, high-quality, multi-decadal data set on the dynamical
properties of the TC environment, most notably vertical wind shear in the
850-200 hPa layer. This shear has been observed to be highly correlated with
TC intensity change.

3) Data on the net thermodynamical forcing of the TC -- precipitation.

The "super Best Track" or "superBT" ('sbt' in the files) helps to reduce these
deficiencies by adding information/data from several new data sources,
specifically:

1) a curated, global pTC data set from 2007-2022 including both developers
(9Xdev) and non-developers (9Xnon).

2) the latest global ECMWF reanalysis ERA5 with twice-daily 10-d forecasts from 1969-202310.

3) three satellite-based, near-global precipitation data sets 2001-2022.

details on the data sets are given in Table 1.

This paper gives a scientific description of the superBT, documents Version
V04 and an example application to the difference between developing and
non-developing pTCs.




First, the operational best tracks of the JTWC/NHC are in the 'ATCF' format in the form of one text
file per storm called a 'bdeck' (b for best track).  The file with operational TC data for tracking
TCs in NWP models and satellite reconnaissance and forecast for 'aids' is in the 'adeck'

see:			https://www.nrlmry.navy.mil/atcf_web/docs/database/new/database.html
and for the 'bdecks:	https://www.nrlmry.navy.mil/atcf_web/docs/database/new/abdeck.txt

There are a/bdecks for two types of systems:

1) a numbered storm (a TC) with numbers from 01-50
2) 9X or INVESTS with numbers from 90-99

In a typical season there are about 80 INVESTS or 9X and about 30 TCs so that there may be 4-6 9OB
invests so that the a/bdecks with the filename a|bBB##YYY.dat where

BB the two character basin id
## is the storm number
YYYY is the year

For example bwp902022.dat is the 'bdeck' for invest number '90' in the western North Pacific
(WPAC). If there are 80 9X in a season, there would be 8 b90wp2022.dat, i.e., the file is
overwritten after the 1st 90wp2022.  Recently I have shown that 9X invests are critical for TC
genesis studies and to save each 90wp a different numbering system has to be used to make each 90wp
unique.  The standard system at both JTWC and NHC is to call the 1st 90wp as a0wp and the 2nd b0wp
and so on...

I have maintained a archive of 9X in all basins since 2006-2023 (18 y) in which I add both a and
bdeck 9X storms to a zip archive every time a new one is pulled.  From each 9X .zip file I find the
unique 9Xs and label them using the a,b,c,d,e... convention.  For example the awp902022.zip file
will have every awp902022 during the season and from the zip file will set awpA902022.dat,
awpB902022.dat...

I then create a 'mdeck3' (3rd version of the mdeck) that merges information
from both the 'b' and 'a' so all real-time and best track data is contained in
one file rather than have to scan the two files separately.

0.1 -- mdeck3s
-------------

The first special property of the superBT is: 1) merging of data in the a and bdeck into one file;
and 2) identifying all unique 9X and associating an individual 9X with a number storm.  For exmaple,
Typhoon HAGIBIS of 2019 -- 20W.2019 -- started as D3W or the the 4th 93W of the 2019 season in
WPAC.  Further, it took 60 h before the 1st JTWC warning was issued and 93W renamed as 20W.

0.2 -- lsdiag
-------------

The input to the statistical TC intensity forecast aids, what is called a
'diagnostic file', is calculated using global NWP fields.  I call this process
lsdiag.  There are three sections to the diag file:

1) storm-specifc data known to be related to TC intensity change.  The most important being the mean
850-200 hPa vertical wind shear (VWS).  Below is the storm section of diag file for 2019100900 (the
'date-time-group' or 00Z 09 OCT 2019) 24 h from from the ERA5 reanalyis forecast for HAGIBIS:

NTIME 005
TIME        (HR)     0     6    12    18    24
LATITUDE   (DEG)  19.8  20.6  21.4  22.2  23.2
LONGITUDE  (DEG) 140.2 139.8 139.5 139.3 138.9
MAX WIND    (KT)    54    59    60    57    58
RMW         (KM)   135   118   138   145   147
MIN SLP     (MB)    10    10    10    10    10
SHR MAG     (KT)     3     5    10    14     8
SHR DIR    (DEG)   246   174   190   159   134
STM SPD     (KT)     9     9     8    11    11
STM HDG    (DEG)   335   341   347   340   340
SST        (10C)   282   282   283   284   284
OHC     (KJ/CM2)  9999  9999  9999  9999  9999
TPW         (MM)    76    74    75    76    77
LAND        (KM)  1567  1470  1379  1294  1180
850TANG  (10M/S)   283   296   302   298   299
850VORT     (/S)   184   183   181   166   182
200DVRG     (/S)   151   146    73    46    70

the typhoon was analyzed as a 140 kts 'supertyphoon' by JTWC.  The storm in the ERA5 model was
considerably weaker at 54 kts at 'tau' (or forecast time) 0.  The wind shear VWS was very low at 3
kts...typical for strong TCs (the flow at 200 hPa is strongly anticylonic (warm core, thermal
wind)).

There are three sections to the diag file: 1) storm; 2) custom; and 3) sounding.  The sounding
section contains mean values around the TC (0-500 km) of the primary progostic variables (wind -
u,v, temperature - T and moisture - RH) at manditory pressure levels (1000, 925, 850, 700, 500, 400,
300, 250, 200,150, 100 hPa).  The custom section is where I added other variables, most notably,
model precipitation and the three Hart CPS (cyclone phase space) variables (B - for baroclinicity,
LO for the 1000-600 hPa thickness, and HI or the 600-300 hPa thickness). 

I have run lsdiag on all TCs and pTCs (pre/potential TCs coded as 9X) from 1979-2022 using the twice
daily 10-d forecasts from the ERA5 renalysis model.  These forecasts are not generally available but
are used at ECMWF as a measure of the quality of the ERA5 analysis.  I collected these forecasts
courtesy of Hans Hersbach, head of reanalysis at ECMWF.

In a seperate analysis, I showed that the ERA5 TC track forecasts were very good, even in the early
satellite era (1979-1990) implying the reanalyses are appropriate for TC studies.

To summarize, the 2nd unique aspect of the superBT is diagnostics from lsdiag.


0.3 precipitation
-----------------

Precipitation (rain for TCs) is the net diabatic heating in the atmosphere and
the primary TC thermodynamic driver.  I have collected version 1 of the NCEP
CPC (CMORPH) global satellite rainfall analysis from 1998-present. I also
include Japan JAXA precip analysis (GsMAP) and the USA NASA satellite precip
analysis (IMERG) to calculate mean rain in three radial bands r=300,500,800 km
for both the model and the CMORPH/GsMAP/IMERG obs as a third special feature
of the superBT.

1.0 Construction
----------------

The superBT is simply an extension or superposition on the BT (mdeck3) by
adding to the BT information from three sources:

1) operational information in the 'adecks' and a proper curation of the pTC 9X
storms; 2) storm/environment variables from ERA5
3) precipitation both observed and modeled.

In all there are order 1000 possible variables that could be added to the BT
that is around 30 numbers.  While it is possible to put all the possible data in
the sBT, it is more efficient to built a subset from the 1000 possible #s for
specific problems.  The technical challenge is accessing data from three
disparate sources:

1) a/bdecks best tracks from JTWC/NHC (text files)
2) the ERA5 global NWP model (model fields or grids)
3) gridded satellite analyses.

The other technical challenge is that while the BT data are very
small (order MB), the model data is about 10 TB -- a 6 orders of magnitude
difference!  The precipitation grids are smaller at about 1 TB...

During my two-month visit to AORI I have developed all scripts (python and
GrADS) to built version V01 (alpha testing) of the superBT.

2.0 Summary and What's Next
---------------------------

The first beta version of the superBT (V04) is a merging/combination of:

1) all TCposition/structure operational data from JTWC/NHC (i.e., is more than the
'best track' or ATCF 'bdeck' data available in IBTRaCS)

2) TC storm and environmental diagnostic variables from the latest/greatest
ECMWF reanlysis (dynamics)

3) TC rain from three high-resolution satellite-precipitation analyses
(theromdynamics)

The superBT-V04 consists of three .csv text files:

all-md3-2007-2022-MRG.csv -- the mdeck3 TC position/strucure data
sum-md3-2007-2022-MRG.csv -- summary by storm of each TC in all-md3-2007-2022-MRG.csv
sbt-v04-2007-2022-MRG.csv -- the superBT with diagnostics and precipitation
			     for each TC in the mdeck3 file

each variable in the three .csv is described in the associated meta data
files:

h-meta-md3-vars.csv      -- variables in the mdeck3 TC position/structure data
h-meta-md3-sum.csv       -- summary of mdeck3 by storm
h-meta-sbt-v04-vars.csv  -- variables in the superBT

In 2023, I finalized all processing and did extensive (and exhausting) QC on
the mdeck3 and the superBT.  I then moved everything to tenkiman.github.com
and google blogger. Here are the key links:

https://surperbt.blogspot.com/2023/12/intro-to-superbt.html
https://tenkiman.github.io/superBT-V04/

