<div align="center">

<h1>superBT-V04</h1>
<h3>a "super" Best Track (BT) for Tropical Cyclone (TC) Forecasting and Research</h3>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 12 January 2024 </b>
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
- three TC types:
  - **NN** - a numbered TC
<pre>
    - **TD** - **T**ropical **D**epression (V<sub>max</sub> < 35 kts)
    - **TS** - **T**ropical **S**torm (V<sub>max</sub> >= 35 kts and V<sub>max</sub> < 65 kts )
    - **TY** or **HU** - **TY**phoon or **HU**icane (V<sub>max</sub> >= 65 kts)
    - **STY** - **S**uper **TY**phoon(V<sub>max</sub> >= 130 kts)
    - **SD** - **S**ubtropical **D**epression (V<sub>max</sub> < 35 kts)
    - **SS** - **S**ubtropical *S**torm (V<sub>max</sub> >= 35 kts)
</pre>

  - **9Xdev** - the pre/potential TC (pTC or 9X) disturbance that developed into an **NN** TC
  - **9Xnon** - pTC that did ***not develop*** into an **NN** TC

- superBT-V04 consists of:
  - 3 `.csv` data files
  - 3 corresponding `.csv` metadata files describing the variables.
  - `py2` directory with a python2 interface for analysis and display

### Quick Start

If you are a "just give me the links" person...  There are two ways to install:

- download the superBT tarball: [superBT-V04.tgz](https://tenkiman.github.io/superBT-V04/superBT-V04.tgz
"superBT tarball: https://tenkiman.github.io/superBT-V04/superBT-V04.tgz")

- pull the release from github.com:

- the more complete [README-sbt-v04.md](https://tenkiman.github.io/superBT-V04/README-sbt-v04.md
" https://tenkiman.github.io/superBT-V04/README-sbt-v04.md")

### Contact info

Comments and questions are always welcome and appreciated!  Please contact me at mfiorino@gmu.edu

