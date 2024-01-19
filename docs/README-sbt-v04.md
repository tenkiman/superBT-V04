<div align="center">

<h1>superBT-V04 - The Details</h1>
<h3>a "super" Best Track (BT) for Tropical Cyclone (TC) Forecasting and Research</h3>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 19 January 2024 </b>
</div>

Welcome to the 1st beta release (V04) of Mike Fiorino's <ins><b>superBT</ins></b> -- a <ins><b>super</b></ins>position of **TC-centric** *dynamical*
(ERA5 10-d forecasts) and *thermodynamical* (satellite precipitation analyses)
 data onto the operational TC position/structure <ins><b>BT</ins></b> of
 [JTWC](https://www.metoc.navy.mil/jtwc/jtwc.html "JTWC home page: https://www.metoc.navy.mil/jtwc/jtwc.html")
and [NHC](https://www.nhc.noaa.gov/ "NHC home page: https://www.nhc.noaa.gov/").

The <ins><b>superBT</ins></b> can also be considered as
'[IBTRaCS](https://www.ncei.noaa.gov/products/international-best-track-archive
"IBTRaCS: https://www.ncei.noaa.gov/products/international-best-track-archive" ) ++', i.e., a TC position/structure data set with additional
variables (e.g., vertical wind shear) known to be important in TC intensity
change.

### Key properties of the data set:

[TCs]: ## "
TD  - Tropical Depression : Vmax < 35 kts
TS  - Tropical Storm      : Vmax >=35 & Vmax < 64 kts
HU  - Hurricane           : Vmax >=65kts
STY - Super Typhoon       : Vmax >= 130 kts
SD  - Subtropical Depression : Vmax < 35 kts
SS  - Subtropical Storm      : Vmax >=35 & Vmax < 64 kts
"

- global - ***ALL*** TC basins

- 2007-2022 - 16-y data set

- three TC types **NN** ; **9Xdev** ; **9Xnon**
  - **NN** - [a numbered/named TC in the JTWC/NHC BT files][TCs]
  - **9Xdev** - the pre/potential TC (pTC or 9X) disturbance that developed into an **NN** TC
  - **9Xnon** - pTC that did ***not develop*** into an **NN** TC

- ***dynamical*** variables (e.g., vertical wind shear) from [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5 "https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5") 10-d forecasts

- ***thermo*** variables (rain) from three high-resolution satellite analyses [NCEP-CMORPH](https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph.shtml), [JAXA-GSMaP](https://sharaku.eorc.jaxa.jp/GSMaP/index.htm) & [NASA-IMERG](https://gpm.nasa.gov/data/imerg)

- superBT-V04 consists of:
  - 3 `.csv` data files
  - 3 corresponding `.csv` metadata files describing the variables.
  - `py2` directory with a python2 interface for analysis and display


### Demo of ***formation rate*** or the % of all pTCs --> TCs

below is the percentage of both 9Xdev + 9Xnon that became TCs in the Western north PACific (WPAC) in the 5-y period 2018-2022.

From the plot we see:

150 9Xdev average time to ***develop*** is ***3.6 d***</br>
152 9Xnon average time to ***dissipation*** is ***3.1 d***</br>
50% become NN or the ***formation rate*** is 50%</br>

<!--
![WPAC 2018-22 Formation Rate](https://tenkiman.github.io/superBT-V04/docs/plt/9xlife/all.9xlife.0.w.18-22.png "WPAC 18-22: https://tenkiman.github.io/superBT-V04/docs/plt/9xlife/all.9xlife.0.w.18-22.png")
-->
![WPAC 2018-22 Formation Rate](plt/9xlife/all.9xlife.0.w.18-22.png "WPAC 18-22: https://tenkiman.github.io/superBT-V04/docs/plt/9xlife/all.9xlife.0.w.18-22.png")

### Next Steps...

Here are documentation and date set links:

- the [superBT blog](https://surperbt.blogspot.com/ "https://surperbt.blogspot.com/") has an [introduction](https://surperbt.blogspot.com/2023/12/intro-to-superbt.html "https://surperbt.blogspot.com/2023/12/intro-to-superbt.html") with links and a further analysis of ***formation rate*** in the big basins and the ***dynamical*** (wind shear) and ***thermodynamical*** (precipitation) differences between **9Xdev** and **9Xnon**

- this
  [presentation](https://tenkiman.github.io/superBT-V04/docs/tc-superBT-20230310.pptx
  "https://tenkiman.github.io/superBT-V04/docs/tc-superBT-20230310.pptx") gives:
  - details on the ATCF data files used for the TC positions/structure
  - track forecast skill of the ERA5 forecasts
    - as good or better the ECMWF operational runs
    - consistent skill even in the 1980s v 2000-2022
    - quality of the three precipitation analyses
  
- The simplest way to install is to download the tarball [superBT-V04.tgz](https://tenkiman.github.io/superBT-V04/superBT-V04.tgz
"superBT tarball: https://tenkiman.github.io/superBT-V04/superBT-V04.tgz")

### Contact info

Comments and questions are always welcome and appreciated!  Please contact me at mfiorino@gmu.edu


### Basic Properties:

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

- 2007-2022 – 16-y data set
- Final (latest/greatest) BT:
  - JTWC 2007-2021
  - NHC 2007-2022
- Global - NHEM (A,B,I,W,C,E,L) & SHEM basins (S,P,H)
  - [NHEM Subbasin 1-char codes][NHEMcodes]
  - [SHEM Subbasin 1-char codes][SHEMcodes]
- JTWC/NHC [ATCF](https://www.nrlmry.navy.mil/atcf_web/index1.html
"https://www.nrlmry.navy.mil/atcf_web/index1.html" ) data files
  - "bdeck" -- best track operational (working) or 'final' (post-season) positions/structure
  - "adeck" -- aid files with real-time, operational positions/structure
- **NN** - 'numbered storms' (01-50) designated as TCs
  - not necessarily Tropical Storms (**TS** with winds >= 35 kts) 
- **9Xdev** - pre/potential TC (pTC) that developed into NN or TC (developers)
- **9Xnon** - pre/potential TC (pTC) that did not develop (non-developers)
- [ECMWF ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5
"ERA5: https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5") 10-d NWP global forecasts for:
  - storm and large-scale *environment* diagnostics - the *diagnostic file* - input to e statistical-dynamical TC intensity prediction models 
  - model track/structure forecasts
- Three global, high-resolution precipitation analyses:
  - [CMORPH - USA - NCEP/CPC V1.0](https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph.shtml
"CPC V1.0 : https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph.shtml")
  - [GsMAP - Japan - JAXA V6](https://sharaku.eorc.jaxa.jp/GSMaP/index.htm
"JAXA GsMAP V6.0: https://sharaku.eorc.jaxa.jp/GSMaP/index.htm ")
  - [IMERG - USA - NASA V06D](https://gpm.nasa.gov/data/imerg "NASA IMERG: https://gpm.nasa.gov/data/imerg" )

### Unique Properties:

- curated pTC or TC 'seeds' data set based on a zip archive of all ATCF
  adeck/bdeck (pTCs or '9X' or 'INVESTS') from JTWC/NHC operations.  All TCs
  start as pTCs and by having data on both pTCs that *developed* into **NN** TCs
  (**9Xdev**) and did ***not*** develop (**9Xnon**) we can determine the
  ***formation rate*** and the ***dynamical/thermodynamical difference*** between developers and non-developers

- the ***highest quality global NWP analyses*** to date based on the
  high-quality of the daily 00/12 UTC 10-d ERA5 TC forecasts.  The quality of
  the reanalysis does vary with changes in the observing system, but with ERA5
  the TC track forecasts are consistently better than ECMWF operations and
  nearly as good in the 1980s as the 2000s.

- a python2 interface is provided for simple access/slicing and analysis

### How to access/install:

The simplest way to install is to download the tarball [superBT-V04.tgz](https://tenkiman.github.io/superBT-V04/superBT-V04.tgz
"superBT tarball: https://tenkiman.github.io/superBT-V04/superBT-V04.tgz")

<pre>

cd ~/Download             # typical download directory
mkdir ~/local-dir         # make a 'local-dir' in your home

# from the Download dir

mv superBT-V04.tgz local-dir/ (e.g., ~/superBT)
cd local-dir/
tar -xzvf superBT-V04.tgz

will make local-dir/superBT/V04/ with these files:

     2851 2024-01-10 21:35 superBT/V04/README-sbt
     7926 2023-10-20 17:46 superBT/V04/README-sbt-mike5
      900 2024-01-10 21:07 superBT/V04/README-sbt-py2
     6327 2023-12-08 20:36 superBT/V04/README-sbt-vars
 14745266 2024-01-11 15:36 superBT/V04/dat/all-md3-2007-2022-MRG.csv
     1099 2024-01-11 15:36 superBT/V04/dat/h-meta-md3-sum.csv
     1384 2024-01-11 15:36 superBT/V04/dat/h-meta-md3-vars.csv
     2797 2024-01-11 15:36 superBT/V04/dat/h-meta-sbt-v04-vars.csv
 26085454 2024-01-11 15:36 superBT/V04/dat/sbt-v04-2007-2022-MRG.csv
   676848 2024-01-11 15:36 superBT/V04/dat/sum-md3-2007-2022-MRG.csv
    40026 2023-10-20 13:27 superBT/V04/py2/mf.py
    16943 2024-01-10 19:07 superBT/V04/py2/p-md3-ls.py
     5526 2023-12-08 20:16 superBT/V04/py2/p-md3-stm-anl.py
    10401 2023-12-12 19:33 superBT/V04/py2/p-sbt-v04-anl-ts.py
     5879 2024-01-11 15:36 superBT/V04/py2/p-sbt-v04-anl-var.py
   509285 2024-01-10 18:12 superBT/V04/py2/sBTcl.py
        0 2023-12-12 20:06 superBT/V04/py2/sbtLocal.py -> sbtLocal.py-mike5
      119 2023-12-12 19:33 superBT/V04/py2/sBT.py
    11337 2024-01-08 15:00 superBT/V04/py2/sBTvars.py
   220148 2024-01-08 14:59 superBT/V04/py2/sBTvm.py

edit the sbtLocal.py file to locate (full paths to local the .py and .csv files)

</pre>


### Data files:

The superBT consists of three `.csv` data files and three `.csv` metadata files describing the variables in data files.

| data file | description | # of lines/points
| -:      | :-:   | :-	  
| all-md3-2007-2022-MRG.csv | positions for NN/9Xdev/9Xnondev   | 107050 positions
| sum-md3-2007-2022-MRG.csv  | summary of each storm  | 5233 storms
| sbt-v04-2007-2022-MRG.csv  | superBT     | 86595 positions
| h-meta-md3-vars.csv | metadata for all-md3-*.csv | 32 variables
| h-meta-md3-sum-vars.csv | metadata for sum-md3-*.csv | 25 variables
| h-meta-sbt-v04-vars.csv | metadata for sbt-v04*.csv | 66 variables

