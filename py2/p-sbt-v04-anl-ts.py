#!/usr/bin/env python

from sBT import *

#import pandas as pd
#import numpy as np

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.defaults={
            #'version':'v01',
            }

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'lsVars':           ['L',0,1,' list variable/descriptions'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            #'dtgopt':           ['d:',None,'a',' dtgopt'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'doPlot':           ['P:',None,'a',' plot ivars -- ivar0,ivars1...'],
            'doXv':             ['X',0,1,'do xv of plot if doPlot != None'],
            
            
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- get meta data
#
lsverb=0
if(lsVars): lsverb=1

sMdesc=lsSbtVars(verb=lsverb)
mD3desc=lsMd3Vars(verb=lsverb)
mD3sum=lsMd3SumVars(verb=lsverb)

if(lsVars):  sys.exit()


MF.sTimer('ALL')

MF.sTimer('sbt')
sbt=superBT(versionsBT,verb=verb)
MF.dTimer('sbt')

# -- internal processing verb
#
overb=0

istmopt=stmopt
stmids=None
if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+sbt.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=overb)

    sbtTSDev={}
    sbtTSNonDev={}
    
    nNN=0

    sbt.stmopt=istmopt

    #'m3stmid','storm id in NNB.YYYY format'
    #'m3tcType','TC lifetype type: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt); STY (super typhoon >= 130 kt)'
    #'m3stmType','TC type NN - numbered TC, NONdev - non-developing pTC; DEV - pTC that developed into NN storm'
    #'dtg','date-time-group YYYYMMDDHH'
    #'blat','best track latitude degN'
    #'blon','best track longitude degE'
    #'bvmax','best track Vmax [kts]'
    #'bpmin','best track central pressure [hPa]'
    #'bdir','best track direction of motion [deg]'
    #'bspd','best track speed [kt]'
    #'btccode','best track TC code'
    #'br34m','best track mean R34 [km]'
    #'land','distance from coast [km]'
    #'mvmax','model Vmax [kts]'
    #'r34m','mean r34 km for diag calc'
    #'shrspd','850-200 hPa shear speed kts'
    #'shrdir','850-200 hPa shear direction deg'
    #'stmspd','storm speed in diagnostic file calc'
    #'stmdir','storm direction of motion in diagnostic file calc'
    #'sst','SST ERA5 degC'
    #'ssta','SST anomaly degC'
    #'vort850','850 hPa relative vorticity'
    #'dvrg200','200 hPa divergence'
    #'cpsb','CPS baroclinic'
    #'cpslo','CPS low: 1000-600 thickness'
    #'cpshi','CPS hi:   600-200 thickness'
    #'tpw','total precipitable water'
    #'rh50','relative humidity 500 hPa'
    #'rh70','relative humidity 700 hPa'
    #'rh85','relative humidity 850 hPa'
    #'u85','u wind 850 hPa'
    #'u70','u wind 700 hPa'
    #'u50','u wind 500 hPa'
    #'v85','v wind 850 hPa'
    #'v70','v wind 700 hPa'
    #'v50','v wind 500 hPa'
    #'roci1','roci of penultimate contour'
    #'poci1','poci of penultimate contour'
    #'roci0','roci outermost contour'
    #'poci0','poci outermost contour'
    #'to3','title'
    #'oc3','CMORPH 300-km precip at Best Track position [mm/d]'
    #'og3','GSMaP  300-km precip at Best Track position [mm/d]'
    #'oi3','IMERG  300-km precip at Best Track position [mm/d]'
    #'to5','title'
    #'oc5','CMORPH 500-km precip at Best Track position [mm/d]'
    #'og5','GSMaP  500-km precip at Best Track position [mm/d]'
    #'oi5','IMERG  500-km precip at Best Track position [mm/d]'
    #'to8','title'
    #'oc8','CMORPH 800-km precip at Best Track position [mm/d]'
    #'og8','GSMaP  800-km precip at Best Track position [mm/d]'
    #'oi8','IMERG  800-km precip at Best Track position [mm/d]'
    #'toe3','title'
    #'ec3','CMORPH 300-km precip at ERA5 position [mm/d]'
    #'eg3','GSMaP  300-km precip at ERA5 position [mm/d]'
    #'ei3','IMERG  300-km precip at ERA5 position [mm/d]'
    #'te3','title'
    #'e3','ERA5 500-km precip [mm/d]'
    #'re3','ERA5 ratio Convective/Total 300-km precip [%]'
    #'toe5','title'
    #'ec5','CMORPH 500-km precip at ERA5 position [mm/d]'
    #'eg5','GSMaP 500-km precip at ERA5 position [mm/d]'
    #'ei5','IMERG 500-km precip at ERA5 position [mm/d]'
    #'te5','title'
    #'e5','ERA5 500-km precip [mm/d]'
    #'re5','ERA5 ratio Convective/Total 500-km precip [%]'
    #'toe8','title'
    #'ec8','CMORPH 800-km precip at ERA5 position [mm/d]'
    #'eg8','GSMaP 800-km precip at ERA5 position [mm/d]'
    #'ei8','IMERG 800-km precip at ERA5 position [mm/d]'
    #'te8','title era5 pr'
    #'e8','ERA5 800-km precip [mm/d]'
    #'re8','ERA5 ratio Convective/Total 800-km precip [%]'        
       
        #n 0 a0w.2019 'm3stmid'
        #n 1 TD 'm3tcType'
        #n 2 DEV 'm3stmType'
        #n 3 2019010306 'dtg'
        #n 4 3.1 'blat'
        #n 5 174.8 'blon'
        #n 6 20 'bvmax'
        #n 7 1007 'bpmin'
        #n 8 231 'bdir'
        #n 9 13 'bspd'
        #n 10 DB 'btccode'
        #n 11 -999.0 'br34m'
        #n 12 3040 'land'
        #n 13 21 'mvmax'
        #n 14 -999 'r34m'
        #n 15 17 'shrspd'
        #n 16 339 'shrdir'
        #n 17 5 'stmspd'
        #n 18 233 'stmdir'
        #n 19 30.0 'sst'
        #n 20 1.5 'ssta'
        #n 21 119 'vort850'
        #n 22 132 'dvrg200'
        #n 23 -4 'cpsb'
        #n 24 2 'cpslo'
        #n 25 8 'cpshi'
        #n 26 65 'tpw'
        #n 27 79 'rh50'
        #n 28 78 'rh70'
        #n 29 87 'rh85'
        #n 30 -38 'u85'
        #n 31 10 'u70'
        #n 32 66 'u50'
        #n 33 9 'v85'
        #n 34 44 'v70'
        #n 35 56 'v50'
        #n 36 -999 'roci1'
        #n 37 -999 'poci1'
        #n 38 -999 'roci0'
        #n 39 -999 'poci0'
        #n 40 O3 'to3'
        #n 41 20.3 'oc3'
        #n 42 16.7 'og3'
        #n 43 16.2 'oi3'
        #n 44 O5 'to5'
        #n 45 29.8 'oc5'
        #n 46 35.4 'og5'
        #n 47 34.2 'oi5'
        #n 48 O8 'to8'
        #n 49 26.5 'oc8'
        #n 50 36.3 'og8'
        #n 51 28.3 'oi8'
        #n 52 OE3 'toe3'
        #n 53 29.0 'ec3'
        #n 54 27.9 'eg3'
        #n 55 38.8 'ei3'
        #n 56 E3 'te3'
        #n 57 37.8 'e3'
        #n 58 67 're3'
        #n 59 OE5 'toe5'
        #n 60 36.4 'ec5'
        #n 61 51.5 'eg5'
        #n 62 43.7 'ei5'
        #n 63 E5 'te5'
        #n 64 32.5 'e5'
        #n 65 55 're5'
        #n 66 OE8 'toe8'
        #n 67 28.2 'ec8'
        #n 68 39.0 'eg8'
        #n 69 29.5 'ei8'
        #n 70 E8 'te8'
        #n 71 23.1 'e8'
        #n 72 45 're8'


    ovars=['bvmax','bspd','br34m','stmspd',
           'mvmax',
           'shrspd',
           'cpsb','cpslo','cpshi',
           'tpw','rh70',
           'oc3','og3','oi3',
           'ec3','eg3','ei3',
           'oc5','og5','oi5',
           'ec5','eg5','ei5',
           'oc8','og8','oi8',
           'ec8','eg8','ei8',
           'e3','re3',
           'ssta']

    #ovars=['mvmax','bvmax','stmspd']
    #ovars=['bspd','stmspd']
    
    tovars=[]
    for ovar in ovars:
        tovars.append("%s"%(ovar))
        
    ovars=tovars

    tsNon={}
    tsDev={}
    overb=verb

    for stmid in stmids:
        (sbtType,sbtTS)=sbt.getSbtTS(stmid,verb=overb)
        if(sbtType == 'NONdev'):
            sbtTSNonDev[stmid]=sbtTS
        elif(sbtType == 'DEV'):
            sbtTSDev[stmid]=sbtTS
        else:
            nNN=nNN+1
        
            
    nstmids=sbtTSNonDev.keys()
    nstmids.sort()

    dstmids=sbtTSDev.keys()
    dstmids.sort()

    if(verb == 2):
        
        for nstmid in nstmids:
            print 'NNNN',nstmid
            nsbtts=sbtTSNonDev[nstmid]
            ntimes=nsbtts.keys()
            ntimes.sort()
            for ntime in ntimes:
                print 'nn',ntime,nsbtts[ntime]
            
            for dstmid in dstmids:
                print 'DDDD',dstmid
                dsbtts=sbtTSDev[dstmid]
                dtimes=dsbtts.keys()
                dtimes.sort()
                for dtime in dtimes:
                    print 'dd',dtime,dsbtts[dtime]
                    
    nDev=len(dstmids)
    nNon=len(nstmids)
    
    if(nDev != nNN):
        print 'hhhmmmmmm nDev != nNN ',nDev,nNN
    
    if(nNon != 0 and nNN != 0 and nDev != 0):
        rDev=nDev*1.0/float(nNon+nDev)
        rDev=rDev*100.0
        rDevN=nNN*1.0/float(nNon+nNN)
        rDevN=rDevN*100.0
        pMissN=rDevN-rDev
        print 'NNN for stmopt: ',stmopt,'nNN: ',nNN,'nDev',nDev,'nNon',nNon
        print 'DDD rFormDev: %3.0f%%  NNM rFormN: %3.0f%%  %4.1f%%'%(rDev,rDevN,pMissN)

    rc=sbt.makeGaNonVDevTSDict(sbtTSNonDev,'non',ovars,verb=overb,override=override)
    rc=sbt.makeGaNonVDevTSDict(sbtTSDev,'dev',ovars,verb=overb,override=override)

    if(doPlot != None):
        ivars=doPlot.split(',')
        ropt=''
        ss=istmopt.split('.')
        basin=ss[0]
        years=ss[1]
        for ivar in ivars:
            if(ivar in ovars):
                cmd='''grads -lbc "g-sbt-dev-non.gs %s %s %s"'''%(basin,years,ivar)
                mf.runcmd(cmd,ropt)
            else:
                print 'WWW ivar: ',ivar,' not in ovars: ',str(ovars)
                
            if(doXv):
                pstmopt=istmopt.replace('.','-')
                pmask="%s/plt/dev-non/%s*%s*png"%(sbtRoot,ivar,pstmopt)
                print 'ppp',pmask
                pngpaths=glob.glob(pmask)
                if(len(pngpaths) > 0):
                    cmd='xv %s'%(pngpaths[0])
                    mf.runcmd(cmd,ropt)
                                   
        

MF.dTimer('ALL')



sys.exit()


