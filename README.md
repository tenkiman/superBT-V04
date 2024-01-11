<div align="center">

<h1>superBT-V04</h1>
<h3>a "super" Best Track (BT) for Tropical Cyclone (TC) Forecasting and Research</h3>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 11 January 2024 </b>
</div>

Welcome to the 1st beta release (V04) of Mike Fiorino's <ins><b>superBT</ins></b> -- a <ins><b>super</b></ins>position of **TC-centric** *dynamical*
(ERA5 10-d forecasts) and *thermodynamical* (satellite precipitation analyses)
 data onto the operational TC position/structure <ins><b>BT</ins></b> of
 [JTWC](https://www.metoc.navy.mil/jtwc/jtwc.html "JTWC home page")
and [NHC](https://www.nhc.noaa.gov/ "NHC home page").

The <ins><b>superBT</ins></b> can also be considered as
'[IBTRaCS](https://www.ncei.noaa.gov/products/international-best-track-archive
"IBTRaCS" ) ++', i.e., a TC position/structure data set with additional
variables (e.g., vertical wind shear) known to be important in TC intensity
change.

### Basic Properties:

- 2007-2022 – 16-y data set
- Final (latest/greatest) BT:
  - JTWC 2007-2021
  - NHC 2007-2022
- Global - NHEM & SHEM basins
- JTWC/NHC - best tracks (“bdeck”) & aid files (“adeck”)
- **NN** - 'numbered storms' (01-50) designated as TCs
  - not necessarily Tropical Storms (**TS** with winds >= 35 kts) 
- **9Xdev** - pre/potential TC (pTC) that developed into NN or TC (developers)
- **9Xnon** - pre/potential TC (pTC) that did not develop (non-developers)
- [ECMWF ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5 "ERA5")  10-d NWP global forecasts for:
  - storm and large-scale *environment* diagnostics - the *diagnostic file* - input to e statistical-dynamical TC intensity prediction models 
  - model track/structure forecasts
- Three global, high-resolution precipitation analyses:
  - [CMORPH - USA - NCEP/CPC V1.0](https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph.shtml "CPC V1.0")
  - [GsMAP - Japan - JAXA V6](https://sharaku.eorc.jaxa.jp/GSMaP/index.htm "JAXA GsMAP V6.0")
  - [IMERG - USA - NASA V06D](https://gpm.nasa.gov/data/imerg "NASA IMERG" )

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

The simplest way to install is to download the tarball:

[superBT-V04.tgz](https://tenkiman.github.io/superBT-V04/superBT-V04.tgz "superBT tarball")



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

