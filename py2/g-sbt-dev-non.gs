function main(args)

rc=gsfallow('on')
rc=const()
rc=jaecol2()
basin=subwrd(args,1)
years=subwrd(args,2)
ivar=subwrd(args,3)

ddir='/data/w22/dat/tc/sbt/v01/gadat'
ddir='/data/w22/superBT/V04/gadat'
pdir='/data/w22/superBT/V04/plt/dev-non'

if(ivar = mvmax)
  var='mvmax' ; ylo=0 ; yhi=45 ; yd=5 ;  ylab='ERA5 Vmax[kts]'
endif

if(ivar = shr | ivar = shrspd)
  var='shrspd' ; ylo=0; yhi=40 ; yd=5 ;  ylab='ERA5 850-200 hPa Shear[kts]'
endif

if(ivar = tpw)
  var='tpw' ; ylo=40; yhi=80 ; yd=5 ;  ylab='ERA5 TotPrecipWater [mm]'
endif

if(ivar = rh7)
  var='rh7' ; ylo=45; yhi= 85 ; yd=5 ;  ylab='ERA5 700 hPa RH [%]'
endif

if(ivar = cpshi)
  var='cpshi' ; ylo=-60; yhi= 80 ; yd=20;  ylab='ERA5 CPS High [m]'
endif

if(ivar = cpslo)
  var='cpslo' ; ylo=-60; yhi= 80 ; yd=20;  ylab='ERA5 CPS Low [m]'
endif

if(ivar = og5)
  var='og5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 500-km precip [mm/d]'
endif

if(ivar = oi5)
  var='oi5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 500-km precip [mm/d]'
endif

if(ivar = oc5)
  var='oc5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='CMORPH 500-km precip [mm/d]'
endif

if(ivar = og3)
  var='og3' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 300-km precip [mm/d]'
endif

if(ivar = oi3)
  var='oi3' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 300-km precip [mm/d]'
endif

if(ivar = oc3)
  var='oc3' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='CMORPH 300-km precip [mm/d]'
endif

if(ivar = og8)
  var='og8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 800-km precip [mm/d]'
endif

if(ivar = oi8)
  var='oi8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 800-km oecip [mm/d]'
endif

if(ivar = oc8)
  var='oc8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='CMORPH 800-km precip [mm/d]'
endif

if(basin = 'l') ; t1=ylab' LANT 'years ; endif
if(basin = 'w') ; t1=ylab' WPAC 'years ; endif
if(basin = 'e') ; t1=ylab' EPAC 'years ; endif
if(basin = 'h') ; t1=ylab' SHEM 'years ; endif

pngpath=pdir'/'var'-'basin'-'years'.png'

ncol=23 ; ncola=29 ; nsty=3
dcol=33 ; dcola=39 ; dsty=3
xlab='Time to Genesis(dev) v Dissipation(nondev) [h] '
npath=ddir'/ts-non-'basin'.'years'.ctl'
nf=ofile(npath)

dpath=ddir'/ts-dev-'basin'.'years'.ctl'
df=ofile(dpath)

rc=metadata(nf,y, 0)
rc=metadata(df,y, 0)

nyn=_ny.nf
nyd=_ny.df

print 'ddd 'nyd' nn 'nyn

if(nyd >= nyn) ; nyall=nyn ; endif
if(nyn > nyd)  ; nyall=nyd ; endif
# -- weird problem when nyd>nyn and using npvalid.gsf...
#
if(basin = 'l')
nyn=nyall
nyd=nyall
endif

print 'nnnn 'nyn' 'nyd' 'nyall
'set grads off'
'set timelab on'
'set missconn on'
'set mproj off'
'set parea 1 10.5 0.75 7.5'
'set lon -120 0'
'set y 1'
nave='ave('var'.'nf',y=1,y='nyn')'
dave='ave('var'.'df',y=1,y='nyd')'

#'d 'nave
#'d 'dave
#'q pos'
'set xlint 24'
'set vrange 'ylo' 'yhi
'set ylint 'yd
yy=1
while(yy <= nyn)

# -- non dev
#
nv=var'.'nf'(y='yy')'
nnp=npvalid(nv)

#print 'nnnnnpppp 'nnp
'set cmark 0'
'set ccolor 'ncol
'set cthick 1'
'set cstyle 'nsty

if(nnp != 999)
  'd 'nv
endif
yy=yy+1
endwhile  
 
# -- dev
#
yy=1
while(yy <= nyd)
dv=var'.'df'(y='yy')'
nnd=npvalid(dv)

'set cmark 0'
'set ccolor 'dcol
'set cthick 1'
'set cstyle 'dsty

if(nnd != 999)
  'd 'dv
endif

yy=yy+1

endwhile
'set y 1'
'set cmark 0'
'set ccolor 0'
'set cthick 10'
'd 'nave

'set cmark 0'
'set ccolor 'ncola
'set cthick 8'
'd 'nave

'set cmark 0'
'set ccolor 0'
'set cthick 10'
'd 'dave

'set cmark 0'
'set ccolor 'dcola
'set cthick 8'
'd 'dave

if(var = 'shr')
'set cmark 0'
'set ccolor 1'
'set cthick 15'
'd const('dave',15,-a)'
endif

'draw xlab 'xlab
'draw ylab 'ylab

t2='#Dev(green): '_ny.df' #NonDev(red): '_ny.nf
rc=toptitle(t1,t2,1.25)

'gxprint 'pngpath' x1024  y768'

'q pos'
'quit'

return
