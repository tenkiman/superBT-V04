<div align="center">

<h1>superBT-V04</h1>
<h3>a "super" Best Track (BT) for Tropical Cyclone (TC) Forecasting and Research</h3>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 16 January 2024 </b>
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

- global - ***ALL*** TC basins

- 2007-2022 - 16-y data set

- three TC types **NN** ; **9Xdev** ; **9Xnon**
  - **NN** - a numbered/named TC in the JTWC/NHC BT files
    - **TD** - **T**ropical **D**epression (V<sub>max</sub> < 35 kts)
    - **TS** - **T**ropical **S**torm (V<sub>max</sub> >= 35 kts and V<sub>max</sub> < 65 kts )
    - **TY** or **HU** - **TY**phoon or **HU**icane (V<sub>max</sub> >= 65 kts)
    - **STY** - **S**uper **TY**phoon(V<sub>max</sub> >= 130 kts)
    - **SD** - **S**ubtropical **D**epression (V<sub>max</sub> < 35 kts)
    - **SS** - **S**ubtropical *S**torm (V<sub>max</sub> >= 35 kts)
  - **9Xdev** - the pre/potential TC (pTC or 9X) disturbance that developed into an **NN** TC
  - **9Xnon** - pTC that did ***not develop*** into an **NN** TC

- ***dynamical*** variables (e.g., vertical wind shear) from [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5 "https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5") 10-d forecasts

- ***thermo*** variables (rain) from three high-resolution satellite analyses [NCEP-CMORPH](https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph.shtml), [JAXA-GSMaP](https://sharaku.eorc.jaxa.jp/GSMaP/index.htm) & [NASA-IMERG](https://gpm.nasa.gov/data/imerg)

- superBT-V04 consists of:
  - 3 `.csv` data files
  - 3 corresponding `.csv` metadata files describing the variables.
  - `py2` directory with a python2 interface for analysis and display

### Quick Starts and documentation

#### ***docs***

The more complete doc [README-sbt-v04.md](https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md
"https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md")
gives more details on the data and processing, and two science applications that demonstrate the unique capabilities possible with the `superBT`.
Links to the python2 applications are also included in [README-sbt-v04.md](https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md
"https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md")

The [superBT-blog](https://surperbt.blogspot.com/2023/12/intro-to-superbt.html
"superBT Intro & applications:
https://surperbt.blogspot.com/2023/12/intro-to-superbt.html") has an
introduction with and an expanded version of the two science applications in [README-sbt-v04.md](https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md
"https://raw.githubusercontent.com/tenkiman/superBT-V04/main/docs/README-sbt-v04.md")

- formation rate of 9Xdev --> NN or the percentage of TC 'seeds' that become TCs (about 50% in 2018-2022 WPAC)
- differences in shear(decreases)/rain(increases) in 9Xdev v 9Xnon shear(increases)/rain(decreases) about 48 h before formation or dissipation

An earlier version of the more comprehensive doc is available at [QuickStartV04](https://tenkiman.github.io/superBT-V04/QuickStartV04.html "https://tenkiman.github.io/superBT-V04/QuickStartV04.html")

#### ***install*** -- if you are a "just give me the links to the data" person...

There are two ways to install:

- download the superBT tarball: [superBT-V04.tgz](https://tenkiman.github.io/superBT-V04/superBT-V04.tgz
"superBT tarball: https://tenkiman.github.io/superBT-V04/superBT-V04.tgz") and
<pre>
mkdir local-dir                        # local-dir is the directory to untar and will be ...
cd local-dir                           # the root of the git repo
tar -zxvf ~/Downloads/superBT-V04.tgz  # ~/Downloads is the typical location of downloads
</pre>

- pull the release from github.com/tenkiman/superBT-V04
  - [download the git repo tarball](https://github.com/tenkiman/superBT-V04/archive/refs/tags/v0.1-beta1.tar.gz "https://github.com/tenkiman/superBT-V04/archive/refs/tags/v0.1-beta1.tar.gz")
  - clone the git repo: `git clone git@github.com:tenkiman/superBT-V04.git superBT`

#### `wxmap2.com` weather maps and TC NWP displays

The code used to manage the NWP, TC and precipitation data flows and to
construct the superBT comes from the python implementation of my 'weather
maps' web site WxMAP at FNMOC in 1997 and JTWC in 2002.  WxMAP runs on my home
PC and is pushed to my `wxmap2.com` domain.

Here are some links:

- [maps.wxmap2.com](https://maps.wxmap2.com)     -- original weather maps
- [jtdiag.wxmap2.com](https://jtdiag.wxmap2.com)   -- display tracks and 'diagnostic' file for real-time storms and sync'd to operational forecasting
- [tcgen.wxmap2.com](https://tcgen.wxmap2.com) -- TC genesis forecasts from the 5 operational global NWP systems
  - USA-NCEP(GFS)/EU-ECMWF(IFS)/Canada-CMC(CGD)/USA-Navy(NAVGEM)/Japan-JMA(GSM)
- [tcact.wxmap2.com/cur/llmap.htm](https://tcact.wxmap2.com/cur/llmap.htm) - maps of TC activity in the current year basins (20230701-20240630 the 2024-SHEM season)
- [tcact.wxmap2.com/cur/spec.htm](https://tcact.wxmap2.com/cur/spec.htm) - TC activity 'spectographs' in the current year basins (2024-SHEM season)
- [tcact.wxmap2.com/cur/ts.htm](https://tcact.wxmap2.com/cur/ts.htm) - TC activity time series 4,8,16,32,48 years the current year basins (2024-SHEM season)


### Contact info

Comments and questions are always welcome and appreciated!  Please contact me at mfiorino@gmu.edu

##### ispell local words
LocalWords:  superBT BT Fiorino br Fiorino's JTWC NHC IBTRaCS NN Xdev Xnon py
LocalWords:  ropical kts uper pre pTC thermo NCEP CMORPH JAXA GSMaP IMERG csv
LocalWords:  README sbt md TCs WPAC QuickStartV tgz mkdir dir untar cd repo
LocalWords:  zxvf wxmap NWP WxMAP FNMOC sync'd GFS ECMWF CMC CGD NAVGEM JMA
LocalWords:  GSM
