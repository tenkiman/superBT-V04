<div align="center">

<h1>TC and TC-basin codes</h1>

Mike Fiorino (mfiorino@gmu.edu)</br>
<b> 30 January 2024 </b>
</div>

## TC codes

TCc	TC type code
TCc: LO,DB,WV,MT,TD,TS,TY,ST,SD,SS,XT


### pre TC (9Xdev and 9Xnon)

LO	low
DB	disturbance
WV	wave
MT	monsoon trough

### TC

TD	tropical depression
TS	tropical storm
TY	hurricane/typhoon
ST 	super typhoon (Vmax >= 130 kts)

### sub-tropical TC

SD	subtropical depression
SS	subtropical storm

### eXtra-tropical TC

XT	eXtra-tropical cyclone


## TC numbering convention

The general form is

nnX.YYYY

where
nn   : number
X    : basin
YYYY : year of season, NB: the YYYY SHEM season starts on 1 July YYYY-1 and ends 30 June YYYY, e.g., the 2023 SHEM season ran from 20220701 to 20230630

- **NN** storms nn = 01-50
- **9X** storms An = A = a,b,c,...z and n = 0-9
  - first 90X would be a0X, second b0X
  - zn


B - subbasin code

  B=
  w - wpac	       western N Pacific
  c - cpac (180W-140W) central N Pacific 
  e - epac (140W-)     eastern N Pacific
  l - lant 	       north Atlantic
  i - IO - Indian Ocean
  a - Arabian Sea
  b - Bay of Bengal
  h - SHEM - souther Hemisphere
  s - southern Indian Ocean
  p - southwest Pacific

[A-Z]nB -- for INVESTs or 9X storms

e.g., C8W --> 3rd 98W of season
   for w,i,a,b,h,s,p --JTWC
                 e,l -- NHC
		   c -- CPHC/NHC

