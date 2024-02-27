### superBT-v04 listing
<pre>

         var : description
--------------------------
   'm3stmid' : storm id in NNB.YYYY format
  'm3tcType' : TC lifetype type: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt); STY (super typhoon >= 130 kt)
 'm3stmType' : TC type NN - numbered TC; NONdev - non-developing pTC; DEV - pTC that developed into NN storm
       'dtg' : date-time-group YYYYMMDDHH
      'blat' : best track latitude degN
      'blon' : best track longitude degE
     'bvmax' : best track Vmax [kts]
     'bpmin' : best track central pressure [hPa]
      'bdir' : best track direction of motion [deg]
      'bspd' : best track speed [kt]
   'btccode' : best track TC code
     'br34m' : best track mean R34 [km]
      'land' : distance from coast [km]
     'mvmax' : model Vmax [kts]
      'r34m' : mean r34 km for diag calc
    'shrspd' : 850-200 hPa shear speed kts
    'shrdir' : 850-200 hPa shear direction deg
    'stmspd' : storm speed in diagnostic file calc
    'stmdir' : storm direction of motion in diagnostic file calc
       'sst' : SST ERA5 degC
      'ssta' : SST anomaly degC
   'vort850' : 850 hPa relative vorticity
   'dvrg200' : 200 hPa divergence
      'cpsb' : CPS baroclinic
     'cpslo' : CPS low: 1000-600 thickness
     'cpshi' : CPS hi:   600-200 thickness
       'tpw' : total precipitable water
      'rh50' : relative humidity 500 hPa
      'rh70' : relative humidity 700 hPa
      'rh85' : relative humidity 850 hPa
       'u85' : u wind 850 hPa
       'u70' : u wind 700 hPa
       'u50' : u wind 500 hPa
       'v85' : v wind 850 hPa
       'v70' : v wind 700 hPa
       'v50' : v wind 500 hPa
     'roci1' : roci of penultimate contour
     'poci1' : poci of penultimate contour
     'roci0' : roci outermost contour
     'poci0' : poci outermost contour
       'oc3' : CMORPH 300-km precip at Best Track position [mm/d]
       'og3' : GSMaP  300-km precip at Best Track position [mm/d]
       'oi3' : IMERG  300-km precip at Best Track position [mm/d]
       'oc5' : CMORPH 500-km precip at Best Track position [mm/d]
       'og5' : GSMaP  500-km precip at Best Track position [mm/d]
       'oi5' : IMERG  500-km precip at Best Track position [mm/d]
       'oc8' : CMORPH 800-km precip at Best Track position [mm/d]
       'og8' : GSMaP  800-km precip at Best Track position [mm/d]
       'oi8' : IMERG  800-km precip at Best Track position [mm/d]
       'ec3' : CMORPH 300-km precip at ERA5 position [mm/d]
       'eg3' : GSMaP  300-km precip at ERA5 position [mm/d]
       'ei3' : IMERG  300-km precip at ERA5 position [mm/d]
        'e3' : ERA5 500-km precip [mm/d]
       're3' : ERA5 ratio Convective/Total 300-km precip [%]
       'ec5' : CMORPH 500-km precip at ERA5 position [mm/d]
       'eg5' : GSMaP 500-km precip at ERA5 position [mm/d]
       'ei5' : IMERG 500-km precip at ERA5 position [mm/d]
        'e5' : ERA5 500-km precip [mm/d]
       're5' : ERA5 ratio Convective/Total 500-km precip [%]
       'ec8' : CMORPH 800-km precip at ERA5 position [mm/d]
       'eg8' : GSMaP 800-km precip at ERA5 position [mm/d]
       'ei8' : IMERG 800-km precip at ERA5 position [mm/d]
        'e8' : ERA5 800-km precip [mm/d]
       're8' : ERA5 ratio Convective/Total 800-km precip [%]
</pre>

### mD3-v03  variable listing

<pre>
         var : description
--------------------------
       'dtg' : date-time-group YYYYMMDDHH
     'stmid' : storm id in NNB.YYYY format
    'osname' : storm name
    'tcvmax' : max lifetime category: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt) STY (super typhoon >= 130 kt)
    'tctype' : TC type NN - numbered TC; NONdev - non-developing pTC; DEV - pTC that developed into NN storm
      'rlat' : BT latitude [degN]
      'rlon' : BT longitude [degE]
      'vmax' : BT max wind [kts]
      'pmin' : BT central pressuer [hPa]
       'dir' : BT direction of motion [deg]
       'spd' : BT speed of motion [kts]
    'trkdir' : Real-time direciton of motion [deg]
    'trkspd' : Real-time speed of motion [kts]
      'r34m' : mean radius of 34 kt winds [nmi]
     'r34ne' : NE quadrant radius of 34 kt winds [nmi]
     'r34se' : SE quadrant radius of 34 kt winds [nmi]
     'r34sw' : SW quadrant radius of 34 kt winds [nmi]
     'r34nw' : NW quadrant radius of 34 kt winds [nmi]
      'r50m' : mean radius of 50 kt winds [nmi]
     'r50ne' : NE quadrant radius of 50 kt winds [nmi]
     'r50se' : SE quadrant radius of 50 kt winds [nmi]
     'r50sw' : SW quadrant radius of 50 kt winds [nmi]
     'r50nw' : NW quadrant radius of 50 kt winds [nmi]
    'tccode' : TC code
    'wncode' : Warning Code: WN in a warning status; NW - no warnings
   'dirtype' : direction of motion type
  'posttype' : post BT motion type
      'roci' : BT ROCI [nmi]
      'poci' : BT POCI [hPa]
       'alf' : % land
     'depth' : TC BT Depth code: S - shallow; M - medium; D - deep
      'rmax' : BT radius of max wind
       'tdo' : forecaster initials
</pre>

### mD3-v03 summary variable listing

<pre>
         var : description
--------------------------
     'stmid' : storm id in NNB.YYYY format
     'tcype' : TC lifetype type: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt); STY (super typhoon >= 130 kt)
    'stmflg' : TC type NN - numbered TC; NONdev - non-developing pTC; DEV - pTC that developed into NN storm
     'sname' : TC name
      'maxv' : lifetime Vmax [kts]
      'ndtc' : # days TC [d]
     'ndstm' : # days TS or greater [d]
      'blat' : beginning latitude [degN]
      'blon' : beginning longitude [degE]
      'bdtg' : beginning DTG YYYYMMDDHH
      'edtg' : ending DTG YYYYMMDDHH
    'minlat' : minimum latitude [degN]
    'maxlat' : maximum latitude [degN]
    'minlon' : maximum longitude [degE]
    'maxlon' : maximum longitude [degE]
      'stcd' : scaled TC days [d]
       'ace' : life-time scaled ACE [d]
       'nri' : number of RI - rapid intensification >= 30 kts/24 h
       'ned' : number of ED - explosive deepening  >= 50 kts/24 h
       'nrw' : number of RW - rapid weakening <= 30kts/24 h
    'ricode' : RI/RW/ED code
      '9xid' : if NN storms; the stmid of the pTC that became NN
     't2gen' : time from start of pTC to becoming a TC (as set by JTWC/NHC)
    'gendtg' : DTG of genesis YYYYMMDDHH
    'wncode' : warning status at genesis time
</pre>
