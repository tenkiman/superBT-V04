### uname -a

<pre>
Linux tenkiS.wxmap2.com 5.14.21-150500.55.28-default #1 SMP PREEMPT_DYNAMIC Fri
Sep 22 10:04:29 UTC 2023 (c11336f) x86_64 x86_64 x86_64 GNU/Linux

cat /etc/os-release

NAME="openSUSE Leap"
VERSION="15.5"
ID="opensuse-leap"
ID_LIKE="suse opensuse"
VERSION_ID="15.5"
PRETTY_NAME="openSUSE Leap 15.5"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:opensuse:leap:15.5"
BUG_REPORT_URL="https://bugs.opensuse.org"
HOME_URL="https://www.opensuse.org/"
DOCUMENTATION_URL="https://en.opensuse.org/Portal:Leap"
LOGO="distributor-logo-Leap"
</pre>

### anaconda:

<pre>
conda info

     active environment : py2
    active env location : /w21/app/anaconda3/envs/py2
            shell level : 8
       user config file : /home/fiorino/.condarc
 populated config files : 
          conda version : 23.5.2
    conda-build version : 3.25.0
         python version : 3.11.3.final.0
       virtual packages : __archspec=1=x86_64
                          __glibc=2.31=0
                          __linux=5.14.21=0
                          __unix=0=0
       base environment : /w21/app/anaconda3  (writable)
      conda av data dir : /w21/app/anaconda3/etc/conda
  conda av metadata url : None
           channel URLs : https://repo.anaconda.com/pkgs/main/linux-64
                          https://repo.anaconda.com/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/r/linux-64
                          https://repo.anaconda.com/pkgs/r/noarch
          package cache : /w21/app/anaconda3/pkgs
                          /home/fiorino/.conda/pkgs
       envs directories : /w21/app/anaconda3/envs
                          /home/fiorino/.conda/envs
               platform : linux-64
             user-agent : conda/23.5.2 requests/2.29.0 CPython/3.11.3 Linux/5.14.21-150500.55.28-default opensuse-leap/15.5 glibc/2.31
                UID:GID : 1000:100
             netrc file : /home/fiorino/.netrc
           offline mode : False

</pre>

### python2 packages

<pre>
# packages in environment at /w21/app/anaconda3/envs/py2:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
alabaster                 0.7.12                   py27_0  
asn1crypto                1.4.0                      py_0  
attrs                     21.4.0                   pypi_0    pypi
babel                     2.9.0              pyhd3eb1b0_0  
backports-functools-lru-cache 1.6.6                    pypi_0    pypi
bsddb3                    6.0.0                    py27_0    bnoon
ca-certificates           2023.08.22           h06a4308_0  
certifi                   2020.6.20          pyhd3eb1b0_3  
cffi                      1.15.1                   pypi_0    pypi
chardet                   3.0.4                 py27_1003  
cryptography              2.8              py27h1ba5d50_0  
cycler                    0.10.0                   pypi_0    pypi
docutils                  0.15.2                   py27_0  
eccodes                   1.6.0                    pypi_0    pypi
enum34                    1.1.6                    py27_1  
findlibs                  0.0.5                    pypi_0    pypi
idna                      2.10               pyhd3eb1b0_0  
imagesize                 1.2.0              pyhd3eb1b0_0  
ipaddress                 1.0.23                     py_0  
jinja2                    2.11.3             pyhd3eb1b0_0  
kiwisolver                1.1.0                    pypi_0    pypi
libffi                    3.3                  he6710b0_2  
libgcc-ng                 11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libstdcxx-ng              11.2.0               h1234567_1  
markupsafe                1.1.1            py27h7b6447c_0  
matplotlib                2.2.5                    pypi_0    pypi
natsort                   6.2.1                    pypi_0    pypi
ncurses                   6.4                  h6a678d5_0  
numpy                     1.16.6                   pypi_0    pypi
openssl                   1.1.1w               h7f8727e_0  
packaging                 20.9               pyhd3eb1b0_0  
pip                       19.3.1                   py27_0  
pycparser                 2.21                     pypi_0    pypi
pygments                  2.5.2                      py_0  
pygrads                   1.2.1                    pypi_0    pypi
pyopenssl                 20.0.1             pyhd3eb1b0_1  
pyparsing                 2.4.7              pyhd3eb1b0_0  
pysocks                   1.7.1                    py27_0  
python                    2.7.18               ha1903f6_2  
python-dateutil           2.8.2                    pypi_0    pypi
pytz                      2023.3                   pypi_0    pypi
readline                  8.2                  h5eee18b_0  
requests                  2.25.1             pyhd3eb1b0_0  
setuptools                44.0.0                   py27_0  
six                       1.16.0             pyhd3eb1b0_1  
snowballstemmer           2.1.0              pyhd3eb1b0_0  
sphinx                    1.8.5                    py27_0  
sphinxcontrib             1.0                      py27_1  
sphinxcontrib-websupport  1.2.4                      py_0  
sqlite                    3.41.2               h5eee18b_0  
subprocess32              3.5.4                    pypi_0    pypi
tk                        8.6.12               h1ccaba5_0  
typing                    3.7.4.1                  py27_0  
urllib3                   1.25.7                   py27_0  
webcolors                 1.10                     pypi_0    pypi
wheel                     0.37.1             pyhd3eb1b0_0  
zlib                      1.2.13               h5eee18b_0  
</pre>

### openGrADS

<pre>

              Welcome to the OpenGrADS Bundle Distribution
              --------------------------------------------

For additional information enter "grads --manual".

Starting "/data/w22/app/opengrads-2.2.1.oga.1/Contents/Linux/Versions/2.2.1.oga.1/x86_64/grads   -h " ...

Grid Analysis and Display System (GrADS) Version 2.2.1.oga.1
Copyright (C) 1988-2018 by George Mason University
GrADS comes with ABSOLUTELY NO WARRANTY
See file COPYRIGHT for more information

Config: v2.2.1.oga.1 little-endian readline grib2 netcdf hdf4-sds hdf5 opendap-grids,stn athena geotiff shapefile
Issue 'q config' and 'q gxconfig' commands for more detailed configuration information
Loading User Defined Extensions table </data/w22/app/opengrads-2.2.1.oga.1/Contents/Linux/Versions/2.2.1.oga.1/x86_64/gex/udxt> ... ok.
Landscape mode? ('n' for portrait):  
GX Package Initialization: Size = 11 8.5 

Config: v2.2.1.oga.1 little-endian readline grib2 netcdf hdf4-sds hdf5 opendap-grids,stn athena geotiff shapefile
Grid Analysis and Display System (GrADS) Version 2.2.1.oga.1
Copyright (C) 1988-2018 by George Mason University 
GrADS comes with ABSOLUTELY NO WARRANTY 
See file COPYRIGHT for more information 

Configured on 02/02/19 for x86_64-unknown-linux-gnu

This build of GrADS has the following features:
 -+- Byte order is LITTLE ENDIAN 
 -+- Athena Widget GUI ENABLED 
 -+- Command line editing ENABLED 
 -+- GRIB2 interface ENABLED  g2clib-1.6.0 
 -+- NetCDF interface ENABLED  netcdf-4.3.3 
 -+- OPeNDAP gridded data interface ENABLED
 -+- OPeNDAP station data interface ENABLED  libgadap 2.0.oga.1 
 -+- HDF4 interface ENABLED  hdf-4.2r14 
 -+- HDF5 interface ENABLED  hdf5-1.8.12 
 -+- KML contour output ENABLED
 -+- GeoTIFF and KML/TIFF output ENABLED
 -+- Shapefile interface ENABLED

 -+- GX Display "Cairo"  /data/w22/app/opengrads-2.2.1.oga.1/Contents/Linux/Versions/2.2.1.oga.1/x86_64/gex//libgxdCairo.so  X11.0 cairo-1.14.10 
 -+- GX Print   "Cairo"  /data/w22/app/opengrads-2.2.1.oga.1/Contents/Linux/Versions/2.2.1.oga.1/x86_64/gex//libgxpCairo.so  cairo-1.14.10 
</pre>
