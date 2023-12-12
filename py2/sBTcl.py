from sBTvars import *
from sBTvm import *

# -- CCCCCCCCCCCCCCCCCCCC -- wxmap2
#
class MFbase():

    def sendEmail(self,to_addr_list,subject,message,
                  passwdFile='/data/amb/users/fiorino/w21/prc/lib/python/passwdMFemail',
                  cc_addr_list=[],
                  from_addr='michael.fiorino@noaa.gov',
                  smtpserver='smtp.gmail.com:587',
                  login='michael.fiorino@noaa.gov',
                  password=None,
                  ):


        import smtplib,base64

        # did base64.b64encode(real password) - put in passwdFile and made it rw by owner only
        # and did NOT include in svn
        #

        password=open(passwdFile).read()
        password=base64.b64decode(password)

        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        if(len(cc_addr_list) > 0): header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject

        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()

    def find(self,mystr,pattern):
            rc=0
            if(mystr.find(pattern) != -1): rc=1
            return(rc)


    def ls(self,findstr=None,lsopt=None,maxchar=116,varsonly=0,quiet=0):

        methods=[]
        variables=[]
        clss=[]
        nvar=0

        mlen=28

        mformat="MMM: %%-%ds: %%s"%(mlen)
        cformat="CCC: %%-%ds: %%s"%(mlen)
        vformat="VVV(%%3d): %%-%ds: %%s"%(mlen)
        dd=inspect.getmembers(self)

        for d in dd:
            name=d[0]
            if(findstr != None):
                if(not(find(name,findstr))): continue

            if(type(d[1]) is ListType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            elif(type(d[1]) is DictType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            else:
                try:
                    val=str(d[1])
                except:
                    val='undef...'

            if(lsopt != None): val=str(d[1])
            

            if(find(val,'<bound method') or find(val,'<module ')):
                methods.append(mformat%(name[0:mlen],val[0:maxchar]))
            elif(find(val,'instance at')):
                clss.append(cformat%(name[0:mlen],val[0:maxchar]))
            else:
                if(len(val) >= maxchar): val=val[0:maxchar] + '... NOT ListType or DictType'
                variables.append(vformat%(nvar,name[0:mlen],val))
                nvar=nvar+1

        if(not(quiet)):

            if(len(clss) > 0 and not(varsonly)):
                print
                for cls in clss:
                    print cls
                print

            if(len(methods) > 0 and not(varsonly)):
                for method in methods:
                    print method
                print

            for variable in variables:
                print variable


        return(clss,methods,variables)


    def setObjVarsNone(self):

        keepvars=keepclss=None

        if(hasattr(self,'keepObjVars')):
            keepvars=self.keepObjVars

        if(hasattr(self,'keepObjClss')):
            keepclss=self.keepObjClss

        if(keepvars == None and keepclss == None):
            return


        # -- get the classes, methods, vars
        #
        (clss,methods,variables)=self.ls(quiet=1)

        if(keepvars != None):
            for var in variables:
                vvar=var.split()[2].strip()
                if(find(vvar,'__')): continue
                if(not(vvar in keepvars)):
                    try:
                        cmd="self.%s=None"%(vvar)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vvar: ',vvar

        if(keepclss != None):
            for cls in clss:
                vcls=cls.split()[1].strip()
                if(find(vcls,'__')): continue
                if(not(vcls in keepclss)):
                    try:
                        cmd="self.%s=None"%(vcls)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vcls: ',vcls




    def setPyppath(self,pyppath=None):
        """ method to set the pyppath for getPyp and putPyp"""

        if(pyppath == None and hasattr(self,'pyppath') and self.pyppath == None):
            ppath='/tmp/zy0x1w2.pyp'

        elif(pyppath != None):
            ppath=pyppath

        elif(hasattr(self,'pyppath') and self.pyppath != None):
            ppath=self.pyppath

        else:
            print 'EEE unable to open either pyppath: ',pyppath,' or self.pyppath: ',self.pyppath
            return(None)

        return(ppath)



    def getPyp(self,pyppath=None,unlink=0,verb=0):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(unlink):
            try:    os.unlink(ppath)
            except:  None

        if(os.path.exists(ppath)):
            if(verb): print "getPyp opening: ",ppath
            PS=open(ppath)
            try:
                FR=pickle.load(PS)
                if(verb): print "hai, getPyp ha, itadakimasu..."
            except:
                if(verb): print "IEE, getPyp ga, komarimashita ne! "
                FR=None
            PS.close()
            return(FR)

        else:
            return(None)


    def putPyp(self,pyp=None,pyppath=None,unlink=0,
               unlinkException=0,
               unlinkBadDump=0,
               verb=1):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(pyp != None):
            pyppckle=pyp
        else:
            pyppckle=self

        if(unlink):
            try:
                os.unlink(ppath)
            except:
                None

        try:
            PS=open(ppath,'w')
            pickle.dump(pyppckle,PS)
            PS.close()
            siz=os.path.getsize(ppath)
            if(verb):
                print 'III dumping pyp: ',pyppckle
                print 'III     to path: ',ppath,' size: ',siz
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',ppath,' on open/dump exception'
                os.unlink(ppath)
                try:
                    PS=open(ppath,'w')
                    pickle.dump(pyppckle,PS)
                    PS.close()
                except:
                    print """EEEEE unable to pickle.dump: ',ppath,' after unlinkException, kill it anyway...it's baaad, it's baaad..."""
                    os.unlink(ppath)

            else:
                print 'EEEEE unable to pickle.dump: ',ppath,' so unlink it???'
                if(unlinkBadDump): os.unlink(ppath)


    def initCurState(self):

        self.curdtg=mf.dtg()
        self.curphr=mf.dtg('phr')
        self.curyear=self.curdtg[0:4]

        if(not(hasattr(self,'curtime'))):  self.curtime=[]

        self.curtime.append(mf.dtg('dtg.phms'))



    def sTimer(self,tag='notag'):

        if(not(hasattr(self,'stimers'))):    self.stimers={}
        value=timer()
        self.loadDictList(self.stimers,tag,value)

    def dTimer(self,tag='notag'):

        sleep(0.1)
        phms=mf.dtg('dtg.phms')
        if(hasattr(self,'stimers')):
            value=time.time()-self.stimers[tag][-1]
            
        card="TTTTTTTTTTTTTTTTTTTTTTT-------------------timer: %-72s: %6.3f      at: %s"%(tag,value,phms)
        print card
        return(card)

    def sTime(self,tag='notag'):

        if(not(hasattr(self,'stimes'))):    self.stimes={}
        value=timer()
        self.loadDictList(self.stimes,tag,value)


    def dTime(self,tag='notag'):

        if(not(hasattr(self,'curdtimes'))):
            self.curdtimes={}
        else:
            if( type(self.curdtimes) is not(DictType) ): self.curdtimes={}

        value=mf.dtg('dtg.phms')
        self.loadDictList(self.curdtimes,tag,value)

        if(not(hasattr(self,'dtimes'))):   self.dtimes={}
        value=time.time()-self.stimes[tag][-1]
        self.loadDictList(self.dtimes,tag,value)



    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)




class MFutils(MFbase):

    import mf

    calendar='gregorian'

    mname = {
        '01':'January',
        '02':'February',
        '03':'March',
        '04':'April',
        '05':'May',
        '06':'June',
        '07':'July',
        '08':'August',
        '09':'September',
        '10':'October',
        '11':'November',
        '12':'December'
    }

    mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
    mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
    aday=(1,32,60,91,121,152,182,213,244,274,305,335)
    adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)

    sec2hr=1/3600.0

    pyppath=None

    def nDayYear(self,yyyy):
        nd=365
        if (int(yyyy)%4 == 0): nd=366
        return(nd)

    def nDayMonth(self,yyyymm):
        yyyy=int(yyyymm[0:4])
        mm=int(yyyymm[4:6])

        leap=0
        if (yyyy%4 == 0): leap=1

        #
        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): leap=0

        if(leap):
            return(self.mdayleap[mm])
        else:
            return(self.mday[mm])


    def TimeZoneName(self):

        import time
        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)


    def Dtg2JulianDay(self,dtg):

        import time
        year=int(str(dtg)[0:4])
        month=int(str(dtg)[4:6])
        day=int(str(dtg)[6:8])

        t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        jday=time.gmtime(t)[7]
        jday="%03d"%(int(jday))
        return (jday)

    def YearJulianDay2YMD(self,year,jday):

        from datetime import date,timedelta
        ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
        ymd=ymd.strftime("%Y%m%d")
        return(ymd)



    def YearJulianDay2Dtg(self,year,jday,chour=None):

        from datetime import date,timedelta
        ijday=int(jday)
        rjdayhr=jday-ijday*1.0
        ymd=date(int(str(year)),1,1) + timedelta(ijday-1)
        if(chour == None):
            chour="%02d"%(int(rjdayhr*24.0+0.5))
        ymd=ymd.strftime("%Y%m%d")
        dtg=ymd+chour
        return(dtg)


    def Dtg2Timei(self,dtg):
        timei=time.strptime(dtg,"%Y%m%d%H")
        return(timei)


    def DeltaTimei(self,timei1,timei2):

        t1=time.mktime(timei1)
        t2=time.mktime(timei2)
        dt=(t1-t2)/3600.0
        return(dt)

    def getGtime4DTG(self,dtg,
                     #localTZ='America/Denver', localTZname='MST', localTZnameDST='MDT',
                     localTZ='US/Eastern', localTZname='EST', localTZnameDST='EDT',
                     local=1,verb=0):
        
        from datetime import datetime
        from dateutil import tz
        from datetime import date
        import calendar
        import pytz
        
        
        def findDay(year,month,day):
            born = date(year, month, day)
            return born.strftime("%a")
        
        
        def is_dst (localTZ,dtg=None):
            
            """Determine whether or not Daylight Savings Time (DST)
            is currently in effect"""
            # -- use dtg
        
            if(dtg != None):
                yy=int(dtg[0:4])
                mm=int(dtg[4:6])
                dd=int(dtg[6:8])
    
                x=datetime(yy,1,1,0,0,0)
                y=datetime(yy,mm,dd,0,0,0)
                timezone = pytz.timezone(localTZ)
                tzy = timezone.localize(y, is_dst=None)
                tzx = timezone.localize(x, is_dst=None)
                xoff=str(tzx)[-6:-3]
                yoff=str(tzy)[-6:-3]
                xoff=int(xoff)
                yoff=int(yoff)
                
                return not(xoff == yoff)
        
            # -- use current
            else:
                x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(localTZ)) # Jan 1 of this year
                y = datetime.now(pytz.timezone(localTZ))
        
                # if DST is in effect, their offsets will be different
                return not (y.utcoffset() == x.utcoffset())
        
    
        utcTZname='UTC'
        
        isDst=is_dst(localTZ,dtg=dtg)
        if(isDst): localTZname=localTZnameDST
        
        from_zone = tz.gettz('utc'.upper())
        to_zone = tz.gettz(localTZ)
        
        if(verb): print 'iii ',isDst,from_zone,to_zone
            
        cdtg=str(dtg)
        
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])
        ct='%4d-%02d-%02d %02d:%02d:%02d'%(yy,mm,dd,hh,0,0)
        if(verb): print ct
        
        utc = datetime.strptime(ct, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
    
        # -- get the standard time string for utc and local
        #
        uuu=utc.astimezone(from_zone)
        uu=str(uuu)
    
        mountain = utc.astimezone(to_zone)
        mm=str(mountain)
        
        myy=int(mm[0:4])
        mmm=int(mm[5:7])
        mdd=int(mm[8:10])
        mhh=int(mm[11:13])
        mmn=int(mm[14:16])
        
        uyy=int(uu[0:4])
        umm=int(uu[5:7])
        udd=int(uu[8:10])
        uhh=int(uu[11:13])
        umn=int(uu[14:16])
        
        
        mDDName=findDay(myy,mmm,mdd)
        uDDName=findDay(uyy,umm,udd)
        
        mmName=mountain.strftime('%b').upper()
        ummName=uuu.strftime('%b').upper()
        
        mgtime="%s %02d%02d %s %02d %s"%(mDDName,mhh,mmn,localTZname,mdd,mmName)
        ugtime="%s %02d%02d %s %02d %s"%(uDDName,uhh,umn,utcTZname,udd,ummName)
        if(verb): 
            print 'gggg: ',mgtime
            print 'uggg: ',ugtime
        
        gtime=ugtime
        if(local):
            gtime=mgtime
            
        return(gtime)


    def PathCreateTimeDtgdiff(self,dtg,path):

        # -- handle broken symbolic link -- return -666.66 -- for gfs2 when /public down
        #
        if(os.path.islink(path) and not(os.path.exists(path))): return(-666.66)
         
        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)

        return(dt)


    def PathModifyTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getmtime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)

    def PathCreateTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getctime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)


    def PathModifyTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getmtime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathCreateTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getctime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathModifyTimeDtgdiff(self,dtg,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)+tzoff

        return(dt)

    def getCurTimei(self):

        ctimei=time.gmtime(time.time())
        return(ctimei)


    def PathModifyTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def PathCreateTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def GetPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathNlines(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            nlines=-999
        else:
            nlines=int(check_output(['wc', '-l', path]).split()[0])
            
        return(nlines)
    
    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def listTxtPath(self,path,ncprint=None):

        if(self.GetPathSiz(path) != None):
            cards=open(path).readlines()
            ncards=len(cards)
            if(ncprint != None):
                ncprint=min(ncprint,ncards)
            else:
                ncprint=ncards
            for n in range(0,ncprint):
                print cards[n][0:-1]



    def GetDirFilesSiz(self,dir,pathopt='exit',mask="*",verb=0):

        if(self.ChkPath(dir,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            paths=glob.glob("%s/%s"%(dir,mask))
            siz=0
            for path in paths:
                fsiz=self.GetPathSiz(path)
                if(fsiz != None): siz=siz+fsiz

        return(siz)

    def GetNfilesDir(self,dir,mask="*"):
        files=glob.glob("%s/%s"%(dir,mask))
        return(len(files))

    def ChkDirOld(dir,diropt='verb'):
    
        if(dir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not(os.path.isdir(dir)) :
            if(diropt != 'quiet'): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('mkdir -p %s'%(dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",dir
            return(1)


    def ChkDir(self,ddir,diropt='verb'):
    
        if(ddir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not os.path.exists(ddir):
            
            if(diropt != 'quiet'): print "dir  (not there): ",ddir
            if(diropt == 'mk' or diropt == 'mkdir'):
        
                try:
                    os.makedirs(ddir)
                    print 'dir     (MADE): ',ddir
                    return(2)
                    
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
                        #print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                        #return(-1)
                    else:
                        print "\nBE CAREFUL! Directory %s already exists." % path
        
            else:
                return(0)
            
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",ddir
            return(1)

    def ChangeDir(self,ddir,verb=1,docurtime=0):

        dtgcurtime=''
        if(docurtime):  dtgcurtime=mf.dtg('curtime')

        try:
            os.chdir(ddir)
            if(verb == 1): print 'cd---> ',ddir,dtgcurtime
            return(1)
        except:
            if(verb != -1): print 'WWW(MF.ChangeDir()) unable to cd to: ',ddir
            return(0)


    def ChkPath(self,path,pathopt='noexit',verb=0):

        if(path == None): return(0)

        if not(os.path.exists(path)) :
            if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
            if(pathopt == 'exit'):
                print "EEE(ChkPath): Sayoonara..."
                sys.exit()
            else:
                return(0)
        else:
            return(1)


    def is0618Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '06' or hh == '18'): rc=1
        return(rc)

    def is0012Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '00' or hh == '12'): rc=1
        return(rc)

    def isSynopticHour(self,dtg,dtau=6):

        hh=int(dtg[8:10])
        rc=0
        remainder=hh%dtau
        if(remainder == 0): rc=1
        return(rc,remainder)

    def TimeZoneName(self):

        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)

    def dtg(self,opt="default"):

        tzname=" %s "%(self.TimeZoneName())

        if (opt == "curtime" or opt == "curtimeonly" ):
            t=time.localtime(time.time())
        else:
            t=time.gmtime(time.time())

        yr="%04d" % t[0]
        mo="%02d" % t[1]
        dy="%02d" % t[2]
        hr="%02d" % t[3]
        fhr="%02d" % (int(t[3]/6)*6)
        phr=int(t[3])%6
        mn="%02d" % t[4]
        sc="%02d" % t[5]
        fphr=float(phr)*1.0 + float(mn)/60.0;

        if opt == "default":
            dtg=yr + mo + dy + fhr
        elif opt == "phr":
            dtg="%4.2f"%(fphr)
        elif opt == "fphr":
            dtg=fphr
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.phm":
            cphr="%02d"%(phr)
            dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
        elif opt == "dtgmn":
            dtg=yr + mo + dy +  hr + mn
        elif opt == "dtg_ms":
            dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
        elif opt == "dtg_hms":
            dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.hms":
            dtg=yr + mo + dy +  " " + hr + ":" + mn + ":" + sc
        elif opt == "dtgcurhr":
            dtg=yr + mo + dy + hr
        elif (opt == "timeonly"):
            dtg=hr+":"+mn+":"+sc+ " UTC "
        elif (opt == "time"):
            dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtime"):
            dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtimeonly"):
            dtg=hr+":"+mn+":"+sc+ tzname
        else:
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

        return(dtg)

    def dtg2time(self,dtg):

        cdtg=str(dtg)

        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
        return(time)

    def dtg2YMDH(self,dtg):

        cdtg=str(dtg)

        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]

        return(yy,mm,dd,hh)
    
    def dtg2ISODateTime(self,dtg):
        (yy,mm,dd,hh)=self.dtg2YMDH(dtg)
        isodate="%s-%s-%s"%(yy,mm,dd)
        isohour="%02d:00:00"%(int(hh))
        return(isodate,isohour)
        


    def DtgDiff(self,dtg1,dtg2):

        dtg1=str(dtg1)
        dtg2=str(dtg2)

        yyyy1=int(dtg1[0:4])
        yyyy2=int(dtg2[0:4])

        offyear=1981
        if(yyyy1%4==0):
            offyear=1980
        if(yyyy2%4==0):
            offyear=1979

        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): offyear=1981

        #
        # 20030828 -- fix crossing year if offsetting
        #

        dyyyy=yyyy2-yyyy1

        if(yyyy1 < offyear or yyyy2 < offyear):
            dtg1off=offyear-int(dtg1[0:4])
            dtg1="%04d"%(offyear)+dtg1[4:10]
            dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

        t1=self.dtg2time(dtg1)
        t2=self.dtg2time(dtg2)
        nhr=(t2-t1)*self.sec2hr

        return(nhr)

    def DiffDtgHms(self,dtghms1,dtghms2):
        """ diff of dtghms2 (2nd arg) - dtghms1"""
        ymd1=dtghms1.split()[0]
        y1=ymd1[0:4]
        #ndy1=self.nDayYear(y1) -- constant length of year
        ndy1=365.0
        jday1=self.Dtg2JulianDay(ymd1)
        (hh1,mm1,ss1)=dtghms1.split()[1].split(':')
        ymdh1=(float(y1)*float(ndy1) + float(jday1))*24.0 + int(hh1)*1.0 + int(mm1)/60.0 + int(ss1)/3600.0
        #print '11111111111 ',y1,ndy1,ymd1,hh1,mm1,ss1,ymdh1

        ymd2=dtghms2.split()[0]
        y2=ymd2[0:4]
        #ndy2=self.nDayYear(y2)
        ndy2=ndy1
        jday2=self.Dtg2JulianDay(ymd2)
        (hh2,mm2,ss2)=dtghms2.split()[1].split(':')
        
        ymdh2=(float(y2)*float(ndy2) + float(jday2))*24.0 + int(hh2)*1.0 + int(mm2)/60.0 + int(ss2)/3600.0
        #print '22222222222 ',y2,ndy2,ymd2,hh2,mm2,ss2,ymdh2
        diff=ymdh2-ymdh1
        #print 'ddddddddddd ',diff

        return(diff)



    def YearRange(self,byear,eyear=None,inc=1):

        def yearinc(year,inc):
            nyear=int(year)+inc
            return(nyear)

        if(eyear == None):
            eyear=byear

        years=[]

        byear=int(byear)
        eyear=int(eyear)

        year=byear

        while(year<=eyear):
            years.append(year)
            year=yearinc(year,inc)

        return(years)


    def makeDtgsString(self,dtgs,msiz=1024,osiz=132,ndtg=10):
        """ clean up list of dtgs"""

        #card=str(dtgs)[0:msiz].replace(', ','').replace("""''""",' ').replace("""['""",'').replace("""']""",'')
        #
        #if(len(card) > osiz):
        #    card=card[0:osiz]
        #    card=card+'...'



        nend=len(dtgs)
        card='N: %4d  dtgs: '%(nend)
        if(nend == 0): return(card)
        if(len(dtgs) >= ndtg): nend=ndtg/2

        for dtg in dtgs[0:nend]:
            card=card+dtg+' '


        if(len(dtgs) >= ndtg):
            card=card+'... '
            for dtg in dtgs[(len(dtgs)-ndtg/2):]:
                card=card+dtg+' '

        return(card)


    def setDirFromHash(self,ss,n):

        sbdir=''
        for sb in ss[0:len(ss)-n]:
            sbdir="%s/%s"%(sbdir,sb)
        sbdir=sbdir.replace('//','/')

        return(sbdir)



#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
# time
#

    def rhh2hhmm(hh):

        if(hh < 0):
            rhh=abs(hh)
            lt0=1
        else:
            rhh=hh
            lt0=0

        imm=int(rhh*60.0+0.5)
        ihh=imm/60
        imm=imm%60
        if(lt0):
            ohhmm="-%02d:%02d"%(ihh,imm)
        else:
            ohhmm="+%02d:%02d"%(ihh,imm)

        return(ohhmm)


    #uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
    # utilities

    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)


    def uniqDictList(self,tdict):

        kk=tdict.keys()

        for k in kk:
            tlist=tdict[k]
            tlist=uniq(tlist)
            tdict[k]=tlist
            
        return(tdict)

    def uniqDict2List(self,ddict):
    
        kk1=ddict.keys()
        
        for k1 in kk1:
            kk2=ddict[k1].keys()
            
            for k2 in kk2:
                dlist=ddict[k1][k2]
                dlist=uniq(dlist)
                ddict[k1][k2]=dlist

    def uniqDictDict(self,dict):
        """ uniq a dict of dicts"""
        kk=dict.keys()

        for k in kk:
            dict2=dict[k]
            kk2=dict2.keys()
            self.uniqDictList(dict2)
            dict[k]=dict2
            
        return(dict)



    def addList2DictList(self,dict,key,list):
        try:
            dict[key]=dict[key]+list
        except:
            dict[key]=list


    def appendList(self,list,value):

        try:
            list.append(value)
        except:
            list=[]
            list.append(value)

    def appendDictList(self,dict,key,value):

        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)

    def append2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2].append(value)

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=[]
            dict[key1][key2].append(value)

    def set2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2]=value

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=value


    def append3KeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1][key2][key3]=value
        except:
            try:
                dict[key1][key2]={}
                dict[key1][key2][key3]=value
            except:
                dict[key1]={}
                dict[key1][key2]={}
                dict[key1][key2][key3]=value



    def append2TupleKeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1,key2].append(value)
        except:
            dict[key1,key2]=[]
            dict[key1,key2].append(value)


    def append3TupleKeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1,key2,key3].append(value)

        except:
            dict[key1,key2,key3]=[]
            dict[key1,key2,key3].append(value)



    def DictTr(self,dic):
        dict={}
        kk=dic.keys()
        for k in kk:
            val=dic[k]
            try:
                dict[val].append(k)
            except:
                dict[val]=[]
                dict[val].append(k)

        return(dict)

    def DictAdd(self,dic1,dic2,priority=2):
        dic={}
        kk1=dic1.keys()
        kk2=dic2.keys()
        kk=kk1+kk2
        kk.sort()
        kk=self.uniq(kk)

        for k in kk:

            hk1=dic1.has_key(k)
            hk2=dic2.has_key(k)

            if(hk1 and hk2):
                if(priority == 2):
                    dic[k]=dic2[k]
                else:
                    dic[k]=dic1[k]

            elif(hk1 and not(hk2)):
                dic[k]=dic1[k]
            elif(not(hk1) and hk2):
                dic[k]=dic2[k]
            else:
                print 'EEE DicAdd'
                sys.exit()

        return(dic)


    def uniqDict(self,dict):
        tt={}
        for kk in dict.keys():
            dd=dict[kk]
            dd=self.uniq(dd)
            tt[kk]=dd
        return(tt)

    def Dic2list(self,dic,ne):
        kk=dic.keys()
        kk.sort()

        list=[]
        for k in kk:
            list.append(dic[k][ne])

        return(list)


    def List2Dict(self,dic,list,ne):

        kk=dic.keys()
        kk.sort()

        for i in range(0,len(kk)):
            dic[kk[i]][ne]=list[i]

        return

    def List2String(self,ilist):

        ostring='\n'.join(ilist)
        ostring=ostring+'\n'
        return(ostring)
    
    def setList2String(self,ilist):
                
        lstring=''
        
        for n in range(0,len(ilist)):
            im=ilist[n]
            lstring=lstring+'%s'%(im)
            if(n < len(ilist)-1):
                lstring=lstring+','
            if(n > 0):
                lstring=lstring+' '
        return(lstring)
                

    def PrintDict(self,dict,name='dict'):

        cards=[]
        kk=dict.keys()
        kk.sort()
        nh=len(dict)

        # -- case of empty dict
        #
        if(len(kk) == 0):
            print 'WWW MF.PrintDict dict={} ... return cards=[]'
            return(cards)

        if(isinstance(kk[0],tuple)):   nk=len(kk[0])
        else:                          nk=1

        card="%s %d %d"%(name,nk,nh)
        cards.append(card)

        for k in kk:
            card=''
            if(isinstance(k,tuple)):
                for n in k:
                    card=card+' '+n
            else:
                card=card+' '+k
            card=card+' : '
            for n in dict[k]:
                card=card+' '+str(n)
            cards.append(card)

        return(cards)



    def WriteString2File(self,string,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open (MF.WriteString2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        c.writelines(string)
        c.close()
        return


    def WriteList2File(self,list,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in list:
            rcard=card.rstrip()
            if(verb): print rcard
            rcard=rcard+'\n'
            c.writelines(rcard)
        c.close()
        return


    def WriteList2Path(self,dlist,path,append=0,verb=0,warnonly=1):

        try:
            if(append):
                c=open(path,'a')
            else:
                c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in dlist:
            if(verb): print card
            card=card.rstrip()+'\n'
            c.writelines(card)
        c.close()
        return

    def WriteString2Path(self,string,path,verb=0,warnonly=1):

        self.WriteString2File(string,path,verb=verb)

        return


    def WriteHash2File(self,hash,path,verb=0):

        keys=hash.keys()
        keys.sort()

        O=open(path,'w')
        for key in keys:
            O.writelines(hash[key]+'\n')

        O.close()



    def ReadFile2List(self,path,verb=0):

        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2List) unable to open path: %s"%(path)
            return(None)

        return(list)


    def ReadFile2String(self,path,verb=0):

        string=''
        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2String) unable to open path: %s"%(path)
            return(string)

        for tt in list:
            if(verb): print tt
            string=string+str(tt)
        return(string)


    def WriteCtl(self,ctl,ctlpath,verb=0):

        try:
            c=open(ctlpath,'w')
        except:
            print "EEE unable to open: %s"%(ctlpath)
            sys.exit()

        if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
        c.writelines(ctl)
        c.close()
        return


    def PrintList(self,list,verb=0):

        for card in list:
            print card


    def sumList(self,list):
        if(list == None):
            sum=None
        else:
            sum=0.0
            for l in list:
                sum=sum+float(l)
        return(sum)


    # --- fundamentals
    #

    def uniq(self,list):
        weirdtest='asdasdfasdfasdfasdf'
        #
        # sort before length check for case of two
        #
        list.sort()
        rlist=[]

        if(len(list) > 2):
            test=list[1]
            test=weirdtest
        elif(len(list) == 0):
            return(rlist)
        else:
            test=list[0]

        if(test != weirdtest):
            rlist.append(test)

        for l in list:
            #if(repr(l) != repr(test)):
            if(l != test):
                rlist.append(l)
                test=l
        return(rlist)


    def find(self,mystr,pattern):
        rc=0
        if(mystr.find(pattern) != -1): rc=1
        return(rc)



    def h2hm(self,age):

        fh=int(age)*1.0
        im=int( (age-fh)*60.0+0.5 )
        if(im == 60):
            fh=fh+1.0
            im=0

        cage="%4.0f:%02d"%(fh,im)
        return(cage)


    def min2minsec(self,min):

        fm=int(min)*1.0
        im=int( (min-fm)*60.0+0.5 )
        if(im == 60):
            fm=fm+1.0
            im=0

        cmin="%4.0f:%02d"%(fm,im)
        return(cmin)



    def runcmdLog(self,cmd,ropt='',quiet=0,printCmd='runcmdLog'):

        if(ropt == 'norun'):
            print "CCC(%s): %s"%(printCmd,cmd)
            return([])
        else:
            if(not(quiet)): print "CCC(%s): %s"%(printCmd,cmd)
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()
            lines=output.split('\n')

        return(lines)


    def runcmdLogOutput(self,cmd,ropt='',quiet=0):

        if(ropt == 'norun' or not(quiet)): print "CCC(runcmdLog): %s"%(cmd)

        if(ropt == 'norun'):
            return([])
        else:
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()

        return(output)



    def runcmd(self,command,logpath='straightrun',lsopt=''):

        if(logpath == ''):
            logpath='straightrun'

        if(logpath == 'straightrun' or logpath == 'norun'):
            if(lsopt != 'q'): print "CCC: %s"%command
            if(logpath != 'norun'): os.system(command)
            return

        if(logpath == 'quiet'):

            tt=command.split()
            mycmd=tt[0]
            myarg=''
            if(len(tt) > 1):
                for t1 in tt[1:]:
                    myarg="%s %s"%(myarg,t1)

            #p=Popen([mycmd,myarg], stdout=PIPE)
            #(o,e)=p.communicate()

            rc=os.popen(command).readlines()
            return(rc)

        global LF

        #
        # output to log file (append and add title line)
        #

        if(logpath != 'nologpath'):

            log=getCommandOutput2(command)

            lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6 ('curtime'),command)
            lout=lout+log

            if(not(os.path.exists(logpath))):
                try:
                    LF=open(logpath,'a')
                    LF.writelines(lout)
                    LF.flush()
                except:
                    print 'EEE(runcmd): unable to open logpath: %s'%(logpath)
                    return
            else:
                try:
                    LF.writelines(lout)
                    LF.flush()
                except:
                    try:
                        LF=open(logpath,'a')
                        LF.writelines(lout)
                        LF.flush()
                    except:
                        LF.writelines(lout)
                        LF.flush()
                        print 'EEE(runcmd): unable to write to logpath: %s'%(logpath)
                        return

        #
        # output to terminal
        #

        else:

            log=getCommandOutput2(command)

            print "CCC(log): %s\n"%command
            print log

        return

    def runcmdRetry(self,cmd,ropt='',nTry=0,nTryMax=3,trySleep=5,
                    errorString='error',printCmd='runcmdRetry'):

        rsyncOK=1
        rc=0
        output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
        for o in output:
            print o
            if(find(o,errorString)): rsyncOK=0

        if(rsyncOK == 0): 
            nTry=1
        elif(rsyncOK):
            rc=1
            return(rc)

        while(nTry <= nTryMax):
            rsyncOK=1
            print
            print "IIIIIIII--------------------------retry cmd:",cmd, "ntry: ",nTry,' nTryMax: ',nTryMax
            print
            time.sleep(trySleep)  

            output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
            for o in output:
                print o
                if(find(o,errorString)): rsyncOK=0

            if(rsyncOK):
                nTry=nTryMax+1
                rc=1
            else:
                nTry=nTry+1
                rc=0

        return(rc)



    def get0012fromDtgs(self,dtgs):

        odtgs=[]
        for dtg in dtgs:
            hh=int(dtg[8:10])
            if(hh == 12 or hh == 0): odtgs.append(dtg)

        return(odtgs)



    def chkIfJobIsRunningOld(self,job,jobopt=None,killjob=1,verb=1,incron=0,nminWait=10,timesleep=5):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()


        def isRunning(job,jobopt,killjob):

            pids=LsPids()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2])
                jobchk=find(prc,job)

                if(jobopt != None):  joboptchk=find(prc,jobopt)
                else:                joboptchk=1

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=mf.dtg('curtime')
                    if(find(prc,'tcsh') or find(prc,'/bin/sh -c')): continue
                    print 'isRunning...cpid:',cpid,'curpid: ',curpid,'prc: ',prc,'aaaaaaaaaaaaafter tcsh check',killjob
                    rc=rc+1

                    if(killjob):
                        print 'KKKKKKKKKKK killing this job since a previous instance is already running....'
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,'')

            return(rc)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        if(nminWait > 0 and isRunning(job,jobopt,killjob) >= 1):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isRunning(job,jobopt,killjob) > 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isRunning(job,jobopt,killjob)
            if(verb): print 'chkIfJobIsRunning rc: ',rc

        return(rc)


    def whoIsRunningNew(self,job,jobopt=None,killjob=0,rcPid=0):
        """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""
        cpidOut=-999
        rc=0

        runPids=findPyPids(job)
        nrunPids=len(runPids)
        
        for runp in runPids:
            print runp
            
        # -- if only one return 0 to not cycle
        #
        if(nrunPids == 1):
            (cpid,opid,prc,ptime)= runPids[0]
            return(0)
        
        if(nrunPids > 1):

            jobchk=1
            (curpid,opid,curprc,ptime)=runPids[-1]

            for (cpid,opid,prc,ptime) in runPids:
            
                if(jobopt != None):
                    try:
                        prcjobopt=prc.split()[2:]
                    except:
                        prcjobopt=None

                    if(prcjobopt != None):
                        prcjoboptS=''
                        for pp in prcjobopt:
                            prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)
                else:
                    joboptchk=1
                    
                print 'jjjjjjjjjjjjjjjj',prc,cpid,curpid
                if(jobchk and joboptchk and cpid != curpid):

                    ctime=mf.dtg('curtime')
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                    cpidOut=cpid
                    rc=rc+1

                    kropt='quiet'
                    kropt='norun'
                    kropt=''
                    # -- do the killing inside whoIsRunning
                    #
                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,kropt)
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        runcmd(cmd,kropt)

        if(rc > 0 and rcPid): rc=cpidOut
        
        return(rc)




    def chkRunning(self,pyfile,setJobopt=None,strictChkIfRunning=0,verb=0,killjob=0,
                   timesleep=5,nminWait=5):
        
        """ big and complete check
"""
    # -- get command line vars, except -N
        pyfileopt=''
        for s in sys.argv[1:]:
            if(s != '-N'):
                pyfileopt='%s %s'%(pyfileopt,s)
    
        jobopt=pyfileopt.split()[0]
        # -- if very sctrict check -- any instance of pyfile
        if(strictChkIfRunning): jobopt=None
        
        if(setJobopt != None): jobopt=setJobopt
        
        if(verb): self.sTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        rc=self.chkIfJobIsRunning(pyfile,jobopt=jobopt,killjob=killjob,verb=verb,nminWait=nminWait,
                                  timesleep=timesleep)
        if(verb): self.dTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        
        return(rc)



    def chkIfJobIsRunning(self,job,jobopt=None,killjob=1,verb=0,incron=0,
                          nminWait=10,timesleep=5,rcPid=0,
                          # -- two types of joboptchk finding the jobopt string in prc or must be equal to jobopt
                          joboptchkType='find'):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()

        def isRunning(job,jobopt,killjob,rcPid=0):

            pids=LsPids()
            cpidOut=-999

            pids=uniq(pids)
            pids.sort()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()

                # -- uninteresting procs
                #
                if(find(prc,'[') and find(prc,']') or find(prc,'/dev/tty') or find(prc,'-tcsh') or find(prc,'-bash') or
                   find(prc,'/usr') or find(prc,'vmhgfs') or
                   find(prc,'sbin') or find(prc,'automount') or find(prc,'crond') or find(prc,'sshd')): continue

                jobchk=find(prc,job)

                if(verb): print 'M.chkIfJobIsRunning() jobchk ',jobchk,'prc:',prc,'job: ',job,jobopt
                if(jobopt != None):

                    # -- 20120326 new/better logic to check if exact job running
                    # -- 20131127 -- even better checks whole cmd line arg
                    #
                    if(jobchk):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None

                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)

                else:
                    joboptchk=1
                    

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=mf.dtg('curtime')
                    if(find(prc,'tcsh') or find(prc,'/bin/sh -c')): continue
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid, prc: ',cpid,prc,' job,jobopt',job,jobopt
                    cpidOut=cpid
                    rc=rc+1

                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,'quiet')
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            return(rc)



        def whoIsRunning(job,jobopt,killjob,rcPid=0):
            """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""

            pids=LsPids()
            cpidOut=-999

            pids=uniq(pids)
            pids.sort()
            
            runPids=[]
            # -- rc is the number of jobs
            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()
                # -- look for non cron jobs
                if(find(prc,job)):
                    if(find(prc,'cron')): continue
                    runPids.append((prc,cpid))

            nrunPids=len(runPids)
            
            # -- if only one return 0 to not cycle
            #
            if(nrunPids == 1):
                (prc,cpid)= runPids[0]
                return(0)
                
            if(nrunPids > 1):

                jobchk=1
                (curprc,curpid)=runPids[-1]

                for (prc,cpid) in runPids:
                
                    if(jobopt != None):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None
    
                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)
    
                            if(joboptchkType == 'find'): 
                                joboptchk=find(prcjoboptS,jobopt)
                            else:
                                joboptchk=(prcjoboptS == jobopt)
                    else:
                        joboptchk=1
                        
                
                    if(jobchk and joboptchk and cpid != curpid):

                        ctime=mf.dtg('curtime')
                        print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                        cpidOut=cpid
                        rc=rc+1
    
                        # -- do the killing inside whoIsRunning
                        #
                        if(killjob == 1):
                            print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                            cmd="kill %s"%(curpid)
                            runcmd(cmd,'quiet')
                        elif(killjob == -1):
                            print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                            cmd="kill %s"%(cpid)
                            runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            
            return(rc)


        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW M.chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        #
        rc=whoIsRunning(job,jobopt,killjob,rcPid=rcPid)
        if(verb): print '111111111111111111111111111 rc whoIsRunning: ',rc,'job: ',job,'jobopt: ',jobopt,' killjob: ',killjob
        
        # -- only cycle if not killjob...
        #
        if(nminWait > 0 and not(killjob) and rc >= 1 ):
            nsleep=0
            rc=whoIsRunning(job,jobopt,killjob,rcPid=0)
            if(verb): print '22222222222222222222222222222222222222 rc whoIsRunning: ',rc
            print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',mf.dtg('curtime')
            while(nsleep < (nmaxsleep-1) and rc >= 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep,' job,jobopt: ',job,jobopt
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

                rc=isRunning(job,jobopt,killjob,rcPid=0)
                print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',mf.dtg('curtime')

            rc=0


        return(rc)




    def chkIfFileIsOpen(self,path,verb=0,nminWait=10,timesleep=5):

        def isOpen(path,verb=0):

            if(not(self.GetPathSiz(path) > 0)):
                print 'WWW in chkIfFileIsOpen: ',path,' does not exist or is 0 length'
                return(0)

            rc=0
            openpids=[]
            cmd="lsof %s"%(path)
            lines=self.runcmdLog(cmd)
            if(len(lines[0]) > 0):

                if(verb):
                    olines=lines[1:-1]
                    olines=uniq(olines)
                    for line in olines:
                        pid=line.split()[1]
                        openpids.append(pid)
                        print 'chkIfFileIsOpen: ',line

                rc=1

            return(rc,openpids)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW chkIfFileIsOpen is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        if(nminWait > 0 and isOpen(path,verb=verb) ):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isOpen(path,verb=verb) ):
                print 'SSSleeping in chkIfFileIsOpen nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfFileIsOpen...path: ',path,'still open...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isOpen(path,verb=verb)
            if(verb): print 'chkIfFileIsOpen rc: ',rc

        return(rc)
    
    def loopCmd2(self,cmd,nLoop=5,sLoop=5,ropt='',verb=0):
        rc=runcmd2(cmd,ropt=ropt)
        if(ropt != 'norun' and verb): print '0000-loopCmd2-rc: ',rc
    
        if(rc < 0): 
            print 'EEEE rsync error GGGEEETTTIING INVentory...retry for %d times sleeping %d seconds..'%(nLoop,sLoop)
            for n in range(0,nLoop):
                sleep(sLoop)
                rc=runcmd2(cmd,ropt='')
                if(ropt != 'norun'): print '0000-runcmd2-rc: ',rc
                if(rc >= 0): 
                    return(rc)
        
        if(rc < 0):
            print 'bailing in loopCmd: ',cmd,'nLoop: ',nLoop,' sLoop: ',sLoop
            sys.exit()
        else:
            return(rc)


MF=MFutils()

class DataSet(MFbase):

    from mfbase import ptmpBaseDir
    
    def __init__(self,
                 name='test',
                 version='0.1',
                 dtype='hash',
                 bdir=ptmpBaseDir,
                 unlink=0,
                 verb=0,
                 ):

        self.name=name
        self.version=version
        self.dtype=dtype
        self.bdir=bdir
        self.pyppath="%s/%s.pyp"%(self.bdir,self.name)
        if(unlink):
            try:
                os.unlink(self.pyppath)
            except:
                print 'WWW M.DataSet -- failed to unlink: ',self.pyppath
                
        self.data={}
        self.verb=verb

    def getPyp(self):

        if(self.verb):
            print 'M.DataSet(getPyp): pyppath: ',self.pyppath

        if(os.path.exists(self.pyppath)):
            if(self.verb):  print 'M.DataSet(getPyp): pyppath: ',self.pyppath
            try:
                PS=open(self.pyppath)
                FR=pickle.load(PS)
                PS.close()
                return(FR)
            except:
                print 'WWW M.DataSet.getPyp() error opening: ',self.pyppath,' returning None'
                return(None)

        else:
            return(None)


    def putPyp(self,override=0):


        if(ChkDir(self.bdir,'mk') == -1): sys.exit()

        if(override and os.path.exists(self.pyppath)):
            os.unlink(self.pyppath)
            self.curtime=[]


        if(not(hasattr(self,'curtime'))):
            self.curtime=[]

        self.curtime.append(mf.dtg('dtg.phm'))

        try:
            if(self.verb):  print 'M.DataSet(putPyp): pyppath: ',self.pyppath
            PS=open(self.pyppath,'w')
            pickle.dump(self,PS)
            PS.close()
        except:
            print 'EEEEE unable to pickle.dump: ',self.pyppath
            sys.exit()


    def getData(self):

        return(self.data)



    def putData(self,key,value,verb=1,override=0):

        if(not(hasattr(self,'data'))):
            print 'IIII making data'
            self.data={}

        try:
            haskey=self.data.has_key(key)
        except:
            haskey=0

        try:
            lkey=len(self.data[key])
        except:
            lkey=0


        if(not(haskey) or override or ( lkey != len(value)) ):
            print 'PPPPP adding value to data[key]'
            self.data[key]=value

        else:
            if(verb):  print 'data for key: ',key,' already there'



class DataSets(DataSet):

    from mfbase import ptmpBaseDir

    def __init__(self,bdir=ptmpBaseDir,name='datasets',dtype='model',version='0.1',verb=0,backup=0,unlink=0,
                 unlinkWithRm=0,
                 docp1st=0,
                 doDSsWrite=0,
                 dowriteback=True,
                 doFileLock=0,
                 doMkdir=1,
                 warn=0,
                 chkifopen=0,nminWait=10):

        self.bdir=bdir
        self.name=name
        self.version=version
        self.dtype=dtype
        self.verb=verb
        self.docp1st=docp1st


        if(doDSsWrite and doMkdir):
            if(ChkDir(bdir,'mk') == -1): 
                print 'M.Datasets - cannot mkdir bdir: ',bdir,'bailing...'
                sys.exit()
        else:
            if(not(ChkDir(bdir,'quiet'))):
                print 'M.Datasets - doDSsWrite==0 bdir: ',bdir,'not there, bailing...'
                sys.exit()
                

        path=os.path.join(bdir,name)
        if(os.path.exists(path) and backup):
            cmd="cp %s %s.SAV"%(path,path)
            runcmd(cmd,'')
        elif(os.path.exists(path) and unlink):
            try:
                if(unlinkWithRm):
                    print 'III(M.DataSets rm -v): ',path
                    runcmd("rm -v %s"%(path),'')
                else:
                    # -- use .os to rm...
                    print 'III(M.DataSets unlinking): ',path
                    os.unlink(path)
            except:
                print 'III(M.DataSets unlinking): ',path,' failed because...'


        self.path=path
        self.pathCP=None

        from WxMAP2 import W2adminuSer,W2currentuSer,W2adminuSers

        if(self.docp1st):
            curpid=os.getpid()
            pathCP="%s-%d"%(path,curpid)
            cmd="cp %s %s"%(path,pathCP)
            runcmd(cmd,'')
            path=pathCP
            self.pathCP=pathCP
            print "III M.Dataset.__init__() docp1st from: %s to: %s"%(self.path,self.pathCP) 

        if(chkifopen):
            rc=MF.chkIfFileIsOpen(path,nminWait=nminWait,verb=verb)

        isDSsThere=os.path.exists(path)

        if(not(isDSsThere) and not(doDSsWrite)):
            if(warn): print 'WWW M.Dataset.__init_() -- path: ',path,' not there do not create shelve...doDSsWrite = 0'
            return

        if( ( (W2currentuSer == W2adminuSer) or (W2currentuSer in W2adminuSers) )  and doDSsWrite):

            if(doFileLock):
                self.db=sopen(path,flag='c',writeback=dowriteback)
            else:
                self.db=shelve.open(path,writeback=dowriteback)

        else:
            self.db=shelve.open(path,'r')

        if(verb): print 'DataSets.dbpath: ',path
        self.dbpath=path

    def putDataSet(self,dataset,key,
                   unlinkException=0,
                   verb=0,
                   doDbSync=0,
                   ):

        if(not(hasattr(dataset,'curdtghms'))):
            dataset.curdtghms=[]

        dataset.curdtghms.append(mf.dtg('dtg.hms'))

        if(not(hasattr(self,'putKeys'))): self.putKeys=[]
        self.putKeys.append(key)

        try:
            self.db[key]=dataset
            if(doDbSync): self.db.sync()
            if(verb): print 'PPP putDataSet    putting key: ',key,'   to: %s/%s  dbsync: %d'%(self.bdir,self.name,doDbSync)
            return(0)
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',self.dbpath,' on open/dump exception in putDataSet'
                os.unlink(self.dbpath)
            print 'PPP EEE(M.putDataSet() error in putting key: ',key,'   to: %s/%s'%(self.bdir,self.name)
            print 'PPP WWW press!'
            return(-1)


    def closeDataSet(self,verb=0,warn=0):
        if(hasattr(self,'db')):
            #self.db.sync()  -- not needed; done before close in shelve.py
            self.db.close()
            if(verb):
                print 'M.DataSets.closeDataSet() -- success'
        else:
            if(warn):
                print 'M.DataSets.closeDataSet() -- failed'

    def syncDataSet(self):
        if(hasattr(self,'db')):
            self.db.sync()     


    def getDataSet(self,key,override=0,verb=0,warn=1):

        if(override): return(None)

        try:
            self.db.has_key(key)
        except:
            if(warn): print 'EEE bad dataset in DataSets.getDataSet()...return None key: ',key
            return(None)

        if(self.db.has_key(key)):

            # return None if problem getting pyp from db...
            #pyp=self.db[key]
            #return(pyp)
            try:
                pyp=self.db[key]
                if(self.verb or verb): print 'GGG DataSets.getDataSet() getting key: ',key,' in: %s/%s'%(self.bdir,self.name)
            except:
                if(self.verb or verb): print 'EEE DataSets.getDataSet()     got key: ',key,' problem with unpickling in: %s/%s'%(self.bdir,self.name)
                pyp=None
            return(pyp)
        else:
            if(self.verb or verb): print 'GGG  DataSets.getDataSet()  NNNOOO key: ',key,' in: %s/%s'%(self.bdir,self.name)
            return(None)

    def lsKeys(self):

        kk=self.db.keys()
        kk.sort()
        for k in kk:
            print 'key: ',k

    def getKeys(self):

        kk=self.db.keys()
        kk.sort()
        return(kk)

class W2GaBase(MFbase):
    
    def c(self):
        self._cmd('clear')
        
    def d(self,var):
        rc=self._cmd('d %s'%(var))
        return(rc)
        
    def q(self,var):
        rc=self.query(var)
        return(rc)
        
        
    def getGxout(self):

        self('q gxout')
        g1s=self.rword(2,6)
        g1v=self.rword(3,6)
        g2s=self.rword(4,6)
        g2v=self.rword(5,6)
        stn=self.rword(6,4)
        gxout=gxGxout(g1s,g1v,g2s,g2v,stn)
        return(gxout)


    def getExprStats(self,expr):

        # get the current graphics and rank of display grid
        rank=len(self.coords().shape)
        cgxout=self.getGxout()

        # set gxout to stats; display expression
        self('set gxout stat')
        self('d %s'%(expr))
        cards=self.Lines

        # reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))
        exprstats=gxStats(cards)
        return(exprstats)


    def resetCurgxout(self,cgxout):

        rank=len(self.coords().shape)
        #reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))


    def LogPinterp(self,var,lev,texpr=None,mfact=None,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                if(mfact != None):
                    f2=f2*mfact
                    f1=f1*mfact
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2

                if(texpr == None):
                    expr="(%s(lev=%-6.1f)*%f + %s(lev=%-6.1f)*%f)"%(var,lev1,f1,var,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev1,f1)
                        
                else:
                    expr="(%s(%s,lev=%-6.1f)*%f + %s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1,var,texpr,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1)
                    
                expr=expr.replace(' ','')

                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)



    def LogPinterpTinterp(self,var,lev,tm1=1,tp1=1,tfm1=0.5,tfp1=0.5,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2
                    
                exprm1="( (%s(t-%d,lev=%-6.1f)*%f + %s(t-%d,lev=%-6.1f)*%f)*%f )"%(var,tm1,lev1,f1,var,tm1,lev2,f2,tfm1)
                exprp1="( (%s(t+%d,lev=%-6.1f)*%f + %s(t+%d,lev=%-6.1f)*%f)*%f )"%(var,tp1,lev1,f1,var,tp1,lev2,f2,tfp1)
                expr="(%s + %s)"%(exprm1,exprp1)
                
                expr=expr.replace(' ','')
                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)


class GaLats(W2GaBase):

    prcdir=W2BaseDirPrc
    
    def cmd2(self,gacmd,RcCheck=0):
        self._ga.cmd2(gacmd,Quiet=0,RcCheck=RcCheck)


    def initGrads(self,ga,ge,quiet=1,RcCheck=1):

        #self._cmd=ga.cmd(gacmd='',oRcCheck=RcCheck)
        if(hasattr(ga,'quiet')): quiet=ga.quiet

        if(quiet):
            self._cmd=ga.cmdQ
            ga.__call__=ga.cmdQ
        else:
            self._cmd=ga.cmd

        self._ga=ga
        self._ge=None
        if(ge != None):self._ge=ge

        self.rl=ga.rline
        self.rw=ga.rword

        self.ga=ga
        self.ge=ge

        

    def __init__(self,ga,ge,dtg=None,
                 model='rtfim',
                 center='esrl',
                 comment='grib1 output for tm tracker',
#                 outconv='grads_grib',
                 outconv='grib_only',
                 calendar='standard',
                 ptable=None,
                 frequency='forecast_hourly',
                 timeoption='dim_env',
                 gridtype='linear',
                 btau=0,
                 etau=168,
                 dtau=6,
                 taus=None,
                 regrid=0,
                 remethod='re',
                 smth2d=0,
                 doyflip=0,
                 quiet=0,
                 reargs=None,
                 ):

        if(hasattr(ga,'quiet')): quiet=ga.quiet
        self.initGrads(ga,ge,quiet=quiet)
        self.dtg=dtg
        self.model=model
        self._cmd=self.cmd2
        
        self.frequency=frequency
        
        self.regrid=regrid
        self.remethod=remethod
        self.smth2d=smth2d
        self.doyflip=doyflip
        self.reargs=reargs
                 
        self.area='global'

        self.btau=btau
        self.etau=etau
        self.dtau=dtau

        if(taus == None):
            self.taus=range(btau,etau+1,dtau)
        else:
            self.taus=taus
            #dtau=self.taus[-1]-self.taus[-2]
            # -- base on beginning vice end for models where e.g., dtau = 12 > tau48 (ukm2)
            if(len(taus) > 1):
                dtau=self.taus[1]-self.taus[0]
            else:
                if(dtau != None): dtau=dtau
                else: print 'EEE GaLats dtau == None and len of taus = 1, set dtau in __init__'; sys.exit()
        

        if(ptable == None):
            ptable="%s/hfip/lats.hfip.table.txt"%(self.prcdir),

            
        self("set_lats parmtab %s"%(ptable))
        self("set_lats convention %s"%(outconv))
        self("set_lats calendar %s"%(calendar))
        self("set_lats model %s"%(model))
        self("set_lats center %s"%(center))
        self("set_lats comment %s"%(comment))
        self("set_lats timeoption %s"%(timeoption))
        self("set_lats frequency %s"%(frequency))

        if(self.frequency == 'forecast_hourly'):
            self("set_lats deltat %d"%(dtau))
        elif(self.frequency == 'forecast_minutes'):
            self("set_lats deltat %d"%(dtau*60))

        self("set_lats gridtype %s"%(gridtype))

        if(hasattr(ga,'fh')):
            self.fh=ga.fh
        else:
            print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
            sys.exit()
        
        ge.getFileMeta(self)
        

    def q(self):
        self('query_lats')
        for n in range(1,self._ga.nLines):
            print self._ga.rline(n)

    def create(self,opath):
        self("set_lats create %s"%(opath))
        self.id_file=int(self.rw(1,5))
        

    def basetime(self,dtg):
        yyyy=int(dtg[0:4])
        mm=int(dtg[4:6])
        dd=int(dtg[6:8])
        hh=int(dtg[8:10])
        self("set_lats basetime %d %d %d %d %d 0 0"%(self.id_file,yyyy,mm,dd,hh))
        self.dtg=dtg


    def grid(self,areaObj=None):

        if(self.regrid > 0):
            if(self.remethod == 're2'):
                if(hasattr(self,'reargs') and self.reargs != None):
                    self("vargrid=re2(%s,%s)"%(self.vars[0],self.reargs))
                else:
                    self("vargrid=re2(%s,%5.3f)"%(self.vars[0],self.regrid))
            else:
                self.dlon=self.dlat=self.regrid
                self.nxre=int((360.0-self.regrid)/self.regrid+0.5)+1
                self.nyre=int(180.0/self.regrid+0.5)+1
                
                if(hasattr(self,'reargs') and self.reargs != None):
                    varexpr="vargrid=re(%s,%s)"%(self.vars[0],self.reargs)
                else:
                    varexpr="vargrid=re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(self.vars[0],self.nxre,self.dlon,self.nyre,self.dlat)

                self(varexpr)

        else:
            self("vargrid=%s"%(self.vars[0]))


        latN=latS=lonW=lonE=dLat=dLon=dx=dy=None

        if(areaObj != None):
            latN=areaObj.latN
            latS=areaObj.latS
            lonW=areaObj.lonW
            lonE=areaObj.lonE
            dLat=areaObj.dLat
            dLon=areaObj.dLon
            dx=areaObj.dx
            dy=areaObj.dy
            
        # -- old version of setting up grid
        #

        if(self.area == 'global' and latS == None):
            self("set x 1 %d"%(self.nx))
            self("set y 1 %d"%(self.ny))
            if(self.regrid > 0):
                elon=360.0-self.regrid
                self("set lon 0 %f"%(elon))
                self("set lat -90 90")
                
##         else:
##             return


        # -- new version using areaObj
        #
        if(latS != None and latN != None):
            self("set lat %f %f"%(latS,latN))

        if(lonW != None and lonE != None):

            lon1=lonW
            lon2=lonE
            if(dLon == 360): lon2=lonE-dx
            self("set lon %f %f"%(lon1,lon2))

        if(self.doyflip): self("set yflip on")

        self("lats_grid vargrid")
        self.id_grid=int(self.rw(1,5))


    def plevdim(self,uavars,verb=0):

        plevs=[]
        for uavar in uavars:
            plevs=plevs+uavar[2]

        plevs=mf.uniq(plevs)

        lexpr="set_lats vertdim plev "
        for plev in plevs:
            lexpr="%s %f"%(lexpr,plev)

        if(verb): print 'lllllllllllllll ',lexpr
        self(lexpr)
        self.id_vdim=int(self.rw(1,5))

    def plevvars(self,uavars):

        self.id_uvars={}
        for uavar in uavars:
            if(len(uavar) == 3):
                (name,levtype,levs)=uavar
            elif(len(uavar) == 4):
                (name,levtype,levs,exprs)=uavar
            elif(len(uavar) == 5):
                (name,levtype,levs,mfact,afact)=uavar

            latscmd="set_lats var %d %s %s %d %d"%(self.id_file,name,levtype,self.id_grid,self.id_vdim)
            self(latscmd)
            self.id_uvars[name]=int(self.rw(1,5))

    def sfcvars(self,svars):

        self.id_svars={}
        for svar in svars:
            
            if(len(svar) == 2):
                (name,sfctype)=svar
            elif(len(svar) == 3):
                (name,sfctype,expr)=svar
                
            self("set_lats var %d %s %s %d 0"%(self.id_file,name,sfctype,self.id_grid))
            self.id_svars[name]=int(self.rw(1,5))


    def outvars(self,svars,uavars,verb=0):

        for tau in self.taus:
            vdtg=mf.dtginc(self.dtg,tau)
            gtime=mf.dtg2gtime(vdtg)
            
            self("set time %s"%(gtime))
            if(self.frequency == 'forecast_hourly'):
                self("set_lats fhour %f "%(tau))
            elif(self.frequency == 'forecast_minutes'):
                self("set_lats fminute %f "%(tau*60))

            
            for uavar in uavars:
                
                rc=uavar
                doregular=0
                doexpr=0
                mfact=None
                afact=None
                dofact=0
                
                if(len(rc) == 3):
                    (name,uatype,levs)=rc
                    doregular=1
                    
                elif(len(rc) == 4):
                    (name,uatype,levs,exprs)=rc
                    if(not(type(exprs) is ListType)):
                        print 'simple expression exprs: ',exprs
                        doregular=1
                        doexpr=1
                        
                elif(len(rc) == 5):
                    (name,uatype,levs,mfact,afact)=rc
                    doregular=1
                    dofact=1
                        
                
                if(doregular):
                    
                    id=self.id_uvars[name]
    
                    for lev in levs:
                        self("set_lats write %d %d %f"%(self.id_file,self.id_uvars[name],lev))
                        self("set lev %f"%(lev))
                        if( (name == 'ta' or name == 'tmpp') and lev == 401):
                            expr="(vint(const(%s,500,-a),%s,300)/vint(const(%s,500,-a),const(%s,1,-a),300))"%(name,name,name,name)
                            if(verb): print 'vint expr: ',expr 
                        else:
                            if(lev in self.levs):
                                if(doexpr):
                                    expr=exprs
                                else:
                                    expr=name
                                if(dofact and mfact != None):
                                    expr="%s*%f"%(expr,mfact)
                            else:
                                if(verb): print 'IIII dooohhh!  ',lev,' not in: y',self.levs,' do ln(p) interp...for: ',name
                                if(doexpr):
                                    expr=self.LogPinterp(exprs,lev,mfact=mfact)
                                else:
                                    expr=self.LogPinterp(name,lev,mfact=mfact)
                                if(verb): print 'IIII lev: ',lev,' expr: ',expr
                                
                        if(self.regrid > 0):
                            
                            if(self.remethod == 're2'):
                                if(hasattr(self,'reargs') and self.reargs != None):
                                    expr="re2(%s,%s)"%(expr,self.reargs)
                                else:
                                    expr="re2(%s,%5.3f)"%(expr,self.regrid)
                            else:
                                if(hasattr(self,'reargs') and self.reargs != None):
                                    expr="re(%s,%s)"%(expr,self.reargs)
                                else:
                                    expr="re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(expr,self.nxre,self.dlon,self.nyre,self.dlat)
    
                        if(self.smth2d > 0):
                            expr="smth2d(%s,%d)"%(expr,self.smth2d)
    
                        self("lats_data %s"%(expr))
                        if(verb):
                            for n in range(1,self._ga.nLines):
                                print self._ga.rline(n)
                else:
                    
                    id=self.id_uvars[name]
                    
                    for lev in levs:
                        self("set_lats write %d %d %f"%(self.id_file,self.id_uvars[name],lev))
                        expr=exprs[levs.index(lev)] 
                        self("lats_data %s"%(expr))
                        if(verb):
                            for n in range(1,self._ga.nLines):
                                print self._ga.rline(n)
                    

            for svar in svars:
                
                sfcexpr=None
                if(len(svar) == 2):
                    (name,sfctype)=svar
                elif(len(svar) == 3):
                    (name,sfctype,sfcexpr)=svar
                    
                id=self.id_svars[name]

                self("set_lats write %d %d 0"%(self.id_file,self.id_svars[name]))
                
                expr=name
                if(sfcexpr != None): expr=sfcexpr

                if(self.regrid > 0):
                        
                    if(self.remethod == 're2'):
                        if(hasattr(self,'reargs') and self.reargs != None):
                            expr="re2(%s,%s)"%(expr,self.reargs)
                        else:
                            expr="re2(%s,%5.3f)"%(expr,self.regrid)
                    else:
                        if(hasattr(self,'reargs') and self.reargs != None):
                            expr="re(%s,%s)"%(expr,self.reargs)
                        else:
                            expr="re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(expr,self.nxre,self.dlon,self.nyre,self.dlat)

                if(self.smth2d > 0):
                    expr="smth2d(%s,%d)"%(expr,self.smth2d)

                self("lats_data %s"%(expr))
                if(verb):
                    for n in range(1,self._ga.nLines):
                        print self._ga.rline(n)


    def close(self):

        self("set_lats close %d"%(self.id_file))

                

    
    __call__=cmd2



class GaLatsQ(GaLats):

    def cmd2(self,gacmd,RcCheck=0):
        self._ga.cmd2(gacmd,Quiet=1,RcCheck=RcCheck)

    __call__=cmd2
        


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# runGrads

class runGrads(MFutils):


    gradscmd='''grads -Hlc'''


    def __init__(self,files,gsprc='',verb=0,filetype=''):

        if(type(files) != ListType): files=[files]

        print 'files: ',files
        gs="""function main(args)
# prelims:

rc=gsfallow('on')
rc=const()"""

        gaopencmd='open'
        if(filetype == 'xdf'): gaopencmd='xdfopen'
        if(filetype == 'sdf'): gaopencmd='sdfopen'

        for file in files:
            gs="""%s
print 'opening: %s'
'%s %s'
"""%(gs,file,gaopencmd,file)

        gs="""%s
%s
"""%(gs,gsprc)


        gspath='/tmp/runGrads.gs'
        self.WriteString2File(gs,gspath)
        cmd='''%s "%s" -g 1024x768-30'''%(self.gradscmd,gspath)
        os.system(cmd)







#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline

class CmdLine(MFutils):

    def __init__(self,argv=sys.argv):

        self.argv=argv

        self.argopts={
            'dtgopt': 'no default',
            'model': 'no default',
        }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'source':['S:','rtfim','a','source'],
        }

        self.defaults={
            'zy0x1w2':0,
            'zy0x1w2y3':'test'
        }

        self.purpose='''
purpose -- to boldly go, where no man has gone before!'''

        self.examples='''
%s test
'''

    def initDoc(self):

        argdoc="%s "

        optdoc='''
plain args:'''
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            val=self.argopts[n][1]
            argdoc="%s %s"%(argdoc,key)
            optdoc=optdoc+'''
  %-20s - %s'''%(key,val)



        argdoc=argdoc+' ['
        optdoc=optdoc+'''

switches:'''
        kk=self.options.keys()
        kk.sort()
        for k in kk:
            oo=self.options[k]
            argdoc="%s -%s"%(argdoc,oo[0][0])
            optdoc=optdoc+'''
  -%1s :: %s=[%s] %s'''%(oo[0][0],k,oo[1],oo[3])


        argdoc=argdoc+' ]'

        exampledoc="""
Example(s):%s"""%(self.examples)

        purposedoc="""
Purpose:%s"""%(self.purpose)

        self.__doc__="""%s
%s
%s
%s
"""%(argdoc,optdoc,purposedoc,exampledoc)



    def initFlagOpts(self):

        self.flagOpts=''
        vv=self.options.values()
        for v in vv:
            self.flagOpts=self.flagOpts+v[0]


    def initArgOpts(self):

        narg=len(self.argopts)

        if(narg == 0):
            estr="self.istart=%d"%(narg+1)
            exec(estr)
            return

        for n in range(1,narg+1):

            key=self.argopts[n][0]
            val=self.argopts[n][1]

            if(n == 1):
                estr="self.%s=self.argv[%d]"%(key,n)
                exec(estr)
                estr="self.istart=%d"%(n+1)
                exec(estr)
            else:
                exec("if(self.narg > %d): self.%s=self.argv[%d]"%(n-1,key,n))
                exec("self.istart=%d"%(n+1))


    def getFlagOpts(self):

        self.foptions={}
        for o, a in self.opts:
            for k in self.options.keys():
                oo=self.options[k]
                if(o == "-%s"%(oo[0][0])):
                    if(oo[2] == 'a'):
                        self.foptions[k]=a
                    elif(oo[2] == 'i'):
                        self.foptions[k]=int(a)
                    elif(oo[2] == 'f'):
                        self.foptions[k]=float(a)
                    else:
                        self.foptions[k]=oo[2]

        for k in self.options.keys():
            if(not(self.foptions.has_key(k))):
                self.foptions[k]=self.options[k][1]


    def setFlagOpts(self):

        self.estrFlag=''
        for k in self.foptions.keys():
            if(type(self.foptions[k]) == StringType):
                estr="%s='%s'"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == IntType):
                estr="%s=%d"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == FloatType):
                estr="%s=%g"%(k,self.foptions[k])
            elif(self.foptions[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrFlag="%s%s\n"""%(self.estrFlag,estr)


    def setArgOpts(self):

        self.estrArg=''
        istart=1
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            try:
                exec("kk=self.%s"%(key))
            except:
                print "!!!!"
                print "!!!!EEE CmdLine.setArgOpts: need to set the plain arg n: ",n,' key: ',key,' !!!!'
                print "!!!!"
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                sys.exit()
            estr="%s='%s'"%(key,kk)
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrArg="%s%s\n"""%(self.estrArg,estr)


    def setDefaults(self):

        self.estrDefaults=''
        try:
            self.defaults.keys()
        except:
            return
        for k in self.defaults.keys():
            if(type(self.defaults[k]) == StringType):
                estr="%s='%s'"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == IntType):
                estr="%s=%d"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == FloatType):
                estr="%s=%g"%(k,self.defaults[k])
            elif(self.defaults[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrDefaults="%s%s\n"""%(self.estrDefaults,estr)

    def CmdLine(self,blankPlainArgs=0):

        self.blankPlainArgs=blankPlainArgs

        self.initFlagOpts()
        self.initDoc()

        self.curpid=os.getpid()
        self.curdtg=mf.dtg()
        self.curphr=mf.dtg('phr')
        self.curdir=os.getcwd()
        self.curyear=self.curdtg[0:4]
        self.curtime=mf.dtg('curtime')

        (self.tttdtg,self.curphr)=mf.dtg_phr_command_prc(self.curdtg) 

        self.pypath=self.argv[0]
        self.abspypath=os.path.abspath(self.pypath)
        (self.pydir,self.pyfile)=os.path.split(self.abspypath)

        self.estrCur="""curdtg='%s'\ncurphr='%s'\ncuryear='%s'\ncurtime='%s'\ncurdir='%s'\n"""%(self.curdtg,
                                                                                                self.curphr,
                                                                                                self.curyear,
                                                                                                self.curtime,
                                                                                                self.curdir,
                                                                                                )

        self.estrCur="""%s\npydir='%s'\npypath='%s'\npyfile='%s'\n"""%(self.estrCur,self.pydir,self.pypath,self.pyfile)

        gspath=os.path.abspath(self.pypath)
        (base,ext)=os.path.splitext(gspath)
        self.gspath=base+'.gs'

        self.narg=len(self.argv)-1

        if(self.narg >= 1 and not(self.blankPlainArgs)):

            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError, e:
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print
                print "EEE"
                print """EEE invalid getopt opt error: '%s'"""%(e)
                print "EEE"
                print
                sys.exit(2)

            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur



        # -- 20111023 -- tried allowing blank plain args -- need to rewrite the whole section
        #

        elif(self.blankPlainArgs):


            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError:
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print "EEE invalid getopt opt"
                sys.exit(2)


            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.nargsFlag=len(self.opts)

            print '0000000000000000000 ',self.narg,self.nargsFlag
            print '1111111111111111111 ',self.estrArg
            print '2222222222222222222 ',self.opts,self.args
            print '3333333333333333333 ',self.nargsFlag,self.estrFlag,self
            print '4444444444444444444 ',self.estrCur
            print '5555555555555555555 ',self.estrDefaults
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur


        else:
            usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
            sys.exit(1)


    
class LsDiagFile(MFutils):
    
    sfcLevel='surf'
    model='era5'

    stmVarNameByIndex={

        1:'latitude',
        2:'longitude',
        3:'max_wind',
        4:'rms',
        5:'min_slp',
        6:'shr_mag',
        7:'shr_dir',
        8:'stm_spd',
        9:'stm_hdg',
        10:'sst',
        11:'ohc',
        12:'tpw',
        13:'land',
        14:'850tang',
        15:'850vort',
        16:'200dvrg',
    }


    customVarNameByIndex={
        1:'ADECK  VMAX (KT)',
        2:'DIAG   VMAX (KT)',
        #3:'ADECK  PMIN (MB)',
        3:'precip',             # -- use psl into jtdiag table
        4:'DIAG   PMIN (MB)',
        5:'sstanom',
        6:'precip-actual',
        7:'PR  ASYM/TOT (%)',
        8:'TOTSHR MAG  (KT)',
        9:'SHR/TOTSHR   (%)',
        10:'SHR ASYM/TOT (%)',
        11:'CPS  B(AROCLINC)',
        12:'CPS   VTHERM(LO)',
        13:'CPS   VTHERM(HI)',
        14:'POCI        (MB)',
        15:'ROCI        (KM)',
        16:'R34mean     (KM)',
        17:'R50mean     (KM)',
        18:'R64mean     (KM)',
    }


    def __init__(self,dtg,
                 lsdiagpath,
                 verb=0,
                 dobail=0,
                 quiet=1,
                 ):

        self.dtg=dtg
        self.lsdiagpath=lsdiagpath
        self.sbtProdDir=sbtProdDir
        self.verb=verb
        self.dobail=dobail

        self.year=dtg[0:4]
        
        wdir=sbtProdDir
        dtgdir="%s/%s"%(self.year,dtg)
        urldir="%s/%s"%(dtgdir,self.model)
        pltdir="%s/%s"%(wdir,urldir)
        
        self.pltdir=pltdir
        self.tbdir=tsbdbdir
        self.tdir="%s/%s/%s/%s"%(self.tbdir,self.year,dtg,self.model)
        
        
    
    def parseDiag(self,stmid,dobail=1,verb=0):
        """ parse output from lsdiag.x
        """


        def makekey(label):
            tt=label.lower().split()
            nlabel=tt[0]
            ne=-1
            if(nlabel == 'cps'): ne=0
            for n in range(1,len(tt)+ne):
                nlabel="%s_%s"%(nlabel,tt[n])

            nlabel=nlabel.replace(')','')
            nlabel=nlabel.replace('(','')

            return(nlabel)

        lsdiagpath=self.lsdiagpath

        # -- check if SHEM storm
        #
        stmIsShem=0
        if(isShemBasinStm(stmid)): stmIsShem=1
        
        rc=1
        # -- stm vars
        #
        self.stmData={}
        self.stmDataVars={}
        self.cstmData={}
        self.stmLabels={}
        
        # -- custom vars
        #
        self.customData={}
        self.ccustomData={}
        self.customLabels={}

        # -- snd vars
        #
        self.sndData={}
        self.sndDataVar={}
        self.sndPlevs=[]
        self.sndKeys=[]
        self.csndData={}
        self.sndLabels={}
        
        self.diagVals={}
        self.diagTypes={}
        self.diaguRls={}
        self.diagKeys=[]
        self.diagFilenames={}

        self.diagTaus=[]
        self.urlData={}


        self.nstmvars=16
        self.nsndvars=5

        self.curstmid=stmid


        gotstm=0
        gotusr=0
        gotsnd=0
        try:
            cards=open(lsdiagpath).readlines()
        except:
            print """WWW TCDiag.parseDiag couldn't read file: %s"""%(lsdiagpath)
            return(0)

        if(len(cards) == 0):
            print """WWW TCDiag.parseDiag file: %s is 0 length"""%(lsdiagpath)
            return(0)

        for n in range(0,len(cards)):
            if(gotstm and gotusr and gotsnd): break
            card=cards[n]
            if(n == 0 and find(card,'*')):
                tt=card.split()
                aid=tt[1]
                dtg=tt[2]

            if(n == 1 and find(card,'*')):
                tt=card.split()
                stm2id=tt[1]
                stmname=tt[2]

            if(find(card,'STORM') and gotstm == 0):
                gotstm=1
                n=n+1
                card=cards[n]
                if(find(card,'NTIME')):
                    tt=card.split()
                    ntau=int(tt[1])
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for i in range(0,ntau):
                        self.diagTaus.append(int(tt[i]))

                    if(self.verb): print 'self.diagTaus: ',self.diagTaus


                for i in range(0,self.nstmvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        if(find(card,'LAT') or find(card,'LON')):
                            val=float(tt[j])
                        else:
                            # -- convert rel vort to cyclonic vort
                            #
                            ival=int(tt[j])
                            if(find(label,'850VORT') and stmIsShem): ival=-1*ival
                            val=ival
                        self.stmData[tau,i+1]=val
                        self.cstmData[tau,i+1]=tt[j]
                        self.stmLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(find(card,'CUSTOM') and gotusr == 0):
                gotusr=1
                n=n+1
                card=cards[n]
                self.ncustomvars=int(card.split()[1])
                n=n+1
                for i in range(0,self.ncustomvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        val=int(tt[j])
                        self.customData[tau,i+1]=val
                        self.ccustomData[tau,i+1]=tt[j]
                        self.customLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(find(card,'SOUNDING') and gotsnd == 0):
                gotsnd=1
                n=n+1
                card=cards[n]
                self.nlevs=int(card.split()[1])
                n=n+1
                for i in range(0,self.nlevs):
                    for ii in range(0,self.nsndvars):
                        n=n+1
                        card=cards[n]
                        label=card[0:16]
                        label=label.replace('/','_')
                        tt=card[16:].split()

                        var=label.split()[0].split('_')[0]
                        var=var.lower()

                        plev=label.split()[0].split('_')[-1]
                        plev=plev.lower()
                        if(plev == self.sfcLevel):
                            ilev=plev
                        else:
                            ilev=int(plev)

                        self.sndPlevs.append(plev)
                        for j in range(0,ntau):
                            tau=self.diagTaus[j]
                            val=int(tt[j])
                            self.sndDataVar[tau,var,ilev]=val
                            self.sndData[tau,ii+1,i+1]=val
                            self.csndData[tau,ii+1,i+1]=tt[j]
                            self.sndLabels[ii+1,i+1]=label

                self.sndPlevs=uniq(self.sndPlevs)

        if(self.verb > 1):

            for i in range(0,self.nlevs):
                for ii in range(0,self.nsndvars):
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        print 'ssss(parseDiag) ',tau,self.csndData[tau,ii+1,i+1],self.sndData[tau,ii+1,i+1]





        #ppp -- glob for fields plots to set urlData
        #

        pltpaths=[]
        tpltpaths=glob.glob("%s/*.png"%(self.pltdir))

        for tp in tpltpaths:
            if(not(find(tp,'trkplt')) and not(find(tp,'bm.'))): pltpaths.append(tp)

        for p in pltpaths:
            (dir,file)=os.path.split(p)
            tt=file.split('.')
            pltkey=tt[0]
            pltstm="%s.%s"%(tt[1],tt[2])
            plttau=int(tt[-2])

            # -- match the stmid to plot
            #
            if(pltstm == stmid):
                urlpath="%s/%s/%s/%s"%(self.year,self.dtg,self.model,file)
                MF.set2KeyDictList(self.urlData,plttau,pltkey,urlpath)


        #lll -- load diagVals,diagKeys,diagFilenames
        # storm

        if(self.verb): print
        for i in range(1,self.nstmvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.stmData[tau,i]
                cval=self.cstmData[tau,i]
                label=self.stmLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    cstmkey=makekey(label)
                    if(not(cstmkey in self.diagKeys)):
                        self.diagKeys.append(cstmkey)
                    self.diagFilenames[cstmkey]="%s.%s"%(cstmkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ssstttmmmmm %2d     %-15s %6.0f'%(i,cstmkey,val)

                MF.set2KeyDictList(self.diagVals,tau,cstmkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,cstmkey,'storm')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,self.urlData[tau][cstmkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, cstmkeky: ',tau,cstmkey,self.urlData[tau][cstmkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,'None')


        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # custom

        if(self.verb): print
        for i in range(1,self.ncustomvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.customData[tau,i]
                cval=self.ccustomData[tau,i]
                label=self.customLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    ccustomkey=makekey(label)
                    if(not(ccustomkey in self.diagKeys)):
                        self.diagKeys.append(ccustomkey)
                    self.diagFilenames[ccustomkey]="%s.%s"%(ccustomkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ccccccccccc %2d     %-15s %6.0f'%(i,ccustomkey,val)

                MF.set2KeyDictList(self.diagVals,tau,ccustomkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,ccustomkey,'custom')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,self.urlData[tau][ccustomkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, ccustomkey: ',tau,ccustomkey,self.urlData[tau][ccustomkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,'None')

        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # sounding

        if(self.verb): print
        for i in range(1,self.nlevs+1):
            for ii in range(1,self.nsndvars+1):
                for j in range(0,ntau):
                    tau=self.diagTaus[j]
                    val=self.sndData[tau,ii,i]
                    cval=self.csndData[tau,ii,i]
                    label=self.sndLabels[ii,i]
                    if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                        csndkey=makekey(label)
                        if(not(csndkey in self.diagKeys)):
                            self.diagKeys.append(csndkey)
                        self.diagFilenames[csndkey]="%s.%s"%(csndkey,stmid)

                    MF.set2KeyDictList(self.diagVals,tau,csndkey,cval)
                    MF.set2KeyDictList(self.diagTypes,tau,csndkey,'sounding')

                    if(j == 0 and self.verb > 1):
                        print 'sssdddnnngg %2d %2d  %-15s %6.0f'%(ii,i,csndkey,val)

                    try:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,self.urlData[tau][csndkey])
                        if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, csndkey: ',tau,csndkey,self.urlData[tau][csndkey]
                    except:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,'None')

        if(self.verb): print
        for kk in self.diagKeys:
            card=kk
            for tau in self.diagTaus:
                card="%15s %5s"%(card,self.diagVals[tau][kk])
            if(self.verb): print 'parseDiag:',card

        # -- set the taus
        #
        self.taus=self.diagTaus

        return(rc)




class Mdeck3(MFutils):
    

    def __init__(self,
                 tbdir=None,
                 oyearOpt=None,
                 verb=0,
                 doclean=0,
                 stmdtg=None,
                 basinopt=None,
                 doBT=0,
                 doWorkingBT=0,
                 quiet=1,
                 doSumOnly=0,
                 ):
        

        if(not(quiet)): self.sTimer('md3-init')
        self.verb=verb
        self.doBT=doBT
        
        if(tbdir == None):
            tbdir=sbtSrcDir
            tbdir=sbtVerDir
            tbdir=sbtVerDirDat
            tbdir=sbtRoot

        self.tbdir=tbdir
        
        if(oyearOpt == None):
            oyearOpt='%s-%s'%(bm3year,em3year)
            
        oyearOpt="%s"%(oyearOpt)
        self.oyearOpt=oyearOpt

        # -- (allCvsPath) = md3 track cards with data by storm and dtg
        # -- (sumCvsPath) = md3 storm summary cards 
        #
        rc=self.getCvsYearPaths(doBT=doBT)
        (allCvsPath,sumCvsPath)=rc
        if(verb):
            print 'allCvsPath: ',allCvsPath
            print 'sumSvsPath: ',sumCvsPath

        # -- get hashes with storm summary and names
        #
        stmSum={}
        tcNamesHash={}
        scards=open(sumCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            tt=scard.split(',')
            stmid=tt[0]
            ss=stmid.split(".")
            year=ss[1]
            b3id=ss[0]
            tccode=tt[1]
            tcdev=tt[2]
            name=tt[3]
            tcNamesHash[(year,b3id)]=name
            stmSum[stmid]=tt
            
        self.stmSum=stmSum
        self.tcNamesHash=tcNamesHash
        
        stmMetaMd3={}
        stmMetaMd3Card={}
        
        if(not(doSumOnly)):
            dtgMd3={}
            stmMd3={}
            
            # -- get the md3 track
            #
            acards=open(allCvsPath).readlines()
            #print 'aaa',allCvsPath
            for acard in acards[1:]:
                # -- the last entry has '\n' skip
                tt=acard.split(',')
                dtg=tt[0]
                stmid=tt[1]
                MF.appendDictList(dtgMd3, dtg, stmid)
                MF.appendDictList(stmMd3, stmid, tt[0:-1])
            

            dtgMd3=MF.uniqDict(dtgMd3)
            md3dtgs=dtgMd3.keys()
            md3dtgs.sort()
            self.md3dtgs=md3dtgs
            self.dtgMd3=dtgMd3
            md3stmids=stmMd3.keys()
            md3stmids.sort()
            self.md3stmids=md3stmids
            self.stmMd3=stmMd3


        # -- get the summary cards with stmid meta data
        #
        acards=open(sumCvsPath).readlines()
        for acard in acards[1:]:
            #print 'sss',acard
            tt=acard.split(',')
            stmid=tt[0]
            #print 'sss',stmid,tt[-1]
            # skip the last entry which is always '\n'
            stmMetaMd3[stmid]=tt[0:-1]
            stmMetaMd3Card[stmid]=acard[0:-1]

        # -- decorate
        #
        self.stmMetaMd3=stmMetaMd3
        self.stmMetaMd3Card=stmMetaMd3Card
        
        if(not(quiet)): self.dTimer('md3-init')

    def getMd3Stmids(self,stmopt,yearopt=None,dobt=0,dofilt9x=0,verb=0):
        
        # -- like tcnames hash
        #
        tcnames=self.tcNamesHash.keys()
    
        def getBnum1and2(bnum1,bnum2):
            
            try:
                bnum1=int(bnum1)
            except:
                bnum1=str(bnum1)
     
            try:
                bnum2=int(bnum2)
            except:
                bnum2=str(bnum2)
                
            return(bnum1,bnum2)
     
        
        # -- get years
        #
        def getyears(yyy):
        
            if(yyy == 'cur'):
                curdtg=mf.dtg()
                yyy=curdtg[0:4]
        
            years=[]
            n1=0
            n2=0
        
            tt0=yyy.split('-')
            tt1=yyy.split(',')
        
            if(len(tt1) > 1):
                for tt in tt1:
                    yyyy=add2000(tt)
                    years.append(yyyy)
                return(years)
        
            if(len(tt0) > 1):
                y1=tt0[0]
                y2=tt0[1]
                yyyy1=add2000(y1)
                yyyy2=add2000(y2)
        
                if(len(yyyy1) != 4 or len(yyyy2) != 4):
                    print 'EEEE getyears tt:',tt
                    return(None)
        
                else:
                    n1=int(yyyy1)
                    n2=int(yyyy2)
                    for n in range(n1,n2+1):
                        years.append(str(n))
        
            else:
                if(len(yyy) <= 2): yyy=add2000(yyy)
                years=[yyy]
        
            return(years)
        
        
        # -- get stmids by filtering from master list
        #
        def getstmids(sss,year,dos3id=0,dofilt9x=dofilt9x):
        
            sids=[]
            n1=0
            n2=0
            tt=sss.split('-')
            
            if(len(tt) > 1):
                
                if(len(tt[0]) != 2 or len(tt[1]) != 3):
                    print 'EEEE getstmids tt:',tt
                    return(None)
        
                else:
                    n1=int(tt[0])
                    n2=int(tt[1][0:2])
                    bid=tt[1][2].upper()
        
                    for n in range(n1,n2+1):
                        sss="%02d%1s"%(n,bid)
                        sid="%s.%s"%(sss,year)
                        sid=getstmids(sss,year,dos3id=1)
                        sids.append(sid[0])
                        
        
            elif(len(sss) == 1 or dos3id):
        
                doChkNum=0
                doChk9x=0
    
                if(dos3id and len(sss) == 3):
                    
                    bchk=sss[-1].upper()
                    bnum=sss[0:2]
                    bnum1=sss[0]
                    bnum2=sss[1]
                    
                    try:
                        bnum=int(bnum)
                        if(bnum >= 1 and bnum <=70):
                            bnum="%02d"%(bnum)
                            doChkNum=1
                        elif(bnum >= 90):
                            doChkNum=0
                        else:
                            print 'WWW -- invalid bnum in getstmids'
                            sys.exit()
                    except:
                        bnum=str(bnum)
    
    
                    (bnum1,bnum2)=getBnum1and2(bnum1, bnum2)
    
                    if(type(bnum1) is StringType or 
                       (type(bnum1) is IntType and (bnum1 >= 0 and bnum2 <=9)) or
                       (type(bnum2) is StringType and bnum2 == 'X')
                       ):
                        doChk9x=1
                        
                    #print 'aaaaaaa',bchk,bnum,type(bnum),bnum1,type(bnum1),bnum2,type(bnum2),doChkNum,doChk9x
                        
                else:
                    bchk=sss.upper()
                    
        
                for tcname in tcnames:
                    # -- improved subbasin checking...
                    #
                    tcyear=tcname[0]
                    tcb3id=tcname[1].upper()
                    tcstmid="%s.%s"%(tcb3id,tcyear)
                    tcnum=tcb3id[0:2]
                    tcbnum1=tcnum[0]
                    tcbnum2=tcnum[1]
                    (tcbnum1,tcbnum2)=getBnum1and2(tcbnum1,tcbnum2)
                    
                    
                    tc9X=tcb3id[1]
                    tcsubbasin=tcb3id[2:3]
                    
                    chk0=(tcyear == year)
                    chk1=(tcsubbasin == bchk)
                    chk2=0
                    chk3=0
                    if(bchk == 'H'): chk3=(isShemBasinStm(tcsubbasin) and isShemBasinStm(bchk))
                    if(bchk == 'I'): chk2=(isIOBasinStm(tcsubbasin) and isIOBasinStm(bchk))
                    
                    # -- first check year only
                    #
                    if(chk0):
                        
                        if(doChkNum): 
                            chknum=(str(bnum) == tcnum)
                            chkb=((chk1 or chk2 or chk3) and chknum)
                            
                        elif(doChk9x):
                            
                            chk90=(type(bnum1) is IntType and bnum1 == 9 and type(tcbnum1) is StringType)
    
                            chk91=(type(bnum1) is StringType and type(tcbnum1) is StringType and
                                   (bnum1 == tcbnum1))
                            chk92=(type(bnum2) is IntType and type(tcbnum2) is IntType and
                                   (bnum2 == tcbnum2))
                            
                            chk93=(type(bnum1) is IntType and bnum1 == 9 and 
                                   type(bnum2) is StringType and bnum2 == 'X' and
                                   not(IsNN(tcstmid)))
                            
                            chk9a=(chk90 and chk92) 
                            chk9b=(chk91 and chk92)
                            chk9c=(chk93)
                            chkb=((chk1 or chk2 or chk3) and (chk9a or chk9b or chk9c) )
            
                        else:
                            chkb=(chk1 or chk2 or chk3)
                        
                        if(chkb):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None
                        
        
            else:
                print 'EEEE getstmids sss:',sss
                return(None)
        
        
            sids.sort()
            osids=sids
            if(dobt):
                osids=[]
                for sid in sids:
                    if(IsNN(sid)): osids.append(sid)
                    
            return(osids)
    
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        curdtg=mf.dtg()
        curyear=curdtg[0:4]
        
    
        # -- defaults
        #
        if(stmopt == None):
        
            sopt='w,e,c,l,i,a,b,p,s'
            if(yearopt == None):
                yopt='cur'
            else:
                yopt=yearopt
            years=getyears(yopt)
        
        # -- by stmopt
        #
        elif(stmopt != None and stmopt != 'all'):
            
            ttt=stmopt.split('-')
            ttc=stmopt.split(',')
            tt=stmopt.split('.')
            
            #print 'sssssssssssssss',stmopt,len(ttt),len(ttc),len(tt)
            
            if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
                if(len(tt[0]) == 3):
                    stmid=tt[0][2]
                elif(len(tt[0]) != 1):
                    print 'tcVM.MakeStmList() EEEE bad stm3id: tt:',tt,'ttt: ',ttt,'ttc: ',ttc,'stmopt: ',stmopt
                    sys.exit()
                else:
                    stmid=tt[0]
        
                if(isShemBasinStm(stmid)):
                    stmyear=getShemYear(curdtg)
                else:
                    stmyear=curyear
        
                if(isIOBasinStm(stmid)):
                    stmyear=curyear
                    
                stmyear=add2000(stmyear)
        
                stmopt=stmopt+'.'+stmyear
                tt=stmopt.split('.')
                
            # -- stm spanning using current year
            #
            elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):
                stmids=getstmids(stmopt,curyear,dos3id=1,dofilt9x=dofilt9x)
                return(stmids)
        
            # -- list of individual stmid (sss.y)
            #
            if(len(ttc) > 1):
        
                stmids=[]
                for stmopt in ttc:
                    stmids=stmids+self.getMd3Stmids(stmopt,self.tcNamesHash,dobt=dobt,dofilt9x=dofilt9x,
                                              verb=verb)
        
                return(stmids)
        
        
            if(len(ttc) > 1 and len(tt) > 2):
        
                stmids=[]
        
                for stmid in ttc:
                    ss1=stmid.split('.')
                    if(len(ss1) != 2):
                        print 'EEE invalid individual stm: ',stmid
                        sys.exit()
        
                    sid=ss1[0]
                    yid=ss1[1]
                    if(len(yid) >= 1): yid=add2000(yid)
                    rc=getstmids(sid,yid,dofilt9x)
                    stmids=stmids+rc
        
                return(stmids)
        
            sopt=tt[0]
            yopt=tt[1]
            years=getyears(yopt)
        
        else:
        
            sopt='w,e,c,l,i,a,b,p,s'
            if(yearopt == None):
                yopt='cur'
            else:
                yopt=yearopt
            years=getyears(yopt)
        
        
        if(verb):
            print 'getMd3Stmids sopt: ',sopt
            print 'getMd3Stmids yopt: ',yopt,years
        
        
        stmids=[]
        
        for year in years:
        
            sopt=sopt.upper()
            ss=sopt.split(',')
            
            if(len(ss) > 1):
                for sss in ss:
                    rc=getstmids(sss,year,dofilt9x=dofilt9x)
                    if(rc != None):
                        stmids=stmids+rc
        
            else:
                stmopt="%s.%s"%(sopt,year)
                rc=getstmids(sopt,year,dos3id=1,dofilt9x=dofilt9x)
                if(rc != None):
                    stmids=stmids+rc
        
        #  -- filter out 9X
        #
        if(dofilt9x):
            nstmids=[]
            for stmid in stmids:
                (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid,convert9x=1)
                if(snum >= 90):
                    nstmids.append(stmid)
        
            stmids=nstmids
        
        
        if(verb):
            for stmid in stmids:
                print 'getMd3Stmids stmid: ',stmid
        
        return(stmids)
    
    def getCvsYearPaths(self,doBT=0):
        """
not sure about this...MRG has BT .csv has working best track
always use all-BT because m-md3-all-cpy does a merge process
that generates of -MRG.txt where the working is updated with BT
        """
        if(doBT == -1):
            allCvsPath="%s/all-md3-%s.csv"%(self.tbdir,self.oyearOpt)
            sumCvsPath="%s/sum-md3-%s.csv"%(self.tbdir,self.oyearOpt)
        else:
            allCvsPath="%s/all-md3-%s-MRG.csv"%(self.tbdir,self.oyearOpt)
            sumCvsPath="%s/sum-md3-%s-MRG.csv"%(self.tbdir,self.oyearOpt)
    
        return(allCvsPath,sumCvsPath)

    
    def getCvsYearOptPaths(self,tbdir,oyearOpt,headAll,headSum):
        
        
        allCvsPath=allCvsPathBT=sumCvsPath=sumCvsPathBT=None
        
        allCvsPath="%s/all-md3-%s.csv"%(self.tbdir,oyearOpt)
        allCvsPathBT="%s/all-md3-%s-BT.csv"%(self.tbdir,oyearOpt)
        sumCvsPath="%s/sum-md3-%s.csv"%(self.tbdir,oyearOpt)
        sumCvsPathBT="%s/sum-md3-%s-BT.csv"%(self.tbdir,oyearOpt)
            
        return(allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)
    
    def getBasin4b1id(self,b1id):
        ib1id=b1id.lower()
        if(ib1id == 'l'):
            basin='lant'
        elif(ib1id == 'w'):
            basin='wpac'
        elif(ib1id == 'e' or ib1id == 'c'):
            basin='epac'
        elif(ib1id == 'i' or ib1id == 'b' or ib1id == 'a'):
            basin='io'
        elif(ib1id == 'h' or ib1id == 's' or ib1id == 'p'):
            basin='shem'
        else:
            print 'EEE in getBasin4b1id b1id: ',b1id
            sys.exit()
            
            
        return(basin)
            
    
    def parseStmSumCard(self,card):
        
        tt=card.split(",")
        tstmid=tt[0]
        sname=tt[3]
        bdtg=tt[9]
        edtg=tt[10]
        stm9x=tt[22]
        t2gen=tt[23]
        dtggen=tt[24].strip()
        rc=(tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)
        return(rc)
        
    
    def getTcData(self,year,basin):
        
        if(basin =='shem'):
            stmopt='h.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='io'):
            stmopt='i.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='epac'):
            stmopt='c.%s,e.%s'%(year,year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='lant'):
            stmopt='l.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='wpac'):
            stmopt='w.%s'%(year)
            tD=TcData(stmopt=stmopt)
        return(tD)
    
    def getMd3path(self,tstmid):
        
        rc=getStmParams(tstmid)
        stm3id="%s%s"%(rc[0],rc[1])
        stm3id=stm3id.upper()
        
        tyear=rc[2]
        tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
        odirs=glob.glob("%s"%(tmask))
        if(len(odirs) == 1):
            sdir=odirs[0]
        else:
            print 'EEE -- finding sdir in getMd3path for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
            sys.exit()
    
        if(IsNN(tstmid)):
            md3mask="%s/*-%s-md3-BT.txt"%(sdir,tyear)
            md3paths=glob.glob(md3mask)
        else:
            md3mask="%s/*-%s-md3.txt"%(sdir,tyear)
            md3paths=glob.glob(md3mask)
            
        if(len(md3paths) == 1):
            md3path=md3paths[0]
        else:
            print 'EEE -- finding md3path in getMd3Spath for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
            sys.exit()
            
        return(md3path)
        
    
    
    def getTstmidsSum(self,year,basin,spath,ropt='norun',doBTonly=0,verb=0):
        
        (ddir,ffile)=os.path.split(spath)
        cards=open(spath).readlines()
        
        basinStm={}
        allStm={}
        for card in cards:
            
            if(verb):
                n=0
                tt=card.split(',')
                for n in range(0,len(tt)):
                    print 'n: %2d'%(n),tt[n]
            
            rc=parseStmSumCard(card)
            (tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)=rc
            
            # -- option to do BT only
            #
            if(doBTonly and not(IsNN(stm1id))):
                continue
    
            basinStm[rc[0]]=(bdtg,edtg,sname,stm9x,t2gen,dtggen)
            
        bstmids=basinStm.keys()
        for bstmid in bstmids:
            allStm[bstmid]=basinStm[bstmid]
            
    
        return(allStm)    
    
    
    def getMd3Stmids4dtg(self,dtg,dobt=0,verb=0,warn=0):
        
        try:
            stmids=self.dtgMd3[dtg]
        except:
            if(warn): print 'WWW no md3 stms for dtg: ',dtg
            stmids=[]
            return(stmids)

        ostmids=stmids
        
        if(dobt):
            ostmids=[]
            for stmid in stmids:
                if(IsNN(stmid)): ostmids.append(stmid)
                
        return(ostmids)
        
    def getMd3StmMeta(self,stmid,doprint=0):

        #n 0 30w.2019
        #n 1 TY
        #n 2 NN
        #n 3 PHANFONE
        #n 4 105
        #n 5 7.2
        #n 6 12.0
        #n 7 9.9
        #n 8 131.6
        #n 9 2019121718
        #n 10 2019122918
        #n 11 4.4
        #n 12 15.5
        #n 13 110.8
        #n 14 158.5
        #n 15 6.5
        #n 16 7.3
        #n 17 6
        #n 18 0
        #n 19 4
        #n 20 ddRI
        #n 21 9X
        #n 22 z0w
        #n 23 96
        #n 24 2019122118
        
        sm=self.stmMetaMd3[stmid]
        # -- parse
        #
        livestatus=' '
        sstmid=sm[0]
        (stm,yyyy)=sstmid.split('.')
        tctype=sm[1]
        stmDev=sm[2]
        sname=sm[3]
        ovmax=str(sm[4])
        tclife=float(sm[5])
        stmlife=float(sm[6])
        latb=float(sm[7])
        lonb=float(sm[8])
        bdtg=sm[9]
        edtg=sm[10]
        latmn=float(sm[11])
        latmx=float(sm[12])
        lonmn=float(sm[13])
        lonmx=float(sm[14])
        stcd=float(sm[15])
        oACE=float(sm[16])
        nRI=int(sm[17])
        nED=int(sm[18])
        nRW=int(sm[19])
        RIstatus=sm[20]
        if(RIstatus == 'NaN'): RIstatus='    '
        stm9xtype=sm[21]
        stm9x=sm[22]
        stm9x="%s: %s"%(stm9xtype,stm9x.upper())
        
        if(sm[23] != 'NaN'):
            timeGen=int(sm[23])
        else:
            timeGen=0
            
        timeGen="tG:%3d"%(timeGen)
        ogendtg=sm[24].strip()
        if(ogendtg == 'NaN'): ogendtg=edtg
        
        stm=stm.upper()
        
        ocard="%s %s%1s %3s %-10s :%3s :%4.1f;%4.1f :%5.1f %5.1f : %s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%4.1f :%4.1f :%2d:%2d:%2d:%s :%s %s %s"%\
            (yyyy,stm,livestatus,tctype,sname[0:9],ovmax,tclife,stmlife,latb,lonb,bdtg[4:],edtg[4:],
             latmn,latmx,lonmn,lonmx,
             stcd,oACE,
             nRI,nED,nRW,
             RIstatus,timeGen,stm9x,ogendtg)

        rc=(yyyy,stm,livestatus,tctype,sname,ovmax,tclife,stmlife,latb,lonb,bdtg,edtg,
            latmn,latmx,lonmn,lonmx,
            stcd,oACE,
            nRI,nED,nRW,
            RIstatus,timeGen,stm9x,ogendtg)
        
        #ocard=ocard[0:-1]
        if(doprint): 
            print ocard
            
        return(rc,ocard)

        
    
    def getMd3track(self,stmid,dobt=0,undef=-999.,verb=0,domiss=0):
        
        #mkFloat=self.mkFloat
        
        #n:  0 2019122118
        #n:  1 30w.2019
        #n:  2 PHANFONE
        #n:  3 TY
        #n:  4 NN
        #n:  5 6.4
        #n:  6 139.9
        #n:  7 30
        #n:  8 1002
        #n:  9 293
        #n: 10 14
        #n: 11 293
        #n: 12 14
        #n: 13 NaN
        #n: 14 NaN
        #n: 15 NaN
        #n: 16 NaN
        #n: 17 NaN
        #n: 18 NaN
        #n: 19 NaN
        #n: 20 NaN
        #n: 21 NaN
        #n: 22 NaN
        #n: 23 TD
        #n: 24 WN
        #n: 25 B  dirtype
        #n: 26 B  posttype
        #n: 27 140
        #n: 28 1006
        #n: 29 NaN
        #n: 30 S
        #n: 31 30
        #n: 32 RCB
             
        m3trk={}
        stmid=stmid.lower()

        try:
            smeta=self.stmMetaMd3[stmid]
        except:
            print 'EEE in getMd3track for: ',stmid
            return(0,m3trk)
            
            
        m3trk={}
        stmcards=self.stmMd3[stmid]

        if(IsNN(stmid)):
            # --smeta[-1] has the type of gendtg
            smkey=len(smeta)
            stmid9x="%s.%s"%(smeta[-4],stmid.split('.')[-1])
            stmcards9x=self.stmMd3[stmid9x]
            stmcards=stmcards9x+stmcards
            
        for mm in stmcards:

            rc=parseMd3Card(mm,dobt=dobt,verb=verb)
            if(verb):
                if(rc != None):
                    smm=str(mm)
                    orc="%s %s %s %s"%(smm[2:12],str(mm[1]),str(mm[5:10]),str(mm[-10:-8]))
                    print 'Mdeck3.getMd3track stmcard: ',orc
            
            if(rc == None):continue

            (dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
             tcstate,warn,
             roci,poci,alf,
             depth,eyedia,tdo,ostmid,ostmname,r34,r50)=rc

            m3trk[dtg]=(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
            
        def interpM3trk(m1,m2,f1,f2):
            
            def dointerp(v1,v2,f1,f2):
                if(v1 != undef and v1 != undef): vi=v1*f1+v2*f2
                if(v1 != undef and v2 == undef): vi=v1
                if(v2 != undef and v1 == undef): vi=v2
                if(v1 == undef and v2 == undef): vi=undef
                
                return(vi)
                
                
            (rlat1,rlon1,vmax1,pmin1,tdir1,tspd1,r34m1,r50m1,tcstate1,warn1,roci1,poci1,alf1,depth1,eyedia1,tdo1,ostmid1,ostmname1,r341,r501)=m1
            (rlat2,rlon2,vmax2,pmin2,tdir2,tspd2,r34m2,r50m2,tcstate2,warn2,roci2,poci2,alf2,depth2,eyedia2,tdo2,ostmid2,ostmname2,r342,r502)=m2
            
            rlati=rlat1*f1+rlat2*f2
            rloni=rlon1*f1+rlon2*f2
            vmaxi=dointerp(vmax1,vmax2,f1,f2)
            pmini=dointerp(pmin1,pmin2,f1,f2)
            tdiri=dointerp(tdir1,tdir2,f1,f2)
            tspdi=dointerp(tspd1,tspd2,f1,f2)
            r34mi=dointerp(r34m1,r34m2,f1,f2)
            r50mi=dointerp(r50m1,r50m2,f1,f2)
            tcstatei=tcstate1
            warni=warn1
            rocii=dointerp(roci1,roci2,f1,f2)
            pocii=dointerp(poci1,poci2,f1,f2)
            alfi=dointerp(alf1,alf2,f1,f2)
            depthi=depth1
            eyediai=eyedia1
            tdoi=tdo1
            ostmidi=ostmid1
            ostmnamei=ostmname1
            r34i=r341
            r50i=r501
            
            mi=(rlati,rloni,vmaxi,pmini,tdiri,tspdi,r34mi,r50mi,tcstatei,warni,rocii,pocii,alfi,depthi,eyediai,tdoi,ostmidi,ostmnamei,r34i,r50i)
            return(mi)
            
        # -- check if we need to interpolate for missing dtgs
        #
        idtgs=m3trk.keys()
        idtgs.sort()
        fdtgs=mf.dtgrange(idtgs[0],idtgs[-1],6)
        li=len(idtgs)
        lf=len(fdtgs)
        
        # -- we do need to interpolate... can handle 12 and 18 gaps
        
        if(li != lf):

            mdtgs=[]
            if(verb): print 'li lf',stmid,li,lf
            for n in range(0,lf):
                fdtg=fdtgs[n]
                try:
                    m3i=m3trk[fdtg]
                except:
                    
                    dtg1=fdtgs[n-1]
                    indx=idtgs.index(dtg1)
                    dtg2=idtgs[indx+1]
                    
                    if(verb): print 'have to interpolate...',fdtg,'dtg1 2',dtg1,dtg2
                    # -- do the interpolation here...
                    #
                    dtgib=mf.dtginc(dtg1,+6)
                    dtgie=mf.dtginc(dtg2,-6)
                    dtgis=mf.dtgrange(dtgib, dtgie)
                    iden=dtgdiff(dtg1, dtg2)
                    if(iden > 36.0):
                        print'EEE big iterp interval for stmid',stmid,dtg1,dtg2,iden
                        sys.exit()
                    m1=m3trk[dtg1]
                    m2=m3trk[dtg2]

                    for dtgi in dtgis:

                        inum1=dtgdiff(dtg1, dtgi)
                        inum2=dtgdiff(dtgi,dtg2)

                        f1=inum2/iden
                        f2=inum1/iden
                    
                        if(verb): print 'interp for dtg',dtg1,dtgi,dtg2,inum1,inum2,f1,f2
                        m3trk[dtgi]=interpM3trk(m1,m2,f1,f2)
                        mdtgs.append(dtgi)
                        n=n+1
                    n=n+1
                    
                    
                    
            if(domiss): return(None,mdtgs)
            return(1,m3trk)
            
        return(1,m3trk)
            
    def getMd3tracks(self,stmids,dobt=0,undef=-999.,verb=0):
        m3trks={}
        for stmid in stmids:
            (rc,m3trk)=self.getMd3track(stmid,dobt=dobt)
            m3trks[stmid]=m3trk
        return(m3trks)
    
    def getMd3StmDtgs4Stmopt(self,stmopt,syear=None,dobt=0,undef=-999.,verb=0):
        stmopts=getStmopts(stmopt)
        
        m3dtgs=[]
        for stmopt in stmopts:
            tstmids=self.getMd3Stmids(stmopt)
            for stmid in tstmids:
                (rc,m3trk)=self.getMd3track(stmid,dobt=dobt)
                if(rc):
                    m3dtgs=m3dtgs+m3trk.keys()
                    
        m3dtgs=uniq(m3dtgs)
        if(syear != None):
            om3dtgs=[]
            for m3dtg in m3dtgs:
                if(m3dtg[0:4] == syear):
                    om3dtgs.append(m3dtg)
                    
            m3dtgs=om3dtgs
        
        return(m3dtgs)
    
    
    def getTstmidsSumOLD(self,year,basin,spath,ropt='norun',doBTonly=0):
        
        (ddir,ffile)=os.path.split(spath)
        cards=open(spath).readlines()
        tstmids=[]
        
        for card in cards:
            tt=card.split(":")
            stm3id=tt[0].split()[1]
            stm1id="%s.%s"%(stm3id,year)
            
            # -- option to do BT only
            #
            if(doBTonly and not(IsNN(stm1id))):
                continue
    
            tstmids.append(stm1id)
    
        return(tstmids)    
    
    
    
    def getTstmidsByYearBasin(self,years,basins,stbdir):
        
        tstmids=[]
        for year in years:
            tdir="%s/%s"%(stbdir,year)
            MF.ChkDir(tdir,'mk')
            
            for basin in basins:
                spath="%s/stm-%s-%s.txt"%(tdir,basin,year)
                tstmids=tstmids+getTstmidsSum(year,basin,spath)
        
        return(tstmids)        
    
    def makeTCvCard(self,stmid,dtg,trk,verb=0):
    
            # -- set rmax to None

            rmax=None
            (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
             tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=trk[dtg]
            (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dozero=1)
    
            carqvmax=vmax*knots2ms
            if(carqvmax > 0.0):
                vitvmax="%02d"%(nint(carqvmax))
            else:
                carqvmax=-9
                vitvmax="%02d"%(carqvmax)
    
    
            if(poci != None and poci != undef):
                carqpoci=poci
                vitpoci="%04d"%(nint(carqpoci))
            else:
                carqpoci=-999.
                vitpoci="%04d"%(carqpoci)
    
    
            if(roci != None and roci != undef):
                carqroci=roci*nm2km
                vitroci="%04d"%(nint(carqroci))
            else:
                carqroci=-999
                vitroci="%04d"%(carqroci)
    
            if(rmax != None):
                carqrmax=rmax*nm2km
                vitrmax="%03d"%(nint(carqrmax))
            else:
                carqrmax=-99
                vitrmax="%03d"%(carqrmax)
    
    
            tcdepth=depth
            if(not(depth == 'S' or depth == 'M' or depth == 'D')): tcdepth='X'
    
            # -- one posit for c7w.07
            #
            if(tdir == undef):
                vitdir='-99'
            else:
                vitdir="%03.0f"%(tdir)
    
            if(tspd == undef):
                vitspd='-99'
            else:
                vitspd="%03.0f"%(tspd*10.0*knots2ms)
    
    
            if(pmin != None and pmin != undef):
                vitpmin="%04d"%int(pmin)
            else:
                pmin=-999
                vitpmin="%04d"%int(pmin)
    
            carqr34ne=r34[0]*nm2km
            carqr34se=r34[1]*nm2km
            carqr34sw=r34[2]*nm2km
            carqr34nw=r34[3]*nm2km
            
            if(carqr34ne > 0.0):
                vitr34ne="%04.0f"%(carqr34ne)
            else:
                r34ne=-999.
                vitr34ne="%04.0f"%(r34ne)
    
            if(carqr34se > 0.0):
                vitr34se="%04.0f"%(carqr34se)
            else:
                r34se=-999.
                vitr34se="%04.0f"%(r34se)
    
            if(carqr34sw > 0.0):
                vitr34sw="%04.0f"%(carqr34sw)
            else:
                r34sw=-999.
                vitr34sw="%04.0f"%(r34sw)
    
            if(carqr34nw > 0.0):
                vitr34nw="%04.0f"%(carqr34nw)
            else:
                r34nw=-999.
                vitr34nw="%04.0f"%(r34nw)
    
            vitdepth=tcdepth
    
            # MFTC 97S UNKNOWN   20100415 1200 083S 1017E 130 007 1010 -999 -999 08 -99 -999 -999 -999 -999 X
    
            stm3id=stmid.split('.')[0].upper()
            tcvitalscard="%4s %3s %-9s %8s %04d %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
                (tcVcenterid,stm3id,ostmname[0:9],
                 dtg[0:8],int(dtg[8:10])*100,
                 clat,clon,
                 vitdir,vitspd,
                 vitpmin,
                 vitpoci,vitroci,
                 vitvmax,vitrmax,
                 vitr34ne,vitr34se,vitr34sw,vitr34nw,
                 vitdepth)
    
            if(verb): print tcvitalscard
            return(tcvitalscard)
    
    
    def makeTCvCards(self,stmids,dtg,trks,override=0,verb=0,filename='tcvitals',tcvPath=None):

        cards=''
        for stmid in stmids:
            cards=cards+self.makeTCvCard(stmid,dtg,trks[stmid])+'\n'

        if(verb): 
            print
            for card in cards.split('\n'):
                if(len(card) > 1): print card

        if(tcvPath != None):
            tcvpath=tcvPath
            rc=MF.WriteString2File(cards,tcvPath,verb=verb)
            return(cards,tcvpath)
        else:
            tcvpath="%s/%s.%s.txt"%(TcVitalsDatDir,filename,dtg)
            return(cards,tcvpath)


# -- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCc
#


class Trkdata(MFbase):

    def __init__(self,
                 rlat,
                 rlon,
                 vmax,
                 pmin=undef,
                 dir=undef,
                 spd=undef,
                 tccode='XX',
                 wncode='XX',
                 trkdir=undef,
                 trkspd=undef,
                 dirtype='X',
                 b1id='X',
                 tdo='XXX',
                 ntrk=0,
                 ndtgs=0,
                 r34m=undef,
                 r50m=undef,
                 r34=undef,
                 r50=undef,
                 alf=undef,
                 depth='X',
                 poci=undef,
                 roci=undef,
                 rmax=undef,
                 ):


        self.undef=undef
        self.rlat=rlat
        self.rlon=rlon
        self.vmax=vmax
        self.pmin=pmin
        self.dir=dir
        self.spd=spd
        self.tccode=tccode
        self.wncode=wncode
        self.trkdir=trkdir
        self.trkdir=trkspd
        self.dirtype=dirtype
        self.b1id=b1id
        self.tdo=tdo
        self.ntrk=ntrk
        self.ndtgs=ndtgs
        self.r34=r34
        self.r50=r50
        self.r34m=r34m
        self.r50m=r50m
        self.alf=alf
        self.depth=depth
        self.poci=poci
        self.roci=roci
        self.rmax=rmax


    def gettrk(self):

        trk=(self.rlat,self.rlon,self.vmax,self.pmin,
             self.dir,self.spd,
             self.tccode,self.wncode,
             self.trkdir,self.trkspd,self.dirtype,
             self.b1id,self.tdo,self.ntrk,self.ndtgs,
             self.r34m,self.r50m,self.alf,self.sname,
             self.r34,self.r50,self.depth,
             )

        return(trk)


    def getposit(self):

        posit=(self.rlat,self.rlon,self.vmax,self.pmin,
               self.dir,self.spd,self.tccode,
               )
        return(posit)

class ADutils(MFutils):


    def Smth121(self,data,npass=0):

        nd=len(data)

        if(npass == 0):
            tdata=copy.deepcopy(data)
            return(tdata)

        odata=copy.deepcopy(data)
        tdata=copy.deepcopy(data)

        for n in range(0,npass+1):

            for i in range(0,nd):
                if(i == 0 or i == nd-1):
                    tdata[i]=odata[i]
                else:
                    tdata[i]=0.25*odata[i-1]+0.5*odata[i]+0.25*odata[i+1]

            for i in range(0,nd):
                odata[i]=tdata[i]

        return(tdata)




    def FcTrackInterpFill(self,itrk,dtx=3,npass=0,dovmaxSmth=0,verb=0,idtmax=6,doExtrap=1):

        """
----------------------------------------------------------------------
 routine to smooth input track in lat,lon
 doextrap -- extrap from last point using previous motion to add
 taus  -- similar to nhc_interp.f except done on INuPT to rumterp
----------------------------------------------------------------------
"""
        itaus=itrk.keys()
        itaus.sort()

        btau=itaus[0]

        deftrk={}
        mottrk={}

        jtrk={}

        #  -- check for extra vars
        #
        
        doextra1=0
        doextra2=0
        dor34s=0
        dor50s=0
        dor64s=0
        
        for tau in itaus:

            if(type(tau) is IntType and int(tau)%idtmax != 0): continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
                
            # -- detect new BT2 with dir,speed,'TC' and 'NW' in -2 and -1 position
            #
            if(itrkLen == 5):
                fextra1=itrk[tau][-2]
                if(fextra1 != None and not( ( (type(fextra1) is StringType) and len(fextra1) == 2 ) ) ): doextra1=1
            
            if(itrkLen == 6):
                fextra2=itrk[tau][-1]
                if(fextra2 != None and not( ( (type(fextra2) is StringType) and len(fextra2) == 2 ) ) ): doextra2=1
                
        for tau in itaus:

            # -- filter out non 6 h trackers -- hwrf now hoursly 0-9 h, otherwise 3-h
            #    assumed tau was an integer for check --- not true for BT which is DTG
            # -- only do check if int -- assumes dtg are always 6 h
            # -- 20190910 -- add exception 
            if(type(tau) is IntType and int(tau)%idtmax != 0): 
                print 'WWW-ADutils-FcTrackInterpFill -- skipping tau: ',tau
                continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])

            try:
                fvmax=itrk[tau][2]
            except:
                fvmax=-9999.
            if(fvmax == None or fvmax == 0.0): fvmax=-9999.
            
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
            if(fpmin == None or fpmin == 0.0): fpmin=-9999.

            
            # -- if itrkLen == 7 then will deal is have the three radii
            #
            if(itrkLen == 7):
                try:
                    fr34s=itrk[tau][4]
                except:
                    fr34s=None
                    
                try:
                    fr50s=itrk[tau][5]
                except:
                    fr50s=None
                    
                try:
                    fr64s=itrk[tau][6]
                except:
                    fr64s=None
                    

            try:
                fextra1=itrk[tau][-2]
            except:
                fextra1=-9999.
                
            if(fextra1 == None): fextra1=-9999.

            try:
                fextra2=itrk[tau][-1]
            except:
                fextra2=-9999.
                
            if(fextra2 == None): fextra2=-9999.

            # -- bounds check on latitude
            #
            if(flat < 85.0 and flat > -85.0):
                
                deftrk[tau]=[flat,flon,fvmax,fpmin]
                
                if(doextra1):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1]
                    
                if(doextra2):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1,fextra2]
              
                # -- wind radii
                #
                if(itrkLen == 7):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fr34s,fr50s,fr64s]
                    
                    

        deftaus=deftrk.keys()
        deftaus=deftrk.keys()
        deftaus.sort()

        ntaus=len(deftaus)

        etau=0
        if(ntaus>1): etau=deftaus[ntaus-1]


        #
        # bail if no forecasts
        #
        if(etau == 0):

            #
            # case of initial position only, return for phr=0...
            #
            try:
                jtrk[etau]=deftrk[etau]
            except:
                jtrk[etau]=[]
            return(jtrk,deftaus)

        #
        # get motion of defined track
        #

        for i in range(0,ntaus):

            tau=deftaus[i]

            i0=i
            ip1=i+1

            if(ntaus > 1):

                if(i0 < ntaus-1):
                    i0=i
                    ip1=i+1

                elif(i0 == ntaus-1):
                    i0=i-1
                    ip1=i

                try:
                    dtau=deftaus[ip1]-deftaus[i0]
                except:
                    dtau=dtgdiff(deftaus[i0],deftaus[ip1])

            else:

                dtau=0.0

            
            if(dtau == 0.0):
                edir=270.0
                espd=0.0
                dvmax=0.0
                dpmin=0.0
                dextra1=0.0
                dextra2=0.0

            else:

                tau0=deftaus[i0]
                tau1=deftaus[ip1]

                flat0=deftrk[tau0][0]
                flon0=deftrk[tau0][1]
                fvmax0=deftrk[tau0][2]
                fpmin0=deftrk[tau0][3]
                
                if(doextra1):
                    fextra10=deftrk[tau0][4]
                    fextra11=deftrk[tau1][4]

                if(doextra2):
                    fextra20=deftrk[tau0][5]
                    fextra21=deftrk[tau1][5]
                    
                # -- wind radii
                #
                if(itrkLen == 7):
                    
                    fr34s0=deftrk[tau0][4]
                    fr34s1=deftrk[tau1][4]
                    
                    fr50s0=deftrk[tau0][5]
                    fr50s1=deftrk[tau1][5]

                    fr64s0=deftrk[tau0][6]
                    fr64s1=deftrk[tau1][6]
                    

                flat1=deftrk[tau1][0]
                flon1=deftrk[tau1][1]
                fvmax1=deftrk[tau1][2]
                fpmin1=deftrk[tau1][3]

                # -- 20190910 -- test for both vmax and pmin, if undef then set to 0.0 or persistence
                #
                if(fvmax1 > 0.0 and fvmax0 > 0.0 ):
                    dvmax=fvmax1-fvmax0
                else:
                    dvmax=0.0
                    
                if(fpmin1 > 0.0 and fpmin0 > 0.0):
                    dpmin=fpmin1-fpmin0
                else:
                    dpmin=0.0
                
                if(doextra1):
                    dextra1=fextra11-fextra10
                
                if(doextra2):
                    dextra2=fextra21-fextra20

                (course,speed,eiu,eiv)=rumhdsp(flat0,flon0,flat1,flon1,dtau)

            #
            # use penultimate motion for end motion
            # set vmax/pmin change to 0.0
            #

            if(i == ip1):
                otau=deftaus[ip1]
                dvmax=0.0
                dpmin=0.0
                if(doextra1): dextra1=0.0
                if(doextra2): dextra2=0.0

            else:
                otau=deftaus[i0]

            mottrk[otau]=[course,speed,dvmax,dpmin]
            if(doextra1):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1]
            if(doextra2):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1,dextra2]
                
            # -- wind radii --  assume no change in wind radii in the tau interval -- set to beginning
            #
            if(itrkLen == 7):
                mottrk[otau]=[course,speed,dvmax,dpmin,fr34s0,fr50s0,fr64s0]
                

        taus=mottrk.keys()
        taus.sort()
        
        'ffffffffffffffffffffffff',mottrk

        # -- only go out +dtx(3) h at the end for the smoother only
        # -- final extrap after bias corr + smoothing
        #
        
        etau=taus[-1]
        
        if(doExtrap):
            try:    
                etaux=etau+dtx
            except:
                etaux=mf.dtginc(etau,dtx)
        else:
            etaux=etau
            

        try:
            otaus=range(btau,etaux+1,dtx)
        except:
            otaus=mf.dtgrange(btau,mf.dtginc(etaux,1),dtx)

        nt=len(taus)

        n=0
        tau0=taus[n]
        if(nt >= 1): tau1=taus[n+1]

        
        # -- rhumb-line interpolation ""rumterp" to the dtx track (0,3,6,9,12), nhc_interpfcst.f uses linear
        #

        for otau in otaus:

            if(otau == tau0):
                dtau=0

            # -- otau  is beyond the bounding interval
            #

            elif(otau >= tau1):

                atend=0

                # -- increment to set the interval so that otau is equal to tau0 or between tao0 and tau1
                #
                n=n+1
                if(n == nt-1):
                    n=n-1
                    atend=1

                tau0=taus[n]

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                # -- dtx > delta of deftrk, e.g., deftrk is 3 h from RAP and target is 6 h
                #

                if(tau0 < otau):
                    while(tau0 < otau):
                        n=n+1

                        # -- check if beyond def trk
                        #
                        if(n > nt-1):
                            tau0=taus[-1]
                            n=nt-1
                            break
                        else:
                            tau0=taus[n]

                    # -- check if at end
                    #
                    if(n == nt-1):
                        n=n-1
                        atend=1


                    # -- case where tau0 = otau
                    #
                    if(tau0 == otau): dtau=0

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                if(nt >= 1): tau1=taus[n+1]

                dtau=0
                #
                # correct handling of extrap point
                #
                if(atend and doExtrap):
                    tau0=tau1
                    tau1=otaus[-1]
                    try:
                        dtau=otau-tau0
                    except:
                        dtau=dtgdiff(tau0,otau)


            else:
                try:
                    dtau=otau-tau0
                except:
                    dtau=dtgdiff(tau0,otau)

            rlat0=deftrk[tau0][0]
            rlon0=deftrk[tau0][1]
            vmax0=deftrk[tau0][2]
            pmin0=deftrk[tau0][3]
            if(doextra1): extra10=deftrk[tau0][4]
            if(doextra2): extra20=deftrk[tau0][5]

            course=mottrk[tau0][0]
            speed=mottrk[tau0][1]
            dvmax=mottrk[tau0][2]
            dpmin=mottrk[tau0][3]
            if(doextra1): dextra1=mottrk[tau0][4]
            if(doextra2): dextra2=mottrk[tau0][5]
            
            # -- wind radii at beginning of interval
            #
            if(itrkLen == 7):
                r34sI=mottrk[tau0][4]
                r50sI=mottrk[tau0][5]
                r64sI=mottrk[tau0][6]

            if(dtau > 0):
                (rlat1,rlon1)=rumltlg(course,speed,dtau,rlat0,rlon0)
                try:
                    dt=float((tau1-tau0))
                except:
                    dt=dtgdiff(tau0,tau1)

                vfact=float(dtau)/dt
                vmax1=vmax0+vfact*dvmax
                pmin1=pmin0+vfact*dpmin
                if(doextra1): extra11=extra10+vfact*dextra1
                if(doextra2): extra21=extra20+vfact*dextra2
                
                # -- do radius interp here -- set to tau0 for now -- use fr??s0 and fr??s1
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]
                
            else:
                rlat1=rlat0
                rlon1=rlon0
                vmax1=vmax0
                pmin1=pmin0
                if(doextra1): extra11=extra10
                if(doextra2): extra21=extra20
                vfact=0.0
                
                # -- wind radii for dtau = 0
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]

            #
            # make sure
            #

            jtrk[otau]=[rlat1,rlon1,vmax1,pmin1]

            if(doextra1):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11]
                
            if(doextra2):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11,extra21]
            
            # -- wind radii -- the 'interpolated' from above
            #
            if(itrkLen == 7):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,r34sI,r50sI,r64sI]

        rlats=self.Dic2list(jtrk,0)
        srlats=self.Smth121(rlats,npass)

        rlons=self.Dic2list(jtrk,1)
        srlons=self.Smth121(rlons,npass)

        vmaxs=self.Dic2list(jtrk,2)
        if(dovmaxSmth):
            svmaxs=self.Smth121(vmaxs,npass)
        else:
            svmaxs=vmaxs

        pmins=self.Dic2list(jtrk,3)
        spmins=self.Smth121(pmins,npass)

        if(doextra1):
            extra1s=self.Dic2list(jtrk,4)
            sextra1s=self.Smth121(extra1s,npass)

        if(doextra2):
            extra2s=self.Dic2list(jtrk,5)
            sextra2s=self.Smth121(extra2s,npass)

        self.List2Dict(jtrk,srlats,0)
        self.List2Dict(jtrk,srlons,1)
        self.List2Dict(jtrk,svmaxs,2)
        self.List2Dict(jtrk,spmins,3)
        if(doextra1): self.List2Dict(jtrk,sextra1s,4)
        if(doextra2): self.List2Dict(jtrk,sextra2s,5)

        return(jtrk,deftaus)



    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc
    #
    # bias correct and 3-h interp track from above 
    #
    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc

    def BiasCorrFcTrackInterpFill(self,jtrk,itrk,deftaus,phr,dtx,
                                  btlat,btlon,btdir,btspd,btvmax,
                                  model,dtg,stm3id,
                                  latlontaucut=0.0,latlontaumin=120.0,latloncorrmin=1.0,  # for lat/lon ghmi
                                  
                                  # -- 20190904 -- can duplicate hwfi with hwfr06 with the older and more
                                  #    standard? setup...
                                  
                                  #latlontaucut=0.0,latlontaumin=24.0,latloncorrmin=0.0,  # for modern models with better small tau errors
                                  vmaxtaucut=0.0,vmaxtaumin=24.0,vmaxcorrmin=200.0,     # bad to make blow up if vmaxCorrScheme not set correctly
                                  dopc=1,vmaxmin=20.0,vmaxCorrScheme='global',verb=0):


        #------------------------------------------------------------------------------------

        def PersistCorr(tau,lat0,lon0,course,speed,
                        latfc,lonfc,
                        pctauend=12,pcmin=0.33):

            (latp,lonp)=rumltlg(course,speed,tau,lat0,lon0)

            if(tau <= pctauend):
                pcorr=pcmin+(1.0-(float(tau)/pctauend))*(1.0-pcmin)
                latpc=(1.0-pcorr)*latfc + pcorr*latp
                lonpc=(1.0-pcorr)*lonfc + pcorr*lonp
                #print 'vvvvvvvvv------------------ ',tau,pcmin,pcorr,' lat: ',latfc,latp,latpc,' lon: ',lonfc,lonp,lonpc
            return(latpc,lonpc)


        # hard-wired from nhc_interp.f for dt=3
        #

        def fiextrap(t,a,b,c):
            x=(2.0*a + t*(4.0*b - c - 3.0*a + t*(c - 2.0*b + a)))/2.0
            return(x)


        def setfvmaxoffact(tau,atend,
                           vmaxtaumin,vmaxtaucut,vmaxcorrmin):

            ftau=float(tau)
            if(vmaxtaumin  > 0.0):

                if((ftau >= vmaxtaucut and ftau <= vmaxtaumin) ):
                    fvmaxofffact=((vmaxtaumin-ftau)/(vmaxtaumin-vmaxtaucut))*(1.0-vmaxcorrmin) + vmaxcorrmin

                elif(ftau > vmaxtaumin or atend):
                    fvmaxofffact=vmaxcorrmin

                elif((ftau < 0) or (ftau >= 0 and ftau < vmaxtaucut) ):
                    fvmaxofffact=1.0

                else:
                    print 'EEEEEEEEEEEEEEEE setfvmaxoffact error'
                    sys.exit()


            else:
                fvmaxofffact=1.0

            if(fvmaxofffact < 0.0): fvmaxofffact=0.0
            if(vmaxtaumin == 0.0):  fvmaxofffact=1.0

            return(fvmaxofffact)



        if(vmaxCorrScheme == 'global'):
            vmaxtaucut=0.0
            vmaxtaumin=72.0
            vmaxcorrmin=0.0
        elif(vmaxCorrScheme == 'lame' or vmaxCorrScheme == 'limited'):
            vmaxtaucut=0.0
            vmaxtaumin=24.0
            vmaxcorrmin=0.0



        #------------------------------------------------------------------------------------


        itaus=itrk.keys()
        itaus.sort()

        otrk=copy.deepcopy(itrk)

        taus=jtrk.keys()
        taus.sort()

        #
        #
        #
        try:
            latoff=btlat-jtrk[phr][0]
            lonoff=btlon-jtrk[phr][1]
            fvmaxoff=btvmax-jtrk[phr][2]

        except:
            print 'WWWWW no jtrk for: ',stm3id,'  dtg: ',dtg,'  phr: ',phr
            return(otrk)



        #print 'OO11111 latoff,lonoff %02f %5.1f %5.1f %6.1f %6.1f :: %6.1f %6.1f '%(phr,btlat,jtrk[phr][0],btlon,jtrk[phr][1],latoff,lonoff)

        if(verb > 2):
            itaus=itrk.keys()
            itaus.sort()
            for tau in itaus:
                # ['2008061806', 9.5, 132.1, 21.0, 0.0, 42.3, 0.100001, 42.3, -16.3001, -38.9, -29.6, 30.0, [-999, -999, -999, -999], [-999, -999, -999, -999]]
                print 'III tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(itrk[tau][0],itrk[tau][1],itrk[tau][2])
            for tau in taus:
                print 'JJJ tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(jtrk[tau][0],jtrk[tau][1],jtrk[tau][2])



        jtrknopc={}

        for tau in taus:

            atend=0
            if(tau == taus[-1]): atend=1

            vmoff=0.0
            dtau=tau-phr

            vmoff=setfvmaxoffact(dtau,atend,
                                 vmaxtaumin,vmaxtaucut,vmaxcorrmin)

            factlloff=setfvmaxoffact(dtau,atend,
                                     latlontaumin,latlontaucut,latloncorrmin)
            latbc=jtrk[tau][0]+latoff*factlloff
            lonbc=jtrk[tau][1]+lonoff*factlloff
            vmaxbc=jtrk[tau][2]+fvmaxoff*vmoff

            # -- undef
            #
            if(jtrk[tau][2] <= 0.0):
                vmaxbc=0.0

            jtrknopc[tau]=[latbc,lonbc,vmaxbc]

            latcur=loncur=-999.
            if(dtau >= 3 and dtau <= 12 and dopc):
                (latpc,lonpc)=PersistCorr(dtau,btlat,btlon,btdir,btspd,
                                          latbc,lonbc
                                          )
                latbc=latpc
                lonbc=lonpc

            jtrk[tau][0]=latbc
            jtrk[tau][1]=lonbc
            jtrk[tau][2]=vmaxbc

        # --do the extrap
        #

        xtaus=range(taus[-1],taus[-1]+phr,dtx)

        try:
            etaum1=taus[-2]
        except:
            etaum1=taus[0]


        for xtau in xtaus:
            tm2=xtau-3*dtx
            tm1=xtau-2*dtx
            tm0=xtau-dtx
            jtrknopc[xtau]=[0,0,0]
            jtrk[xtau]=[0,0,0,[],[]]
            for j in range(0,3):
                a=jtrk[tm2][j]
                b=jtrk[tm1][j]
                c=jtrk[tm0][j]
                jtrk[xtau][j]=fiextrap(3,a,b,c)

                try:
                    if(j == 0 and verb):  print 'try',xtau
                except:
                    if(j == 0 and verb): print 'except',xtau
                    jtrk[xtau]=jtrk[taus[-1]]
                    jtrk[xtau][j]=fiextrap(3,a,b,c)

                jtrknopc[xtau][j]=jtrk[xtau][j]

            # -- set radii constant from etau -> last xtau
            #
            #for j in range(3,5):
            #    jtrk[xtau][j]=jtrk[etaum1][j]


        taus=jtrk.keys()
        taus.sort()

        if(verb > 2):
            for tau in taus:
                print 'FFF tau: %03d'%(tau)," lat: %5.1f PC: %5.1f  lon: %6.1f PC: %6.1f"%(jtrk[tau][0],jtrknopc[tau][0],
                                                                                           jtrk[tau][1],jtrknopc[tau][1])

        # -- put out final track; shift radii to phr from tau=0, i.e., do not interpolate but assume forecast unchanged
        #
        if(verb):
            print 'model: ',model,' dtg: ',dtg,' stm3id: ',stm3id,' phr: ',phr,\
                  ' btdir/spd: ',btdir,btspd,' offset: ',latoff,lonoff,'bt lat/lon/vmax: ',btlat,btlon,btvmax

        # -- relabel/recenter 
        #
        for tau in deftaus:
            
            otrk[tau][0]=jtrk[tau+phr][0]
            otrk[tau][1]=jtrk[tau+phr][1]

            # -- make sure intensity does not fall below vmaxmin
            #
            ovmax=jtrk[tau+phr][2]
            if(ovmax < vmaxmin):
                ovmax=vmaxmin
            otrk[tau][2]=ovmax

            # -- do not use interpolated radii; assume the forecast is the constant  
            #
            #otrk[tau][12]=jtrk[tau][3]
            #otrk[tau][13]=jtrk[tau][4]

            if(verb):
                print 'OOO tau: %03d'%(tau)," %5.1f | %6.1f |  %3.0f III:  %5.1f | %6.1f |  %3.0f "%(otrk[tau][0],otrk[tau][1],otrk[tau][2],
                                                                                                     itrk[tau][0],itrk[tau][1],itrk[tau][2]
                                                                                                     )


        return(otrk)
    



class Adeck(ADutils):

    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,adeckpathmasks,mD=None,dtgopt=None,taids=None,verb=0,warn=0,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None,
                 adeckCards=None,
                 ):

        
        #
        # trick to dectect if mask is a list...
        #
        if(type(adeckpathmasks) is ListType):
            adeckpaths=[]
            for adeckpathmask in adeckpathmasks:
                adeckpaths=adeckpaths+glob.glob(adeckpathmask)

        else:
            adeckpaths=glob.glob(adeckpathmasks)

        if(dtgopt != None):
            self.tdtgs=dtgs=dtg_dtgopt_prc(dtgopt,ddtg=6)


        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.mD=mD
        self.mDp1=mDp1

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.adecks=adeckpaths
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        if(adeckCards == None):
            self.initAdeckPaths(adeckpaths)
        else:
            self.getCards(adeckCards)
            
        self.initAdeck()

        if(doVD):
            import vdVM
            self.makeVdeck=VD.MakeVdeck
        

    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtausStatus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]

    def getCards(self,adeckCards):

        #cards=[]
        #for adeckpath in adeckpaths:
            #(adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            #if(adyear != None):
                #self.adeckyears.append(adyear)
                #self.adeckbasins.append(adbasin)
            
            #try:
                #ttt=open(adeckpath).readlines()
            #except:
                #ttt=None

            #if(cards == None):
                #return
            #else:
                #cards=cards+ttt

        self.cards=adeckCards
        

    def initAdeckPaths(self,adeckpaths):

        cards=[]
        for adeckpath in adeckpaths:
            (adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            if(adyear != None):
                self.adeckyears.append(adyear)
                self.adeckbasins.append(adbasin)
            
            try:
                ttt=open(adeckpath).readlines()
            except:
                ttt=None

            if(cards == None):
                return
            else:
                cards=cards+ttt

        self.cards=cards
        
        self.adeckyears=uniq(self.adeckyears)
        self.adeckbasins=uniq(self.adeckbasins)


    def isValidB2id(self,b2id):

        rc=0
        if(b2id.upper() in Basin2toBasin1.keys()): rc=1
        return(rc)


    def isAidVmaxOnly(self,aid):

        rc=0
        if( aid == None): return(rc)

        if(
            aid.upper() == 'SHF5' or
            aid.upper() == 'SHFR' or
            aid.upper() == 'IVCN' or
            aid.upper() == 'ICON' or
            aid.upper() == 'ST11' or
            aid.upper() == 'ST5D' or
            aid.upper() == 'S5YY' or
            aid.upper() == 'DSHA' or
            aid.upper() == 'DSHN' or
            aid.upper() == 'CCON' or
            aid.upper() == 'DSHW' or
            aid.upper() == 'SHIW' or
            aid.upper() == 'SHIP' or
            aid.upper() == 'S511' or
            aid.upper() == 'S5RI' or
            aid.upper() == 'SHIA' or
            aid.upper() == 'SHIE' or
            aid.upper() == 'SHIN' or
            aid.upper() == 'DSHE' or
# -- 20211028 -- from nhc
            aid.upper() == 'DSNS' or
            aid.upper() == 'SHNS' or
#
            aid.upper() == 'DSHP' or
            aid.upper() == 'CMES' or
            aid.upper() == 'CMSD' or
            aid.upper() == 'SHIU' or
            aid.upper() == 'DSHU' or
            aid.upper() == 'DC30' or
            
            aid.upper() == 'RI20' or
            aid.upper() == 'RI25' or
            aid.upper() == 'RI30' or
            aid.upper() == 'RI35' or
            aid.upper() == 'RI40' or
            aid.upper() == 'RI45' or
            aid.upper() == 'RI55' or
            aid.upper() == 'RI56' or
            aid.upper() == 'RI65' or
            aid.upper() == 'RI70' or
            aid.upper() == 'RIPA' or
            aid.upper() == 'RIDE' or
            aid.upper() == 'RD25' or

            aid.upper() == 'RVCN' or
            aid.upper() == 'RVCX' or
            aid.upper() == 'TVCC' or
            
            aid.upper() == 'IV15' or
            aid.upper() == 'IVCR' or
            aid.upper() == 'LGEM' or
            aid.upper() == 'SPC3' or
            aid.upper() == 'KSF5' or
            aid.upper() == 'KSFR' or
            aid.upper() == 'IVRI' or
            aid.upper() == 'KLGM' or
            aid.upper() == 'KSHP' or
            aid.upper() == 'KDSP' or
            aid.upper() == 'DSHF' or
            aid.upper() == 'CNTR' or
            #aid.upper() == 'PEST' or
            
            aid.upper() == 'TCCN' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            aid.upper() == 'ICNW' or
            aid.upper() == 'ICNX' or
            aid.upper() == 'RD20' or
            aid.upper() == 'RD30' or
            aid.upper() == 'RD35' or
            aid.upper() == 'RD40' or
            aid.upper() == 'RD45' or
            aid.upper() == 'RD55' or
            aid.upper() == 'RD56' or
            aid.upper() == 'RD65' or
            aid.upper() == 'RD70' or
            aid.upper() == 'FRIA' or
            aid.upper() == 'ICNE' or
            aid.upper() == 'JTWX' or
            
            
            aid.upper() == 'S5XX'

            ): rc=1

        return(rc)




    def makeIposit(self,tt,card,ncards,ntt,verb=0,aid=None,ipositPrev=None):

        def tt2rad(tt):
            try:
                rad=(float(tt[13]),float(tt[14]),float(tt[15]),float(tt[16]))
            except:
                print 'error in tt2rad for tt: ',tt
            return(rad)
            
        #WP, 22, 2014112912, 03, FIM9, 108, 119N, 1385E,  77,  985, XX,  64, NEQ,   95,   69,    0,   85,
        #0    1           2   3     4    5     6      7    8     9  10   11   12    13    14    15    16
        # --------- get tau and lat/lons, vmax, p,in
        #
        try:
            tau=tt[5].strip()
            itau=int(tau)

            # -- basic sanity check, if alat=alon=0, and vmax is not there... noload
            #
            clat=tt[6].strip()
            clon=tt[7].strip()
        except:
            if(self.warn): print 'WWW gooned up card, failed tau,clat,clon: %6i'%(ncards),' card: ',card[0:-1],ntt
            return(None,None)

        try:     vmax=float(tt[8])
        except:  vmax=self.undef
        
        if(vmax == 0):
            vmax=self.undef

        try:
            (alat,alon)=Clatlon2Rlatlon(clat,clon)
        except:
            # -- set  blank clat,clon to 0.0 for next check
            #
            if(clat == '' and clon == ''):
                alat=0.0
                alon=0.0
            else:
                if(self.warn): print 'WWW gooned up clat,clon: %6i'%(ncards),'clat,clon: ',clat,clon,'card: ',card[0:-1],'ntt: ',ntt
                return(None,None)

        if((alat == 0.0 and (alon == 0.0 or alon == 360.0)) and not(self.isAidVmaxOnly(aid)) ):
            if(self.warn): print 'WWW(Adeck.makeIpost): 0N 0W NOLOAD aid: ',aid,'isVmaxOnly: ',self.isAidVmaxOnly(aid),'card: ',card[:-1]
            return(None,None)

        #if(alat == 0.0 and (alon == 0.0 or alon == 360.0) and vmax == 0.0):
        #    if(verb): print '0N 0W Vmax0 NOLOAD : ',card[:-1]
        #    return(None,None)

        try:      pmin=float(tt[9])
        except:   pmin=self.undef
        if(pmin == 0.0): pmin=self.undef

        # -- pull r34 by default if ipositPrev == None
        #
        if(ipositPrev == None):
            
            r34=None
            r50=None
            r64=None

            #r34=(self.undef,self.undef,self.undef,self.undef)
            #r50=(self.undef,self.undef,self.undef,self.undef)
            #r64=(self.undef,self.undef,self.undef,self.undef)

            try:
                if(len(tt) > 16 and int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
            try:
                if(len(tt) > 16 and int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                
            try:
                if(len(tt) > 16 and int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                        
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        # -- !!!!!!!! - need to add code class Adeck to pass in previous iposit to check if only updating r50,r64
        #
        else:

            print 'WWWWWWWWWWWWWWWWXXXXXXXXXXXXXXXXXXx - no code to handle passing in prevIposit into Adeck.makeIposit...bye'
            sys.exit()
            r34=(self.undef,self.undef,self.undef,self.undef)
            r50=(self.undef,self.undef,self.undef,self.undef)
            r64=(self.undef,self.undef,self.undef,self.undef)
            
            if(len(tt) > 16):
                if(int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
                if(int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
                if(int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
                
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        return(itau,iposit)


    def setDtgNCard(self,tt):
        dtg=tt[2].strip()
        if(len(dtg) != 10):
            return(None)

        return(dtg)



    def makeBidDtg(self,tt,card,maxPrevYearDtgdiff=240.0):

        b2id=tt[0].strip()
        bnum=tt[1].strip()
        bnumi=bnum
        ibnum=bnum

        # check for ** in b2id  -- from rerun of tracker on tacc?
        #
        if(b2id == '**'):
            if(self.dob2idchk):
                print """EEEEEEEEEEE b2id check gives '**', we'll stop in initAdeck, until you mod the code want to just continue"""
                print 'card: ',card
                sys.exit()
            else:
                b2id='XX'

        elif(b2id.isdigit()):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is a number: ',card[:-1],' ...'
            return(None)

        if(not(self.isValidB2id(b2id)) and self.chkb2id):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is NOT standard: ',card[0:-1],' ...'
            return(None)

        #  check for unspecified bnum, e.g., when b2id == '**'
        #
        if(len(bnum) == 2):

            # -- handle new [A-Z][0-9] for 9X
            #
            bnum1=bnum[0].upper()
            if(ord(bnum1) >= 65 and ord(bnum1) <= 90):
                try:
                    bnum=90+int(bnum[1])
                    bnum=str(bnum)
                except:
                    print 'WWW bad acard in makeBidDtg(bad ord(bnum1): ',card[:-1],' bnum not defined...onward...'
                    return(None)

            try:      
                int(bnum)
            except:   
                print 'WWW bad acard in makeBidDtg(non int): ',card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 3-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 3):
            if(type(bnumi[0]) is str):
                bnumi="9%s"%(bnumi[1:])
            try:
                ibnum=int(bnumi[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 333333 bad acard(Adeck): ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        elif(len(bnum) >= 4):
            try:
                ibnum=int(bnum[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 44444 bad acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 1-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 1):
            try:
                ibnum=int(bnum[0])
                bnum="%02d"%(ibnum)
                print 'WWW single bnum: ',bnum,'stm2id: ',stm2id
            except:
                print 'WWW 111111 bad bnun in acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- blank bnum
        #
        elif(len(bnum) == 0):
            print 'WWW 000000 bad bnum in acard: ',bnum,card[:-1],' bnum 0 length...onward...'
            return(None)

        # -- filter out 8X storms
        #
        if(ibnum >= 80 and ibnum <= 89): return(None)

        # -- check if adeck uses sss.yyyy form of storm id vice standard 2-char stm id
        #

        if(len(bnum.split('.')) == 2):
            bn=bnum.split('.')[0]
            b1=bn[2]
            bn=bn[0:2]
            by=bnum.split('.')[1]
            bnum=bn

        # -- 9999999999999999999999999999999999 filter out 9X
        #
        if(self.dofilt9x and Is9XSnum(bnum)): return(None)
        
        dtg=self.setDtgNCard(tt)
        if(dtg == None):
            print 'WWW Adeck().setDtgNCard bad dtg: ',dtg,card 
            return(None)


        byear=dtg[0:4]
        # -- handle shem...
        #
        stm2id="%s%s.%s"%(b2id,bnumi,byear)
        if(isShemBasinStm(stm2id)):  byear=getShemYear(dtg)
        
        # -- if not an adeck use -- return
        #
        if(not(hasattr(self,'adyear'))):
            #print '11111111111111111111 ',dtg,b2id,bnumi,byear
            return(dtg,b2id,bnumi,byear)
        
        # -- check byear for storms starting in previous year
        #
        if( (self.adyear != None and self.adyearp1 != None) ):

            yeardiffSH=0
            isSH=isShemBasinStm(b2id)
            if(isSH):  yeardiffSH=int(dtg[0:4])-int(self.adyear)

            yeardiff=int(byear)-int(self.adyear)

            if(yeardiff == -1 and not(isSH)):
                prevYearDtgdiff=dtgdiff(dtg,"%4s010100"%(self.adyear[0:4]))
                if(prevYearDtgdiff > maxPrevYearDtgdiff):
                    print 'WWW Adeck().makeBidDtg() !!!!!!!!!!!!!!!!!!!!!! storm dtg < ',self.adyear,' prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' > maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40],'...press...'
                    return(None)
                else:
                    print 'WWW Adeck().makeBidDtg() storm dtg < ',self.adyear,' set to self.adyear when prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' < maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40]
                byear=self.adyear
            elif(yeardiffSH < -1):
                print 'EEE  Adeck().makeBidDtg() year diff too big for card: ',card[0:70]
                return(None)
            
        # -- check if byear in the adeckyears implied by the adeckpaths...if not, bail
        #
        if(len(self.adeckyears) > 0 and not(byear in self.adeckyears)): 
            print 'WWW Adeck.makeBidDtg byear of the storm NOT in the year implied by the adeck file name...press...',card[0:48]
            return(None)

        #print 'llllllllllllllllll',dtg,b2id,bnumi,byear
        return(dtg,b2id,bnumi,byear)


    def setAidNCard(self,tt):
        aid=tt[4].strip()
        return(aid)


    def makeAid(self,tt,card):

        aid=self.setAidNCard(tt)
        aid=aid.lower()


        # -- filter out carq
        #
        gotaid=0
        if(self.skipcarq and aid == 'carq'):
            return(gotaid,None,None)

        # -- aliases
        #
        if(self.aliases != None):
            for k in self.aliases.keys():
                if(aid == k):
                    oaid=self.aliases[k].upper()
                    iaid=aid.upper()

                    # -- convert 3-char aid -> 4-char
                    #
                    if(len(aid.upper()) <= 3): iaid="%4s"%(iaid)
                    card=card.replace(iaid,oaid)

                    # -- case where iaid is lowercase in card
                    #
                    card=card.replace(aid,oaid)
                    aid=oaid.lower()


        # --- replace _ with X in aid name
        #
        if(aid.replace('_','X')):
            aid=aid.replace('_','X')

        if(self.taids != None):
            gotaid=0
            for taid in self.taids:
                if(aid == taid):
                    gotaid=1
                    break
        else:
            gotaid=1

        return(gotaid,aid,card)


    def initAdeck(self,skipcarq=1,nlenmin=6,nlenmax=-999,filtHiFreq=1,maxDtau=6,verb=0):

        """  main method that parses the adeck cards and associates 9X storms with real NN storms using
        the mdeck object mD that has dicts and methods to get bt lat/lons

        """
        iposits={}
        
        ncards=1
        for card in self.cards:

            tt=card.split(',')
            ntt=len(tt)
            
            # -- check for blank card
            #
            if(ntt <= 1):
                continue
                
            # -- check for short cards
            #
            if(ntt <= nlenmin):
                print 'WWW short adeck card # ',ncards,card[:-1]
                continue

            #  -- check for long cards -- problem on jet/nccs in io from marchok tracker
            #
            if(nlenmax > 0 and ntt > nlenmax):
                print 'WWW LONG  adeck card # ',ncards,card[:-1]
                continue


            # -- get bid, dtg
            #
            rc=self.makeBidDtg(tt,card)
            if(rc == None): continue
            (dtg,b2id,bnum,byear)=rc

            # -- get aid
            #
            (gotaid,aidin,card)=self.makeAid(tt,card)
            if(hasattr(self,'prependAid')):
                if(self.prependAid != None):
                    aid="%1s%s"%(self.prependAid,aidin)
                else:
                    aid=aidin
            else:
                aid=aidin 
            
            if(self.aliases != None):
                try:
                    aidout=self.aliases[aidin.upper()]
                    card=card.replace(aidin.upper(),aidout,1)
                except:
                    None
            

            if(gotaid == 0): continue

            # -- get posit list
            #
            (itau,iposit)=self.makeIposit(tt,card,ncards,ntt,aid=aid)
            
            
            # -- filter out hi-frequency, e.g., hwrf in 2014 hourly 0-9 then 3 hourly
            #
            if(filtHiFreq and itau != None):
                if(itau%maxDtau != 0): continue
                
                
            if(itau == None): continue


            b2id=basin2Chk(b2id)

            stm2id="%s%s.%s"%(b2id,bnum,byear)
            stm2id=stm2id.lower()

            #######if(self.verb): print 'AAA ',aid,dtg,stm2id,itau
            # -- put correct 2-char basin in the input card
            #
            card=b2id+card[2:]

            # --- make lists and dicts
            #
            self.appendList(self.dtgs,dtg)
            self.appendList(self.stm2ids,stm2id)
            self.appendList(self.aids,aid)

            self.appendDictList(self.stmdtgs,stm2id,dtg)
            self.appendDictList(self.aiddtgs,(aid,stm2id),dtg)
            self.appendDictList(self.aidstms,aid,stm2id)
            self.appendDictList(self.aidtaus,(aid,stm2id,dtg),itau)

            self.append2KeyDictList(self.aidcards,(aid,stm2id),dtg,card)
            #self.append3KeyDictList(self.aidtrks,(aid,stm2id),dtg,itau,iposit)
            self.append3TupleKeyDictList(iposits,(aid,stm2id),dtg,itau,iposit)

            ncards=ncards+1
            
        kk=iposits.keys()
        kk.sort()
        for k in kk:
            k1=k[0]
            k2=k[1]
            k3=k[2]
            posits=iposits[k]
            
            r34Final=r50Final=r64Final=None
            
            if(len(posits) == 1):
                iposit=posits[0]
                if(verb):
                    print '1111111111',k1,k2,k3,'111: ',iposit
                
            elif(len(posits) == 2):
                
                iposit1=posits[0]
                iposit2=posits[1]
                
                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                if(verb):
                    print '2222222222',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '2222222222 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '2222222222 r342:',r342,' r502: ',r502,' r642: ',r642
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642

                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                iposit=tuple(iposit)

                
            elif(len(posits) == 3):

                iposit1=posits[0]
                iposit2=posits[1]
                iposit3=posits[2]

                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                r343=iposit3[-3]
                r503=iposit3[-2]
                r643=iposit3[-1]
                
                if(verb):
                    print '33333333',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '33333333 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '33333333 r342:',r342,' r502: ',r502,' r642: ',r642
                    print '33333333 r343:',r343,' r503: ',r503,' r643: ',r643
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                if(r343 != None): r34Final=r343
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                if(r503 != None): r50Final=r503
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642
                if(r643 != None): r64Final=r643
                
                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                
                iposit=tuple(iposit)
                
            if(verb): print 'FFFFFFFFF ',k1,k2,k3,iposit
            
            self.append3KeyDictList(self.aidtrks,k1,k2,k3,iposit)
                
        # --- uniq
        #

        self.dtgs=self.uniq(self.dtgs)
        self.aids=self.uniq(self.aids)
        self.stm2ids=self.uniq(self.stm2ids)
        self.uniqDictList(self.aidtaus)

        for stm2id in self.stm2ids:
            temp=self.uniq(self.stmdtgs[stm2id])
            self.stmdtgs[stm2id]=temp

        for aid in self.aids:
            for stm2id in self.stm2ids:
                try:
                    temp=self.uniq(self.aiddtgs[aid,stm2id])
                    self.aiddtgs[aid,stm2id]=temp
                except:
                    iok=0

        for aid in self.aids:
            self.aidstms[aid]=self.uniq(self.aidstms[aid])


        for stm2id in self.stm2ids:
            self.stm1ids.append(stm2idTostm1id(stm2id))

        self.dtgs.reverse()
        self.aids.sort()

        self.naids=len(self.aids)
        self.ndtgs=len(self.dtgs)

    #eeeeeeeeeeeeeeeee end of initAdeck methed




    def relabelAidcards(self,warn=1):

        for (aid,stm2id) in self.aiddtgs.keys():
            dtgs=self.aiddtgs[aid,stm2id]
            snum=int(stm2id[2:4])
            for dtg in dtgs:
                acards=self.aidcards[aid,stm2id][dtg]
                tau0=self.aidtaus[aid,stm2id,dtg][0]
                posit0=self.aidtrks[aid,stm2id][dtg][tau0]

                if(tau0 != 0 and warn):
                    print 'WWW AD.Adeck.relabelAidcards() initial tau for aid: ',aid,' stm2id: ',stm2id,' dtg: ',dtg,' tau0: ',tau0,' posit0: ',posit0,' MISSING'

                if(int(snum) >= 90 and int(snum) <=99):
                    alat=posit0[0]
                    alon=posit0[1]
                    self.relabel9X(stm2id,dtg,alat,alon)
                    if(self.gothit):
                        self.relabelAcards(acards,aid,stm2id,dtg)


    def getAiddtgsFromAidcards(self,tag=''):

        aiddtgs={}
        kk=self.aidcards.keys()
        kk.sort()
        for k in kk:
            (aid,stm2id)=k
            bnum=int(stm2id[2:4])
            if(bnum >= 80): continue
            kkk=self.aidcards[k]
            dtgs=kkk.keys()
            dtgs.sort()
            aiddtgs[k]=dtgs

        return(aiddtgs)


    def cmpAiddtgs(self,Bdtgs,Adtgs):
        astms=Adtgs.keys()
        bstms=Bdtgs.keys()

        allstms=astms+bstms
        allstms=self.uniq(allstms)

        for stm in allstms:
            try:    bds=Bdtgs[stm]
            except: bds=[]

            try:    ads=Adtgs[stm]
            except: ads=[]

            try:    aldtg=ads[-1]
            except: aldtg='None      '

            try:    bldtg=bds[-1]
            except: bldtg=' --None--  '

            print 'Stm: ',stm,"Before: %3d  After: %3d   Bldtg: %s  Aldtg: %s "%(len(bds),len(ads),bldtg,aldtg)



    def lsAidcards(self,tag='',dtgopt=None,warn=0):

        if(dtgopt != None):
            dtgs=dtg_dtgopt_prc(dtgopt,ddtg=6)

        # -- new method to print the cards
        #
        if(hasattr(self,'acards')):
            
            kk=self.acards.keys()
            kk.sort()
    
            for k in kk:
                if(dtgopt == None or (dtgopt != None and  k in dtgs) ):
                    print
                    print 'bdtg: ',k,' aid: ',self.aid
                    cc=self.acards[k]
                    for c in cc:
                        print c[:-1]

        elif( (hasattr(self,'aidcards') and self.aidcards != None) and 
              (hasattr(self,'aiddtgs') and self.aiddtgs != None)
              ):

            # -- older form
            kk=self.aidcards.keys()
    
            for (aid,stm2id) in kk:
                bnum=int(stm2id[2:4])
                if(bnum >= 80): continue
                dtgs=self.aiddtgs[aid,stm2id]
                snum=stm2id[2:4]
                for dtg in dtgs:
                    print
                    print 'bdtg: ',dtg,' aid: ',self.taid
                    acards=self.aidcards[aid,stm2id][dtg]
                    for acard in acards:
                        print acard[0:156],'...'
                    #taus=self.aidtaus[aid,stm2id,dtg]
                    #posits=self.aidtrks[aid,stm2id][dtg]
                    
        else:
            if(warn):
                print   
                print 'IIIIIIIII' 
                print 'IIIIIIIIIIIIIII adCL.Adeck.lsAidcards -- no acards in newer AD for ',self.taid
                print 'IIIIIIIII' 
                


    def relabel9X(self,stm2id,dtg,alat,alon,verb=0):

        try:
            #tcs=self.mD.stm2dtg[dtg]
            tcs=self.mD.getTC2idsFromDtg(dtg,dofilt9x=1)
        except:
            print 'WWW no tcs for stm2id: ',stm2id,' for dtg: ',dtg
            self.gothit=0
            self.nstm2id=stm2id
            return


        stms=tcs.keys()

        distmin=1e20
        gothit=0
        for stm in stms:
            tt=tcs[stm]
            blat=tt[0]
            blon=tt[1]
            dist=gc_dist(blat,blon,alat,alon)
            if(dist < distmin):
                distmin=dist
                stm2idmin=stm

            if(verb): print 'RRRRRRRR ',stm2id,stm,dtg,alat,alon,blat,blon,dist,self.distminHIT,self.distminHIT9X
            if(distmin < self.distminHIT or
               (stm2id[2] == '9' and (distmin < self.distminHIT9X)) ):
                gothit=1


        if(gothit):
            if(verb): print 'HHHHHHHHHHH(relabel9X) ','stm2id: ',stm2id,' ==> nstm2id: ',stm2idmin," distmin: %6.2f"%(distmin),' dtg: ',dtg

        else:
            gohit=0
            stm2idmin=stm2id
            if(self.warn):
                print 'WWW in AD: could not find storm for stm2id: ',stm2id,' do not set here... ',alat,alon,dtg

        self.gothit=gothit
        self.nstm2id=stm2idmin



    def relabelAcards(self,acards,aid,stm2id,dtg):

        isnum=stm2id[2:4]

        ob2id=stm2id[0:2].upper()
        osnum=self.nstm2id[2:4]

        ostmid="%s, %s, "%(ob2id,osnum)

        #print '---------------------------------------------: ',ostmid,self.nstm2id,len(acards)

        ocards=[]
        for card in acards:
            istmid="%s, %s, "%(card[0:2],isnum)
            ncard=card.replace(istmid,ostmid)
            ocards.append(ncard)

        for ocard in ocards:
            self.append2KeyDictList(self.aidcards,(aid,self.nstm2id),dtg,ocard)


    def getAidTrk(self):


        try:
            ats=self.ats
        except:
            ats={}


        if(len(ats) == 0):
            AT=AidTrk()
            if(hasattr(self,'taid')):
                AT.aid=self.taid
            else:
                AT.aid='undef'
            return(AT)

        trks=ats

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)

        if(hasattr(self,'taid')):
            AT.aid=self.taid
        else:
            AT.aid='undef'

        if(hasattr(self,'tstmid')):
            AT.stmid=self.tstmid
        else:
            AT.stmid='undef'

        return(AT)


    def getBestTrk(self):

        from tcCL import BestTrk
        
        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            if(hasattr(self,'tstmid')):
                BT.stmid=self.tstmid
            else:
                BT.stmid='undef'
        else:
            BT=BestTrk()
            BT.stmid='undef'

        return(BT)



    def GetAidTrks(self,aid,stm2id=None,stm1id=None,verb=0):


        if(stm2id == None and stm1id != None): stm2id=stm1idTostm2id(stm1id)
        if(stm1id == None and stm2id != None): stm1id=stm2idTostm1id(stm2id)

        try:
            trks=self.aidtrks[aid,stm2id]
        except:
            trks={}


        if(len(trks) == 0):
            AT=AidTrk()
            AT.aid=aid
            AT.stmid=stm1id
            return(AT)

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)
        AT.aid=aid
        AT.stmid=stm1id

        return(AT)


    def getBestTrks(self,stm1id):


        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            BT.stmid=stm1id
        else:
            BT=BestTrk()

        return(BT)



    def GetAidStmids(self,taid):

        stmids=[]

        try:
            stm2ids=self.aidstms[taid]
        except:
            stm2ids=[]

        for tstm in stm2ids:
            stm1id=self.getAidStm1idFromStm2id(taid,tstm)
            if(stm1id != None):
                stmids.append(stm1id)

        stmids=self.uniq(stmids)

        return(stmids)


    def GetAidCards(self,aid,stm1id):

        try:
            stm2ids=self.stm1ids[stm1id.lower()]
        except:
            stm2id=stm1idTostm2id(stm1id.lower())
            stm2ids=[stm2id]

        stm2ids.sort()

        allcards={}

        for stm2id in stm2ids:
            try:
                acards=self.aidcards[aid,stm2id]
            except:
                acards={}

            allcards=self.DictAdd(allcards,acards,priority=1)

        return(allcards)



    def GetEaids(self,model,dtg=None,ncepSource='adeck',verb=0):

        iaids=self.aids
        eaids=[]
        if(model == 'esrl'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'F8' and iaid[2:4].isdigit()) or iaid[0:4].upper() == 'F8EM' ):
                    eaids.append(iaid)

        elif((model == 'ncep' or model == 'nhc') and find(ncepSource,'adeck') ):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'AP' and iaid[2:4].isdigit()) or iaid.upper() == 'AC00'):
                    eaids.append(iaid)

        elif(find(model,'cmc') and ncepSource == 'adeck'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'CP' and iaid[2:4].isdigit()) or iaid.upper() == 'CC00'):
                    eaids.append(iaid)

        else:
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if(iaid != 'ecmt' and iaid != 'ecfx' and iaid != 'edet' and iaid != 'eanl' ):
                    eaids.append(iaid)

        eaids.sort()

        self.ensembleAids=eaids

        return(eaids)


    def GetDetaid(self,model,dtg,ncepSource='adeck',verb=0):

        iaids=self.aids

        if(model == 'esrl'):
            daid=None
            sdaids=['f9em','f8em']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ncep' and find(ncepSource,'adeck') ):
            daid=None
            sdaids=['avno','avni']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ukmo'):
            daid=None
            sdaids=['ukm','egrr']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid


        elif(model == 'cmc' and ncepSource == 'adeck'):
            daid=None
            sdaids=['cmc']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        else:
            daid='edet'

        self.deterministicAid=daid
        return(daid)



    def writeAcards(self,taids=None,tstms=None,
                    tdir='/tmp',
                    odtgs=None,
                    dowrite=0,
                    tag=None,
                    aliases=None,
                    verb=0):

        if(taids == None):
            taids=self.aids
        if(tstms == None):
            tstms=self.stm2ids


        def corrVmaxPmin(card):

            tt=card.split(',')
            vmax=tt[8]
            pmin=tt[9]

            if(vmax == ' ***'): tt[8]='    '
            if(pmin == '  -99'): tt[9]='     '

            ocard=''
            for n in range(0,len(tt)):
                t1=tt[n]
                if(n == len(tt)-1):
                    ocard="%s%s"%(ocard,t1)
                else:
                    ocard="%s%s,"%(ocard,t1)

            return(ocard)



        cards=[]

        for tstm in tstms:

            if(tag != None):  cards=[]

            for taid in taids:

                otaid=taid
                if(aliases != None):
                    for (iname,oname) in aliases:
                        if(taid.upper() == iname.upper()): otaid=oname.upper()

                acards=self.aidcards[taid,tstm]

                dtgs=acards.keys()
                dtgs.sort()

                for dtg in dtgs:
                    acds=acards[dtg]
                    for acd in acds:

                        acd=corrVmaxPmin(acd)
                        # the b2id in the adeck card is NOT changed, just the stm2id
                        # do the conversion here
                        #
                        b2id=acd[0:2]
                        b2id=basin2Chk(b2id)
                        acd=b2id+acd[2:]
                        if(aliases != None):
                            acd=acd.replace(taid.upper(),otaid)
                        if(verb): print acd[0:-1]
                        cards.append(acd)

                stm2id=tstm

                if(tag == None):
                    fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),otaid.lower())
                    MF.WriteList2File(cards,fpath,verb=1)

            if(tag != None):
                fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),tag)
                MF.WriteList2File(cards,fpath,verb=1)


class AdeckFromCards(Adeck):
    
    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,acards,
                 mD=None,
                 dtgopt=None,
                 taids=None,
                 verb=0,warn=1,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None):

        

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.cards=acards
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        self.initAdeck()


    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]

class GaProc(MFbase):
    """ object to hang a 'ga' to pass between processing objects"""

    def __init__(self,ga=None,
                 verb=0,
                 ctlpath=None,
                 Quiet=1,
                 Window=0,
                 Opts='',
                 doLogger=0,
                 Bin='grads',
                 ):

        self.ga=ga
        self.verb=verb
        self.ctlpath=ctlpath
        self.Quiet=Quiet
        self.Window=Window
        self.Opts=Opts
        self.doLogger=doLogger
        self.Bin=Bin

    def initGA(self,ctlpath=None,doreinit=0):

        # -- do grads: 1) open files; 2) get field data
        # -- decorate the GaProc (gaP) object
        #
        if(self.ga == None):
            print 'GaProc MMMMMM -- making self.ga'
            from ga2 import setGA
            ga=setGA(Opts=self.Opts,Quiet=self.Quiet,Window=self.Window,doLogger=self.doLogger,verb=self.verb,Bin=self.Bin)
            self.ga=ga
            self.ge=ga.ge
            
        else:
            ga=self.ga
            ge=self.ge

        if(doreinit): ga('reinit')

        if(self.ctlpath != None or ctlpath != None):
            if(self.ctlpath != None):
                print 'GaProc OOOOO -- open self.ctlpath: ',self.ctlpath
                ga.fh=ga.open(self.ctlpath)
            if(ctlpath != None):
                print 'GaProc OOOOO -- open ctlpath: ',ctlpath
                ga.fh=ga.open(ctlpath)

            ge=ga.ge
            ge.fh=ga.fh
            ge.getFileMeta()
            self.ga=ga
            self.ge=ga.ge

        self.gp=self.ga.gp

class InvHash(MFbase):

    def __init__(self,
                 dbname,
                 tbdir=None,
                 dbkeyLocal='inventory',
                 diag=0,
                 verb=0,
                 override=0,
                 lsInv=0,
                 unlink=0):

        MF=MFutils()
        self.dbname=dbname
        self.tbdir=tbdir

        self.dbname=dbname
        self.dbfile="%s.pypdb"%(dbname)
        if(tbdir == None):
            tbdir='/tmp'
            self.dsbdir="%s/DSs"%(tbdir)
        else:
            self.dsbdir=tbdir
            
        invPath="%s/%s"%(self.dsbdir,self.dbfile)
        MF.ChkDir(self.dsbdir,'mk')

        doDSsWrite=1
        if(lsInv): doDSsWrite=0
        
        self.DSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,
                          verb=verb,unlink=unlink,doDSsWrite=doDSsWrite)
        self.dbkeyLocal=dbkeyLocal

        if(diag): MF.sTimer('setDSs')
        try:
            self.dsL=self.DSs.getDataSet(key=self.dbkeyLocal,verb=verb)
            self.hash=self.dsL.data
        except:
            self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
            self.hash={}

        if(override): self.hash={}

        if(diag): MF.dTimer('setDSs')

    def put(self,verb=0):

        self.dsL.data=self.hash
        self.DSs.putDataSet(self.dsL,key=self.dbkeyLocal,verb=verb)


    def lsInv(self,
              models,
              dtgs,
              basins=None,
              gentaus=None,
              dogendtg=None,
              ):

        type='fcst'
        if(dogendtg): type='veri'


        kk=self.hash.keys()
        for k in kk:
            print 'key: ',k,'hash.val: ',self.hash[k]


# -- CCCCCCCCCCCCC -- lsdiag

class W2areas(MFbase):


    mapres='mres'
    pareaxl=0.4
    pareaxr=10.8
    pareayb=0.65
    pareayt=8.25
    lonW=-120.0
    lonE=0.0
    latS=-10.0
    latN=60.0
    mpval1='default'
    mpval2='default'
    mpval3='default'
    mpval4='default'
    xlint=20
    ylint=10
    xsize=W2plotXsize
    ysize=int(xsize*W2plotAspect)
    dx=1.0
    dy=1.0

    def __init__(self,
                 lonW=None,
                 lonE=None,
                 latS=None,
                 latN=None,
                 dx=None,
                 dy=None):

        if(lonW != None and lonE != None):
            self.setLons(lonW,lonE)

        if(latS != None and latN != None):
            self.setLats(latS,latN)

        self.dx=dx
        self.dy=dy
        
        if( (type(self.dx) is FloatType) and (type(self.dy) is FloatType) ):
            self.setGrid(self.dx,self.dy)

        
        

    def setLons(self,lonW,lonE):
        
        self.lonW=lonW
        self.lonE=lonE
        if(lonW < 0.0): self.lonW=lonW+360.0
        if(lonE < 0.0): self.lonE=lonE+360.0
        if(self.lonW > self.lonE): self.lonE=self.lonE+360.0

        self.dLon=self.lonE-self.lonW
        
    def setLats(self,latS,latN):
        
        self.latS=latS
        self.latN=latN
        self.dLat=self.latN-self.latS
        

    def setGrid(self,dx,dy):


        # -- E-W wrap check
        #
        wrapEW=0
        dxoffset=1.01
        if(self.lonE - self.lonW == 360.0):
            wrapEW=1
            dxoffset=0.01
        ni=(self.lonE - self.lonW)/dx + dxoffset

        dyoffset=1.01
        nj=(self.latN - self.latS)/dy + dyoffset

        self.wrapEW=wrapEW
        self.dx=dx
        self.dy=dy
        
        self.ni=int(ni)
        self.nj=int(nj)
        



class W2areaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-90.0,
                 latN=90.0,
                 dx=1.0,
                 dy=1.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)



class W2areaLant(W2areas):


    def __init__(self,
                 lonW=-120,
                 lonE=0.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaEpac(W2areas):


    def __init__(self,
                 lonW=160.0,
                 lonE=280.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)


class W2areaCpac(W2areas):


    def __init__(self,
                 lonW=120.0,
                 lonE=240.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)



class W2areaWpac(W2areas):

    def __init__(self,
                 lonW=80,
                 lonE=200.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.lonW=lonW
        self.lonE=lonE
        self.latS=latS
        self.latN=latN

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)


class W2areaSio(W2areas):

    def __init__(self,
                 lonW=10.0,
                 lonE=130.0,
                 latS=-60.0,
                 latN=10.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaNio(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=120.0,
                 latS=-10.0,
                 latN=50.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaIo(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=160.0,
                 latS=-50.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaSwpac(W2areas):

    def __init__(self,
                 lonW=120.0,
                 lonE=280.0,
                 latS=-60.0,
                 latN=20.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.latS=latS
        self.latN=latN

class W2areaShem(W2areas):

    def __init__(self,
                 lonW=30.0,
                 lonE=210.0,
                 latS=-60.0,
                 latN=10.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaPrwLant(W2areas):

    def __init__(self,
                 lonW=-100.0,
                 lonE=-10.0,
                 latS=-10.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaPrwWpac(W2areas):

    def __init__(self,
                 lonW=100.0,
                 lonE=200.0,
                 latS=-10.0,
                 latN=45.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

class ctlProps(MFbase):


    def __init__(self,ctlpath,verb=0):

        siz=MF.GetPathSiz(ctlpath)
        if(siz == None or siz == 0):
            print 'EEE WxMAP2.ctlProps: ctlpath: ',ctlpath,' siz: ',siz
            return

        self.path=ctlpath
        
        cards=open(ctlpath).readlines()

        
        for n in range(0,len(cards)):
            
            card=cards[n].lower()
            
            if(verb): print 'cccCtlCard ',card[:-1]

            if(mf.find(card,'xdef')):
                tt=card.split()
                self.nx=tt[1]
                self.xtype=tt[2]
                self.blon=float(tt[3])
                self.dlon=float(tt[4])
            
            if(mf.find(card,'ydef')):
                tt=card.split()
                self.ny=tt[1]
                self.ytype=tt[2]
                if(self.ytype == 'linear'):
                    self.blat=float(tt[3])
                    self.dlat=float(tt[4])
                else:
                    self.lats=[]
                    n1=3
                    for nn in range(n+1,len(cards)):
                        card1=cards[nn].lower()
                        #print 'nnnnn ',nn,n1,card1[0:-1]
                        if(mf.find(card1,'def')):
                            break
                        elif(n1 == 0):
                            tt=card1.split()
                            for i in range(n1,len(tt)):
                                self.lats.append(float(tt[i]))
                            n=n+1
                            n1=0
                        elif(n1 == len(tt)):
                            n1=0
                            n=n+1
                            continue
                        else:
                            for i in range(n1,len(tt)):
                                self.lats.append(float(tt[i]))
                            n=n+1
                            n1=0
                                
                    self.blat=self.lats[0]
                    self.dlat=self.lats[-1]-self.lats[-2]
                    continue
            
            if(mf.find(card,'zdef')):
                self.levs=[]
                tt=card.split()
                self.nz=tt[1]
                self.ztype=tt[2]
                if(self.ztype == 'linear'):
                    self.blev=float(tt[3])
                    self.dlev=float(tt[4])

                else:
                    # -- assume all levels on one card
                    for i in range(3,len(tt)):
                        self.levs.append(float(tt[i]))

            
class TcBasin(MFbase):


    def __init__(self,basin=None):

        if(basin == None):
            self.basin=None
            self.parea=None
        else:
            self.getBasinPareaFromBasin(basin)

    def getBasinPareaFromStm1id(self,stm1id):

        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm1id)
        basin=Basin1toFullBasin[b1id]
        self.getBasinPareaFromBasin(basin)
        return(self.parea)

    def isMidSeason(self,basin,dtg):
        
        rc=0
        mm=int(dtg[4:6])
        
        if(mf.find(basin,'wpac')):
            if(mm >= 7 and mm <=10): rc=1

        if(mf.find(basin,'epac')):
            if(mm >= 8 and mm <=9): rc=1
            
        if(mf.find(basin,'lant')):
            if(mm >= 7 and mm <=9): rc=1
            
        return(rc)
    

    def getBasinPareaFromBasin(self,basin):

        if(mf.find(basin,'epac')):

            self.basin='epac'
            self.parea='tropepac'
            self.tropicalLats=[-25,25]
            self.tropicalLatsMidSeason=[-30,30]

        elif(mf.find(basin,'cpac')):

            self.basin='cpac'
            self.parea='tropcpac'
            self.tropicalLats=[-25,25]


        elif(mf.find(basin,'wpac')):

            self.basin='wpac'
            self.parea='tropwpac'
            self.tropicalLats=[-25,25]
            self.tropicalLatsMidSeason=[-30,30]


        elif(mf.find(basin,'lant')):

            self.basin='lant'
            self.parea='troplant'
            self.tropicalLats=[-25,30]
            self.tropicalLatsMidSeason=[-30,35]
            

        elif(mf.find(basin,'slant')):

            self.basin='slant'
            self.parea='tropslant'
            self.tropicalLats=[-25,25]
            

        elif(mf.find(basin,'nio')):
            self.basin='nio'
            self.parea='tropnio'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'sio')):
            self.basin='sio'
            self.parea='tropsio'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'swpac')):
            self.basin='swpac'
            self.parea='tropswpac'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'shem')):

            self.basin='shem'
            self.parea='tropshem'
            self.tropicalLats=[-25,25]
        

    def getBasinFromLatLon(self,lat,lon):

        self.isepac=( (lon >= 276 and lon <= 282 and lat <  9 ) or
                    (lon >= 273 and lon <  276 and lat < 12 ) or
                    (lon >= 267 and lon <  273 and lat < 15 ) or
                    (lon >= 261 and lon <  267 and lat < 17 ) or
                    (lon >= 180 and lon <  261 and lat >  0)
                    )

        self.isepacTC=( (lon >= 276 and lon <= 282 and lat <  9 ) or
                    (lon >= 273 and lon <  276 and lat < 12 ) or
                    (lon >= 267 and lon <  273 and lat < 15 ) or
                    (lon >= 261 and lon <  267 and lat < 17 ) or
                    (lon >= 160 and lon <  261 and lat >  0)
                    )
        
        self.iscpac=( (lon >= 180 and lon <= 220) and lat >=  0 )
        

        self.islant=( (lon >= 276 and lon <= 282 and lat >=  9 ) or
                    (lon >= 273 and lon <  276 and lat >= 12 ) or
                    (lon >= 267 and lon <  273 and lat >= 15 ) or
                    (lon >= 261 and lon <  267 and lat >= 17 ) or
                    (lon >= 276 and lon <= 360 and lat >   0 ) 
                    )
        
        self.iswpac=( (lon >= 100 and lon <= 180) and lat >=  0 )
        
        self.iswpacTC=( (lon >= 100 and lon <= 200) and lat >=  0 )
        
        self.isnio=( (lon >= 40 and lon <= 100) and lat >=  0 )
        
        self.isshem=( (lon >= 35 and lon <= (360-150)) and lat <  0 )


        self.llbasin=None
        
        if(self.isepac):  self.llbasin='epac'
        if(self.iscpac):  self.llbasin='cpac'
        if(self.iswpac):  self.llbasin='wpac'
        if(self.islant):  self.llbasin='lant'
        if(self.isnio):   self.llbasin='nio'
        if(self.isshem):  self.llbasin='shem'

        if(self.basin == None):

            if(self.llbasin == None):
                print "EEE in tc2.TcBAsin.getBasinFromLatLon: problem lat/lon: ",lat,lon
                sys.exit()

            self.getBasinPareaFromBasin(self.llbasin)


    def isLLin(self,lat,lon,doTC=0):

        self.getBasinFromLatLon(lat,lon)
        
        if(self.basin == 'epac'):
            if(doTC and hasattr(self,'isepacTC')): return(self.isepacTC)
            return(self.isepac)

        elif(self.basin == 'lant'):
            return(self.islant)

        elif(self.basin == 'wpac'):
            if(doTC and hasattr(self,'iswpacTC')): return(self.iswpacTC)
            return(self.iswpac)

        elif(self.basin == 'nio'):
            return(self.isnio)

        elif(self.basin == 'shem'):
            return(self.isshem)

    def isLatTropical(self,lat,dtg=None,override=0):
        
        if(override):
            rc=1
            return(rc)
        
        rc=0
        tlat0=self.tropicalLats[0]
        tlat1=self.tropicalLats[1]
        
        if(dtg != None):
            
            if(self.isMidSeason(self.basin,dtg) and hasattr(self,'tropicalLatsMidSeason')):
                tlat0=self.tropicalLatsMidSeason[0]
                tlat1=self.tropicalLatsMidSeason[1]
                

        if(lat >= tlat0 and lat <= tlat1): rc=1
        return(rc)


class f77GridOutput(MFbase):

    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine
    
    rexopt='linear'
    reyopt='linear'

    outDatType='f77'
    pcntundefMax=10.0
    diag=0  # -- diagnostic prints
    
    def __init__(self,model,dtg,
                 area=None,
                 taus=None,
                 vars=None,
                 doregrid=1,
                 tdir='mftrk',
                 doLogger=0,
                 tauoffset=0,
                 Quiet=1,
                 doByTau=1,
                 pcntundefMax=pcntundefMax,
                 prcdir='/tmp',
                 filename='Zy0x1W2',
                 ):

        self.model=model
        self.dtg=dtg
        self.area=area
        self.taus=taus
        self.tauoffset=tauoffset
        self.vars=vars
        self.doregrid=doregrid
        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.doByTau=doByTau
        self.pcntundefMax=pcntundefMax
        self.prcdir=prcdir
        
        self.initVars()
        self.setCtl(tdir=tdir)
        self.setOutput(filename=filename)


    def initVars(self,undef=1e20):
        
        if(self.area == None): self.area=W2areaGlobal()

        if(self.vars == None): self.vars=['uas.uas.0.-999.-999.uas [m/s]',
                                          'vas.vas.0.-999.-999.vas [m/s]',
                                          'vrt8.(hcurl(ua,va)*1e5).850.-999.-999.rel vort 850 [*1e5 /s]',
                                          ]

        self.dpaths={}

        self.undef=undef
        
        if(self.taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)

        else:

            self.btau=taus[0]
            self.etau=taus[-1]
            self.dtau=6
            if(len(taus) > 1): self.dtau=taus[-1]-taus[-2]
            self.tunits='hr'


        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None

        

    def setCtl(self,ctlpath=None,tbdir=None,tdir=None,dols=0):

        self.status=1
        if(ctlpath == None):
            rc=self.getW2fldsRtfimCtlpath(self.model,self.dtg)
            isthere=rc[0]
            if(isthere):
                ctlpath=rc[1]
            else:
                print 'EEE no w2flds for model: ',self.model,' dtg: ',self.dtg
                self.status=0
                return

            (bdir,ctlfile)=os.path.split(ctlpath)
            self.ctlpath=ctlpath

        if(ctlpath != None):
            self.ctlpath=ctlpath
            
        if(hasattr(self,'tdir')):
            if(not(dols)): MF.ChkDir(self.tdir,'mk')
            return
            
                          
        if(tdir != None):
            self.tdir=tdir
            if(not(dols)): MF.ChkDir(self.tdir,'mk')

        elif(tbdir != None):
            bdir="%s/%s"%(tbdir,self.dtg)
            self.tdir="%s/%s/%s"%(tbdir,self.dtg,self.model)
            if(not(dols)): MF.ChkDir(self.tdir,'mk')
            
        return


    def setOutput(self,filename,codename='f77Output.f',f77dir='/tmp'):

        # -- output file name
        #
        self.filename=filename

        # -- output code name
        #
        if(self.outDatType == 'f77'): self.ftype='-sq'

        self.dpath="%s/%s.dat"%(self.tdir,filename)
        self.cpath="%s/%s.ctl"%(self.tdir,filename)
        self.mpath="%s/%s.meta.txt"%(self.tdir,filename)

        if(hasattr(self,'f77dir')):
            self.f77path="%s/%s"%(self.f77dir,codename)
        else:
            self.f77path="%s/%s"%(f77dir,codename)
        
        
    def makeFldMeta(self,taus=None,verb=0):

        aa=self.area

        nk=0

        if(taus == None):
            otaus=self.taus
        else:
            otaus=taus
          
        nvarsUA=0
        if(hasattr(self,'varSl')): 
            nk=len(self.varSl)
            levs=self.varSl
            nvarsUA=len(self.varSuavar)


        nvarsSfc=len(self.vars)
        if(hasattr(self,'varSsfc')):
            nvarsSfc=len(self.varSsfc)
        
##         meta="""filename: %-20s
## grid  ni: %3d  nj: %3d
## lonW: %6.2f  lonE: %6.2f
## latS: %6.2f  latN: %6.2f
## dlon: %6.3f  dlat: %6.3f
## nk: %3d"""%\
##         (self.filename,aa.ni,aa.nj,
##          aa.lonW,aa.lonE,
##          aa.latS,aa.latN,
##          aa.dx,aa.dy,
##          nk,
##          )

        # -- use q dims to get exact dims of the output grid, done in makeFldInput.setLatLonLocal()
        # -- 20170717 -- ukm2 grid > 999 points, change from %3d to %4d
        #
        meta="""filename: %-20s
grid  ni: %4d  nj: %4d
lonW: %6.2f  lonE: %6.2f
latS: %6.2f  latN: %6.2f
dlon: %6.3f  dlat: %6.3f
nk: %3d"""%\
        (self.filename,self.Gnx,self.Gny,
         self.GlonW,self.GlonE,
         self.GlatS,self.GlatN,
         self.Gdx,self.Gdy,
         nk,
         )


        if(nk > 0):
            for lev in levs:
                meta="""%s
%7.1f"""%(meta,lev)

        if(self.doByTau):
            ntaucard='ntf: %3d (N taus/file)'%(len(otaus))
        else:
            ntaucard='ntf: %3d (N taus/file)'%(1)
            
            meta="""%s
%s"""%(meta,ntaucard)

        taucard='nt: %3d (taus)'%(len(otaus))

        meta="""%s
%s"""%(meta,taucard)


        # -- 20230324 -- modify tau in meta to tau-tauoffset to handle 06/18Z ERA5 dtgs
        #
        if(self.doByTau):
            for tau in otaus:
                dtau=tau-self.tauoffset
                meta="""%s
%3d %s"""%(meta,dtau,self.dpaths[tau][-1])

        else:
            for tau in otaus:
                
                meta="""%s
%3d %s"""%(meta,tau,self.dpath)
            

        meta="""%s
nvarsSfc: %3d  nvarsUA: %3d"""%\
        (meta,
         nvarsSfc,nvarsUA,
         )


        if(hasattr(self,'varSsfc')):

            for var in self.varSsfc:
                vp=varProps(var)
                meta="""%s
%-10s %-10s %-30s"""%(meta,vp.vvar,vp.vlev,vp.vdesc)

        
        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):

            for var in self.varSuavar:
                expr=self.varSu[var][0]
                desc=self.varSu[var][1]
                meta="""%s
%-10s %-10s %-30s"""%(meta,var,'plevs',desc)
        
        else:

            for var in self.vars:
                vp=varProps(var)
                meta="""%s
%-10s %-10s %-30s"""%(meta,vp.vvar,vp.vlev,vp.vdesc)

        MF.WriteString2File(meta,self.mpath,verb=verb)

        return


    def makef77Output(self,taus=None,verb=0):

        f77='''cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c
      module f77Output

      use trkParams
      use f77OutputMeta
      use mfutils
      
      implicit none
'''

        if(hasattr(self,'varSsfc')):
            
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):

            for var in self.varSuavar:
                expr=self.varSu[var][0]
                desc=self.varSu[var][1]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s
      real*4, allocatable, dimension(:,:) :: %s"""%(f77,fldname)



        f77=f77+'''
        
      contains

      subroutine initFlds

      integer istat'''

        if(hasattr(self,'varSsfc')):
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):
            for var in self.varSuavar:
                expr=self.varSu[var][0]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s

      allocate(%s(ni,nj),stat=istat)
      if(istat.gt.0) go to 814"""%(f77,fldname)

        f77=f77+"""

      return

 814  continue
      print*,'error in allocate... '
      stop 814
      
      return
      end subroutine initFlds


      subroutine readFlds(ntau)

      integer ntau,iunittcf,ierr,ierrfld,itau,irecvv

      real undef

      character*24 qtitle

c--  initialize variables
c

      undef=1e10
      iunittcf=99

      if(ntf == 1) then
        open(iunittcf,file=trim(DataPaths(ntf)),
     $       form='unformatted',
     $       status='old',err=805)

      else

        open(iunittcf,file=trim(DataPaths(ntau)),
     $       form='unformatted',
     $       status='old',err=805)
      endif"""

        
        if(hasattr(self,'varSsfc')):
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):
            for var in self.varSuavar:
                expr=self.varSu[var][0]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s

c--       read %s
c         
      read(iunittcf,err=810,end=810) %s

      call chkfld(%s,ni,nj,undef,%f,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verbFld) then
        qtitle='%-6s input           '
        call qprntn(%s,qtitle,1,1,ni,nj,15,6)
      endif"""%(f77,fldname,fldname,fldname,self.pcntundefMax,fldname[0:6],fldname)

        f77=f77+'''
      return

 805  continue
      ierr=1
      print*,'EEEEE: error opening file in readFlds'

 810  continue
      ierr=1
      print*,'EEEEE: error reading field in readFlds'
      return

 820  continue
      ierr=1
      print*,'UUUUU: field undefined ntau: ',ntau

      return

      end subroutine readFlds


      subroutine chkfld(a,ni,nj,undef,pcntundefMax,ierr)

      real undef
      real*4 a,pcntundef,pcntundefMax
      integer i,j,ierr,nundef,ntot,ni,nj

      dimension a(ni,nj)

      ntot=ni*nj
      ierr=0
      nundef=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) then
            nundef=nundef+1
          endif
        end do
      end do

      pcntundef=float(nundef)/float(ntot)

      
      if(pcntundef >= pcntundefMax) ierr=1
      
      return
      
      end subroutine chkfld


      end module f77Output'''

                


        MF.WriteString2File(f77,self.f77path,verb=verb)

        return



    def makeFldInputGA(self,Bin='grads'):

        # -- do grads: 1) open files; 2) get file data
        #
        from ga2 import setGA

        quiet=self.GAQuiet
        ga=setGA(Bin=Bin,doLogger=self.GAdoLogger,Quiet=quiet)
        ga.ge.fh=ga.open(self.ctlpath)
        ga.ge.getFileMeta()
        
        self.ga=ga
        self.ge=ga.ge

    def isGlobal(self,dlat=2):

        rc=0
        if(hasattr(self,'ge')):
            if(
                (180.0-(abs(self.ge.lat1)+abs(self.ge.lat2)) <= dlat) and
                (360.0-(abs(self.ge.lon1)+abs(self.ge.lon2)) <= dlat)
                ): rc=1

        return(rc)
        
        
    def getDpaths(self,useAvailTaus=0,ttaus=None,verb=0,bail=1):

        # -- meteo
        #
        nfields=len(self.vars)
        aa=self.area
        
        self.meteoTausDone=[]
        self.meteoTaus2Do=[]

        if(self.doByTau == 0 and self.filename != None):
            fullsiz=(nfields*len(self.taus))*aa.ni*aa.nj*4 + (nfields*len(self.taus))*8
            siz=MF.GetPathSiz(dpath)
            if(siz == fullsiz):
                self.meteoTausDone.append('all')
                self.meteoTaus2Do.append('all')
            else:
                self.meteoTausDone.append('all')
                self.meteoTaus2Do.append('all')
                

            print 'III single file with all taus: ',self.dpath
            return
        

        for tau in self.taus:

            if(ttaus != None and not(tau in ttaus)): continue

            self.dpaths[tau]=None

            # -- 20230324 -- modify tau in meteoDone to tau-tauoffset to handle 06/18Z ERA5 dtgs
            #
            ftau=tau
            ftau=tau-self.tauoffset
            
            if(self.filename != None):
                (dir,file)=os.path.split(self.dpath)
                file=file.replace('.dat','.f%03d.dat'%(ftau))
                dpath="%s/%s"%(dir,file)
                
                # -- why? onKishou because of the space in big fs "PROMISE PEGAuS"
                #
                #if(not(onKishou)): dpath=os.path.realpath(dpath)
                #dpath=os.path.realpath(dpath)
                # -- check if already done
                #

                sizmpath=MF.GetPathSiz(self.mpath)
                if(sizmpath == None): sizmpath=-999
                if(hasattr(self,'Gxb')):
                    Fni=self.Gnx
                    Fnj=self.Gny
                    fnij='Gxb'
                    
                elif(sizmpath > 0 ):
                    # get from metafile
                    #
                    mlist=MF.ReadFile2List(self.mpath,verb=verb)
                    for m in mlist:
                        if(mf.find(m,'grid')):
                            tt=m.split()
                            Fni=int(tt[2])
                            Fnj=int(tt[4])
                    fnij=self.mpath

                else:
                    Fni=aa.ni
                    Fnj=aa.nj
                    fnij='area'
                    

                    
                fullsiz=nfields*Fni*Fnj*4 + nfields*8
                fullsiz=nfields*Fni*Fnj*4 + nfields*8
                siz=MF.GetPathSiz(dpath)

                if(verb): print 'WxMAP2.getDpaths() Fni,Fnj: ',Fni,Fnj,' from: ',fnij,' nfields: ',nfields,' fullsiz: ',fullsiz,' siz: ',siz

                if(siz == fullsiz):
                    self.dpaths[tau]=(1,dpath)
                    self.meteoTausDone.append(ftau)
                    if(verb): print 'III(WxMAP2.getDpaths()) already made dpath: ',dpath,' override=0'
                else:
                    if(verb): print 'EEE(WxMAP2.getDpaths()) -- did not make full set of fields for model: ',self.model,' dpath: ',dpath
                    self.meteoTaus2Do.append(ftau)
                    self.dpaths[tau]=(0,dpath)

        self.meteoDone=0
        if(len(self.meteoTausDone) > 0 and useAvailTaus): self.meteoDone=1
        if(len(self.meteoTausDone) > 0 and len(self.meteoTaus2Do) == 0): self.meteoDone=1

        # -- oisst
        #
        nfields=3
        fullsiz=nfields*aa.ni*aa.nj*4 + nfields*8
        siz=MF.GetPathSiz(self.sstdpath)
        
        self.sstDone=0
        if(siz == fullsiz):
            self.sstDone=1
            
        rc=0
        if(self.meteoDone and self.sstDone):
            rc=1
            
        return(rc)
               

    def getVarExpr(self,var,tau,dologz=1,
                   tm1=1,tp1=1,tfm1=0.5,tfp1=0.5,verb=0):
        """ special variable -> expression handling"""

        ga=self.ga

        zthk900_600="(%s-%s)"%(self.zCpsexpr[600],self.zCpsexpr[900])
        zthk600_300="(%s-%s)"%(self.zCpsexpr[300],self.zCpsexpr[600])

        zthk900_600Tinterp="(%s-%s)"%(self.zCpsexprTinterp[600],self.zCpsexprTinterp[900])
        zthk600_300Tinterp="(%s-%s)"%(self.zCpsexprTinterp[300],self.zCpsexprTinterp[600])

        vp=varProps(var)
        expr=vp.vexpr
        
        try:
            doTinterp=self.doTinterp[tau]
        except:
            doTinterp=0
            
        # -- set vtexpr for var t interp expr for case of doing log z interp below...
        #
        vtexpr=None
        if(doTinterp):
            if(hasattr(vp,'vexprTinterp')):
                expr=vp.vexprTinterp
                if(expr != None):
                    expr=expr.replace('TM1',str(tm1))
                    expr=expr.replace('TP1',str(tp1))
                    expr=expr.replace('TFM1',str(tfm1))
                    expr=expr.replace('TFP1',str(tfp1))
                    vtexpr=expr
                
                    
            else:
                print 'EEE need to do Tinterp but vexprTinterp not in getVarExpr.varProps'
                sys.exit()
            
        if(vp.vvar == 'zthklo'):
            expr=zthk900_600
            if(doTinterp): expr=zthk900_600Tinterp

        elif(vp.vvar == 'zthkup'):
            expr=zthk600_300
            if(doTinterp): expr=zthk600_300Tinterp

        elif(vp.vvar[0] == 'z' and vp.vexpr == 'getexpr'):
            zlev=int(vp.vvar[1:])
            expr=self.zCpsexpr[zlev]
            if(doTinterp): expr=self.zCpsexprTinterp[zlev] 


        elif((vp.vvar == 'vrt925' or vp.vvar == 'vrt850' or vp.vvar == 'vrt700') and dologz):

            zlev=int(vp.vvar[-3:])
            uaxpr=ga.LogPinterp('ua',zlev)
            vaxpr=ga.LogPinterp('va',zlev)
            
            if(doTinterp):
                uaxprm1=ga.LogPinterp('ua',zlev,texpr='t-%d'%(tm1))
                vaxprm1=ga.LogPinterp('va',zlev,texpr='t-%d'%(tm1))
                uaxprp1=ga.LogPinterp('ua',zlev,texpr='t+%d'%(tp1))
                vaxprp1=ga.LogPinterp('va',zlev,texpr='t+%d'%(tp1))
                expr='(hcurl((%s+%s)*%f,(%s+%s)*%f)*1e5)'%(uaxprm1,uaxprp1,tfm1,vaxprm1,vaxprp1,tfp1)
            else:
                expr='(hcurl(%s,%s)*1e5)'%(uaxpr,vaxpr)
                

        elif(vp.vvar == 'pr'):

            prexpr=self.m2.setprvar(dtg=self.dtg,tau=tau)
            prexpr=prexpr.split('=')[1]
            expr="(%s)"%(prexpr.replace("""'""",''))
            
            # 20111102 -- bypass for ecmwf/ukm/cmc -- just use current tau -- problem is complicated expression for pr that include (t+0|1|2)
            #
            if(doTinterp
               and not(self.model == 'ecm2')
               and not(self.model == 'ecm4')
               and not(self.model == 'ecm5')
               and not(self.model == 'ukm2')
               and not(self.model == 'cmc2')
               and not(self.model == 'cgd2')
               ):
                expr=expr.replace('(t+0)','')
                expr=expr.replace('pr','(pr(t-%d)*%f + pr(t+%d)*%f)'%(tm1,tfm1,tp1,tfp1))

        elif(vp.vvar == 'prc'):

            prexpr=self.m2.setprvarc(dtg=self.dtg,tau=tau)
            prexpr=prexpr.split('=')[1]
            expr="(%s)"%(prexpr.replace("""'""",''))
            
            # 20111102 -- bypass for ecmwf/ukm/cmc -- just use current tau -- problem is complicated expression for pr that include (t+0|1|2)
            #
            if(doTinterp
               and not(self.model == 'ecm2')
               and not(self.model == 'ecm4')
               and not(self.model == 'ecm5')
               and not(self.model == 'ukm2')
               and not(self.model == 'cmc2')
               and not(self.model == 'cgd2')
               ):
                expr=expr.replace('(t+0)','')
                expr=expr.replace('pr','(pr(t-%d)*%f + pr(t+%d)*%f)'%(tm1,tfm1,tp1,tfp1))

        elif(vp.vvar == 'prw' or vp.vvar == 'prwup'):

            rhfact='0.01'
            # -- ngp2 going to ncep is now navgem as of 20130312
            #if(self.model == 'ngp2'): rhfact='1.0'
            vaporP='(esmrf(ta)*hur*%s)'%(rhfact)
            vaporP='(esmrf(const(ta,273.16,-u))*hur*%s)'%(rhfact)
            
            # -- special case of hi-res CMC
            #
            if(self.model == 'cgd2'):
                mixingR='hus'
            else:
                mixingR="0.622*(%s/(lev-%s))"%(vaporP,vaporP)
            prwexpr="vint(psl*0.01,%s,100)"%(mixingR)
            if(vp.vvar == 'prwup'):
                prwexpr="vint(const(psl,400,-a),%s,100)"%(mixingR)
            if(doTinterp):
                vaporP='(esmrf(const((ta(t-%d)*%f + ta(t+%d)*%f),273.16,-u))*((hur(t-%d)*%f + hur(t+%d)*%f)*%s))'%(tm1,tfm1,tp1,tfp1,
                                                                                                                   tm1,tfm1,tp1,tfp1,
                                                                                                                   rhfact)
                mixingR="(0.622*(%s/(lev-%s)))"%(vaporP,vaporP)
                prwexpr="vint( (psl(t-%d)*%f + psl(t+%d)*%f) * 0.01,%s,100)"%(tm1,tfm1,tp1,tfp1,mixingR)

            # -- special case
            #
            if(self.model == 'gfs2'): prwexpr='prw'
            if(self.model == 'ecmt'): prwexpr='prw'
            if(self.model == 'ecm5'): prwexpr='prw'
            if(self.model == 'era5'): prwexpr='prw'
            
            expr=prwexpr

        # -- inf zinterp flag set from varProps
        if(vp.zinterp):
            if(vtexpr != None):
                expr=ga.LogPinterp(vtexpr,vp.vlev)
            else:
                expr=ga.LogPinterp(vp.vexpr,vp.vlev)

        if(verb): print 'vvvvvvvvvvvvvvv ',vtexpr,vp.vvar,expr

        return(vp,expr)
    

    def getValidTaus(self,ratioMax=0.05,pThere=0.80,dofullChk=0,verb=0):
        
        """ find taus with undef """

        self.doTinterp={}
        self.stats={}
        
        ntaus=len(self.taus)
        
        for n in range(0,ntaus):

            tau0=self.taus[n]
            taum1=tau0
            taup1=tau0

            nm1=n
            np1=n
            
            if(n > 0):
                nm1=n-1
            if(n < ntaus-1):
                np1=n+1

            taum1=self.taus[nm1]
            taup1=self.taus[np1]

            nvalidMin=1e20
            nundefMax=-1e20

            pcntThere=[]
            
            fdtg=mf.dtginc(self.mdtg,tau0)
            for n in range(0,len(self.vars)):

                self.ga.ge.setTimebyDtg(fdtg,verb=0)
                if(hasattr(self,'getVarExpr') and dofullChk):
                    (vp,expr)=self.getVarExpr(self.vars[n],tau0)
                    varExpr=expr
                else:
                    vp=varProps(self.vars[n])
                    varExpr=vp.vexpr
                
                if(vp.vlev > 0):
                    self.ga('set lev %d'%(vp.vlev))
                else:
                    self.ga('set z 1')
    
                try:
                    self.stats[tau0]=self.ga.get.stat(varExpr)
                except:
                    if(dofullChk):
                        print 'WWWWWWWWWWWW bad stats',vp.vvar,varExpr,fdtg,' dofullChk'
                    continue
                
                nvalid=self.stats[tau0].nvalid
                nundef=self.stats[tau0].nundef

                # -- ratio of undef / total
                
                ratioundef2total=1.0
                if(nvalid > 0):
                    ratioundef2total=float(nundef)/(float(nvalid)+float(nundef))

                there=1
                if(ratioundef2total > ratioMax and  tau0 != 0): there=0
                pcntThere.append(there)

                if(nvalid < nvalidMin): nvalidMin=nvalid
                if(nundef > nundefMax): nundefMax=nundef
                
                if(verb):
                    print 'VVVVVVVVVVVVVVVV ',n,tau0,vp.vlev,varExpr,tau0,nvalid,nundef
                    print 'MMMMMMMMMMMMMMMM ',tau0,nvalidMin,nundefMax


            # -- final check if we should do an interp in time
            #
            
            self.doTinterp[tau0]=0

            # -- percent complete
            #
            nthere=len(pcntThere)
            there=0
            for t in pcntThere:
                there=there+t

            pcntComplete=0.0
            if(nthere > 0):
                pcntComplete=float(there)/float(nthere)

            if(pcntComplete < pThere):
                self.doTinterp[tau0]=1
                print 'PPP--doTinterp tau: ',tau0,pcntComplete,' pThere: ',pThere
            

            if(not(dofullChk)):
                # -- max/min undef/valid
                #
                nvalid=nvalidMin
                nundef=nundefMax
                ratioundef2valid=1.0
                if(nvalid > 0):
                    ratioundef2valid=float(nundef)/float(nvalid)
                if(ratioundef2valid > ratioMax and tau0 != 0):
                    self.doTinterp[tau0]=1
                    print 'SSS--doTinterp tau: ',tau0,self.stats[tau0].nundef
                
            ##self.stats[tau0].ls()


    def makeFldInput(self,
                     dogetValidTaus=1,
                     doconst0=0,
                     doglobal=0,
                     override=0,
                     verb=0,
                     taus=None,
                     ):


        def setLatlonGlobal():

            ge=self.ge
            
            cmd="""set lat %f %s
set lon %f %f"""%(ge.lat1,ge.lat2,ge.lon1,ge.lon2)
            ga(cmd)

        def setLatlonLocal(expand=1,getIgridDims=0):

            # -- expand data grid +/- 1point in x and y for vort calc
            # -- dregrid() uses re() to dump exact grid
            #
            aa=self.area

            dy=dx=0.0
            if(expand):
                dy=aa.dy
                dx=aa.dx
            
            flatS=aa.latS-dy
            flatN=aa.latN+dy

            if(flatS < -90.0): flatS=-90.0
            if(flatN >  90.0): flatN= 90.0

            # -- set the output dimension env
            #
            cmd="""set lat %f %s
set lon %f %f"""%(flatS,flatN,aa.lonW-dx,aa.lonE+dx)
            ga(cmd)

            # -- use grads dim env to get dims of input grid
            #
            if(getIgridDims):
                gh=ga.query('dims',Quiet=1)

                nx=gh.nx
                ny=gh.ny
                (xb,xe)=gh.xi
                (yb,ye)=gh.yi

                # -- assume cyclic continuity in x
                #
                if(xe > len(ge.lons)): xe=xe-len(ge.lons)

                lonb=ge.lons[xb-1]
                lone=ge.lons[xe-1]

                latb=ge.lats[yb-1]
                late=ge.lats[ye-1]

                # -- assum constant grid increment
                #
                self.Adx=ge.lons[-1]-ge.lons[-2]
                self.Ady=ge.lats[-1]-ge.lats[-2]

                self.Axb=xb
                self.Axe=xe

                self.Ayb=yb
                self.Aye=ye

                self.Anx=nx
                self.Any=ny

                self.Alatb=latb
                self.Alate=late

                self.Alonb=lonb
                self.Alone=lone

            

        self.varPs={}
        self.ovars=[]

        for var in self.vars:
            vp=varProps(var)
            self.ovars.append(vp.vvar)
            self.varPs[vp.vvar]=[vp.vexpr,vp.vlev,vp.afact,vp.mfact,vp.vdesc]

        self.getDpaths()

        if(self.meteoDone and not(override)):
            print """III self.meteoDone ... and not(override)...don't need to makeFldInput...return..."""
            return


        if(self.doByTau == 0):
            self.getDpaths()
            siz=MF.GetPathSiz(self.dpath)
            if(override == 0 and  (siz != None and siz > 0) and self.meteoDone == 0):
                print 'WWW doByTau=1 and self.dpath: ',self.dpath,' already exists...bail...'
                sys.exit()
            return
            
            
        if(not(hasattr(self,'ga'))):
            self.makeFldInputGA()
            
        ga=self.ga
        ge=self.ge


        # -- expressions for hart cps
        #
        zlevsCps=[900,850,800,750,700,650,600,550,500,450,400,350,300]

        self.zCpsexpr={}
        self.zCpsexprTinterp={}
        
        for zlev in zlevsCps:
            self.zCpsexpr[zlev]=ga.LogPinterp('zg',zlev)
            self.zCpsexprTinterp[zlev]=ga.LogPinterpTinterp('zg',zlev)


        # -- set undef
        #
        ga('set undef %g'%(self.undef))

        # -- get valid taus
        #
        if(dogetValidTaus):
            MF.sTimer('getValidTaus')
            self.getValidTaus(dofullChk=0,verb=0)
            MF.dTimer('getValidTaus')

        nfields=len(self.vars)
        
        ga.verb=verb

        if(self.doByTau == 0):
            ga.ge.setFwrite(name=self.dpath,type=self.ftype)
            ga('set gxout fwrite')
            alreadyDone=0

        mtaus=self.taus

        for tau in mtaus:
            
            otau=tau

            timerlab='fldtau: %s : %4s : %s : %s'%(self.areaname,otau,self.dtg,self.model)
            MF.sTimer(timerlab)

            if(self.doByTau):

                (rc,dpath)=self.dpaths[otau]
                #print 'ooooooooooooooooo',otau,rc,dpath
                if(rc == 0 or override):
                    ga.ge.setFwrite(name=dpath,type=self.ftype)
                    ga('set gxout fwrite')
                    alreadyDone=0
                else:
                    alreadyDone=1
                    continue

            # -- since we're setting time by dtg -- will automatically account for the tauOffset!
            #
            fdtg=mf.dtginc(self.dtg,tau)
            ga.ge.setTimebyDtg(fdtg)

            dologz=1
            for var in self.vars:
                # -- get expression to output; includes special variable handling
                #
                (vp,expr)=self.getVarExpr(var,tau,dologz=dologz)

                if(vp.testvar != None):
                    tvar=vp.testvar
                    if(not(tvar in ge.vars)):
                        expr="const(lat,%f,-a)"%(ge.undef)
                        if(self.diag): print 'III WxMAP2.varProps: setting: ',tvar,' to undef using expr: ',expr
                    
                # -- set the plev
                #
                if(vp.vlev > 0):
                    ga('set lev %d'%(vp.vlev))
                else:
                    ga('set z 1')

                # -- avoid conflict with grads var names and defined vars
                #
                varD=vp.vvar+'X'

                # -- set the lat/lon dim env to global and do define
                #
                if(doglobal and self.isGlobal()):
                    rc=setLatlonGlobal()
                    ga.dvar.var(varD,expr)

                    
                # -- set the lat/lon dim to local
                #
                # -- expand one grid point in all directions for 
                rc=setLatlonLocal(expand=1)
                ga.dvar.var(varD,expr)
                
                # -- apply mfact
                #
                if(vp.mfact != None and vp.mfact != -999):
                    mexpr='%s*%f'%(varD,vp.mfact)
                    ga.dvar.var(varD,mexpr)
                
                getIgridDims=0
                if(not(hasattr(self,'Gxb'))): getIgridDims=1
                
                rc=setLatlonLocal(expand=0,getIgridDims=getIgridDims)

                # -- get the exact grid dims of the output grid
                #
                if(not(hasattr(self,'Gxb'))):

                    if(self.doregrid == 0):
                        
                        self.Gxb=self.Axb
                        self.Gxe=self.Axe
                    
                        self.Gyb=self.Ayb
                        self.Gye=self.Aye
                        
                        self.Gdx=self.Adx
                        self.Gdy=self.Ady
                        
                        
                        self.Gnx=self.Anx
                        self.Gny=self.Any
                        
                        self.GlatS=self.Alatb
                        self.GlatN=self.Alate
                        
                        self.GlonW=self.Alonb
                        self.GlonE=self.Alone

                    else:

                        aa=self.area
                        
                        self.Gxb=aa.lonW
                        self.Gxe=aa.lonE
                    
                        self.Gyb=aa.latS
                        self.Gye=aa.latN
                        
                        self.Gdx=aa.dx
                        self.Gdy=aa.dy
                        
                        
                        self.Gnx=aa.ni
                        self.Gny=aa.nj
                        
                        self.GlatS=aa.latS
                        self.GlatN=aa.latN
                        
                        self.GlonW=aa.lonW
                        self.GlonE=aa.lonE
                        
                        
                if(self.reargs != None):
                    dore=1
                    if(doconst0):
                        #ga.dvar.dregrid0(vp.vvar,expr,self.reargs,undef=self.undef)
                        print '000000000000000000',varD,self.reargs
                        gacmd=ga.dvar.dregrid0(varD,varD,self.reargs,undef=self.undef)
                    else:
                        #ga.dvar.dregrid(vp.vvar,expr,self.reargs)
                        gacmd=ga.dvar.dregrid(varD,varD,self.reargs)

                else:
                    dore=0
                    if(doconst0):
                        gacmd=ga.dvar.dundef0(varD)
                    else:
                        ga('d %s'%(varD))
                        gacmd=varD

                if(verb):
                    print 'vvvvvv varD: %-20s'%(varD),' expr: ',gacmd
                    
                    
            if(self.doByTau):   ga('disable fwrite')

            
            MF.dTimer(timerlab)

        ga('disable fwrite')
        

        self.ga=ga
        self.ge=ga.ge

        if(override or alreadyDone == 0):
            self.makeCtlfile()
            self.makeFldMeta()
            self.makef77Output()


    def makeCtlfile(self):

        aa=self.area
        gtime=mf.dtg2gtime(self.dtg)

        (ddir,dfile)=os.path.split(self.dpath)

        if(self.doByTau):
            dfile=dfile.replace('.dat','''.f%f3.dat''')

        self.ctl="""dset ^%s
title test
undef %g
options sequential template
xdef %3d linear %7.2f %7.3f
ydef %3d linear %7.2f %7.3f"""%(dfile,self.undef,
            self.Gnx,self.GlonW,self.Gdx,
            self.Gny,self.GlatS,self.Gdy)

        #if(hasattr(self,'varSsfc')):

        self.makeCtlZdef()

        btau=self.taus[0]
        etau=self.taus[-1]
        if(self.dtau > 0):
            ntimes=(etau-btau)/self.dtau +1
        else:
            print 'EEE dtau in WxMAP2.f77GridOutput.makeCtlfile() '
            sys.exit()
            
        self.ctl=self.ctl+"""
%s
tdef %d linear %s %d%s"""%(
            self.zdef,ntimes,gtime,self.dtau,self.tunits,
            )
        
        self.makeCtlVars()

        MF.WriteString2File(self.ctl,self.cpath,verb=1)


    def makeCtlZdef(self):
        
        if(hasattr(self,'varSl')):
            self.zdef='zdef  %d levels'%(len(self.varSl))
            for lev in self.varSl:
                self.zdef=self.zdef+' %d'%(lev)

        else:
            self.zdef='zdef  1 levels 1013'




    def makeCtlVars(self):

        if(hasattr(self,'varSuavar') and hasattr(self,'varSl') and hasattr(self,'varSsfc') ):

            sfvars=self.varSsfc
            uavars=self.varSuavar

            self.ctl="""%s
vars %d"""%(self.ctl,len(sfvars)+len(uavars))

            for var in sfvars:
                vp=varProps(var)
                self.ovars.append(vp.vvar)
                card="%-12s %3d 0 %s"%(vp.vvar,0,vp.vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)


            for var in uavars:
                (vexpr,vlev,afact,mfact,vdesc)=self.varPs[var]
                #vexpr=self.varSu[var][0]
                #vdesc=self.varSu[var][-1]
                card="%-12s %3d 0 %s"%(var,len(self.varSl),vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)

        else:
            
            self.ctl=self.ctl+"""
vars %d"""%(
                len(self.vars),
                )

            for var in self.ovars:
                (vexpr,vlev,afact,mfact,vdesc)=self.varPs[var]
                card="%-12s 0 0 %s"%(var,vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)

        
        self.ctl="""%s
endvars"""%(self.ctl)



    def clean(self):

        try:
            os.unlink(self.dpath)
        except:
            print 'EEE unable to rm: ',self.dpath

        

class varProps(MFbase):

    def __init__(self,var=None,
                 vvar=None,
                 vexpr=None,
                 vexprTinterp=None,
                 vlev=None,
                 afact=None,
                 mfact=None,
                 vdesc=None,
                 f77name=None,
                 testvar=None,
                 ):

        if(var != None):
            
            tt=var.split(':')

            if(len(tt) == 6):
                (vvar,vexpr,vlev,afact,mfact,vdesc)=tt
            elif(len(tt) == 7):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc)=tt
            elif(len(tt) == 8):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc,f77name)=tt
            elif(len(tt) == 9):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc,f77name,testvar)=tt
                
            if(f77name == None): f77name=vvar

            zinterp=0
            if(vlev[0] == 'Z'):
                vlev=str(vlev[1:])
                zinterp=1
                
            vlev=float(vlev)
            afact=float(afact)
            mfact=float(mfact)

        self.vvar=vvar
        self.vexpr=vexpr
        self.vexprTinterp=vexprTinterp
        self.vlev=int(vlev)
        self.zinterp=zinterp
        self.afact=afact
        self.mfact=mfact
        self.vdesc=vdesc
        self.f77name=f77name
        self.testvar=testvar




# -- CCCCCCCCCCCCCCCCCCC -- Adeck
# main classes
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckSink
#

class AidTrk(MFbase):

    def __init__(self,dtgs=None,trks=None):


        if(dtgs == None):
            self.dtgs=[]
        else:
            self.dtgs=dtgs

        if(trks == None):
            self.atrks=[]
        else:
            # -- convert trks to dict of lists v tuples
            #
            otrks={}
            odtgs=[]
            for dtg in trks.keys():
                odtgs.append(dtg)

                dd=trks[dtg]
                odd={}
                for d in dd.keys():
                    odd[d]=list(dd[d])

                otrks[dtg]=odd

            odtgs=mf.uniq(odtgs)
            self.dtgs=odtgs
            self.atrks=otrks

    def getLatLonVmaxPminFromAtrk(self,atrk,tau):
        rc=atrk[tau]
        lat1=rc[0]
        lon1=rc[1]
        vmax1=rc[2]
        pmin1=rc[3]
        
        return(lat1,lon1,vmax1,pmin1)
    
    def qcMotion(self,latT=30.0,vmaxT=35.0,vmaxM=55.0,
                 stmid=None,aid=None,
                 forspdAdjfact=1.35,
                 forspdMaxTau0=24,
                 verb=0):


        spdflgT={}
        spdtauT={}
        spdflgM={}
        spdtauM={}

        xspdlog=[]

        for dtg in self.dtgs:

            otaus=[]

            taus=self.atrks[dtg].keys()
            taus.sort()
            nt=len(taus)
            atrk=self.atrks[dtg]
            otrk={}

            err=-1

            spdflgT[dtg]=0
            spdtauT[dtg]=-999
            spdflgM[dtg]=0
            spdtauM[dtg]=-999

            if(nt > 0): 
                otaus.append(taus[0])

            for n in range(0,nt):

                course=270
                speed=0.0
                tau0=taus[0]
                tau1=taus[0]

                if(nt > 1):
                    if(n == 0):
                        n0=0
                        n1=1
                    elif(n == nt-1):
                        n0=n-1
                        n1=n
                    else:
                        n0=n
                        n1=n+1

                    tau0=taus[n0]
                    tau1=taus[n1]
                    dtau=tau1-tau0

                    rc0=atrk[tau0]
                    rc1=atrk[tau1]
                    
                    (lat0,lon0,vmax0,pmin0)=self.getLatLonVmaxPminFromAtrk(atrk,tau0)
                    (lat1,lon1,vmax1,pmin1)=self.getLatLonVmaxPminFromAtrk(atrk,tau1)

                    # -- bypass bad; single points
                    #
                    #if(dtau == 0 or (lat0 == lat1 and lon0 == lon1)): continue

                    try:
                        (course,speed,eiu,eiv)=rumhdsp(lat0,lon0,lat1,lon1,dtau)
                    except:
                        print 'EEEEEEEEEEEEEEEEEEEEEEEEEEE in qcSpeed.rumhdsp(lat0,lon0,lat1,lon1,dtau): ',tau0,tau1,lat0,lon0,lat1,lon1,dtau,\
                              ' stmid: ',self.stmid,'aid: ',self.aid,' dtg: ',dtg,' setting speed to 200 to kill off...'
                        speed=200.0

                    # -- similar to tcnavytrk/mf.modues.f  and mf.trackem.f -- allow faster motion in early period
                    #
                    vmaxTcomp=vmaxT
                    if(tau0 <= forspdMaxTau0):
                        vmaxTcomp=vmaxT*forspdAdjfact

                    if(abs(lat0) <= latT and speed >= vmaxTcomp):
                        card="AidTrk(): EEExssive speed in tropics stmid: %s aid: %s dtg: %s tau0: %3d speed: %7.1f lat0: %5.1f  vmaxTcomp: %5.0f"%\
                            (self.stmid,self.aid,dtg,tau0,speed,lat0,vmaxTcomp)
                        print card
                        xspdlog.append(card)

                        err=n0
                        spdflgT[dtg]=1
                        spdtauT[dtg]=tau1


                    if(abs(lat0) > latT and speed >= vmaxM):
                        card="AidTrk(): EEExssive speed in MIDLATS stmid: %s aid: %s dtg: %s tau0: %3d speed: %7.1f lat0: %5.1f  vmaxTcomp: %5.0f"%\
                            (self.stmid,self.aid,dtg,tau0,speed,lat0,vmaxTcomp)
                        print card
                        xspdlog.append(card)

                        err=n0
                        spdflgM[dtg]=1
                        spdtauM[dtg]=tau1

                    if(err >= 0):
                        break

                    else:
                        if(n != n1):
                            otaus.append(taus[n1])


            nto=len(otaus)
            nti=len(taus)
            if(verb): print 'dddd ',dtg,' nto: ',nto,' nti: ',nti
            if(nto < nti):
                for tau in otaus:
                    otrk[tau]=atrk[tau]

                self.atrks[dtg]=otrk
                if(verb): print 'dtg',dtg,tau0,course,speed,lat0,lon0,lat1,lon1,dtau,err

        self.spdflgT=spdflgT
        self.spdtauT=spdtauT
        self.spdflgM=spdflgM
        self.spdtauM=spdtauM

        self.xspdlog=xspdlog

    def lsAT(self,stmid,dtgopt=None):

        dtgs=self.atrks.keys()
        dtgs.sort()

        tdtgs=None
        if(dtgopt != None):
            tdtgs=mf.dtg_dtgopt_prc(dtgopt)
            
        for dtg in dtgs:

            if(tdtgs != None and not(dtg in tdtgs)): continue
            atrk=self.atrks[dtg]
            print
            print stmid,dtg,'aid: ',self.aid
            taus=atrk.keys()
            taus.sort()

            for tau in taus:
                vdtg=mf.dtginc(dtg,tau)
                aa=atrk[tau]
                alat=aa[0]
                alon=aa[1]
                try:
                    r34=aa[4]
                except:
                    r34=None

                if(r34 == None):
                    or34='[-99,-99,-99,-99]'
                else:
                    or34=str(r34)

                (clat,clon)=Rlatlon2Clatlon(alat,alon)
                if(aa[2] != None): ovmax="%3.0f"%(aa[2])
                else: ovmax="---"
                if(aa[3] != None): opmin="%4.0f"%(aa[3])
                else: opmin="____"
                print "%s(%03d) %s %s %s %s %s"%(vdtg,tau,clat,clon,ovmax,opmin,or34)


class AidStruct(MFbase):

    def __init__(self,dtgs=None,trks=None):

        if(dtgs == None):
            self.dtgs=[]
        else:
            self.dtgs=dtgs

        if(trks == None):
            self.atrks=[]
        else:
            self.atrks=trks



class AdeckSink(Adeck):

    """ adeck made from 'sink' version of atcf output from gettrk_gen.x
    """
    

    def __init__(self,adeckpathmasks,mD=None,dtgopt=None,taids=None,verb=0,warn=1,
                 skipcarq=1,
                 dofilt9x=0,
                 undef=-9999.,
                 chkb2id=0,
                 aliases=None):
        
        self.lf=SetLandFrac()
        self.getlf=GetLandFrac

        # -- dectect if mask is a list...
        #
        if(type(adeckpathmasks) is ListType):
            adeckpaths=[]
            for adeckpathmask in adeckpathmasks:
                adeckpaths=adeckpaths+glob.glob(adeckpathmask)
        else:
            adeckpaths=glob.glob(adeckpathmasks)


        if(dtgopt != None):
            self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.mD=mD
        self.adecks=adeckpaths
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.aliases=aliases
        self.chkb2id=chkb2id
        self.dofilt9x=dofilt9x

        self.initVars()
        self.initAdeckPaths(adeckpaths)
        self.initAdeck(nlenmax=31)

        del self.lf
        del self.getlf

    def setAidNCard(self,tt):
        aid=tt[5].strip()
        return(aid)

    def setDtgNCard(self,tt):
        dtg=tt[3].strip()
        return(dtg)



    def makeIposit(self,tt,card,ncards,ntt,aid=None):

        tau=tt[6].strip()
        itau=int(tau)

        clat=tt[7].strip()
        clon=tt[8].strip()

        if(tt[9].strip() == "***" or tt[9].strip() == "****"):
            vmax=-999
        else:
            vmax=float(tt[9])

        # -- check if vmax==0
        # 
        if(vmax == 0.0): vmax=self.undef
        try:
            (alat,alon)=Clatlon2Rlatlon(clat,clon)[0:2]
        except:
            print 'WWW gooned up clat,clon: ',ncards,card[0:-1],ntt
            return(None,None)

        if(alat == 0.0 and alon == 0.0 and (vmax == 0.0 or vmax == self.undef) ):
            if(self.verb): print 'NOLOAD: ',card[:-1]
            return(None,None)

        try:
            pmin=float(tt[10])
        except:
            pmin=self.undef

        if(pmin == 0.0): pmin=self.undef

        if(tt[18].strip() == "****"):
            poci=-999
        else:
            poci=float(tt[18].strip())

        try:    roci=float(tt[19].strip())
        except: roci=float(tt[19].strip())

        try:    rmax=float(tt[20].strip())
        except: rmax=float(tt[20].strip())

        try:    dir=float(tt[21].strip())
        except: dir=self.undef

        try:    spd=float(tt[22].strip())
        except: spd=self.undef

        try:    cpsB=float(tt[23].strip())
        except: cpsB=self.undef

        try:    cpsVTl=float(tt[24].strip())
        except: cpsVTl=self.undef

        try:    cpsVTu=float(tt[25].strip())
        except: cpsVTu=self.undef

        try:    z8mean=float(tt[26].strip())
        except: z8mean=self.undef

        try:    z8max=float(tt[27].strip())
        except: z8max=self.undef

        try:    z7mean=float(tt[28].strip())
        except: z7mean=self.undef

        try:    z7max=float(tt[29].strip())
        except: z7max=self.undef

        name=tt[30].strip()

        # -- put lf (landfrac) into the posit
        #

        alf=self.getlf(self.lf,alat,alon)
        # -- bug in doc on marchok 'sink' format lower then upper for cpsV
        # -- doc has upper/lower; code has it other way

        iposit=(alat,alon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTl,cpsVTu,z8mean,z8max,z7mean,z7max)

        return(itau,iposit)



    def GetAidStruct(self,aid,stm2id=None,stm1id=None,verb=0):

        if(stm2id == None and stm1id != None): stm2id=stm1idTostm2id(stm1id)
        if(stm1id == None and stm2id != None): stm1id=stm2idTostm1id(stm2id)

        try:
            trks=self.aidtrks[aid,stm2id]
        except:
            trks={}


        if(len(trks) == 0):
            AT=AidStruct()
            AT.aid=aid
            AT.stmid=stm1id
            return(AT)

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidStruct(dtgs,trks)
        AT.aid=aid
        AT.stmid=stm1id

        return(AT)



class MDdataset(MFbase):

    undef=-999.
    
    def __init__(self,dtgs,stm2id):

        self.dtgs=dtgs
        self.stm2id=stm2id
        self.stm1id=stm2idTostm1id(stm2id)
        
        self.cq00={}
        self.cq12={}
        self.cq24={}
        self.best={}
        self.wrng={}
        self.of00={}
        self.of03={}
        self.of12={}
        self.of24={}


    def setMDtrk(self,verb=0,docq00=1,btonly=0,only6h=1,useVmax4TcCode=1,
                 dob1idSet=0):

        # -- look for breaks in the dtg
        #
        self.dtgs=self.chkDtgBreaks(self.dtgs,verb=verb)
        
        dtgs=self.dtgs
        dtgs.sort()

        ndtgs=len(dtgs)

        if(only6h):
            dtgs=[]
            for dtg in self.dtgs:
                ihmod=int(dtg[8:10])%6
                if(ihmod == 0):
                    dtgs.append(dtg)
            self.dtgs=dtgs

        self.trk={}
        self.btdtgs=[]

        # -- check to make sure there is eighter carq0 or bt0
        #
        
        idtgs=[]
        for dtg in dtgs:
            c0=None
            try:     c0=self.cq00[dtg]
            except:  None
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(c0 == None and bt== None):
                print 'WWWW no c0 or bt for stmid: ',self.stm1id,' dtg: ',dtg
            else:
                idtgs.append(dtg)

        dtgs=idtgs
        self.dtgs=idtgs

        dtgs.sort()
        self.dtgs.sort()
        ndtgs=len(self.dtgs)

        # -- get btdtgs
        #

        for dtg in dtgs:
            
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(bt == None): continue
            self.btdtgs.append(dtg)

            
        if(btonly):
            dtgs=self.btdtgs
            ndtgs=len(dtgs)
            self.dtgs=dtgs

        # -- get b1id

        b1ids=[]
        b1id=None
        sname=None
        
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            
            if(c0 == None): continue
            if(hasattr(c0,'b1id')):
                if(c0.b1id != c0.undef): 
                    b1id=c0.b1id
                    b1ids.append(b1id)

        # -- check for case where beginning b1d in the carq card is different from the end
        #
        if(dob1idSet):
            if(len(b1ids) == 1): 
                b1id=b1ids[0]
            
            elif(len(b1ids) > 1):
                bb1id=b1ids[0]
                # -- check for multiple  b1ids in the CARQ, e.g., wpac -> IO
                for tb1 in b1ids[1:]:
                    if(tb1 != bb1id):
                        print
                        print
                        for x in range(0,5):
                            print 'WWWW---- b1id changes for stm1id: ',self.stm1id,'... use the first one: ',bb1id
                        print
                        print
                        break
                    
                b1id=bb1id
                    
            

                        

        ntrk=0
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            c12=None
            try:     c12=self.cq12[dtg]
            except:  None

            c24=None
            try:     c24=self.cq24[dtg]
            except:  None

            bt=None
            try:     bt=self.best[dtg]
            except:  None

            o0=None
            try:     o0=self.of00[dtg]
            except:  None

            o12=None
            try:     o12=self.of12[dtg]
            except:  None

            o24=None
            try:     o24=self.of24[dtg]
            except:  None

            w0=None
            try:     w0=self.wrng[dtg]
            except:  None

            lf=rlat=rlon=vmax=pmin=spd=dir=tccode=r34m=r50m=sname=None
            clf=crlat=crlon=cvmax=cpmin=cspd=cdir=ctccode=cr34m=cr50m=csname=None
            blf=brlat=brlon=bvmax=bpmin=bspd=bdir=btccode=br34m=br50m=bsname=None
            depth=cdepth=bdepth=None
            r34=cr34=br34=r50=cr50=br50=None
            poci=cpoci=bpoci=None
            roci=croci=broci=None
            rmax=crmax=brmax=None


            if(verb):
                print 'DDDDDDD',dtg
                if(c0 != None):
                    print 'CCC000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(w0 != None):
                    print 'WWW000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(c12 != None):
                    print 'CCC1212'
                    c12.ls('lat')
                    c12.ls('lon')
                    c12.ls('vmax')
                if(bt != None):
                    print 'BBB000'
                    bt.ls('lat')
                    bt.ls('lon')
                    bt.ls('vmax')
            
                if(o0 != None):
                    print 'OOO000'

                if(o24 != None):
                    print 'OOO2424'

                if(o12 != None):
                    print 'OOO1212'

            if(o0 != None or w0 != None or o12 != None or o24 != None):
                wncode='WN'
                wtccode='TW'
            else:
                wncode='NW'
                wtccode=None
                
            ntrk=ntrk+1
            tdo='---'
            alf=None
            postype='X'
            
            
            if(o0 != None):
                if(hasattr(o0,'tdo')):
                    tdo=o0.tdo

            if(c0 != None):
                crlat=c0.rlat
                crlon=c0.rlon
                if(hasattr(c0,'vmax')): cvmax=c0.vmax
                if(hasattr(c0,'pmin')): cpmin=c0.pmin
                if(hasattr(c0,'dir')):  cdir=c0.dir
                if(hasattr(c0,'spd')):  cspd=c0.spd
                if(hasattr(c0,'r34m')):  cr34m=c0.r34m
                if(hasattr(c0,'r50m')):  cr50m=c0.r50m
                if(hasattr(c0,'tccode')):
                    if(c0.tccode != self.undef): ctccode=c0.tccode
                if(hasattr(c0,'alf')):  clf=c0.alf
                if(hasattr(c0,'sname')):  csname=c0.sname
                if(hasattr(c0,'depth')):  cdepth=c0.depth
                if(hasattr(c0,'r34')):    cr34=c0.r34
                if(hasattr(c0,'r50')):    cr50=c0.r50
                if(hasattr(c0,'poci')):   cpoci=c0.poci
                if(hasattr(c0,'roci')):   croci=c0.roci
                if(hasattr(c0,'rmax')):   crmax=c0.rmax

            crlatm12=crlonm12=None
            if(c12 != None):
                crlatm12=c12.rlat
                crlonm12=c12.rlon
                
            # -- calc CARQ motion from tau-12 to tau using CARQ posits
            #
            if(c0 != None and cdir == None and crlatm12 != None and crlonm12 != None):
                dt=12
                (cdir,cspd,umotion,vmotion)=rumhdsp(crlatm12,crlonm12,crlat,crlon,dt)
                postype='c'
            elif(c0 != None and cdir != None):
                postype='C'

            if(c0 != None and cdir == None):
                postype='b'


            if(bt != None):
                brlat=bt.rlat
                brlon=bt.rlon
                
                if(hasattr(bt,'vmax')): bvmax=bt.vmax
                if(hasattr(bt,'pmin')): bpmin=bt.pmin
                if(hasattr(bt,'dir')): bdir=bt.dir
                if(hasattr(bt,'spd')): bspd=bt.spd
                if(hasattr(bt,'tccode')):
                    if(bt.tccode != self.undef):  btccode=bt.tccode
                if(hasattr(bt,'r34m')):  br34m=bt.r34m
                if(hasattr(bt,'r50m')):  br50m=bt.r50m
                if(hasattr(bt,'alf')):   blf=bt.alf
                if(hasattr(bt,'sname')): bsname=bt.sname
                if(hasattr(bt,'depth')): bdepth=bt.depth
                if(hasattr(bt,'r34')):   br34=bt.r34
                if(hasattr(bt,'r50')):   br50=bt.r50
                if(hasattr(bt,'poci')):  bpoci=bt.poci
                if(hasattr(bt,'roci')):  broci=bt.roci
                if(hasattr(bt,'rmax')):  brmax=bt.rmax



            if(docq00):

                if(crlat != None): rlat=crlat
                if(crlon != None): rlon=crlon
                if(cvmax != None): vmax=cvmax
                if(cpmin != None): pmin=cpmin
                if(cdir  != None): dir=cdir
                if(cspd  != None): spd=cspd
                if(ctccode != None): tccode=ctccode
                if(cr34m   != None): r34m=cr34m
                if(cr34    != None): r34=cr34
                if(cr50m   != None): r50m=cr50m
                if(cr50    != None): r50=cr50
                if(clf     != None): alf=clf
                if(cdepth  != None): depth=cdepth
                if(cpoci   != None): poci=cpoci
                if(croci   != None): roci=croci
                if(crmax   != None): rmax=crmax

                # -- fallback to bt
                #
                if(rlat == None): 
                    rlat=brlat
                if(rlon == None): 
                    rlon=brlon
                    postype='b'
                    
                # -- check if undef too when it's 0 in bdeck -> undef
                #
                if(vmax == None or vmax == self.undef): vmax=bvmax
                if(pmin == None or pmin == self.undef): pmin=bpmin
                if(alf  == None): alf=blf
                if(cdepth == None): depth=bdepth
                if(ctccode == None): tccode=btccode

                if(r34m == None and br34m != None): r34m=br34m
                if(r34  == None and br34  != None): r34=br34
                if(r50  == None and br50  != None): r50=br50
                if(poci == None and bpoci != None): poci=bpoci
                if(roci == None and broci != None): roci=broci
                if(rmax == None and brmax != None): rmax=brmax
                

            if(btonly):
                
                postype='B'
                
                if(brlat   != None): rlat=brlat
                if(brlon   != None): rlon=brlon
                if(bvmax   != None): vmax=bvmax
                if(bpmin   != None): pmin=bpmin
                if(bdir    != None): dir=bdir
                if(bspd    != None): spd=bspd
                if(btccode != None): tccode=btccode
                if(br34m   != None): r34m=br34m
                if(br50m   != None): r50m=br50m
                if(blf     != None): alf=blf
                if(bdepth  != None): depth=bdepth
                if(br34    != None): r34=br34
                if(br50    != None): r50=br50
                if(bpoci   != None): poci=bpoci
                if(broci   != None): roci=broci
                if(brmax   != None): rmax=brmax

                
            if(csname  != None): sname=csname
            if(sname ==  None): sname=bsname

            if(tccode == None and wtccode == None):
                if(not(Is9X(self.stm1id))):
                    if(verb): print """WWW couldn't find tccode in carq or bt; set to 'NT'""",dtg,self.stm1id
                #print """WWW couldn't find tccode in carq or bt; exit and try to figure out what happen""",dtg,self.stm1id
                tccode='NT'
            
            if(wtccode != None and tccode == None):
                tccode=wtccode

            # -- use vmax
            #
            if(useVmax4TcCode and tccode == 'NT'):
                if(vmax != None and IsTcWind(vmax)):
                    tccode='TW'
                else:
                    tccode='NT'
                
            # -- final qc
            #
            if(vmax == None): vmax=-999

            if(verb):
                print 'WWW',dtg,tccode,wncode,wtccode,o0,w0,o12,o24,wncode
                print
            
            self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,b1id=b1id,tdo=tdo,ntrk=ntrk,ndtgs=ndtgs,
                                  r34m=r34m,r50m=r50m,depth=depth,
                                  r34=r34,r50=r50,poci=poci,roci=roci,
                                  rmax=rmax)

            self.trk[dtg].tdo=tdo
            self.trk[dtg].alf=alf
            self.trk[dtg].sname=sname
            self.trk[dtg].stmid=self.stm1id
            self.trk[dtg].postype=postype


        # -- get prev 12-h track dir/spd
        #
        
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        self.ndtgs=ndtgs

        # -- look for warning status in shem/io if WN t-1 or t+2
        #

        if(IsIoShemBasin(self.stm2id[0:2])):
            self.interpWarn(dtgs,verb=verb)

        # -- set the bt dir/spd and dirtype
        #
        for dtg in dtgs:
            
            self.trk[dtg].dirtype=self.trk[dtg].postype

            if( (self.trk[dtg].dir == None) or btonly):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    


    def chkDtgBreaks(self,dtgs,maxdiff=240,verb=0):

        ndtgs=[]
        dtgs.sort()
        foundbreak=0

        ldtgs=len(dtgs)
        for n in range(len(dtgs)-2,-1,-1):
            dt=dtgdiff(dtgs[n],dtgs[n+1])
            ndtgs.append(dtgs[n+1])
            if(verb): print 'dddd chkDtgBreaks:',n,dtgs[n],dtgs[n+1],dt
            if(dt > maxdiff):
                print 'WWW(tcCL.MDdataset.chkDtgBreaks n: ',n,' dt: ',dt,' dtgs[n]: ',dtgs[n],' dtgs[n+1]: ',dtgs[n+1],' foundbreak=1'
                foundbreak=1
                break

        if(not(foundbreak)): ndtgs=dtgs
        lndtgs=len(ndtgs)
        return(ndtgs)


    def interpWarn(self,odtgs,verb=0):

        ndtgs=len(odtgs)

        firstWN=0
        lastWN=ndtgs
        
        # -- find first and last warning
        #
        for n in range(0,ndtgs):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                firstWN=n
                break
            
        for n in range(ndtgs-1,0,-1):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                lastWN=n
                break
            
        if(verb): print 'firstWN: ',firstWN,'lastWN: ',lastWN,'ndtgs: ',ndtgs

        for n in range(firstWN,lastWN+1):
            
            if(ndtgs >= 2 and n <= ndtgs-2):
                
                if(n == 0):
                    nm1=n
                    n0=n
                    np1=n+1
                else:
                    nm1=n-1
                    n0=n
                    np1=n+1
                    
                wnm1=self.trk[odtgs[nm1]].wncode
                wn0=self.trk[odtgs[n0]].wncode
                wnp1=self.trk[odtgs[np1]].wncode
                    
                if(verb):
                    print 'nnnnn ',n,odtgs[n],'nm1:',nm1,wnm1,'n0:',n0,wn0,'np1:',np1,wnp1
                
                if( 
                    ( (wn0 == 'NW' and wnp1 == 'WN') or (wn0 == 'NW' and wnm1 == 'WN') )
                    ):

                    # -- don't interp back if first point or last
                    #
                    self.trk[odtgs[n0]].wncode='WN'
                    if(verb): print 'AAAAA ',ndtgs,n,nm1,n0,np1,self.trk[odtgs[n0]].wncode


    def cleanMD(self):

        #try: del self.cq00
        #except: None
        
        #try: del self.cq12
        #except: None
        
        #try: del self.cq24
        #except: None
        
        try: del self.best
        except: None
        
        try: del self.wrng
        except: None
        
        try: del self.of00
        except: None
        
        try: del self.of03
        except: None


    def getMDtrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg].gettrk()

        return(otrk,dtgs)
    
    def getMDotrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg]

        return(otrk,dtgs)

                
    def lsMDtrk(self,filtTCs=0,doprint=1):


        cards={}
        (otrk,dtgs)=self.getMDtrk()

        for dtg in dtgs:

            (rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,trkdir,trkspd,dirtype,b1id,tdo,
             ntrk,ndtgs,r34m,r50m,alf,sname,r34,r50,depth)=self.trk[dtg].gettrk()
            
            ostmid=self.stm1id
            if(hasattr(self.trk[dtg],'ostmid')): ostmid=self.trk[dtg].ostmid

            gentrk=0
            if(hasattr(self,'gendtgs')):
                if(dtg in self.gendtgs): gentrk=1
            if(rlat != None):
                (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                if(filtTCs and not(IsTc(tccode))): 
                    card="%s -- not a TC...and filtTCs=1"
                else:
                    card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,dir,spd,dirtype,
                                  tdo=tdo,tccode=tccode,wncode=wncode,
                                  ntrk=ntrk,ndtgs=ndtgs,r34m=r34m,r50m=r50m,
                                  alf=alf,sname=sname,gentrk=gentrk,doprint=doprint)
                    
                cards[dtg]=card

        return(cards)
                
                

class MDdeck(Adeck):


    def __init__(self,cards,
                 b2id,bnum,byear,
                 verb=0):

        #from w2 import SetLandFrac
        #from w2 import GetLandFrac

        self.b2id=b2id
        self.bnum=bnum
        self.byear=byear

        self.dofilt9x=0
        
        self.undef=-999
        self.skipcarq=0
        self.chkb2id=1
        self.warn=1
        self.verb=verb

        # -- all cards
        self.cards=cards.split('\n')

        # -- just mdeck related cards
        self.mdcards={}
        
        self.lf=SetLandFrac()
        self.getlf=GetLandFrac

        self.initMDcards()
        self.setMD()


    def initMDcards(self,warn=0,doGenesisCards=1):

        self.curb2id=-999
        self.curbnum=-999
        self.curbyear=-999
        
        for card in self.cards:
            tt=card.split(',')
            # -- scan for genesis nhc cards
            if(find(card,'GENESIS')):
                if(warn): print 'WWW NHC genesis posit...ignore',card
                # -- maybe use?
                if(not(doGenesisCards)): continue
            
            if(len(tt) < 5):
                if(warn): print 'WWW short card in MDdeck.initMDcards: ',card
                continue
            aid=self.setAidNCard(tt)
            if(aid == 'BEST' or
               aid == 'CARQ' or aid == 'WRNG' or aid == 'CNTR' or aid == 'COMS' or
               aid == 'JTWC' or aid == 'OFCL'
               ):
                rc=self.makeBidDtg(tt,card)
                # -- bail for 80-89 storms, etc
                if(rc == None):
                    #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ',rc
                    continue

                else:
                
                    (dtg,b2id,bnum,byear)=rc

                    if(self.chkStm2id() > 0):
                        print 'WWWWWWWWWWWW multiple stmids in this adeck...sayoonara'
                        sys.exit()

                    MF.loadDictList(self.mdcards,dtg,card)

        self.stm2id="%s%s.%s"%(self.b2id,self.bnum,self.byear)


    def chkStm2id(self):
        
        if(self.curb2id != self.b2id): self.curb2id=self.b2id
        if(self.curbnum != self.bnum): self.curbnum=self.bnum
        if(self.curbyear != self.byear): self.curbyear=self.byear

        rc=0
        if(self.curb2id != self.b2id): rc=1
        if(self.curbnum != self.bnum): rc=2
        if(self.curbyear != self.byear): rc=3

        return(rc)
        


    def setMD(self):

        dtgs=self.mdcards.keys()
        dtgs.sort()

        # -- stm2id
        #
        mD=MDdataset(dtgs,self.stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        self.mD=mD


    def getMDByDtgs(self,dtgs,stm2id):


        # -- stm2id
        #
        mD=MDdataset(dtgs,stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        return(mD)


    def getDtgRange(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            for n in range(0,ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRange 11111111111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                diffdtg=dtgdiff(dtg0,dtg1)
                #print 'n:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRange.checkDtg6h() -- continuity problem n: %02d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1
                    if(n+1 == ndtgs-1):
                        print 'problem at end -- remove dtg: ',dtg1,' by bumping n increment'
                        n=n+1
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                        else:
                            print 'problem NOT at end and diffdtg > diffdtgTol ',diffdtgTol,'-- stop!'
                            sys.exit()
                else:
                    cntDtgs.append(dtg0)
                
                if(n == ndtgs-2):
                    cntDtgs.append(dtg1)
                    #print 'fffffffoooooo---finalize: %2d'%(n),dtg1,mD.stm1id
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: ',n,' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: ',dtgdiff

                alldtgs=[]
                for tdtg in mf.dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                # -- if no dtgs do not set the uniqStmdtgs...
                #
                if(len(finaldtgs) > 0):
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                
                # -- set bdtg of next serious to dtg1 with diff > nhours
                #
                bdtg=dtg1

        


    def getDtgRangeNN(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            n=0
            while(n < ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- 1111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                    
                diffdtg=dtgdiff(dtg0,dtg1)
                #print 'n------------------------------:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- continuity problem n: %2d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1,\
                          'diffdtg: ',diffdtg,' stmid: ',mD.stm1id   
                    if(n+1 == ndtgs-1):
                        print
                        print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at end -- remove dtg: ',dtg1,' by bumping n increment +2 for stmid: ',mD.stm1id
                        n=n+2
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                            n=n+1
                        else:
                            print
                            print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem NOT at end and diffdtg: ',diffdtg,' > diffdtgTol ',diffdtgTol,(n+1),ndtgs-1
                            if((n+1) <= 3 and ndtgs > 4):
                                print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at BEGINNING...toss first dtgs before the break at: ',dtg1,n,ndtgs
                                cntDtgs=[]
                                cntDtgs.append(dtg1)
                                
                            n=n+1
                                
                else:
                    cntDtgs.append(dtg0)
                    n=n+1
                
                if(n == ndtgs-1):
                    #print 'fffffffnnnnnn---finalize: %2d'%(n),dtg1,mD.stm1id
                    cntDtgs.append(dtg1)
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: %2d'%(n),' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: %3.0f'%(dtgdiff),mD.stm1id

                alldtgs=[]
                for tdtg in mf.dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                if(len(finaldtgs) > 0):
                    bdtg=finaldtgs[0]
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                    
                # -- set bdtg for next series
                #
                bdtg=dtg1


    def ParseABdeckCard(self,mD,dtg,adcard):
        """
atcf='''BASIN,CY,YYYYMMDDHH,TECHNUM/MIN,TECH,TAU,LatN/S,LonE/W,VMAX,MSLP,TY,RAD,WINDCODE,RAD1,RAD2,RAD3,RAD4,RADP,RRP,MRD,GUSTS,EYE,SUBREGION,MAXSEAS,INITIALS,DIR,SPEED,STORMNAME,DEPTH,SEAS,SEASCODE,SEAS1,SEAS2,SEAS3,SEAS4,USERDEFINED,userdata'''
ttt=atcf.split(',')
for n in range(0,len(ttt)):
    print '''        # %02d, %s'''%(n,ttt[n])
sys.exit()
"""


        # 00, BASIN
        # 01, CY
        # 02, YYYYMMDDHH
        # 03, TECHNUM/MIN
        # 04, TECH
        # 05, TAU
        # 06, LatN/S
        # 07, LonE/W
        # 08, VMAX
        # 09, MSLP
        # 10, TY
        # 11, RAD
        # 12, WINDCODE
        # 13, RAD1
        # 14, RAD2
        # 15, RAD3
        # 16, RAD4
        # 17, RADP
        # 18, RRP
        # 19, MRD
        # 20, GUSTS
        # 21, EYE
        # 22, SUBREGION
        # 23, MAXSEAS
        # 24, INITIALS
        # 25, DIR
        # 26, SPEED
        # 27, STORMNAME
        # 28, DEPTH
        # 29, SEAS
        # 30, SEASCODE
        # 31, SEAS1
        # 32, SEAS2
        # 33, SEAS3
        # 34, SEAS4
        # 35, USERDEFINED
        # 36, userdata


        undef=-999
        sname=''


        def chkRquad(quad):

            allundef=1
            for q in quad:
                if(q != undef): allundef=0

            return(allundef)
        
        def SC2(tt,nn):
            try:
                ostr=tt[nn].strip()
            except:
                ostr=''
            return(ostr)

        def SC(istr):
            ostr=istr[0:-1].strip()
            return(ostr)

        def setRadiicode(rwind):

            if(not(rwind.isdigit())):
                crcode=undef
                return(crcode)
            rwind=int(rwind)
            
            crcode=undef
            if(rwind == 30):                 crcode='r30'
            if(rwind == 35 or rwind == 34):  crcode='r34'
            if(rwind == 50):                 crcode='r50'
            if(rwind == 100):                crcode='r100'
            if(rwind == 64 or rwind == 65):  crcode='r64'
            return(crcode)


        def setDigit(cvar,nezero=0):
            if(cvar.isdigit() or ('-' in cvar)):
                cvar=int(cvar)
            else:
                cvar=undef
            if(nezero and cvar == 0): cvar=undef
            return(cvar)
            

        def setString(cvar,doalpha=1):
            if(not(cvar.isalpha()) and doalpha or (len(cvar) == 0) ):
                cvar=undef
            if(cvar == 'X'): cvar=undef
            return(cvar)


        def setRadii(mm,rcode,rquad):
            
            if(rcode == 'r30'  and chkRquad(rquad) == 0 ): mm.setR30(rquad)
            if(rcode == 'r34'  and chkRquad(rquad) == 0 ): mm.setR34(rquad)
            if(rcode == 'r50'  and chkRquad(rquad) == 0 ): mm.setR50(rquad)
            if(rcode == 'r64'  and chkRquad(rquad) == 0 ): mm.setR64(rquad)
            if(rcode == 'r100' and chkRquad(rquad) == 0 ): mm.setR100(rquad)



        # -- split the card
        tt=adcard.split(',')
        ntt=len(tt)

            
        if(self.verb):
            print '   ntt: ',ntt,' adcard: ',tt
            #adcard[:-1].strip()
            if(self.verb == 2):
                for i in range(0,ntt):
                    print 'adflds: ',i,tt[i]


        nn=0
        b2id=SC2(tt,nn)                                ; nn=nn+1 # 00
        snum=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 01
        dtg=setString(SC2(tt,nn),doalpha=0)            ; nn=nn+1 # 02
        aidnum=setDigit(SC2(tt,nn))                    ; nn=nn+1 # 03
        aid=setString(SC2(tt,nn))                      ; nn=nn+1 # 04
        tau=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 05
        clat=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 06
        clon=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 07
        vmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 08
        pmin=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 09
        tccode=setString(SC2(tt,nn))                   ; nn=nn+1 # 10
        rcode=setRadiicode(SC2(tt,nn))                 ; nn=nn+1 # 11
        qcode=setString(SC2(tt,nn))                    ; nn=nn+1 # 12
        rne=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 13
        rse=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 14
        rsw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 15
        rnw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 16
        radii=[rne,rse,rsw,rnw]
        rquad=radii
        
        # -- convert radii to standard quadrants based on qcode
        #
        if(qcode != undef):   rquad=WindRadiiCode2Normal(qcode,radii)

        poci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 18
        roci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 19
        rmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 20
        gusts=setDigit(SC2(tt,nn))                     ; nn=nn+1 # 20
        deye=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 21
        b1id=setString(SC2(tt,nn))                     ; nn=nn+1 # 22
        maxseas=setDigit(SC2(tt,nn))                   ; nn=nn+1 # 23
        tdo=setString(SC2(tt,nn))                      ; nn=nn+1 # 24
        dir=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 25
        spd=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 26
        name=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 27
        depth=setString(SC2(tt,nn))                    ; nn=nn+1 # 28


        if(clat == undef):
            if(self.verb):
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW undef clat/clon in ParseABdeckCard ',dtg,snum,b2id
            return

        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

        # -- check for bad lat/lon
        if(not(rlat >= -90.0 and rlat <= 90.0)):
            print 'BBBBBBBBBBBBBBBBbaaaaaaaaaaaaaaaaddddddddddddd rlat; aid: ',aid,' dtg: ',dtg,' clat/clon: ',clat,clon
            return

        try:
            alf=self.getlf(self.lf,rlat,rlon)
        except:
            print 'ooooooooooooooopppppppppppppppppppppppssssssssssssssssssssssssss: ',rlat,rlon

        # 25W.1986 has a blank JTWC 12 h lat/lon card, if '' then return
        #
        noload=0
        if(clat == undef and self.verb):
            print 'WWWWWWW noload making mdeck from adeck card: ',adcard[:-1]
            noload=1

        abdata=ABdata(rlat,rlon,vmax,pmin,dir,spd,tccode,tdo,poci,roci,rmax,deye,depth,name,b1id,snum,b2id)
        abdata.alf=alf


        if(name != undef and sname != 'NONAME'):
            sname=name

        
        if(aid == 'CARQ' and tau == 0):

            try:
                mm=mD.cq00[dtg]
            except:
                mD.cq00[dtg]=abdata
                mm=mD.cq00[dtg]
                
            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.cq00[dtg]=mm

        if(aid == 'BEST'):

            try:
                mm=mD.best[dtg]
            except:
                mD.best[dtg]=abdata
                mm=mD.best[dtg]

            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.best[dtg]=mm
            

            if(self.verb): print 'bbbbb',b2id,b1id,snum,dtg,tau,aid,rlat,rlon,vmax,pmin,\
                           rcode,rquad,poci,roci,rmax,gusts,deye,tdo,dir,spd,name,depth
        
            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 0):

            try:
                mm=mD.of00[dtg]
            except:
                mD.of00[dtg]=abdata
                mm=mD.of00[dtg]

            setRadii(mm,rcode,rquad)
            mD.of00[dtg]=mm

            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 3):

            try:
                mm=mD.of03[dtg]
            except:
                mD.of03[dtg]=abdata
                mm=mD.of03[dtg]
            setRadii(mm,rcode,rquad)
            mD.of03[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 24):

            try:
                mm=mD.of24[dtg]
            except:
                mD.of24[dtg]=abdata
                mm=mD.of24[dtg]
            setRadii(mm,rcode,rquad)
            mD.of24[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 12):

            try:
                mm=mD.of12[dtg]
            except:
                mD.of12[dtg]=abdata
                mm=mD.of12[dtg]
            setRadii(mm,rcode,rquad)
            mD.of12[dtg]=mm

            
        if(aid == 'CARQ' and tau == -12):
            
            try:
                mm=mD.cq12[dtg]
            except:
                mD.cq12[dtg]=abdata
                mm=mD.cq12[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq12[dtg]=mm
        
        if(aid == 'CARQ' and tau == -24):
            
            try:
                mm=mD.cq24[dtg]
            except:
                mD.cq24[dtg]=abdata
                mm=mD.cq24[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq24[dtg]=mm

        if(aid == 'WRNG' and tau == 0):

            try:
                mm=mD.wrng[dtg]
            except:
                mD.wrng[dtg]=abdata
                mm=mD.wrng[dtg]
            setRadii(mm,rcode,rquad)
            mD.wrng[dtg]=mm

        
        return

    def lsBest(self,dtg):

        try:
            print 'BBB: ',dtg,self.mD.best[dtg].ls()
        except:
            print 'BBB(nada)'
            



class MD3trk(MDdataset):

    undef=-999.
    
    def __init__(self,cards,stm1id,stm9xid,gendtg=None,
                 dom3=0,basin=None,sname=None,stmDev=None,
                 dobt=0,doPutDSs=0,verb=0):

        # -- input
        #
        self.gendtg=gendtg
        self.dom3=dom3
        self.verb=verb
        self.cards=cards
        
        (self.itrk,self.idtgs)=self.getTrk4Cards()
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm1id)
         
        self.b1id=b1id
        self.snum=snum
        self.syear=year
        self.stm2id=stm2id
        self.ostm2id=stm2id
        self.stm1id=stm1id
        self.stm9xid=stm9xid
        self.basin=basin
        self.sname=sname
        self.stmDev=stmDev

        # -- output
        #
        self.trk={}
        
        # -- make trk and analyze
        #
        rc=self.makeTrkdata(verb=verb)
        rc=self.anlMDtrk()

    def getTrk4Cards(self,verb=0):
        
        undef=self.undef
        cards=self.cards
        itrk={}
        for card in cards:
            tt=card.split(',')
            dtg=tt[0].strip()
            ott=[]
            for t in tt[1:]:
                ott.append(t.strip())
            itrk[dtg]=ott
            
        idtgs=itrk.keys()
        idtgs.sort()
        
        if(self.verb):
            for idtg in idtgs:
                print 'iii',idtg,itrk[idtg]
            
        return(itrk,idtgs)
    
    def getTrkData4Itrk(self,dtg,ntrk,ndtgs,verb=0):
#     01W.2019', '', '11.2', '125.6', '20', '', '183', '9', '195', '8', '', '', '', '', '', '', '', '', '', '', 'NT', 'NW', 'c', 'c', '', '', '0.27', '', '', '', '', '---']   
        #     0   1      2        3     4    5     6    7      8    9   10  11  12  13  14  15  16  17  18  19   20    21    22   23  24  25     26   27  28  29  30    31
        trk=self.itrk[dtg]

        #if(self.verb):
            #for n in range(0,len(trk)):
                #print 'n:',n,trk[n]
            #sys.exit()

        # 33333333333333333333333
        #n: 0 d1w.2019
        #n: 1 9X-D1W
        #n: 2 TD
        #n: 3 NN
        #n: 4 18.0
        #n: 5 128.2
        #n: 6 15
        #n: 7 1010
        #n: 8 270
        #n: 9 6
        #n: 10 270
        #n: 11 6
        #n: 12 NaN
        #n: 13 NaN
        #n: 14 NaN
        #n: 15 NaN
        #n: 16 NaN
        #n: 17 NaN
        #n: 18 NaN
        #n: 19 NaN
        #n: 20 NaN
        #n: 21 NaN
        #n: 22 DB
        #n: 23 NW
        #n: 24 b
        #n: 25 b
        #n: 26 NaN
        #n: 27 NaN
        #n: 28 NaN
        #n: 29 NaN
        #n: 30 NaN
        #n: 31 NaN

        n=0
        stmid=trk[n] ; n=n+1                       # 0
        sname=trk[n] ; n=n+1                       # 1
        
        if(self.dom3): n=4
        
        rlat=float(trk[n]) ; n=n+1                 # 2
        rlon=float(trk[n]) ; n=n+1                 # 3       
        
        if(trk[n] != 'NaN' and trk[n] != '' ): vmax=float(trk[n])       # 4
        else: vmax=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): pmin=float(trk[n])       # 5
        else: pmin=undef
        n=n+1
        
        if(trk[n] != 'NaN'and trk[n] != '' ): dir=float(trk[n])        # 6
        else: dir=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): spd=float(trk[n])        # 7
        else: spd=undef
        n=n+1
        
        if(trk[n] != 'NaN' and trk[n] != '' ): trkdir=float(trk[n])     # 8
        else: trkdir=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): trkspd=float(trk[n])     # 9
        else: trkspd=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34m=float(trk[n])     #10
        else: r34m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34ne=float(trk[n])     #11
        else: r34ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34se=float(trk[n])     #12
        else: r34se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34sw=float(trk[n])     #13
        else: r34sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34nw=float(trk[n])     #14
        else: r34nw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50m=float(trk[n])      #15
        else: r50m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50ne=float(trk[n])     #16
        else: r50ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50se=float(trk[n])     #17
        else: r50se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50sw=float(trk[n])     #18
        else: r50sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50nw=float(trk[n])     #19
        else: r50nw=undef
        n=n+1

        r34=[r34ne,r34se,r34sw,r34nw]
        r50=[r50ne,r50se,r50sw,r50nw]
        
        tccode=trk[n]     #20
        n=n+1

        wncode=trk[n]     #21
        n=n+1

        dirtype=trk[n]     #22
        n=n+1

        postype=trk[n]     #23
        n=n+1


        if(trk[n] != 'NaN' and trk[n] != '' ): roci=float(trk[n])   #24
        else: roci=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): poci=float(trk[n])   #25
        else: poci=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): alf=float(trk[n])   #26
        else: alf=undef
        n=n+1

        depth=trk[n]     #27
        n=n+1

        # -- bug in parseDssTrk
        #
        if(len(trk) > 30 and not(self.dom3)):
            unknown=trk[n]     #28
            n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): rmax=float(trk[n])   #29
        else: rmax=undef
        n=n+1

        tdo=trk[n]   #30
        if(tdo == 'NaN' or tdo == '---'): tdo='   '
        n=n+1

        if(verb):
            print self.b1id,rlat,rlon,vmax,pmin,dir,spd
            print tccode,wncode,self.b1id,tdo,ntrk,ndtgs
            print r34m,r34m,r50m,depth
            print r34,r50,poci,roci,rmax
            
        self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,\
                              tccode,wncode,b1id=self.b1id,tdo=tdo,ntrk=ntrk+1,ndtgs=ndtgs+1,
                              r34m=r34m,r50m=r50m,depth=depth,
                              r34=r34,r50=r50,poci=poci,roci=roci,
                              rmax=rmax)        
        
        self.trk[dtg].tdo=tdo
        self.trk[dtg].alf=alf
        self.trk[dtg].sname=sname
        self.trk[dtg].stmid=stmid
        self.trk[dtg].postype=postype
        self.trk[dtg].ostm2id=self.ostm2id
        
                
    def makeTrkdata(self,verb=0):
        
        ntrk=0
        ndtgs=0

        tdtgs=[]
        for idtg in self.idtgs:
            gendiff=-999
            cmpdtg=idtg

            if(self.gendtg != None and self.gendtg != 'None'):
                cmpdtg=mf.dtginc(self.gendtg,-6)
                gendiff=mf.dtgdiff(idtg,cmpdtg)
                
            if(gendiff >= 0.0):
                if(verb): print 'ddddddddddddddddddddddddddddddddddddd',idtg,cmpdtg,gendiff
                tdtgs.append(idtg)
        
        self.idtgs=tdtgs
        
        dtgs=self.idtgs
        for dtg in dtgs:
            if(verb): print 'ddd',dtg,len(self.itrk[dtg]),self.itrk[dtg]
            self.getTrkData4Itrk(dtg,ntrk,ndtgs)
            ntrk=ntrk+1
            ndtgs=ndtgs+1
            
            
        
        # -- get prev 12-h track dir/spd
        #
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=mf.dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        
        # -- set the bt dir/spd and dirtype
        #
        self.ndtgs=ndtgs
        self.dtgs=dtgs
        
        for dtg in dtgs:
            self.trk[dtg].dirtype=self.trk[dtg].postype
            (trkdir,trkspd)=dirspd[dtg]

            if( (self.trk[dtg].dir == None)):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    
            
        
        
    def anlMDtrk(self,stmD=None,verb=0):

        (ltln,latmn,latmx,lonmn,lonmx,latb,lonb)=self.getlatlon()
        
        (gendtg,gendtgs,genstdd,time2gen,gendtgWN,gendtgBT)=self.getgenesis()
        if(self.sname != None): sname=self.sname
        else:
            sname=self.getname()
            
        (vmax,ace,stcd)=self.getvmax()
        (nRI,nED,nRW,dRI,dED,dRW)=self.getRI()
        (tclife,stclife,stmlife)=self.gettclife()
        syear=self.stm1id.split('.')[1]

        rc=getStmParams(self.stm1id)
        
        # -- if a warning is put, set stmlife to tcgen -- for 9X with warnings in the adecks
        #
        if(time2gen > 0 and Is9X(self.stm1id)):
            stmlife=time2gen/24.0


        if(self.verb):
            print 'FFFFFFFFFF(stm1|2id0:  ',self.stm2id,self.stm1id
            print 'FFFFFFFFFF(tclife):    ',tclife
            print 'FFFFFFFFFF(stclife):   ',stclife
            print 'FFFFFFFFFF(stmlife):   ',stmlife

            print 'FFFFFFFFFF(ace):       ',ace
            print 'FFFFFFFFFF(stcd):      ',stcd

            print 'FFFFFFFFFF(latb):      ',latb
            print 'FFFFFFFFFF(lonb):      ',lonb
            
            print 'FFFFFFFFFF(latmn):     ',latmn
            print 'FFFFFFFFFF(latmx):     ',latmx
            print 'FFFFFFFFFF(lonmn):     ',lonmn
            print 'FFFFFFFFFF(lonmx):     ',lonmx

            print 'FFFFFFFFFF(gendtg):    ',gendtg
            print 'FFFFFFFFFF(gendtgWN):  ',gendtgWN
            print 'FFFFFFFFFF(gendtgBT):  ',gendtgBT
            print 'FFFFFFFFFF(gendtgs):   ',gendtgs
            print 'FFFFFFFFFF(genstdd):   ',genstdd
            print 'FFFFFFFFFF(time2gen):  ',time2gen
            print 'FFFFFFFFFF(sname):     ',sname
            print 'FFFFFFFFFF(vmax):      ',vmax

            print 'FFFFFFFF(nRI):         ',nRI
            print 'FFFFFFFF(nED):         ',nED
            print 'FFFFFFFF(nRW):         ',nRW

            print 'FFFFFFFF(dRI):         ',dRI
            print 'FFFFFFFF(dED):         ',dED
            print 'FFFFFFFF(dRW):         ',dRW


        # -- decorate stm Dataset
        #
        
        self.gendtg=gendtg
        self.gendtgWN=gendtgWN
        self.gendtgBT=gendtgBT
        self.gendtgs=gendtgs
        self.genstdd=genstdd
        self.time2gen=time2gen

        self.sname=sname
        self.vmax=vmax

        self.ace=ace
        self.stcd=stcd

        self.tclife=tclife
        self.stclife=stclife
        self.stmlife=stmlife

        self.latb=latb
        self.lonb=lonb
        
        self.latmn=latmn
        self.lonmn=lonmn
        
        self.latmx=latmx
        self.lonmx=lonmx
    
        self.nRI=nRI
        self.nED=nED
        self.nRW=nRW
        self.dRI=dRI
        self.dED=dED
        self.dRW=dRW
        
        
        # -- adjust 9X dtgs
        #
        if(self.gendtg != None):
            dtg9Xs=mf.dtgrange(self.dtgs[0],self.gendtg)
            if(len(dtg9Xs) > 0):
                for dtg9x in dtg9Xs[0:-1]:
                    if(dtg9x in self.dtgs):
                        self.trk[dtg9x].stmid=self.stm9xid

        
    def getRI(self,dvmaxRI=30,dvmaxED=50,dvmaxRD=-30):

        dRI=dED=-999
        dRW=999
        nRI=0
        nED=0
        nRW=0
        
        for dtg in self.dtgs:
            dtgm24=mf.dtginc(dtg,-24)
            if(dtgm24 in self.dtgs):
                ttm24=self.trk[dtgm24]
                tt=self.trk[dtg]
                vmaxm24=ttm24.vmax
                vmax=tt.vmax
                if(vmax != None):
                    dvmax=vmax-vmaxm24
                else:
                    continue
                if(dvmax >= dvmaxRI):
                    nRI=nRI+1
                    if(dvmax > dRI and dvmax < dvmaxED): dRI=dvmax
                
                if(dvmax >= dvmaxED):
                    nED=nED+1
                    if(dvmax > dED): dED=dvmax

                if(dvmax <= dvmaxRD):
                    nRW=nRW+1
                    if(dvmax < dRW): dRW=dvmax
                

                

        return(nRI,nED,nRW,dRI,dED,dRW)

    def getvmax(self,ddtg=6):
        """assume ddtg=6h"""
        vmax=-999
        ace=0.0
        stcd=0.0
        n=0
        ns=0
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            svmax=tt.vmax
            if(svmax > vmax and svmax != self.undef): vmax=tt.vmax

            tace=aceTC(svmax)
            if(tace > 0.0):
                ace=ace+tace*ddtg
                ns=ns+1

            stcd=stcd+scaledTC(svmax)
            n=n+1

        stcd=stcd*0.25

        if(ns > 0):
            ace=ace/(24.0*tymin*tymin)

        return(vmax,ace,stcd)




    def getname(self):

        sname='---------'
        snames=[]
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            #if(tt.sname[0:5] != 'NONAME' and tt.sname[0:5] != 'INVES' and tt.sname != ''):
            if(tt.sname[0:5] == 'INVES' or tt.sname == ''):
                continue
            else:
                snames.append(tt.sname)

        snames=uniq(snames)
        return(sname)

        
    def getgenesis(self,dtgm=-18,dtgp=+12,vmaxTD=25.0,vmaxMin=10.0,verb=0):

        gendtg=gendtgWN=gendtgBT=gendtgBT1=gendtgBT2=None
        stdd=0.0
        
        gendtgs=[]
        genstd=None

        minvmax=1e20
        maxvmax=-1e20
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            if(tt.wncode.lower() == 'wn' and gendtgWN == None): gendtgWN=dtg

        # -- if gendtg = None; then no warnings!  use when became tc...
        #
        tcCodeWind=0
        is9x=Is9X(self.stm1id)
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            istc=IsTc(tt.tccode)
            if(istc == 1 and gendtgBT1 == None and not(is9x)): 
                tcCodeWind=1
                gendtgBT1=dtg

            if(istc > 1 and gendtgBT2 == None and not(is9x)): 
                tcCodeWind=2
                gendtgBT2=dtg
                

        if(gendtgWN != None):
            if(tcCodeWind >= 0):  gendtg=gendtgWN
            
        else:                 
            time2gen1=time2gen2=-999
            if(gendtgBT1 != None and not(is9x)):
                time2gen1=mf.dtgdiff(self.dtgs[0],gendtgBT1)
            if(gendtgBT2 != None and not(is9x)):
                time2gen2=mf.dtgdiff(self.dtgs[0],gendtgBT2)

            # -- go first for TC
            if(time2gen1 > 0.0):
                gendtgBT=gendtgBT1
            # --  else subTC
            elif(time2gen2 > 0.0):
                gendtgBT=gendtgBT2
            else:
                gendtg=None
                time2gen=0.0
            
        if(gendtg == None and gendtgBT != None): gendtg=gendtgBT
        
        if(gendtg != None):

            time2gen=mf.dtgdiff(self.dtgs[0],gendtg)
            
            bdtg=mf.dtginc(gendtg,dtgm)
            edtg=mf.dtginc(gendtg,dtgp)
            gendtgs=mf.dtgrange(bdtg,edtg)


            stddtime=0.0
            ngd=len(gendtgs)
            for n in range(1,ngd):
                dtgm1=gendtgs[n-1]
                dtg0=gendtgs[n]
                
                if(dtg0 in self.dtgs and dtgm1 in self.dtgs):

                    dtau=mf.dtgdiff(dtgm1,dtg0)
                    ttm1=self.trk[dtgm1]
                    tt0=self.trk[dtg0]
                    
                    vmaxm1=ttm1.vmax
                    vmaxm0=tt0.vmax
                    if(vmaxm1 < 0): vmaxm1=vmaxMin
                    if(vmaxm0 < 0): vmaxm0=vmaxMin

                    if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                    if(vmaxm1 < minvmax): minvmax=vmaxm1
                    if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                    if(vmaxm0 < minvmax): minvmax=vmaxm0
                    
                    stdd=stdd+(((vmaxm1+vmaxm0)*0.5)/vmaxTD)*dtau
                    stddtime=stddtime+dtau

                    if(verb): print 'ggggggggggg ',dtau,dtg0,dtgm1,vmaxm1,vmaxm0,stdd,stddtime

            if(stddtime > 0.0):

                stdd=stdd/24.0
                if(verb): print 'ggggggggggg final stdd: ',stdd


        genstdd=stdd

        if(verb):
            print 'ggggggg ',gendtg
            print 'ggggggg ',gendtgWN
            print 'ggggggg ',gendtgBT
            print 'ggggggg ',gendtgs
            print 'ggggggg ',genstdd
            print 'ggggggg ',time2gen

        return(gendtg,gendtgs,genstdd,time2gen,gendtgWN,gendtgBT)
    
    def getlatlon(self):

        latb=0.0
        lonb=0.0
        
        latmn=999
        latmx=-999
        lonmn=999
        lonmx=-999

        latlon={}
        n=0
            
        for dtg in self.dtgs:
            tt=self.trk[dtg]

            tlat=tt.rlat
            if(n==0):  tlonPri=tt.rlon
            tlon=tt.rlon
            
            # -- cross prime meridion
            if(tlon < primeMeridianChk and tlonPri > primeMeridianChk): tlon=tlon+360.0
            
            if(tlat > latmx): latmx=tlat
            if(tlon > lonmx): lonmx=tlon
            if(tlat < latmn): latmn=tlat
            if(tlon < lonmn): lonmn=tlon
            n=n+1
            latb=latb+tlat
            lonb=lonb+tlon
            latlon[dtg]=(tlat,tlon)
            tlonPri=tlon

        if(n>0):
            latb=latb/n
            lonb=lonb/n

        ndtgs=len(self.dtgs)
        for n in range(0,ndtgs):
            dtg=self.dtgs[n]
            tt=self.trk[dtg]
            
        return(latlon,latmn,latmx,lonmn,lonmx,latb,lonb)


    def gettclife(self):

        tclife=0
        stclife=0
        stmlife=0
        
        ndtgs=len(self.dtgs)

        if(ndtgs == 0):
            return(tclife,stclife,stmlife)
            
        for n in range(1,ndtgs):
            tt=self.trk[self.dtgs[n]]
            dtau=mf.dtgdiff(self.dtgs[n-1],self.dtgs[n])
            stmlife=stmlife+dtau
            if(IsTc(tt.tccode) == 1):
                tclife=tclife+dtau
            if(IsTc(tt.tccode) == 2):
                stclife=stclife+dtau
            
        tclife=tclife/24.0
        stclife=stclife/24.0
        stmlife=stmlife/24.0

        return(tclife,stclife,stmlife)
            

    def lsDSsDtgs(self,dtgs=None,dobt=0,dupchk=0,verb=0,selectNN=1,countsOnly=0,filtTCs=0,doprint=1):

        if(dtgs == None):
            dtgs=self.dtgs
        else:
            if(not(type(dtgs) is ListType)): dtgs=[dtgs]
            else: dtgs=dtgs
            
        itrk=None

        dobtLs=dobt
        if(filtTCs): dobtLs=1

        cards=[]
        ncards=0
        nstrms=0
        nstms=1
        stmid=self.stm1id
        sname=self.sname
        
        for dtg in dtgs:

            if(dtg in self.dtgs):
                
                gentrk=0
                if(dtg in self.gendtgs): gentrk=1
                trk=self.trk[dtg]
                card=printTrk(trk.stmid,dtg,trk.rlat,trk.rlon,trk.vmax,trk.pmin,
                              trk.dir,trk.spd,trk.dirtype,trk.tdo,
                              tccode=trk.tccode,wncode=trk.wncode,
                              r34m=trk.r34m,r50m=trk.r50m,alf=trk.alf,
                              ntrk=trk.ntrk,ndtgs=trk.ndtgs,
                              sname=sname,gentrk=gentrk,doprint=doprint)
                cards.append(card)
                ncards=ncards+1
                
        else:
            nstms=0
            nstmTCs=0
            
        if(countsOnly):
            if(filtTCs):
                print dtg,'N: ',nstmTCs
            else:
                print dtg,'N: ',nstms
                
        if(ncards == 0 and not(countsOnly)): 
            if(filtTCs): 
                print "%s-N"%(dtg),'   NNNNNNNNNNNNNN: filtTCs: ',filtTCs,' nstrms All: ',nstrms
            else:
                print "%s-N -- no storms for this dtg..."%(dtg)    

        return(cards)

    def lsDSsStmSummary(self,
                        doprint=1,warn=0):

        # -- season storm card
        #
        
        stmid=self.stm1id
        sname=self.sname
        if(hasattr(self,'m3tri')): 
            self=self.m3tri
        else:
            None

        if(hasattr(self,'ace')):

            curdtg=mf.dtg()
            curdtgm6=mf.dtginc(curdtg,-6)

            if(len(self.dtgs) == 0):
                if(warn): print 'DDDDDDDDDDDDDDDDDd nada dtgs for stmid: ',stmid
                return

            bdtg=self.dtgs[0]
            edtg=self.dtgs[-1]
            
            ostmid=stmid
                
                
            (snum,b1id,yyyy,b2id,stm2id,stm1id)=getStmParams(ostmid)

            stm=snum+b1id

            livestatus=' '
            tctype=TCType(self.vmax)
            edtgdiff=mf.dtgdiff(edtg,curdtg)
            if(edtg == curdtg or edtg == curdtgm6 or edtgdiff <= 0.0): livestatus='*'
            RIstatus=' NaN '
            timeGen=' NaN '
            if(self.nRI > 0): RIstatus='rrRI'
            if(self.nED > 0): RIstatus='rrED'
            if(self.nRW > 0):
                RIstatus='ddRW'
                if(self.nRI > 0): RIstatus='ddRI'
                if(self.nED > 0): RIstatus='ddED'

                
            stm9x=''
            ostmid9x=self.stm9xid
                
            pad=''
            if(len(stm9x) > 0): pad=' '
            if(self.stmDev == None):
                if(IsNN(ostmid)):
                    stmDev='NN'
                elif(IsNN(ostmid9x)):
                    stmDev='DEV'
                else:
                    stmDev='nonDEV'
            else:
                stmDev=self.stmDev
            
            if(IsNN(ostmid9x)):
                stm9x=stm9x+pad+"NN , %s"%(ostmid9x.split('.')[0])
            else:
                stm9x=stm9x+pad+"9X , %s"%(ostmid9x.split('.')[0])


            otimeGen='NaN'
            if(hasattr(self,'time2gen') and not(Is9X(stmid))):
                if(self.time2gen >= 0.0):
                    timeGen="tG:%3.0f"%(self.time2gen)
                    otimeGen="%3.0f"%(self.time2gen)
                    
            oACE=self.ace
            if(Is9X(stmid)): oACE=0.0


            ovmax="%3d"%(self.vmax)
            if(self.vmax == self.undef): ovmax='***'

            #if(find(stmid,'CC')):
                #tctype='___'

                #ocard="%s %s%1s %3s %-10s :%s :%4.1f;%4.1f :%5.1f %5.1f :%s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%s"%\
                    #(yyyy,stm,livestatus,tctype,sname[0:9],ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
                     #self.latmn,self.latmx,self.lonmn,self.lonmx,
                     #stm9x)
            #else:

            try:
                n=int(stm[0:2])
                ogendtg="%s"%(self.gendtg)
            except:
                ogendtg='NaN'
                
            ogenType='NaN'
            if(IsNN(stmid)):
                if(self.gendtgWN != None): ogenType='wn'
                if(self.gendtgWN == None and self.gendtgBT != None): ogenType='bt'

            ocard="%s.%s ,  %3s , %s , %s , %s , %5.1f , %5.1f , %5.1f , %5.1f , %s , %s , %5.1f , %-5.1f , %5.1f , %-5.1f , %4.1f , %4.1f , %2d , %2d , %2d , %s , %s , %s , %s , %s"%(stm,yyyy,tctype,stmDev,sname,ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
             self.latmn,self.latmx,self.lonmn,self.lonmx,
             self.stcd,oACE,
             self.nRI,self.nED,self.nRW,
             RIstatus,stm9x,otimeGen,ogendtg,ogenType)
            
                
                
            rcsum=(tctype,stmDev)
            if(doprint): 
                print ocard
            return(ocard,rcsum)


class prTCMean(MFbase):
    
    
    def __init__(self,
                 dtg,ctlpath,
                 prvar='pr',
                 undef=-999.,
                 verb=0):
        
        self.dtg=dtg
        self.ctlpath=ctlpath
        self.undef=undef
        self.verb=verb
        self.prvar=prvar

        ga=setGA(Quiet=1)
        try:
            ga.open(ctlpath)
        except:
            print 'EEE-prTCmean opening: ',ctlpath
            self=None
            return(self)
        self.ctlpath=ctlpath
        self.ga=ga
        self.ge=ga.ge
        

    def setGrads(self,sdtg=None,tau=0,regrid=0.5):
        
        idtg=self.dtg
        if(sdtg != None): idtg=sdtg
        fdtg=mf.dtginc(idtg,tau)
        gtime=mf.dtg2gtime(fdtg)
        try:
            self.ga('set time %s'%(gtime))
        except:
            print 'EEE-setGrads: ',gtime,self.ctlpath
        self.prMH={}
        self.prM={}
        
    def setTcprop(self,clat,clon,r,bearing=270,verb=0):
        #expr='pr1=re(pr,1)'
        #self.ga(expr)
        expr='tcprop %s %f %f %f %f'%(self.prvar,clat,clon,r,bearing)
        if(verb): print 'expr: ',expr,self.dtg,self.ctlpath
        
        try:
            self.ga(expr)
            cards=self.ga.Lines
        except:
            print 'EEE-setTCprop: ',expr,self.dtg,self.ctlpath
            cards=[]
        
        cprm=prm=prmh1=prmh2=None
        cprm=prm=prmh1=prmh2=-99.
        
        for card in cards:
            if(find(card,'MeanRadinf')): 
                prm=card.split()[-1]
                prm=float(prm)
                if(prm > 9999.): prm=-99.
                cprm="%5.1f"%(prm)
                #cprm=float(cprm)
                if(verb): print '  prm: ',float(prm)
                
            elif(find(card,'MeanHemi1')): 
                prmh1=card.split()[1]
                prmh2=card.split()[-1]
                if(prmh1 > 9999.): prmh1=-99.
                if(prmh2 > 9999.): prmh2=-99.
                if(verb): print 'prmh1: ',float(prmh1)
                if(verb): print 'prmh2: ',float(prmh2)
                
        self.prMH[r]=[prm,prmh1,prmh2]
        self.prM[r]=cprm
        
class superBT(Mdeck3):
    
    sbtTSmeta={}
    sMdesc={}
    
    btime=-240
    btime=-144
    etime=0
    dtime=6
    
    # -- max # of times for an individual storm
    #
    maxTimes=100
    
    def __init__(self,
                 version,
                 tbdir=None,
                 oyearOpt=None,
                 verb=0,
                 doclean=0,
                 dochk=0,
                  ):
        

        self.sTimer('sbt-init')
        self.verb=verb
        self.version=version

        # -- meta
        #
        smcards=open('%s/%s'%(sbtVerDirDat,sbtMeta)).readlines()
        for n in range(0,len(smcards)):
            tt=smcards[n].split(',')
            tt0=tt[0].replace("\n",'')
            tt1=tt[1].replace("\n",'')
            tt0=tt0.replace("""'""",'')
            self.sbtTSmeta[n]=tt0
            self.sMdesc[tt0]=tt1

        self.sMv=self.sbtTSmeta
            
        if(verb):
            kk=self.sMv.keys()
            kk.sort()
            for k in kk:
                print 'sMv ',k,self.sMv[k]
        

        self.tbdir="%s/dat"%(sbtVerDir)
        self.gadatDir="%s/gadat"%(sbtVerDir)
        MF.ChkDir(self.gadatDir,'mk')
        
        if(oyearOpt == None):
            oyearOpt='%s-%s'%(bm3year,em3year)
        
        oyearOpt="%s"%(oyearOpt)
        self.oyearOpt=oyearOpt
        
        sbtCvsPath="%s/sbt-%s-%s-MRG.csv"%(sbtVerDirDat,versionsBT,oyearOpt)
        sumCvsPath="%s/sum-md3-%s-MRG.csv"%(sbtVerDirDat,oyearOpt)

        # -- 111 -- get the storm meta data
        #
        stmSum={}
        tcNamesHash={}
        scards=open(sumCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            tt=scard.split(',')
            stmid=tt[0]
            ss=stmid.split(".")
            year=ss[1]
            b3id=ss[0]
            tccode=tt[1]
            tcdev=tt[2]
            name=tt[3]
            tcNamesHash[(year,b3id)]=name
            stmSum[stmid]=tt
        self.stmSum=stmSum
        self.tcNamesHash=tcNamesHash
        
        # -- 222 -- get the superBT
        #
        sbtNN={}
        sbtDev={}
        sbtNonDev={}
        
        sbtNNdtgs={}
        sbtDevdtgs={}
        sbtNonDevdtgs={}
        
        stmsNon=[]
        stmsDev=[]
        stmsNN=[]
        
        scards=open(sbtCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            scard=scard.replace(' ','')
            tt=scard.split(',')
            ltt=len(tt)

            if(ltt != 51 and tt[-2] == 'NaN'):
                if(dochk): print 'nnn',ltt,tt[-2],tt
                continue
            else:
                if(dochk): print 'ggg',ltt,tt[0]
                
            stmid=tt[0]
            dtg=tt[3]
            stmDev=tt[2]
            if(stmDev == 'NN'):
                MF.appendDictList(sbtNN, stmid, tt)
                MF.appendDictList(sbtNNdtgs, stmid, dtg)
            elif(stmDev == 'DEV'):
                MF.appendDictList(sbtDev,stmid,tt)
                MF.appendDictList(sbtDevdtgs,stmid,dtg)
            elif(stmDev == 'NONdev'):
                MF.appendDictList(sbtNonDev,stmid, tt)
                MF.appendDictList(sbtNonDevdtgs,stmid, dtg)
                
        stmsNon=sbtNonDev.keys()
        stmsNon.sort()
        
        stmsDev=sbtDev.keys()
        stmsDev.sort
        
        stmsNN=sbtNN.keys()
        stmsNN.sort()
        
        self.sbtNN=sbtNN
        self.sbtDev=sbtDev
        self.sbtNonDev=sbtNonDev
        
        self.sbtNNdtgs=sbtNNdtgs
        self.sbtDevdtgs=sbtDevdtgs
        self.sbtNonDevdtgs=sbtNonDevdtgs
                
        self.stmsNon=stmsNon
        self.stmsDev=stmsDev
        self.stmsNN=stmsNN
        
        # -- make txaxis and xvalsU for TS analysis using grads
        #
        self.makeSbtTSTaxis()
        self.dTimer('sbt-init')

    
    def parseSbt(self,sbt):
        
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


        #for n in range(0,len(sbt)):
            #print 'n',n,sbt[n].strip(),self.sMv[n]
        #sys.exit()

        sbtDict={}
        
        n=3
        dtg=sbt[n] ; n=n+1
        blat=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=blat ; n=n+1
        blon=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=blon ; n=n+1
        bvmax=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bvmax ; n=n+1
        bpmin=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bpmin ; n=n+1
        bdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        bspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        btccode=sbt[n] ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        br34m=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        land=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        mvmax=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        mr34m=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        shrspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=shrspd ; n=n+1
        shrdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=shrdir ; n=n+1
        stmspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=stmspd ; n=n+1
        stmdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=stmdir ; n=n+1
        sst=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=sst ; n=n+1
        ssta=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=ssta ; n=n+1
        vrt850=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=vrt850 ; n=n+1
        div200=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=div200 ; n=n+1
        cpsb=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpsb ; n=n+1
        cpslo=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpslo ; n=n+1
        cpshi=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpshi ; n=n+1
        tpw=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=tpw ; n=n+1
        rh500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh500 ; n=n+1
        rh700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh700 ; n=n+1
        rh850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh850 ; n=n+1
        u500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u500 ; n=n+1
        u700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u700 ; n=n+1
        u850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u850 ; n=n+1
        v500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v500 ; n=n+1
        v700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v700 ; n=n+1
        v850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v850 ; n=n+1
        poci1=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=poci1 ; n=n+1
        roci1=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=roci1 ; n=n+1
        poci0=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=poci0 ; n=n+1 
        roci0=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=roci0 ; n=n+1

        if(len(sbt) > 41):
            n=41
            oprc3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc3 ; n=n+1
            oprg3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg3 ; n=n+1
            opri3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri3 ; n=n+2 
            oprc5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc5 ; n=n+1
            oprg5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg5 ; n=n+1 
            opri5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri5 ; n=n+2
            oprc8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc8 ; n=n+1
            oprg8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg8 ; n=n+1
            opri8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri8 ; n=n+2
            
            eprc3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc3 ; n=n+1
            eprg3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg3 ; n=n+1
            epri3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri3 ; n=n+2
            epre3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre3 ; n=n+1
            eprr3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr3 ; n=n+2
            
            eprc5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc5 ; n=n+1
            eprg5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg5 ; n=n+1
            epri5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri5 ; n=n+2
            epre5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre5 ; n=n+1
            eprr5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr5 ; n=n+2

            eprc8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc8 ; n=n+1
            eprg8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg8 ; n=n+1
            epri8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri8 ; n=n+2
            epre8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre8 ; n=n+1
            eprr8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr8 
            
        else:
            oprc8=oprg8=opri8=undef
            oprc5=oprg5=opri5=undef
            oprc3=oprg3=opri3=undef
            
            eprc8=eprg8=epri8=epre8=eprr8=undef
            eprc5=eprg5=epri5=epre5=eprr5=undef
            eprc3=eprg3=epri3=epre3=eprr3=undef
            
        
        rc=(dtg,blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m,
            land,mvmax,shrspd,shrdir,stmspd,stmdir,
            sst,ssta,
            vrt850,div200,
            cpsb,cpslo,cpshi,tpw,
            rh500,rh700,rh850,
            u500,u700,u850,
            v500,v700,v850,
            roci1,poci1,roci0,poci0,
            oprc3,oprg3,opri3,
            oprc5,oprg5,opri5,
            oprc8,oprg8,opri8,
            eprc3,eprg3,epri3,epre3,eprr3,
            eprc5,eprg5,epri5,epre5,eprr5,
            eprc8,eprg8,epri8,epre8,eprr8)
        
        
        #print sbt
        #print rc
        #sys.exit()
        return(rc)

    def parseSbtDict(self,sbt):
        
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


        #for n in range(0,len(sbt)):
        #    print 'n',n,sbt[n].strip(),self.sMv[n]
        #sys.exit()

        sbtDict={}
        
        n=3
        dtg=sbt[n] ; n=n+1
        blat=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=blat ; n=n+1
        blon=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=blon ; n=n+1
        bvmax=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bvmax ; n=n+1
        bpmin=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bpmin ; n=n+1
        bdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        bspd=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bspd ; n=n+1
        btccode=sbt[n] ; sbtDict[self.sMv[n]]=btccode ; n=n+1
        br34m=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=br34m ; n=n+1
        land=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=land ; n=n+1
        mvmax=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=mvmax ; n=n+1
        mr34m=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=mr34m ; n=n+1
        shrspd=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=shrspd ; n=n+1
        shrdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=shrdir ; n=n+1
        stmspd=mkFloatU(sbt[n]) 
        # -- bug in lsdiag for best track at end ... undefined to 100, use bspd
        if(stmspd > 90.0): 
            stmspd=bspd
        sbtDict[self.sMv[n]]=stmspd ; n=n+1
        stmdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=stmdir ; n=n+1
        sst=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=sst ; n=n+1
        ssta=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=ssta ; n=n+1
        vrt850=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=vrt850 ; n=n+1
        div200=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=div200 ; n=n+1
        cpsb=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpsb ; n=n+1
        cpslo=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpslo ; n=n+1
        cpshi=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpshi ; n=n+1
        tpw=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=tpw ; n=n+1
        rh500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh500 ; n=n+1
        rh700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh700 ; n=n+1
        rh850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh850 ; n=n+1
        u500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u500 ; n=n+1
        u700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u700 ; n=n+1
        u850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u850 ; n=n+1
        v500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v500 ; n=n+1
        v700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v700 ; n=n+1
        v850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v850 ; n=n+1
        poci1=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=poci1 ; n=n+1
        roci1=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=roci1 ; n=n+1
        poci0=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=poci0 ; n=n+1 
        roci0=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=roci0 ; n=n+1

        if(len(sbt) > 41):
            n=41
            oprc3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc3 ; n=n+1
            oprg3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg3 ; n=n+1
            opri3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri3 ; n=n+2 
            oprc5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc5 ; n=n+1
            oprg5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg5 ; n=n+1 
            opri5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri5 ; n=n+2
            oprc8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc8 ; n=n+1
            oprg8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg8 ; n=n+1
            opri8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri8 ; n=n+2
            
            eprc3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc3 ; n=n+1
            eprg3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg3 ; n=n+1
            epri3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri3 ; n=n+2
            epre3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre3 ; n=n+1
            eprr3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr3 ; n=n+2
            
            eprc5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc5 ; n=n+1
            eprg5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg5 ; n=n+1
            epri5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri5 ; n=n+2
            epre5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre5 ; n=n+1
            eprr5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr5 ; n=n+2

            eprc8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc8 ; n=n+1
            eprg8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg8 ; n=n+1
            epri8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri8 ; n=n+2
            epre8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre8 ; n=n+1
            eprr8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr8 
            
        else:
            oprc8=oprg8=opri8=undef
            oprc5=oprg5=opri5=undef
            oprc3=oprg3=opri3=undef
            
            eprc8=eprg8=epri8=epre8=eprr8=undef
            eprc5=eprg5=epri5=epre5=eprr5=undef
            eprc3=eprg3=epri3=epre3=eprr3=undef
            
        
        rc=(dtg,blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m,
            land,mvmax,shrspd,shrdir,stmspd,stmdir,
            sst,ssta,
            vrt850,div200,
            cpsb,cpslo,cpshi,tpw,
            rh500,rh700,rh850,
            u500,u700,u850,
            v500,v700,v850,
            roci1,poci1,roci0,poci0,
            oprc3,oprg3,opri3,
            oprc5,oprg5,opri5,
            oprc8,oprg8,opri8,
            eprc3,eprg3,epri3,epre3,eprr3,
            eprc5,eprg5,epri5,epre5,eprr5,
            eprc8,eprg8,epri8,epre8,eprr8)
        
        
        #print sbt
        #print sbtDict
        #sys.exit()
        return(dtg,sbtDict)
    
    def setsbtTS(self,stmid,sbtType,btime,doDict=1,warn=0,verb=1):
    
        #smeta=self.stmSum[stmid]
        if(sbtType == 'NONdev'):
            sbts=self.sbtNonDev[stmid]
            sdtgs=self.sbtNonDevdtgs[stmid]
        elif(sbtType == 'DEV'):
            sbts=self.sbtDev[stmid]
            sdtgs=self.sbtDevdtgs[stmid]

        sbtUndef=[]
        for n in range(0,21):
            sbtUndef.append(undef)
            
        sdtgs.sort()
        edtg=sdtgs[-1]
        bdtg=sdtgs[0]
        sbtTS={}
        tdtgs=mf.dtgrange(bdtg,edtg,6)
        for tdtg in tdtgs:
            stime=dtgdiff(edtg, tdtg)
            sbtTS[stime]=sbtUndef
        
        #if(verb): print 'NNN',stmid,sdtgs,'ebdtg:',edtg,bdtg
        for sbt in sbts:
            #print 'sss',sbt
            #for n in range(0,len(sbt)):
                #print n,sbt[n]
            #sys.exit()
            if(doDict):
                (pdtg,psbt)=self.parseSbtDict(sbt)
            else:
                psbt=self.parseSbt(sbt)
                pdtg=psbt[0]
            
            if(doDict and verb == 2):
                kk=psbt.keys()
                kk.sort()
                for k in kk:
                    print 'kkk',k,psbt[k]
            
            stime=dtgdiff(edtg,pdtg)
            if(stime < btime and warn):
                print 'WWW-stime: %d < btime %d for stmid: %s'%(stime,btime,stmid)
            else:
                if(doDict):
                    #if(verb): print 'ddddd-ssseeettt',psbt.values().ks
                    sbtTS[stime]=psbt
                else:
                    #if(verb): print 'ssseeettt',stime,psbt[1:]
                    sbtTS[stime]=psbt[1:]

        if(verb == 2):
            stimes=sbtTS.keys()
            stimes.sort()
            for stime in stimes:
                if(doDict):
                    print 'ooo-ddd',stime,sbtTS[stime].values()
                else:
                    print 'ooo',stime,sbtTS[stime],len(sbtTS[stime])
            
        return(sbtTS)
        
    
    def getSbtTS(self,stmid,verb=0):
        
        """
method to pull variables from sbt to compare dev v non-dev storms
"""
        if(stmid in self.stmsDev):
            sbtType='DEV'
            sbtTS=self.setsbtTS(stmid,sbtType,self.btime,verb=verb)
            
        elif(stmid in self.stmsNon):
            sbtType='NONdev'
            sbtTS=self.setsbtTS(stmid,sbtType,self.btime,verb=verb)
        else:
            sbtTS=None
            sbtType='NN'
            
        return(sbtType,sbtTS)
            
    def makeSbtTSTaxis(self):
        
        taxis=[]
        
        xtimes=range(self.btime,self.etime+1,self.dtime)
        xvals={}
        for n in range(0,len(xtimes)):
            xtime=xtimes[n]*1.0
            taxis.append(xtime)
            xvals[xtime]=undef
            
        self.taxis=taxis
        self.xvalsU=xvals
        
    def makeSbtVarTaxis(self):
        
        taxis=[]
        xvals={}
        for n in range(0,self.maxTimes):
            xtime=n
            taxis.append(xtime)
            xvals[xtime]=undefVar
            
        self.taxis=taxis
        self.xvalsU=xvals
        
        

    def makeSbtTS(self,vvals,nvar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            if(k < self.btime):
                if(warn): print 'WWW-makeSbtTS time: %d < btime %d'%(k,self.btime)
            else:
                if(verb): print 'kkkk----',k,vvals[k][nvar]
                ovals[k]=vvals[k][nvar]
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            #if(verb): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)

    def makeSbtTSDict(self,vvals,ovar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            if(k < self.btime):
                if(warn): print 'WWW-makeSbtTS time: %d < btime %d'%(k,self.btime)
            else:
                try:
                    ovals[k]=vvals[k][ovar]
                    if(verb): print 'kkkk----',k,vvals[k][ovar]
                except:
                    None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            if(verb == 2): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)
    
    def makeGaNonDevCtl(self,nx,ny,nvars,verb=0):
            
        ctl="""dset ^%s
title sbt nondev-dev for stmopt: %s
undef %5.1f
xdef %d linear %d %d
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undef,
            nx,self.btime,self.dtime,ny,
            len(nvars))
        for nvar in nvars:
            gvar=self.sMv[nvar]
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[gvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)
    
    def makeGaNonDevCtlDict(self,nx,ny,ovars,verb=0):
            
        ctl="""dset ^%s
title sbt nondev-dev for stmopt: %s
undef %5.1f
xdef %d linear %d %d
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undef,
            nx,self.btime,self.dtime,ny,
            len(ovars))
        for ovar in ovars:
            mvar=ovar
            gvar=ovar
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)
    
    def makeGaNonVDevTS(self,sbtTS,tsType,nvars,verb=0):
        
        gadir=self.gadatDir
        gadatPath="%s/ts-%s-%s.dat"%(gadir,tsType,self.stmopt)
        gactlPath="%s/ts-%s-%s.ctl"%(gadir,tsType,self.stmopt)
        (gdir,gfile)=os.path.split(gadatPath)
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile
        

        B=open(gadatPath,'wb')

        nkk=sbtTS.keys()
        nkk.sort()
        tsOut={}
        
        for nvar in nvars:
            
            for nk in nkk:
                print 'NNNNNNNN nvar: ',nk,nvar,self.sMv[nvar]
                nvvals=sbtTS[nk]
                print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtTS(nvvals,nvar,verb=0)
                print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsOut,nvar,tvals)
                if(verb): print tsType,nk,self.sMv[nvar],tvals[-13:]
                
            tt=tsOut[nvar]
            ny=len(tt)
            print 'tsType ny',tsType,ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        rc=self.makeGaNonDevCtl(nx,ny,nvars)
        
    def makeGaNonVDevTSDict(self,sbtTS,tsType,ovars,verb=0,override=0):

        gadir=self.gadatDir
        gadatPath="%s/ts-%s-%s.dat"%(gadir,tsType,self.stmopt)
        gactlPath="%s/ts-%s-%s.ctl"%(gadir,tsType,self.stmopt)
        print 'qqqqq',gactlPath
        if(MF.ChkPath(gadatPath)):
            if(not(override)):
                print 'gadatPath exists and override=0...press...'
                return(1)

        
        (gdir,gfile)=os.path.split(gadatPath)
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile
        

        B=open(gadatPath,'wb')

        nkk=sbtTS.keys()
        nkk.sort()
        tsOut={}
        
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtTS[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtTSDict(nvvals,ovar,verb=verb)
                #print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsOut,ovar,tvals)
                
            tt=tsOut[ovar]
            ny=len(tt)
            print 'tsType ny',tsType,ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    #print 'asdf',t
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        rc=self.makeGaNonDevCtlDict(nx,ny,ovars)

    def setsbtVar(self,stmid,sbtType,doDict=1,doDtgKey=0,warn=0,verb=0):
    
        #smeta=self.stmSum[stmid]

        if(sbtType == 'NONdev'):
            sbts=self.sbtNonDev[stmid]
            sdtgs=self.sbtNonDevdtgs[stmid]

        elif(sbtType == 'DEV'):
            sbts=self.sbtDev[stmid]
            sdtgs=self.sbtDevdtgs[stmid]

        elif(sbtType == 'NN'):
            sbts=self.sbtNN[stmid]
            sdtgs=self.sbtNNdtgs[stmid]

        # -- dict by dtg with (dict form of sBT by varname)
        #
        sbtVar={}

        # -- set x axis with values to undefVar
        #
        # -- uniq the dtgs for cases where one 9X goes to two basin storms
        #
        sdtgs=mf.uniq(sdtgs)
        sdtgs.sort()
        edtg=sdtgs[-1]
        bdtg=sdtgs[0]
        tdtgs=mf.dtgrange(bdtg,edtg,6)

        for n in range(0,len(tdtgs)):
            skey=n
            if(doDtgKey):
                skey=tdtgs[n]
            sbtVar[skey]=undefVar

        for n in range(0,len(sdtgs)):
         
            skey=n
            if(doDtgKey):
                skey=tdtgs[n]
                
            sbt=sbts[n]
            #print 'nnnnnn',n,sbt,len(sbt)

            if(doDict):
                (pdtg,psbt)=self.parseSbtDict(sbt)
                sbtVar[skey]=psbt
            else:
                psbt=self.parseSbt(sbt)
                pdtg=psbt[0]
                sbtVar[skey]=psbt[1:]
            
            if(doDict and verb == 2):
                kk=psbt.keys()
                kk.sort()
                for k in kk:
                    print 'kkk',k,psbt[k]
            
        if(verb == 2):
            sns=sbtVar.keys()
            sns.sort()
            for sn in sns:
                
                if(doDict):
                    print 'ooo-ddd',sdtg,sbtTS[sn].values()
                else:
                    print 'ooo',sdtg,sbtTS[sn],len(sbtTS[sn])
            
        return(sbtVar)
        

    def getSbtVar(self,stmid,doDict=1,doDtgKey=0,warn=0,verb=0):
        
        """
method to pull variables from sbt to compare dev v non-dev storms
"""
        if(stmid in self.stmsDev):
            sbtType='DEV'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)
            
        elif(stmid in self.stmsNon):
            sbtType='NONdev'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)
            
        elif(stmid in self.stmsNN):
            sbtType='NN'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)

        else:
            sbtVar=None
            sbtType='XXX'

        if(sbtVar == None):
            print 'EEEEEEEEEEE: ',stmid
            sys.exit()

        return(sbtType,sbtVar)
    

    def makeGaVarAllDict(self,sbtvarAll,ovars,verb=0):

        gadir=self.gadatDir
        gadatPath="%s/all-bystm-%s.dat"%(gadir,self.stmopt)
        gactlPath="%s/all-bystm-%s.ctl"%(gadir,self.stmopt)
        gadatPathAll="%s/all-all-%s.dat"%(gadir,self.stmopt)
        gactlPathAll="%s/all-all-%s.ctl"%(gadir,self.stmopt)
        (gdir,gfile)=os.path.split(gadatPath)
        (gdir,gfileAll)=os.path.split(gadatPathAll)
        
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile

        self.gadatPathAll=gadatPathAll
        self.gactlPathAll=gactlPathAll
        self.gadatFileAll=gfileAll

        B=open(gadatPath,'wb')
        A=open(gadatPathAll,'wb')

        nkk=sbtvarAll.keys()
        nkk.sort()
        tsVar={}
        tsVarAll={}
        
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtvarAll[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtVarDict(nvvals,ovar,verb=verb)
                #print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsVar,ovar,tvals)
                
            tt=tsVar[ovar]
            ny=len(tt)
            #print 'varall ny',ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        # -- make the .ctl
        #
        rc=self.makeGaVarAllCtlDict(nx,ny,ovars)
        
        
        # -- all only varies in x
        #

        oNx={}
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtvarAll[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                avals=self.makeSbtVarDictAll(nvvals,ovar,verb=verb)
                if(verb): print 'aaa',nk,ovar,len(avals),avals[-10:]
                MF.appendDictList(tsVarAll,ovar,avals)
                
            tt=tsVarAll[ovar]
            #if(verb == 0): print 'varall nk',nk,tt[-10:]
    
            ox=[]
            
            for t in tt:
                for x in t:
                    ox.append(x)
                    b=struct.pack('1f',x)
                    A.write(b)
                
            oNx[ovar]=len(ox)    
                    
        A.close()
        
        nx=oNx[ovars[0]]
        for ovar in ovars[1:]:
            nx1=oNx[ovar]
            if(nx1 != nx):
                print 'oooooooooooooopppppppppppppppppsssssssssssssssssss',ovar,nx,nx1
                
                
        # -- make the .ctl for all file with vars in x only
        #
        rc=self.makeGaVarAllCtlDictAll(nx,ovars)

    def makeSbtVarDict(self,vvals,ovar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            dovar="'%s'"%(ovar)
            try:
                ovals[k]=vvals[k][dovar]
                if(ovar == 'btccode'):
                    ovals[k]=float(IsTc(ovals[k]))
                if(verb == 2): print 'kkkk----',k,vvals[k][dovar]
            except:
                None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            if(verb == 2): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)

    def makeSbtVarDictAll(self,vvals,ovar,warn=0,verb=0):
        
        ovals={}
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            dovar="'%s'"%(ovar)
            #print 'kkkk----',k,dovar,vvals[k][dovar]
            try:
                ovals[k]=vvals[k][dovar]
                if(ovar == 'btccode'):
                    ovals[k]=float(IsTc(ovals[k]))
                #lovals=len(ovars[k])
                #print 'gggg',k,ovals[k]
                #print 'kkkk----',k,lovals,ovals[k]
            except:
                #print 'ffff',k
                None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            #print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        #print 'tttt',tline
        return(rc)

    
    def makeGaVarAllCtlDict(self,nx,ny,ovars,verb=0):
            
        ctl="""dset ^%s
title sbt var by stm for stmopt: %s
undef %5.1f
xdef %d linear 0 1
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undefVar,
            nx,ny,
            len(ovars))
        for ovar in ovars:
            mvar=ovar
            gvar=ovar
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)

    def makeGaVarAllCtlDictAll(self,nx,ovars,verb=0):
        
        ctlAll="""dset ^%s
title sbt var by stm for stmopt: %s
undef %5.1f
xdef %d linear 0 1
ydef 1 linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFileAll,self.stmopt,undefVar,
            nx,
            len(ovars))
        for ovar in ovars:
            mvar=ovar
            gvar=ovar
            ctlAll=ctlAll+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctlAll=ctlAll+"endvars"
        MF.WriteCtl(ctlAll, self.gactlPathAll,verb=verb)


    def makeGaStnVar(self,sbtvarAll,ovars,sMdesc,verb=0):

        stmids=sbtvarAll.keys()
        stmids.sort()
        ovar='nstm'
        ovars.append(ovar)
        sMdesc[ovar]='storm number 1,2,...,nstm'

        dtgs=[]
        nstms=len(stmids)
        
        for n in range(0,nstms):
            nstm=n+1
            stmid=stmids[n]
            sdtgs=sbtvarAll[stmid].keys()
            sdtgs.sort()
            dtgs=dtgs+sdtgs

        # -- get the dtgs and set ovals with sbt data
        #
        dtgs.sort()
        bdtg=dtgs[0]
        edtg=dtgs[-1]
        odtgs=mf.dtgrange(bdtg,edtg,inc=6)

        # -- data dict with dtg key
        #
        ovals={}
        
        for odtg in odtgs:
            ovals[odtg]=[]

        bdtg=odtgs[0]
        edtg=odtgs[-1]

        # -- set the paths using stmopt & dtg range
        #
        gadir=self.gadatDir
        gabase="stn-bystm-%s-b%s-e%s"%(self.stmopt,bdtg,edtg)
        gaSdatPath="%s/%s.sdat"%(gadir,gabase)
        gaSmapPath="%s/%s.smap"%(gadir,gabase)
        gaSctlPath="%s/%s.ctl"%(gadir,gabase)
        gaSgsPath="%s/%s.gs"%(gadir,gabase)
        
        (gdir,gfileD)=os.path.split(gaSdatPath)
        (gdir,gfileS)=os.path.split(gaSmapPath)
        (gdir,gfileC)=os.path.split(gaSctlPath)
        
        B=open(gaSdatPath,'wb')
        
        # -- cycle by storms & dtgs
        #
        nstm=0.0
        
        gsStmIds=[]
        for stmid in stmids:
            
            nstm=nstm+1
            
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
            stnid="%2s%1s%2s"%(snum,b1id,year[2:4])
            
            # -- get data by storm and storm dtgs
            #
            vvals=sbtvarAll[stmid]
            dtgs=vvals.keys()
            dtgs.sort()

            gsStmIds.append('_snum.%d = %s'%(nstm,stmid))
            stime=mf.dtg2gtime(dtgs[0])
            gsStmIds.append('_stime.%d = %s'%(nstm,stime))


            nstm=nstm*1.0

            for dtg in dtgs:

                olist=[]
                olist.append(stnid)
                
                no=len(ovars)
                for n in range(0,no):
                    ovar=ovars[n]
                    if(ovar != 'nstm'):
                        dovar=ovar
                        pval=vvals[dtg][dovar]
                        if(ovar == 'btccode'):  pval=IsTc(pval)
                        olist.append(pval)
                    
                # -- stick stmnum at end
                #
                
                olist.append(nstm)

                appendDictList(ovals,dtg,olist)
        

        # -- output in grads station data format
        # -- make the end-time record
        #
        stnid='99W00'
        rlat=0.0
        rlon=0.0
        stndt=0
        stnfoot = struct.pack('8sfffii',stnid,rlat,rlon,stndt,0,0)
        cardfoot="%s %f %f"%(stnid,rlat,rlon)
        
        # -- cycle by dtgs
        #
        rlatmin=99999.
        rlatmax=-99999.
        rlonmin=99999.
        rlonmax=-99999.
        
        for odtg in odtgs:

            svals=ovals[odtg]
            
            if(verb):
                print 'sssssssssss',odtg,'#storms: ',len(svals)
                print
            
            if(len(svals) > 0):
                
                # --cycle by data for each storm in the dtg
                #
                for sval in svals:

                    if(verb): print 'sval: ',sval
                    
                    n=0
                    stnid=sval[n] ; n=n+1; np1=n+1 ; np2=n+2 ; np3=n+3 ;np4=n+4
                    stndt=0.0
                    ns=len(sval)
                    rlat=sval[n]
                    rlon=sval[np1]
                    if(rlat < rlatmin): rlatmin=rlat
                    if(rlat > rlatmax): rlatmax=rlat
                    if(rlon < rlonmin): rlonmin=rlon
                    if(rlon > rlonmax): rlonmax=rlon
                    
                    stnhead=struct.pack('8sfffii',stnid,sval[n],sval[np1],stndt,1,1)
                    cardhead="%s %f %f"%(stnid,sval[n],sval[np1])
                    stndat=struct.pack('1f',sval[np2])
                    carddat="%f"%(sval[np2])
                    for i in range(np3,ns):
                        stndat=stndat+struct.pack('f',sval[i])
                        carddat="%s %f"%(carddat,sval[i])
                    B.write(stnhead)
                    B.write(stndat)
                    if(verb):
                        print 'hhh',odtg,cardhead
                        print 'ddd',odtg,carddat,len(sval[np3:])
                    
                if(verb):  print 'fff',odtg,cardfoot
                B.write(stnfoot)
            else:
                if(verb): print 'fff',odtg,cardfoot
                B.write(stnfoot)

        B.close()

        # -- make the .ctl file
        #
        
        
        nodtgs=len(odtgs)
        bgtime=mf.dtg2gtime(bdtg)
        tdefCard="tdef %d linear %s 6hr"%(nodtgs,bgtime)

        nvars=len(ovars[2:])

        gvar='bvmax'
        
        ctl="""dset ^%s
stnmap ^%s
dtype station
undef %s
title sbt station data
tdef %d linear %s 6hr
vars %d"""%(gfileD,gfileS,str(undefVar),nodtgs,bgtime,nvars)
        
        for ovar in ovars[2:]:
            ctl=ctl+"""
%-7s 0 0 %s"""%(ovar,sMdesc[ovar])
            
        ctl=ctl+"""
endvars"""
            
        if(verb): print ctl
        
        # -- make basic .gs to open and display
        #
        
        dlat=5.0
        dlon=10.0
        
        rlatmn=(int(rlatmin)/int(dlat))*dlat - dlat
        rlatmx=(int(rlatmax)/int(dlat))*dlat + dlat
        
        rlonmn=(int(rlonmin)/int(dlon))*dlon - dlon
        rlonmx=(int(rlonmax)/int(dlon))*dlon + dlon
        
        print 'lllaaa',rlatmin,rlatmn,rlatmax,rlatmx
        print 'lllaaa',rlonmin,rlonmn,rlonmax,rlonmx
        
        
        bgtime=mf.dtg2gtime(odtgs[0])
        egtime=mf.dtg2gtime(odtgs[-1])
      
        rlatPmn=0.0
        rlatPmx=45.0
        rlonPmn=90.0
        rlonPmx=180.0
        clevs=' 35 65 130'
        clevs=' 15 20  25 30'
        ccols='5  4  3  6    2'
        
        gshead="""
function main(args)

rc=gsfallow('on')
rc=const()

sf=ofile('%s')

'set xsize 1200 800'

'set lat %3.1f %3.1f'
'set lon %4.1f %4.1f'
'set t 1'

_sizid=0.10
_sizpos=0.15
_gvar=%s

"""%(gaSctlPath,
     rlatPmn,rlatPmx,
     rlonPmn,rlonPmx,
     gvar,
     )
        gsvars="""
# -- var with storm ids
#"""
        for n in range(0,len(gsStmIds)):
            stmvar=gsStmIds[n]

            gsvars="""%s
%s"""%(gsvars,stmvar)

        gsexpr="""

# -- plot by stms
#
nvar=nstm
gvar=_gvar

texp='(time=%s,time=%s)'
gexp=gvar%%texp
nexp=nvar%%texp
ostm=1
while(ostm <= %d)
  'set gxout stnmark'
'set time '_stime.ostm
#print 'ssss 'ostm' '_stime.ostm' '_snum.ostm
'set stid on'
'set digsiz '_sizid
'set cmark 3'
'set ccolor 1'
  'd maskout(maskout('gvar','ostm'-'nexp'),'nexp'-'ostm')'
'set stid off'
'set digsiz '_sizpos
'set cmark 9'

'set clevs %s'
'set ccols %s'
  'd maskout(maskout('gexp','ostm'-'nexp'),'nexp'-'ostm')'
  ostm=ostm+1
  'q pos'
  
endwhile

'draw map'
'cbarn'

return
        
"""%(
     bgtime,egtime,int(nstms),
     clevs,ccols,
   )
       
        
        rc=WriteCtl(ctl,gaSctlPath)

        cmd='stnmap -v -i %s'%(gaSctlPath)
        runcmd(cmd)
        
        gs=gshead+gsvars+gsexpr 
        print gs
        rc=WriteCtl(gs,gaSgsPath)
        
        cmd="""grads -lc '%s'"""%(gaSgsPath)
        runcmd(cmd)
        
        return


    def lsGaVarAllDict(self,sbtvarAll,ovars,sMdesc,verb=0):
        
        # -- all only varies in x
        #
        oNx={}
        stmids=sbtvarAll.keys()
        stmids.sort()

        dtgs=[]
        for stmid in stmids:
            sdtgs=sbtvarAll[stmid].keys()
            dtgs=dtgs+sdtgs

        dtgs.sort()
        bdtg=dtgs[0]
        edtg=dtgs[-1]
        
        odtgs=mf.dtgrange(bdtg,edtg,inc=6)
        ovals={}
        
        for odtg in odtgs:
            ovals[odtg]=[]

        print 'ls of:'
        for ovar in ovars:
            try:
                desc=sMdesc[ovar]
            except:
                desc=None
                
            if(desc == None):
                print 'EEE ovar: ',ovar,' NOT in sBT...sayounara...'
                sys.exit()
                
            print ovar,desc
        
        print
        
        for stmid in stmids:
            
            if(verb): print 'NNNNNNNN--DDD ovar: ',stmid,ovar
            vvals=sbtvarAll[stmid]
            dtgs=vvals.keys()
            dtgs.sort()
            
            hcard='stmid: %s  N: %d'%(stmid,len(dtgs))
            hcard1='dtg        '
            for ovar in ovars:
                hcard1='%s %6s'%(hcard1,ovar[0:6])
                
            print hcard
            print hcard1

            for dtg in dtgs:

                ocard="%s "%(dtg)
                stndat={}
                olist=[]
                for ovar in ovars:

                    dovar=ovar
                    pval=vvals[dtg][dovar]
                    opval=pval
                    if(pval == undefVar): opval=-999.
                    if(ovar == 'btccode'):
                        pval1=pval
                        pval=IsTc(pval1)
                        ocard="%s %3s %1s "%(ocard,pval1,pval)
                    else:
                        ocard="%s %6.1f"%(ocard,opval)
                        
                print ocard
                        
                
        return         

    def chkSpdDirGaVarAllDict(self,sbtvarType,sbtvarAll,stmidNNDev,
                              bspdmax=30.0,
                              bspdmaxNN=40.0,
                              latMaxNN=35.0,
                              verb=0):
        
        def getSpdSbt(stmid):
            
            (sumPath,mpathBT,mpath9X,stmid9X)=getSrcSumTxt(stmid,verb=verb)
            stmidNN=stmid
            scards=open(sumPath).readlines()
            posits={}
            for scard in scards:
                tt=scard.split(',')
                dtg=tt[0].strip()
                blat=float(tt[3].strip())
                blon=float(tt[4].strip())
                posits[dtg]=(blat,blon)

            dtgs=posits.keys()
            dtgs.sort()
            
            ndtgs=len(dtgs)

            for n in range(0,ndtgs):

                odtg=dtgs[n]
                if(ndtgs == 1):
                    dtgm1=dtgs[0]
                    dtg=dtgs[0]
                elif(n == 0 and ndtgs > 1):
                    dtgm1=dtgs[0]
                    dtg=dtgs[n+1]
                else:
                    dtgm1=dtgs[n-1]
                    dtg=dtgs[n]

                blat=posits[dtg][0]
                blatm1=posits[dtgm1][0]

                blon=posits[dtg][1]
                blonm1=posits[dtgm1][1]

                (bdir,bspd,bu,bv)=rumhdsp(blatm1, blonm1,blat,blon,6)

                obspd=bspd
                if(ndtgs == 1):
                    bspd=999.
                    obspd=-999.
                    stmidNN='sngleton'
                card="%s %4.0f %-6s NN: %s"%(stmid,obspd,sbttype,stmidNN)
                card="%s Posit: %s"%(card,odtg)
                card="%s N-1: %5.1f %6.1f N:  %5.1f %6.1f "%(card,blatm1,blonm1,blat,blon)
                card="%s SPD: %5.0f  dir: %5.0f"%(card,obspd,bdir)
                appendDictList(lsCards, stmid, card)
                
                stest9X=(bspd > bspdmax)
                stestNN=(bspd > bspdmaxNN)
                ltest=(abs(blat) < latMaxNN)
                ntest=(sbttype == 'NN')
                
                dtest=(stest9X and not(ntest))
                btest=(stestNN and ltest and ntest)
                if(dtest or btest):
                    try:
                        oCards[stmid]=card
                    except:
                        None
            
        
        # -- all only varies in x
        #

        stmids=sbtvarAll.keys()
        stmids.sort()

        oCards={}
        lsCards={}
        for stmid in stmids:
            
            vvals=sbtvarAll[stmid]
            dtgs=vvals.keys()
            dtgs.sort()
            
            sbttype=sbtvarType[stmid]
            stmidNN='        '
            if(sbttype == 'DEV'):
                stmidNN=stmidNNDev[stmid]
            
            ndtgs=len(dtgs)

            for n in range(0,ndtgs):

                odtg=dtgs[n]
                if(ndtgs == 1):
                    dtgm1=dtgs[0]
                    dtg=dtgs[0]
                elif(n == 0 and ndtgs > 1):
                    dtgm1=dtgs[0]
                    dtg=dtgs[n+1]
                else:
                    dtgm1=dtgs[n-1]
                    dtg=dtgs[n]

                dovar="'%s'"%('blat')
                blat=vvals[dtg][dovar]
                blatm1=vvals[dtgm1][dovar]

                dovar="'%s'"%('blon')
                blon=vvals[dtg][dovar]
                blonm1=vvals[dtgm1][dovar]
                (bdir,bspd,bu,bv)=rumhdsp(blatm1, blonm1,blat,blon,6)

                obspd=bspd
                if(ndtgs == 1):
                    bspd=999.
                    obspd=-999.
                    stmidNN='sngleton'
                card="%s %4.0f %-6s NN: %s"%(stmid,obspd,sbttype,stmidNN)
                card="%s Posit: %s"%(card,odtg)
                card="%s N-1: %5.1f %6.1f N:  %5.1f %6.1f "%(card,blatm1,blonm1,blat,blon)
                card="%s SPD: %5.0f  dir: %5.0f"%(card,obspd,bdir)
                appendDictList(lsCards, stmid, card)
                
                stest9X=(bspd > bspdmax)
                stestNN=(bspd > bspdmaxNN)
                ltest=(abs(blat) < latMaxNN)
                ntest=(sbttype == 'NN')
                
                dtest=(stest9X and not(ntest))
                btest=(stest9X and stestNN and ltest and ntest)
                spdTest=0
                if(dtest or btest):
                    try:
                        oCards[stmid]=card
                        spdTest=1
                    except:
                        None
                        
                # -- update with sumPath if NN storm
                #
                if(spdTest and IsNN(stmid)):
                    print 'NNNUUU -- update with sumPath',stmid
                    rc=getSpdSbt(stmid)
        
        return(oCards,lsCards)
                
class TcBtTrkPlot(DataSet):
    
    def __init__(self,stmid,
                 btrk,
                 pltdir='/tmp',
                 model='bt',
                 stmopt=None,
                 aidtrk=None,
                 aidtaus=None,
                 zoomfact=None,
                 dtgopt=None,
                 otau=48,
                 dobt=1,
                 Quiet=1,
                 Window=0,
                 Bin='grads',
                 doLogger=0,
                 background='black',
                 xsize=1200,
                 #xsize=1600,
                 docp2Dropbox=1,
                 pngmethod='printim',
                 plttag=None,
                 dopbasin=0,
                 verb=0,override=0):

            
        btstmid=stmid
        
        self.btrk=btrk

        self.stmid=stmid
        (self.stm3id,self.stmname)=getStmName3id(self.stmid)        
        
        stmid=getSubbasinStmid(stmid)
        basin=getBasinOptFromStmids(stmid)[0]
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        if(b1id.lower() == 'c'): basin='cepac'
        #latlons=getBasinLatLonsPrecise(basin)
        
        if(dopbasin):
            pbasin=TcGenBasin2PrwArea[basin]
        else:
            pbasin=None
            
        self.model=model
        self.pltdir=pltdir
        MF.ChkDir(pltdir,'mk')

        self.aidtrk=aidtrk
        self.aidtaus=aidtaus
        self.zoomfact=zoomfact
        self.otau=otau
        self.Bin=Bin
        
        self.xsize=xsize
        self.ysize=xsize*(3.0/4.0)
        self.verb=verb
        self.docp2Dropbox=docp2Dropbox
        
        self.plttag=plttag
        self.pngmethod=pngmethod
        if(find(background,'w') or find(background,'W')): background='white'
        if(find(background,'b') or find(background,'B')): background='black'
        
        if(background != 'white' and background != 'black'):
            print "EEE background in TcBtTrkPlot must be white or black"
            sys.exit()
            
        self.background=background
        
        self.bgcol=0
        if(background == 'white'): self.bgcol=1
        
        self.override=override
        self.Window=Window
        self.doLogger=doLogger

        self.centerdtg=None
        if(dtgopt != None): self.centerdtg=dtg_command_prc(dtgopt)

        self.setLatLonBox(pbasin=pbasin,reduceLon1=0.0,reduceLon=10.0,reduceLat=5.0)
        
        (clat1,clon1)=Rlatlon2Clatlon(self.lat1,self.lon1,dozero=1,dotens=0)
        (clat2,clon2)=Rlatlon2Clatlon(self.lat2,self.lon2,dozero=1,dotens=0)
        
        trkstmname=self.stmid
        if(stmopt != None):
            trkstmname=stmopt
        if(self.plttag != None):
            self.pltfile="trkplt-%s.%s.%s.%s-%s.%s-%s.png"%(self.plttag,trkstmname,self.model,clat1,clat2,clon1,clon2)
        else:
            self.pltfile="trkplt.%s.%s.%s-%s.%s-%s.png"%(trkstmname,self.model,clat1,clat2,clon1,clon2)

        self.pltpath="%s/%s"%(self.pltdir,self.pltfile)
        self.trkplotpath=self.pltpath

        self.alreadyDone=0
        if(not(override) and MF.ChkPath(self.trkplotpath)):
            print 'III trkplotpath: ',self.trkplotpath,' already there and override=0...'
            self.alreadyDone=1
            return

        ga=setGA(Quiet=Quiet,Window=Window,doLogger=doLogger,Bin=Bin)

        dumctl="%s/dum.ctl"%(sbtGslibDir)
        ga.fh=ga.open(dumctl)

        self.ga=ga
        self.ge=ga.ge
        
        self.ge.pareaxl=0.50
        self.ge.pareaxr=9.75
        self.ge.pareayb=0.25
        self.ge.pareayt=8.00  # decreased from 8.25
        self.ge.setParea()

        self.curgxout=self.ga.getGxout()
        self.setInitialGA()
        

    def setLatLonBox(self,pbasin=None,timelab=None,reduceLon1=None,reduceLon=None,reduceLat=None,verb=0):
        
        if(pbasin != None):
            if(reduceLon == None): reduceLon=0.0
            if(reduceLat == None): reduceLat=0.0
            if(reduceLon1 == None): reduceLon1=reduceLon
            
            aW2=getW2Area(pbasin)
            self.aW2=aW2
            lon1=aW2.lonW
            lon2=aW2.lonE
            lat1=aW2.latS
            lat2=aW2.latN
            
            print 'LLL',lon1,lon2,lat1,lat2
            if(lat1 < 0): lat1=lat1+reduceLat
            else: lat1=lat1-reduceLat

            if(lat2 < 0): lat2=lat2+reduceLat
            else: lat2=lat2-reduceLat
            
            lon1=lon1+reduceLon1
            lon2=lon2-reduceLon

            print 'LLL----',lon1,lon2,lat1,lat2
             
            self.lon1=lon1
            self.lon2=lon2
            self.lat1=lat1
            self.lat2=lat2
            self.xlint=aW2.xlint
            self.ylint=aW2.ylint
            self.pbasin=pbasin
            
            return


        alats=[]
        alons=[]
        avmaxs=[]
        apmins=[]
        
        dtgs=self.btrk.keys()
        dtgs.sort()

        for dtg in dtgs:
            try:
                # -- md2
                bt=self.btrk[dtg].gettrk()
            except:
                # -- md3
                bt=self.btrk[dtg]
                
            self.btrk[dtg]=bt
            alats.append(bt[0])
            alons.append(bt[1])
            avmaxs.append(bt[2])
            apmins.append(bt[3])
            
        self.alats=alats
        self.alons=alons
        self.avmaxs=avmaxs
        self.apmins=apmins
        
        (lat1,lat2,lon1,lon2)=LatLonOpsPlotBounds(alats,alons,verb=verb)

        if(self.centerdtg != None and (self.centerdtg in dtgs) ):

            bt=self.btrk[self.centerdtg]
            rlat=bt[0]
            rlon=bt[1]

        else:
            rlat=(lat1+lat2)*0.5
            rlon=(lon1+lon2)*0.5

            from numpy import mean
            rlat=mean(alats)
            rlon=mean(alons)


        if(self.zoomfact != None):

            zoom=float(self.zoomfact)

            dlon=(lon2-lon1)/zoom
            dlat=(lat2-lat1)/zoom
            dint=2.5

            if(self.centerdtg == None and zoom < 1.25):
                latOff=0.65
                if(IsNhemBasin(self.stmid)): latOff=0.35
            else:
                latOff=0.50
                
            lonOff=0.50
            
            lat1=rlat-dlat*latOff
            lat1=int(lat1/dint+0.5)*dint
            lat2=lat1+dlat

            lon1=rlon-dlon*lonOff
            lon1=int(lon1/dint+0.5)*dint
            lon2=lon1+dlon


        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
        
        
    def setInitialGA(self):

        ga=self.ga
        ge=self.ge

        ge.lat1=self.lat1           
        ge.lat2=self.lat2   
        ge.lon1=self.lon1   
        ge.lon2=self.lon2   
        
        if(hasattr(self,'xlint')): ge.xlint=self.xlint
        if(hasattr(self,'ylint')): ge.ylint=self.ylint
        # -- clear
        #
        ge.clear()
        ge.mapdset='mres'
        ge.mapdset='hires'
        ge.mapthick=4
        ge.mapcol=self.bgcol
        ge.mapcol=45
        ge.setMap()
        ge.grid='off'
        ge.setGrid()
        ge.setLatLon()
        ge.setXylint()
        ge.setParea()
        ge.setPlotScale()
        ge.setXsize(xsize=self.xsize,ysize=self.ysize)
        ge.setColorTable()
        # -- force this?
        ge.timelab='on'


        

    def PlotTrk(self,
                doft=0,dtg0=None,nhbak=None,nhfor=None,
                ddtg=6,dtg0012=1,maxbt=55,
                doalltaus=1,otau=48,etau=120,dtau=12,
                title2=None,):


        if(self.alreadyDone): return
        
        ga=self.ga
        ge=self.ge

        if(doft):
            self.etau=etau
            self.dtau=dtau
            self.otau=otau

            mktaus=[0,24,48,72,120]
            mkcols={0:1,24:1,48:1,72:2,120:2}
            
            ftlcol=modelTrkPlotProps[self.model][0]
            modeltitle=modelOname[self.model]

            (btau,etau,dtau)=(0,etau,dtau)
            itaus=range(btau,etau+1,dtau)

            taus=[]
            for itau in itaus:
                for ttau in self.aidtaus:
                    if(itau == ttau):
                        taus.append(itau)


        pbt=ga.gp.plotTcBt
        pbt.set(self.btrk,dtg0=dtg0,nhbak=nhbak,nhfor=None,ddtg=ddtg,dtg0012=dtg0012,maxbt=maxbt)
        
        bm=ga.gp.basemap2
        #bm.set(landcol='sienna',oceancol='steelblue')
        # -- try atcf colors
        bm.set(landcol='atcfland',oceancol='atcfocean')
        bm.draw()
        ge.setPlotScale()

        #pbt.dline(times=pbt.otimesbak,lcol=7,lthk=10)
        pbt.dline(times=pbt.otimesbak)
        pbt.dwxsym(times=pbt.otimesbak)
        pbt.legend(ge,times=pbt.otimesbak,ystart=7.9)

        if(doft):

            pft=ga.gp.plotTcFt
            pft.set(self.aidtrk,lcol=ftlcol,doland=1)

            if(ftlcol == -2):
                pft.dline(lcol=15)
                try:     vmcol=pft.lineprop[otau][0]
                except:  None

                if(vmcol != 75):
                    pft.dmark(times=[otau],mkcol=vmcol,mksiz=0.20)
                    pft.dmark(times=[otau],mksiz=0.05)
                else:
                    pft.dmark(times=[otau])
            else:
                pft.dline(times=taus,lsty=3)
                pft.dmark(times=taus,mksiz=0.050)
                for mktau in mktaus:
                    if(mktau in taus):
                        pft.dmark(times=[mktau],mksiz=0.100)
                        pft.dmark(times=[mktau],mkcol=0,mksiz=0.070)
                        pft.dmark(times=[mktau],mkcol=mkcols[mktau],mksiz=0.040)


    

        ttl=ga.gp.title
        ttl.set(scale=0.85)
        
        t2='mdeck2 best track'
        if(title2 != None):
            t2=title2
        if(hasattr(self,'pbasin')):
            t1='pTCs for basin: ',self.pbasin.upper()
            t2='md2 BT'
        else:
            btvmax=max(self.avmaxs)
            t1='TC: %s [%s]  V`bmax`n: %3dkt'%(self.stmid,self.stmname,btvmax)

        ttl.top(t1,t2)

        if(self.Window): ga('q pos')

        #ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,background=self.background,verb=1)



    def PlotTrkAll(self,stmids,dobt=0,
                dtg0=None,nhbak=None,nhfor=None,
                ddtg=6,dtg0012=1,maxbt=55,
                doalltaus=1,otau=48,etau=120,dtau=12):


        ga=self.ga
        ge=self.ge

        pbt=ga.gp.plotTcBt
        cb=ga.gp.cbarn
        
        nTot=0
        nDev=0
        nNonDev=0
        
        pcolsN=[72,73,74,75,77,79]
        pcolsNReverse=[79,77,75,74,73,72]
        pcolsD=[22,23,35,37,39,29]
 
        devstmids=[]
        
        for stmid in stmids:
            
            BT=self.tD.makeBestTrk2(stmid,dobt=dobt)
            (ocard,ocards)=self.tD.lsDSsStm(stmid,dobt=dobt,sumonly=1,doprintSum=0)
            (ocardBT,ocardsBT)=self.tD.lsDSsStm(stmid,dobt=1,sumonly=1,doprintSum=0)
            tt=ocard.split(':')
            
            totTime=float(ocard.split(':')[2].split(';')[0])
            totTimeBT=float(ocardBT.split(':')[2].split(';')[0])

            totTime9X=float(ocard.split(':')[2].split(';')[1])
            totTime9XBT=float(ocardBT.split(':')[2].split(';')[1])
            
            #print 'TTTTTTTT',stmid,ocard.split(':')[2].split(';'),ocardBT.split(':')[2].split(';')
            print 'TTTTTTTT',stmid,totTime,totTimeBT,totTime9X,totTime9XBT
            
            pbt.set(BT.btrk,dtg0=dtg0,nhbak=nhbak,nhfor=None,ddtg=ddtg,dtg0012=dtg0012,maxbt=maxbt)
            
            nTot=nTot+1
            if(IsNN(stmid)):
                dev=1
                devstmids.append(stmid)
                nDev=nDev+1
            else:    
                nNonDev=nNonDev+1
                dev=0
                
            if(stmid == stmids[0]):
                bm=ga.gp.basemap2
                bm.set(landcol='atcfland',oceancol='atcfocean')
                bm.draw()
                
            ge.setPlotScale()
    
            lcol=15
            lthk=5
            mkcol=0
            mkcolB=1
            mkcolE=0
            mksizB=0.040
            mksizE=0.050
            if(dev): 
                lcol=2
                lthk=6
                mksiz=0.035
                mkcol=9
                mkcolB=1
                mkcolE=9
                mksizE=0.075
            
            if(Is9X(stmid)): totTime=totTime9X
            
            print 'stmid: ',stmid,'totTime: ',totTime,'DevFlag: ',dev
            
            if(totTime <= 1.0):
                lcolD=pcolsD[0]
                lcolN=pcolsN[0]
            elif(totTime > 1.0 and totTime <= 2.5):
                lcolD=pcolsD[1]
                lcolN=pcolsN[1]
            elif(totTime > 2.5 and totTime <= 4.0):
                lcolD=pcolsD[2]
                lcolN=pcolsN[2]
            elif(totTime > 4.0 and totTime <= 5.5):
                lcolD=pcolsD[3]
                lcolN=pcolsN[3]
            elif(totTime > 5.5 and totTime <= 7.0):
                lcolD=pcolsD[4]
                lcolN=pcolsN[4]
            elif(totTime > 7.0):
                lcolD=pcolsD[5]
                lcolN=pcolsN[5]
                
            if(dev): 
                lcol=lcolD
            else:
                lcol=lcolN
                lthk=4
            
            pbt.dline(times=pbt.otimes,lcol=lcol,lsty=1,lthk=lthk)
            if(dev):
                pbt.dmark(times=pbt.otimes[0:1],mksym=3,mksiz=mksizB,mkcol=mkcolB)
                pbt.dmark(times=pbt.otimes[-1:],mksym=3,mksiz=mksizE,mkcol=mkcolE)
            else:
                pbt.dmark(times=pbt.otimes[0:1],mksym=3,mksiz=mksizB,mkcol=mkcolB)
                pbt.dmark(times=pbt.otimes[-1:],mksym=3,mksiz=mksizE,mkcol=mkcolE)
                
        ttl=ga.gp.title
        ttl.set(scale=0.85)
        
        pDev=(float(nDev)/float(nTot))*100.0
        
        devstmids.sort()
        
        print 'SSS: ',nTot,nDev,nNonDev,pDev
        if(hasattr(self,'pbasin')):
            t1='Dev v NonDev pTCs for basin: %s nTot: %d nDev: %d  %% Dev: %3.0f'%(self.pbasin.upper(),nTot,nDev,pDev)
            t2='%s -> %s'%(devstmids[0],devstmids[-1])
        else:
            btvmax=max(self.avmaxs)
            t1='TC: %s [%s]  V`bmax`n: %3dkt'%(self.stmid,self.stmname,btvmax)
            t2='mdeck2 best track'
        ttl.top(t1,t2)

        if(self.Window): ga('q pos')
        
        pcols=[79,   77,  75,   74,  73,   72, 22, 23,  24,  35, 47,   29]
        pcols=pcolsNReverse + pcolsD
        pcuts=[ -7.0, -5.5, -4.0, -2.5, -1.0, 0.0, 1.0, 2.5, 4.0, 5.5, 7.0]
        
        cb.draw(sf=0.75, vert=1, side=None, xmid=None, ymid=None, sfstr=1.0, 
               pcuts=pcuts, pcols=pcols, quiet=0)
        
        #ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,background=self.background,verb=1)
        


    def xvPlot(self,ropt='',xb='-50',yb='+50',zfact=1.25):
        cmd="xv  -geometry %ix%i%s%s %s"%(self.xsize*zfact,self.ysize*zfact,xb,yb,self.pltpath)
        #cmd="xv %s"%(self.pltpath)
        MF.runcmd(cmd,ropt)

    def cp2Dropbox(self,ropt='',Dropdir='~/Dropbox/TC'):
        cmd="cp %s %s/."%(self.pltpath,Dropdir)
        MF.runcmd(cmd,ropt)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# w2gabase

class W2GaBase(MFbase):
    
    def c(self):
        self._cmd('clear')
        
    def d(self,var):
        rc=self._cmd('d %s'%(var))
        return(rc)
        
    def q(self,var):
        rc=self.query(var)
        return(rc)
        
        
    def getGxout(self):

        self('q gxout')
        g1s=self.rword(2,6)
        g1v=self.rword(3,6)
        g2s=self.rword(4,6)
        g2v=self.rword(5,6)
        stn=self.rword(6,4)
        gxout=gxGxout(g1s,g1v,g2s,g2v,stn)
        return(gxout)


    def getExprStats(self,expr):

        # get the current graphics and rank of display grid
        rank=len(self.coords().shape)
        cgxout=self.getGxout()

        # set gxout to stats; display expression
        self('set gxout stat')
        self('d %s'%(expr))
        cards=self.Lines

        # reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))
        exprstats=gxStats(cards)
        return(exprstats)


    def resetCurgxout(self,cgxout):

        rank=len(self.coords().shape)
        #reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))


    def LogPinterp(self,var,lev,texpr=None,mfact=None,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                if(mfact != None):
                    f2=f2*mfact
                    f1=f1*mfact
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2

                if(texpr == None):
                    expr="(%s(lev=%-6.1f)*%f + %s(lev=%-6.1f)*%f)"%(var,lev1,f1,var,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev1,f1)
                        
                else:
                    expr="(%s(%s,lev=%-6.1f)*%f + %s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1,var,texpr,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1)
                    
                expr=expr.replace(' ','')

                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)



    def LogPinterpTinterp(self,var,lev,tm1=1,tp1=1,tfm1=0.5,tfp1=0.5,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2
                    
                exprm1="( (%s(t-%d,lev=%-6.1f)*%f + %s(t-%d,lev=%-6.1f)*%f)*%f )"%(var,tm1,lev1,f1,var,tm1,lev2,f2,tfm1)
                exprp1="( (%s(t+%d,lev=%-6.1f)*%f + %s(t+%d,lev=%-6.1f)*%f)*%f )"%(var,tp1,lev1,f1,var,tp1,lev2,f2,tfp1)
                expr="(%s + %s)"%(exprm1,exprp1)
                
                expr=expr.replace(' ','')
                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)


class GradsEnv(MFbase):

    def __init__(self,
                 lat1=-90.0,
                 lat2=90.0,
                 lon1=0.0,
                 lon2=360.0,
                 pareaxl=0.5,
                 pareaxr=10.0,
                 pareayb=0.5,
                 pareayt=8.0,
                 orientation='landscape',
                 xlint=10.0,
                 ylint=5.0,
                 lintscale=1.0,
                 mapdset='hires',
                 mapcol=15,
                 mapstyle=0,
                 mapthick=6,
                 backgroundColor=0,
                 grid='on',
                 gridcol=1,
                 gridstyle=3,
                 pngmethod='printim',
                 gradslab='off',
                 timelab='off',
                 quiet=0,
                 verb=0,
                 xsize=1024,
                 ysize=768,
                 ):


        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
        self.pareaxl=pareaxl
        self.pareaxr=pareaxr
        self.pareayb=pareayb
        self.pareayt=pareayt
        self.xlint=xlint
        self.ylint=ylint
        self.lintscale=lintscale

        self.mapdset=mapdset
        self.mapcol=mapcol
        self.mapstyle=mapstyle
        self.mapthick=mapthick

        self.backgroundColor=backgroundColor
        
        self.grid=grid
        self.gridcol=gridcol
        self.gridstyle=gridstyle

        self.pngmethod=pngmethod

        self.timelab=timelab
        self.gradslab=gradslab

        self.verb=verb

        self.xsize=xsize
        self.ysize=ysize
        



    def makePng(self,
                opath,
                bmpath=None,
                bmcol=0,
                xsize=None,
                ysize=None,
                background='black',
                ropt='',
                verb=1,
                ):

        # -- this the xsize on the _ge object = self; from the set method in gXbasemap2
        #
        if(xsize == None and hasattr(self,'xsize')): xsize=self.xsize
        if(ysize == None and hasattr(self,'ysize')): ysize=self.ysize
        
        if(self.pngmethod == 'printim'):
            bkopt=''
            if(background == 'black'):
                bkopt='black'
            if(bmpath == None):
                cmd="%s %s %s x%d y%d"%(self.pngmethod,opath,bkopt,xsize,ysize)
            else:
                cmd="%s %s %s -b %s -t %d x%d y%d"%(self.pngmethod,opath,bkopt,bmpath,bmcol,xsize,ysize)

        elif(self.pngmethod == 'gxyat'):
            bkopt=''
            if(background == 'black'):
                bkopt='-r'
            cmd="%s -x %d -y %d %s %s"%(self.pngmethod,xsize,ysize,bkopt,opath)

        if(verb):
            print "makePng: %s cmd: %s"%(opath,cmd)

        self._cmd(cmd)

        
    def makePngTransparent(self,opath,ropt=''):
        
        cmd="convert -transparent black %s %s"%(opath,opath)
        runcmd(cmd)
        
        cmd="convert -transparent white %s %s"%(opath,opath)
        runcmd(cmd)
        
    def makePngDissolve(self,pathfeature,pathbase,pathall,
                       disolvfrc=25,
                       ropt=''):

        cmd="composite -dissolve %f %s %s %s"%(disolvfrc,pathfeature,pathbase,pathall)
        runcmd(cmd)
        
        
    def setMap(self):

        self._cmd('set mpdset %s'%(self.mapdset))
        self._cmd('set map %d %d %d'%(self.mapcol,self.mapstyle,self.mapthick))
                  

    def setFwrite(self,name,type='-sq'):

        cmd="""set fwrite %s %s"""%(type,name)
        self._cmd(cmd)



    def drawMap(self):
        self._cmd('draw map')

    def clear(self):
        self._cmd('c')
        

    def getLevs(self,obj=None,verb=0):

        if(obj != None and hasattr(obj,'fh') ):
            fh=obj.fh

        elif(hasattr(self,'fh')):
            fh=self.fh
        else:
            print """WWW in GradsLevs...need a 'fh' var to get filemeta data..."""
            sys.exit()

        if(obj == None): obj=self
        nz=fh.nz
        self.dimLevs=obj.dimLevs=list(self._ga.coords().lev)
        self.dimNlevs=obj.dimNlevs=len(self.dimLevs)
        self._cmd("set z 1 %d"%(nz))
        self.Levs=obj.Levs=list(self._ga.coords().lev)
        if(verb): print 'getLevs: nz: ',nz,'levs: ',self.Levs
        self._cmd("set z 1")
            

    def getFileMeta(self,obj=None):

        if(obj != None and hasattr(obj,'fh') ):
            fh=obj.fh

        elif(hasattr(self,'fh')):
            fh=self.fh
        else:
            print """WWW in GradsEnv...need a 'fh' var to get filemeta data..."""
            sys.exit()
            
        if(obj == None): obj=self

        self.nx=obj.nx=fh.nx
        self.ny=obj.ny=fh.ny
        self.nz=obj.nz=fh.nz
        self.nt=obj.nt=fh.nt
        self.undef=obj.undef=fh.undef

        self.dimlevs=obj.dimlevs=list(self._ga.coords().lev)
        self.dimNlevs=obj.dimNlevs=len(obj.dimlevs)
        self._cmd("set z 1 %d"%(self.nz))

        self.lats=obj.lats=list(self._ga.coords().lat)
        self.lons=obj.lons=list(self._ga.coords().lon)
        if(len(self.lons) > 1):
            self.dlon=obj.dlon=self.lons[1]-self.lons[0]
        else:
            self.dlon=0.0
        
        self.levs=obj.levs=list(self._ga.coords().lev)
        self._cmd("set lev %d"%(self.dimlevs[0]))

        self.vars=obj.vars=list(fh.vars)



    def getGxinfo(self):

        self._cmd('q gxinfo')
        
        #n  1 Last Graphic = Contour
        #n  2 Page Size = 11 by 8.5
        #n  3 X Limits = 0.5 to 10.5
        #n  4 Y Limits = 1.25 to 7.25
        #n  5 Xaxis = Lon  Yaxis = Lat
        #n  6 Mproj = 2

        self.lastgraphic=self.rw(1,4)
        self.pagex=float(self.rw(2,4))
        self.pagey=float(self.rw(2,6))
        self.plotxl=float(self.rw(3,4))
        self.plotxr=float(self.rw(3,6))
        self.plotyb=float(self.rw(4,4))
        self.plotyt=float(self.rw(4,6))
        self.xaxis=self.rw(5,3)
        self.yaxis=self.rw(5,6)

    def getGxout(self):

        self._cmd('q gxout')
        self.gxoutg1s=self.rw(2,6)
        self.gxoug1v=self.rw(3,6)
        self.gxoug2s=self.rw(4,6)
        self.gxoug2v=self.rw(5,6)
        self.gxoustn=self.rw(6,4)

    def getShades(self,verb=0):

        self._cmd('q shades')
        nl=self._ga.nLines
        
        self.nshades=int(self.rw(1,5))

        self.colbar=[]
        for n in range(2,nl+1):
            col=int(self.rw(n,1))
            minval=self.rw(n,2)
            maxval=self.rw(n,3)
            # -- new outout from q shades in 2.0.0.oga1
            #
            if(minval == '<' or minval == '<='):
                minval=-1e20
                maxval=float(maxval)
            elif(maxval == '>' or maxval == '>='):
                minval=float(minval)
                maxval=1e20
            else:
                minval=float(minval)
                maxval=float(maxval)

            self.colbar.append([col,minval,maxval])
            if(verb): print "III(GradsEnv.getShades):",n,col,minval,maxval,self.colbar

    def setShades(self,pcuts,pcols):

        nl=len(pcols)
        self.nshades=nl

        self.colbar=[]

        for n in range(0,nl):
            col=pcols[n]

            if(n == 0):
                minval=-1e20
                maxval=pcuts[n]
            elif(n == nl-1):
                minval=pcuts[n-1]
                maxval=1e20
            else:
                minval=pcuts[n-1]
                maxval=pcuts[n]

            minval=float(minval)
            maxval=float(maxval)
            
            self.colbar.append([col,minval,maxval])

        

    def getShadeCol(self,val):

        if(not(hasattr(self,'colbar'))):
            print 'WWW need to run getShades() before using getShadeCol()'
            return
        
        rval=float(val)
        for colb in self.colbar:
            (col,minval,maxval)=colb
            if(rval > minval and rval <= maxval):
                return(col)

        
        

    def setParea(self):

        self._cmd("set parea %6.3f %6.3f %6.3f %6.3f"%(self.pareaxl,
                                                       self.pareaxr,
                                                       self.pareayb,
                                                       self.pareayt))


    def setGrid(self):
        self._cmd('set grid %s %d %d'%(self.grid,self.gridcol,self.gridstyle))
        
        
    def setXylint(self,scale=None):

        if(scale == None):  lscale=self.lintscale
        else: lscale=scale
        xlint=self.xlint*lscale
        ylint=self.ylint*lscale
        self._cmd("set xlint %6.3f"%(xlint))
        self._cmd("set ylint %6.3f"%(ylint))

    def setXsize(self,xsize=1024,ysize=768):

        if(hasattr(self,'xsize')): xsize=self.xsize
        if(hasattr(self,'ysize')): ysize=self.ysize
        
        self._cmd("set xsize %d %d"%(xsize,ysize))

    def setPlotScale(self):
        self._cmd('set grads %s'%(self.gradslab))
        self._cmd('set timelab %s'%(self.timelab))
        self._cmd('set cmax -1e20')
        self._cmd('set grid on 3 15')
        
        # -- the lat var is displayed differently than a real data var -- use only if one not available
        # -- not really this is a red herring -- conflict with how display is calc with grids that are not 1.0 0.5 deg...
        # -- must be something in the xfrm in grads?  when setting lat/lon to NOT be a multiple of the grid res? pretty weird
        #
        dumvar='lat'
        if(hasattr(self,'vars')): dumvar=self.vars[0]
        
        # -- case of dum.ctl -- use 'lat'
        #
        if(dumvar == 'dum' or dumvar == 't'): dumvar='lat'

        # -- this doesn't work when dumvar in self.vars[0] is undef
        #exprdum="const(%s,1,-a)"%(dumvar)
        #
        # -- 20190224 -- force use of 'lat' with 2.2.1
        #
        dumvar='lat'
        exprdum=dumvar
        
        self._cmd('q dims')
        self._cmd('q ctlinfo')
        self._cmd('d abs(%s)'%(exprdum))


    def setLatLon(self):
        self._cmd("set lat %f %f"%(self.lat1,self.lat2))
        self._cmd("set lon %f %f"%(self.lon1,self.lon2))

    def setLevs(self):

        if(not(hasattr(self,'lev2'))):
            self.lev2=self.lev1
        self._cmd("set lev %f %f"%(self.lev1,self.lev2))

    def setBackgroundColor(self):
        self._cmd("set background %d"%(self.backgroundColor))
        
    def setColorTable(self,table='jaecolw2.gsf'):
        self._cmd("run %s"%(table))

    def setTimebyDtg(self,dtg,verb=0):
        gtime=mf.dtg2gtime(dtg)
        self.gtime=gtime
        if(verb): print "set time to: %s  from: %s"%(gtime,dtg)
        self.cmdQ("set time %s"%(gtime))

    def setTimebyDtgTau(self,dtg,tau,verb=0):
        vdtg=mf.dtginc(dtg,tau)
        gtime=mf.dtg2gtime(vdtg)
        self.gtime=gtime
        if(self.verb or verb): print "set time to: %s  from dtg: %s tau: %d"%(gtime,dtg,tau)
        self.cmdQ("set time %s"%(gtime))

    def reinit(self):
        self._cmd("reinit")
        
class GradsPlot(MFbase):


    def __init__(self,ga,ge):

        self.basemap=gXbasemap(ga,ge)
        self.basemap2=gXbasemap2(ga,ge)
        
        self.title=gXtitle(ga,ge)
        self.plotTcBt=gXplotTcBt(ga,ge)
        self.plotTcFt=gXplotTcFt(ga,ge)
        self.plotTcFtVmax=gXplotTcFtVmax(ga,ge)
        self.polyCircle=gXpolyCircle(ga,ge,ga)
        self.arrow=gXarrow(ga,ge,ga)
        self.cbarn=gXcbarn(ga,ge)

class gXbasemap2(MFbase):


    from mfbase import ptmpBaseDir
    
    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()
        
        

    def set(self,
            lcol=90,
            ocol=91,
            lcolrgb='set rgb 90 100 50 25',
            ocolrgb='set rgb 91 10 20 85',
            bmname='basemap2',
            bmdir=ptmpBaseDir,
            xsize=None,
            ysize=None,
            quiet=0,
            landcol=None,
            oceancol=None,
            ):

        if(xsize == None and hasattr(self._ge,'xsize')): xsize=self._ge.xsize
        if(ysize == None and hasattr(self._ge,'ysize')): ysize=self._ge.ysize

        wC=w2Colors()

        if(landcol != None):
            hex=wC.W2Colors[landcol]
            (r,g,b)=wC.hex2rgb(hex)
            lcolrgb='set rgb %d %d %d %d'%(lcol,r,g,b)
            
        if(oceancol != None):
            hex=wC.W2Colors[oceancol]
            (r,g,b)=wC.hex2rgb(hex)
            ocolrgb='set rgb %d %d %d %d'%(ocol,r,g,b)

        self.lcol=lcol
        self.lcolrgb=lcolrgb
        self.ocol=ocol
        self.ocolrgb=ocolrgb

        self.gsdir=sbtGslibDir

        self.bmname=bmname
        self.bmdir=bmdir
        
        # -- for grads -- must be lower case...
        #
        obmdir=self.bmdir
        obmdirl=obmdir.lower()
        if(obmdir != obmdirl): obmdirl='/tmp'
        
        self.pngpath="%s/bm.%s.png"%(obmdirl,self.bmname)
        self.pngpath=self.pngpath.lower()

        self.xsize=xsize
        self.ysize=ysize
        

    def draw(self):

        if(self.ocolrgb != None):
            self._cmd(self.ocolrgb)
            
        if(self.lcolrgb != None):
            self._cmd(self.lcolrgb)
            
        self._cmd('%s/basemap.2 L %d 1 %s'%(self.gsdir,self.lcol,self.gsdir))
        self._cmd('%s/basemap.2 O %d 1 %s'%(self.gsdir,self.ocol,self.gsdir))
        self._cmd('draw map')


    def putPng(self):

        self._ge.makePng(self.pngpath,xsize=self.xsize,ysize=self.ysize)
        
        obmdir=self.bmdir
        obmdirl=obmdir.lower()
        if(obmdir != obmdirl):
            npngpath=self.pngpath.replace('/tmp',self.bmdir)
            opngpath=self.pngpath
            self.pngpath=npngpath
            cmd="mv -f %s %s"%(opngpath,self.pngpath)
            runcmd(cmd)


            
    

class gXbasemap(gXbasemap2):


    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()


    def set(self,
            lcol=90,
            ocol=91,
            lcolrgb='set rgb 90 100 50 25',
            ocolrgb='set rgb 91 10 20 85',
            quiet=0,
            ):
        
        
        self.lcol=lcol
        self.lcolrgb=lcolrgb
        self.ocol=ocol
        self.ocolrgb=ocolrgb

        self.gsdir=sbtGslibDir


    def draw(self):

        if(self.ocolrgb != None):
            self._cmd(self.ocolrgb)
            
        if(self.lcolrgb != None):
            self._cmd(self.lcolrgb)
            
        self._cmd('%s/basemap L %d M'%(self.gsdir,self.lcol))
        self._cmd('%s/basemap O %d M'%(self.gsdir,self.ocol))
        self._cmd('draw map')
    
class w2Colors(MFbase):

    def __init__(self,verb=0):
        import webcolors
        #Color2Hex={}
        #Color2Hex['black']='#000000'
        #Color2Hex['white']='#FFFFFF'

        #Color2Hex['navy']='#000080'
        #Color2Hex['blue']='#0000FF'
        #Color2Hex['royalblue']='#4169E1'
        #Color2Hex['steelblue']='#4682B4'
        #Color2Hex['usafblue']='#CCCCFF'
        #Color2Hex['mediumslateblue']='#7B68EE'
        #Color2Hex['mediumblue']='#0000CD'
        #Color2Hex['powderblue']='#B0E0E6'
        #Color2Hex['skyblue']='#87CEEB'
        #Color2Hex['lightblue']='#ADD8E6'
        #Color2Hex['deepskyblue']='#00BFFF'
        #Color2Hex['dodgerblue']='#1E90FF'

        #Color2Hex['yellow']='#FFFF00'
        #Color2Hex['gold']='#FFD700'
        #Color2Hex['yellowgreen']='#9ACD32'
        #Color2Hex['khaki']='#F0E68C'
        #Color2Hex['goldenrod']='#DAA520'
        #Color2Hex['lightgoldenrodyellow']='#FAFAD2'
        #Color2Hex['tan']='#D2B48C'
        #Color2Hex['peru']='#CD853F'
        #Color2Hex['sienna']='#A0522D'
        #Color2Hex['chocolate']='#D2691E'


        #Color2Hex['wheat']='#F5DEB3'
        #Color2Hex['usafgrey']='#51588E'
        #Color2Hex['grey']='#808080'

        #Color2Hex['garnet']='#990000'
        #Color2Hex['magenta']='#FF00FF'
        #Color2Hex['maroon']='#800000'

        #Color2Hex['lightgreen']='#90EE00'
        #Color2Hex['green']='#008000'
        #Color2Hex['greenyellow']='#ADFF2F'
        #Color2Hex['olive']='#808000'
        #Color2Hex['olivedrab']='#6B8E23'
        #Color2Hex['mediumturquoise']='#48D1CC'
        
        #Color2Hex['mediumseagreen']='#3CB371'
        #Color2Hex['darkgreen']='#006400'

        #Color2Hex['red']='#FF0000'
        #Color2Hex['tomato']='#FF4637'
        #Color2Hex['indianred']='#CD5C5C'
        #Color2Hex['darkred']='#8B0000'
        #Color2Hex['lightcoral']='#F08080'
        #Color2Hex['orange']='#FFA500'

        #Color2Hex['orchid']='#DA70D6'
        #Color2Hex['violet']='#EE82EE'
        #Color2Hex['fuchsia']='#FF00FF'

        #Color2Hex['purple']='#800080'
        #Color2Hex['indigo']='#4B0082'
        #Color2Hex['plum']='#DDA0DD'
        #Color2Hex['violetred']='#D02090'
        #Color2Hex['teal']='#008080'
        #Color2Hex['atcfland']='#FEDE85'
        #Color2Hex['atcfocean']='#B4FEFE'        

        colors=webcolors.CSS3_NAMES_TO_HEX.keys()
        Color2Hex=webcolors.CSS3_NAMES_TO_HEX
        Color2Hex['grey1']='#CCCCCC'
        Color2Hex['grey2']='#999999'
        Color2Hex['grey3']='#666666'
        Color2Hex['grey4']='#333333'
        Color2Hex['atcfland']='#FEDE85'
        Color2Hex['atcfocean']='#B4FEFE'        
        Color2Hex['violetred']='#D02090'
        
        if(verb):
            colors.sort()
            for color in colors:
                print color,Color2Hex[color]
        
        
        GaColorRgb={}

        GaColorRgb[0] =[0,0,0]
        GaColorRgb[1] =[255,255,255]
        GaColorRgb[2] =[250,60,60]
        GaColorRgb[3] =[0,220,0]
        GaColorRgb[4] =[30,60,255]
        GaColorRgb[5] =[0,200,200]
        GaColorRgb[6] =[240,0,130]
        GaColorRgb[7] =[230,220,50]
        GaColorRgb[8] =[240,130,40]
        GaColorRgb[9] =[160,0,200]
        GaColorRgb[10]=[160,230,50]
        GaColorRgb[11]=[0,160,255]
        GaColorRgb[12]=[230,175,45]
        GaColorRgb[13]=[0,210,140]
        GaColorRgb[14]=[130,0,220]
        GaColorRgb[15]=[170,170,170]

        GaColorName2Rgb={}
        GaColorName2Rgb['black']=GaColorRgb[0] 
        GaColorName2Rgb['white']=GaColorRgb[1] 
        GaColorName2Rgb['red']=GaColorRgb[2] 
        GaColorName2Rgb['green']=GaColorRgb[3] 
        GaColorName2Rgb['blue']=GaColorRgb[4] 
        GaColorName2Rgb['lightblue']=GaColorRgb[5] 
        GaColorName2Rgb['magenta']=GaColorRgb[6] 
        GaColorName2Rgb['yellow']=GaColorRgb[7] 
        GaColorName2Rgb['orange']=GaColorRgb[8] 
        GaColorName2Rgb['purple']=GaColorRgb[9] 
        GaColorName2Rgb['yellowgreen']=GaColorRgb[10]
        GaColorName2Rgb['mediumblue']=GaColorRgb[11]
        GaColorName2Rgb['darkyellow']=GaColorRgb[12]
        GaColorName2Rgb['aqua']=GaColorRgb[13]
        GaColorName2Rgb['darkpurple']=GaColorRgb[14]
        GaColorName2Rgb['gray']=GaColorRgb[15]

        #  0   background       0   0   0 (black by default)
        #  1   foreground     255 255 255 (white by default)
        #  2   red            250  60  60 
        #  3   green            0 220   0 
        #  4   dark blue       30  60 255 
        #  5   light blue       0 200 200 
        #  6   magenta        240   0 130 
        #  7   yellow         230 220  50 
        #  8   orange         240 130  40 
        #  9   purple         160   0 200 
        # 10   yellow/green   160 230  50 
        # 11   medium blue      0 160 255 
        # 12   dark yellow    230 175  45 
        # 13   aqua             0 210 140 
        # 14   dark purple    130   0 220 
        # 15   gray           170 170 170

        self.chex=Color2Hex
        self.W2Colors=Color2Hex
        self.cga=GaColorName2Rgb

        JaeCols={
            #light yellow to dark red
            21:'#FFFAAA',  # 255 250 170
            22:'#FFE878',  # 255 232 120
            23:'#FFC03C',  # 255 192 060
            24:'#FFA000',  # 255 160 000
            25:'#FF6000',  # 255 096 000
            26:'#FF3200',  # 255 050 000
            27:'#E11400',  # 225 020 000
            28:'#C00000',  # 192 000 000
            29:'#A50000',  # 165 000 000


            #light green to dark green
            31:'#E6FFE1',  # 230 255 225
            32:'#C8FFBE',  # 200 255 190
            33:'#B4FAAA',  # 180 250 170
            34:'#96F58C',  # 150 245 140
            35:'#78F573',  # 120 245 115
            36:'#50F050',  # 080 240 080
            37:'#37D23C',  # 055 210 060
            38:'#1EB41E',  # 030 180 030
            39:'#0FA00F',  # 015 160 015

            #light blue to dark blue
            41:'#C8FFFF',  # 200 255 255
            42:'#AFF0FF',  # 175 240 255
            43:'#82D2FF',  # 130 210 255
            44:'#5FBEFA',  # 095 190 250
            45:'#4BB4F0',  # 075 180 240
            46:'#3CAAE6',  # 060 170 230
            47:'#2896D2',  # 040 150 210
            48:'#1E8CC8',  # 030 140 200
            49:'#1482BE',  # 020 130 190

            #light purple to dark purple
            51:'#DCDCFF',  # 220 220 255
            52:'#C0B4FF',  # 192 180 255
            53:'#A08CFF',  # 160 140 255
            54:'#8070EB',  # 128 112 235
            55:'#7060DC',  # 112 096 220
            56:'#483CC8',  # 072 060 200
            57:'#3C28B4',  # 060 040 180
            58:'#2D1EA5',  # 045 030 165
            59:'#2800A0',  # 040 000 160

            #light pink to dark rose  
            61:'#FFE6E6',  # 255 230 230
            62:'#FFC8C8',  # 255 200 200
            63:'#F8A0A0',  # 248 160 160
            64:'#E68C8C',  # 230 140 140
            65:'#E67070',  # 230 112 112
            66:'#E65050',  # 230 080 080
            67:'#C83C3C',  # 200 060 060
            68:'#B42828',  # 180 040 040
            69:'#A42020',  # 164 032 032


            #light grey to dark grey
            71:'#FAFAFA',  # 250 250 250
            72:'#C8C8C8',  # 200 200 200
            73:'#A0A0A0',  # 160 160 160
            74:'#8C8C8C',  # 140 140 140
            75:'#707070',  # 112 112 112
            76:'#505050',  # 080 080 080
            77:'#3C3C3C',  # 060 060 060
            78:'#282828',  # 040 040 040
            79:'#202020',  # 032 032 032
        }

        self.JaeCols=JaeCols


    def hex2dec(self,s):
        return int(s, 16)

    def dec2hex(self,n):
        """return the hexadecimal string representation of integer n"""
        return "%X" % n

    def hex2rgb(self,scolor):

        r=self.hex2dec(scolor[1:3])
        g=self.hex2dec(scolor[3:5])
        b=self.hex2dec(scolor[5:7])
        return(r,g,b)


class gXplotTcBt(MFbase):

    btsizmx=0.275
    btsizmn=0.175
    btsizmx=0.150
    btsizmn=0.125
    btcols=[2,1,3,4]*20
    
    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        

    def set(self,
            bts,dtg0,
            nhbak=72,
            nhfor=0,
            lcol=1,
            lsty=1,
            lthk=5,
            msym=-1,
            mcol=-3,
            msiz=0.0125,
            mthk=5,
            bdtg=None,
            edtg=None,
            ddtg=6,
            ddtgbak=12,
            ddtgfor=12,
            quiet=1,
            dtg0012=0,
            maxbt=50,
            mcolTD=15,
            dttimeDefault=6,
            doland=1,
            maxlandFrac=0.80,
            btMinLand=35.0,
            ):
        
        self.initLF()
        
        ge=self._ge
        self.dtg0=dtg0
        self.nhbak=nhbak
        self.nhfor=nhfor

        self.doland=doland
        self.maxlandFrac=maxlandFrac

        # always clip the plots
        #
        ge.getGxinfo()
        self.clipplot="set clip %f %f %f %f"%(ge.plotxl,ge.plotxr,ge.plotyb,ge.plotyt)

        dtgs=bts.keys()
        dtgs.sort()

        self.dtgs=dtgs

        self.bdtg=bdtg
        self.edtg=edtg
        self.ddtg=ddtg

        if(self.bdtg != None):
            pdtgs=mf.dtgrange(bdtg,edtg,ddtg)
            
            if(len(pdtgs) > maxbt):
                ddtg=12
                self.ddtg=ddtg
                if(dtg0012):
                    bdtg=dtgShift0012(bdtg,round=1)
                    edtg=dtgShift0012(edtg,round=0)
                pdtgs=mf.dtgrange(bdtg,edtg,ddtg)


        else:
            # -- handle ddtg = 12 and dtg0 != None
            #
            if(nhfor == None):
                dtgfor=dtgs[-1]
                if(dtg0 != None and ddtg == 12):
                    if(MF.is0012Z(dtg0) and not(MF.is0012Z(dtgfor))):
                        dtgfor=dtgs[-2]
                    elif(MF.is0618Z(dtg0) and not(MF.is0618Z(dtgfor))):
                        dtgfor=dtgs[-2]
            else:
                if(dtg0 != None): dtgfor=mf.dtginc(dtg0,nhfor)

            if(dtg0012): dtgfor=dtgShift0012(dtgfor,round=0)
                
            # -- handle ddtg = 12 and dtg0 != None
            #
            if(nhbak == None):
                dtgbak=dtgs[0]
                if(dtg0 != None and ddtg == 12):
                    if(MF.is0012Z(dtg0) and not(MF.is0012Z(dtgbak))):
                        dtgbak=dtgs[1]
                    elif(MF.is0618Z(dtg0) and not(MF.is0618Z(dtgbak))):
                        dtgbak=dtgs[1]
                
            else:
                if(dtg0 != None): dtgbak=mf.dtginc(dtg0,-nhbak)

            if(dtg0012): dtgbak=dtgShift0012(dtgbak,round=1)
                

            if(dtg0 != None):
                pdtgsbak=mf.dtgrange(dtgbak,dtg0,ddtgbak)
                pdtgsfor=mf.dtgrange(dtg0,dtgfor,ddtgfor)
            else:
                pdtgsbak=[]
                pdtgsfor=[]
                
            pdtgs=mf.dtgrange(dtgbak,dtgfor,ddtg)

            if(len(pdtgs) > maxbt):
                ddtg=12
                self.ddtg=ddtg
                if(dtg0012):
                    dtgbak=dtgShift0012(dtgbak,round=1)
                    dtgfor=dtgShift0012(dtgfor,round=0)
                pdtgs=mf.dtgrange(dtgbak,dtgfor,ddtg)


        self.platlons={}
        self.pvmax={}
        self.pvmaxflg={}

        self.xys={}
        self.lineprop={}
        self.markprop={}

        odtgs=[]
        odtgsbak=[]
        odtgsfor=[]
        
        pdt=pdtgs.sort()
        n=0
        for dtg in dtgs:
            
            if(not(dtg in pdtgs)):  continue
            
            # -- get lat/lon and check if overland
            #
            plat=bts[dtg][0]
            plon=bts[dtg][1]
            btvmax=bts[dtg][2]
            
            landfrac=self.getLF(plat,plon)
            
            #print 'BBBB ',dtg,plat,plon,landfrac,btvmax
            # -- chuck point if overland and btvmax <= 35 kt (strong tcs overland)
            #
            if(self.doland == 0 and landfrac > self.maxlandFrac and btvmax <= btMinLand): continue            

            odtgs.append(dtg)
            if(dtg in pdtgsbak): odtgsbak.append(dtg)
            if(dtg in pdtgsfor): odtgsfor.append(dtg)
            
            if(len(bts[dtg]) == 8):
                tccode=bts[dtg][-2].lower()
                wncode=bts[dtg][-1].lower()

            # -- md3 btrk from cards
            #

            elif(len(bts[dtg]) == 20):
                tccode=bts[dtg][8].lower()
                wncode=bts[dtg][9].lower()
                
            # -- md3 from -SUM.txt
            #
            elif(len(bts[dtg]) == 22):
                tccode=bts[dtg][6].lower()
                wncode=bts[dtg][7].lower()
            
            else:
                tccode='xx'
                wncode='xx'

            self.platlons[dtg]=(plat,plon)
            self.pvmax[dtg]=btvmax

            self._cmd('q w2xy %f %f'%(plon,plat))
            
            x=float(self._cmd.rw(1,3))
            y=float(self._cmd.rw(1,6))
            self.xys[dtg]=([x,y])

            # -- colorize line seg
            #
            lthk=9
            lcol=0
            lsty=2
            if(btvmax >= 100 and IsTc(tccode) == 1):                   lcol=9  ; lsty=2 ; lthk=10
            if(btvmax >= 65  and btvmax < 100 and IsTc(tccode) == 1):  lcol=2  ; lsty=1
            if(btvmax >= 35  and btvmax < 65  and IsTc(tccode) == 1):  lcol=7  ; lsty=1
            if(btvmax <  35  and IsTc(tccode) == 1):                   lcol=3  ; lsty=1
            if(btvmax >= 35  and IsTc(tccode) == 2):                   lcol=8  ; lsty=1
            if(btvmax <  35  and IsTc(tccode) == 2):                   lcol=4  ; lsty=1
            if(IsTc(tccode) == 0):                                     lcol=10 ; lsty=3
            if(tccode == 'ex' or tccode == 'pt'):                      lcol=1  ; lsty=3
            
            self.lineprop[dtg]=(lcol,lsty,lthk)


            if(msym < 0):
                btsiz=self.btsizmx*(btvmax/135)
                if(btsiz<self.btsizmn): btsiz=self.btsizmn
                
                if(mcol < 0):
                    mcolTS=mcol*(-1)
                    mcolTY=2
                else:
                    mcolTS=mcol
                    mcolTY=mcol
                    
                btsym=41
                btthk=mthk
                
                btcol=mcolTY
                if(btvmax < 65):  btsym=40 ; btcol=mcolTS
                if(btvmax < 25):  btsym=1 ; btcol=mcolTD

                if(tccode != None):
                    if(not(IsTc(tccode))):      btsym=1  ; btcol=mcolTD
                    if(tccode.lower() == 'ex'): btsym=24 ; btcol=mcolTD
                    

                if(mcol < 0):
                    btcol=self.btcols[n]

            else:
                btsiz=msiz
                btsym=msym
                btcol=mcol
                btthk=mthk

            self.markprop[dtg]=(btsym,btsiz,btcol,btthk)
            n=n+1

        self.odtgs=odtgs

        if(dtg0 == None):
            self.otimesbak=odtgs
            self.otimesfor=odtgs
        else:
            self.otimesbak=odtgsbak
            self.otimesfor=odtgsfor

        self.otimes=odtgs
        # -- make sure there are at least two times...
        #
        if(len(self.otimes) > 1):
            self.dttime=dtgdiff(self.otimes[-2],self.otimes[-1])     
        else:
            self.dttime=dttimeDefault

    def initLF(self):
         
        #from w2 import SetLandFrac
        #from w2 import GetLandFrac
        
        self.lf=SetLandFrac()
        self.GetLandFrac=GetLandFrac
        

    def getLF(self,lat,lon):
        landfrac=self.GetLandFrac(self.lf,lat,lon)
        return(landfrac)


    def setGradsData(self,tdtg,
                     tname='btvmax',
                     tdir='/tmp',
                     ):
    
        cpath="%s/%s.%s.ctl"%(tdir,tname,tdtg)
        opath="%s/%s.%s.dat"%(tdir,tname,tdtg)
        
        # -- make the beginning time the 1st track
        #
        bdtg=self.otimes[0]
        bgtime=mf.dtg2gtime(bdtg)
        
        if(not(hasattr(self,'dttime'))): 
            dttime=dtgdiff(self.otimes[-2],self.otimes[-1])
            self.ddtime=dttime
        else:
            dttime=self.dttime
            
        tottime=dtgdiff(self.otimes[0],self.otimes[-1])
        
        nt=int(tottime/dttime)+1
        
        (rlat,rlon)=self.platlons[self.otimes[0]]
        self.platlons0=(rlat,rlon)
        
        ctl="""dset %s
title %s
undef 1e20
xdef 1  levels %6.1f
ydef 1  levels %5.1f
zdef 1  levels 1013
tdef %d linear %s %dhr
vars 1
bvm 0 0 %s
endvars"""%(opath,tname,rlon,rlat,
            nt,bgtime,dttime,
            tname)
        
        MF.WriteString2Path(ctl,cpath)

        stnid='btvmax01'
        stndt=0.0
        
        oB=open(opath,'wb')
        
        # - not station data..
        #stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,0)
        #stnfoot = struct.pack('8sfffii',stnid,rlat,rlon,stndt,0,0)

        for otime in self.otimes:
            #oB.write(stnhead)
            try:
                stnrec = struct.pack('1f',self.pvmax[otime])
            except:
                continue
            oB.write(stnrec)
            #oB.write(stnfoot)
        
        oB.close()
        



    def dline(self,times=None,
              lcol=None,
              lsty=None,
              lthk=None,
              ):

        if(times == None): times=self.otimes
        
        self._cmd(self.clipplot)

        if(len(times) < 2): return
        
        for n in range(1,len(times)):

            try:
                (x0,y0)=self.xys[times[n-1]]
            except:
                continue

            try:
                (x1,y1)=self.xys[times[n]]
            except:
                continue
            
            if(x0 == None or x1 == None): continue 

            (olcol,olsty,olthk)=self.lineprop[times[n]]

            # overrides
            #
            if(lcol != None): olcol=lcol
            if(lsty != None): olsty=lsty
            if(lthk != None): olthk=lthk
            
            self._cmd("set line %d %d %d"%(olcol,olsty,olthk))
            self._cmd("draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1))

        
    def dwxsym(self,times=None,
               wxsym=None,
               wxsiz=None,
               wxcol=None,
               wxthk=None,
               ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                if(x0 == None): continue
            except:
                continue

            (owxsym,owxsiz,owxcol,owxthk)=self.markprop[times[n]]
            
            if(wxsym != None): owxsym=wxsym
            if(wxsiz != None): owxsiz=wxsiz
            if(wxcol != None): owxcol=wxcol
            if(wxthk != None): owxthk=wxthk

            cmd="draw wxsym %d %6.3f %6.3f %6.3f %d %d"%(owxsym,x0,y0,owxsiz,owxcol,owxthk)
            self._cmd(cmd)

            self.wxcol=wxcol

    def dmark(self,times=None,
              mksym=None,
              mksiz=None,
              mkcol=None,
              mkthk=None,
              ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                if(x0 == None):  continue
            except:
                continue
            
            (omksym,omksiz,omkcol,omkthk)=self.markprop[times[n]]
            
            # overrides
            if(mksym != None): omksym=mksym
            if(mksiz != None): omksiz=mksiz
            if(mkcol != None): omkcol=mkcol
            if(mkthk != None): omkthk=mkthk
            
            cmd="set line %d 1 %d"%(omkcol,omkthk)
            self._cmd(cmd)
            cmd="draw mark %d %6.3f %6.3f %6.3f %d %d"%(omksym,x0,y0,omksiz,omkcol,omkthk)
            self._cmd(cmd)

            self.mksiz=omksiz
            self.mkcol=omkcol
            self.mkthk=omkthk

        
    def dlabel(self,times=None,
               lbsiz=0.10,
               lbcol=1,
               lbthk=5,
               #yoffset=0.10,
               yoffset=0.075,
               xoffset=0.05,
               location='c',
               dlab=None,
               rotate=-30,
               #rotate=30,
               ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                y0=y0-lbsiz*0.5-yoffset
                x0=x0-xoffset
                if(dlab == None):
                    label="%3d"%(self.pvmax[times[n]])
                else:
                    label=dlab
                if(x0 == None):  continue
            except:
                continue

            self._cmd('set string %d %s %d %d'%(lbcol,location,lbthk,rotate))
            self._cmd("set strsiz %f"%(lbsiz))
            self._cmd("draw string %f %f %s"%(x0,y0,label))


    def legend(self,ge,
               times=None,
               btcol=None,
               bttitle=None,
               btlgdcol=None,
               resetfinaly=0,
               hiTime=None,
               ystart=7.9,
               ):

        if(times == None): times=self.otimes

        ge=self._ge
        ge.getGxinfo()
        self._cmd("set clip 0 %6.3f 0 %6.3f"%(ge.pagex,ge.pagey))

        ssiz=0.60
        lscl=0.85
        xoffset=0.1
        x=ge.plotxr+(0.10)*(1.5/lscl)+xoffset
        xs=x+(0.15)*lscl

        if((not(hasattr(self,'finaly')) and ystart != None) or resetfinaly):
            y=ystart
        else:
            y=self.finaly
            
        dy=0.165*lscl
        yss=dy*ssiz*lscl
        sthk=6

        if(btlgdcol == None): btlgdcol=1

        for n in range(0,len(times)):
            if(n == 0 and bttitle != None):
                self._cmd('set string %s l %d'%(btlgdcol,sthk))
                self._cmd("set strsiz %f"%(yss))
                self._cmd("draw string %f %f %s"%(xs,y,bttitle))
                y=y-dy
                
                
            time=times[n]
            try:
                (obtsym,obtsiz,obtcol,obtthk)=self.markprop[time]
            except:
                continue
            
            if(btcol != None): obtcol=btcol
            cmd="draw wxsym %d %6.3f %6.3f %6.3f %d %d"%(obtsym,x,y,obtsiz,obtcol,obtthk)
            self._cmd(cmd)
            
            # -- hilite a dtg
            #
            if(hiTime != None and time == hiTime):
                self._cmd('set string 7 l %d'%(sthk+2))
                self._cmd("set strsiz %f"%(yss+0.001))
            else:
                self._cmd('set string 1 l %d'%(sthk))
                self._cmd("set strsiz %f"%(yss))
                
            lgd="- %s %3d"%(time[4:10],self.pvmax[time])
            lgd="%s %3d"%(time[4:10],self.pvmax[time])
            self._cmd("draw string %f %f %s"%(xs,y,lgd))
            y=y-dy

        self.finaly=y
        self.dy=dy
            


class gXplotTcFt(gXplotTcBt):
    

    def set(self,
            fts,lcol=-1,lsty=1,lthk=7,
            msym=3,mcol=3,msiz=0.05,mthk=5,
            dovmaxflg=1,
            doland=0,
            maxlandFrac=0.80,
            verb=0,
            quiet=0,
            ):

        self.dovmaxflg=dovmaxflg
        self.doland=doland
        self.maxlandFrac=maxlandFrac

        self.initLF()
        self.initVars(lcol,lsty,lthk,msym,mcol,msiz,mthk,verb)
        self.setPcutcols()
        self.initProps(fts)
        self.setLineProps()
        self.setMarkProps()


    # init and set methods
    #
    def initVars(self,lcol,lsty,lthk,msym,mcol,msiz,mthk,verb):
        self.lcol=lcol
        self.lsty=lsty
        self.lthk=lthk
        self.msym=msym
        self.mcol=mcol
        self.msiz=msiz
        self.mthk=mthk
        self.verb=verb

        
    def initProps(self,fts):

        ge=self._ge
        # always clip the plots
        #
        ge.getGxinfo()
        self.clipplot="set clip %f %f %f %f"%(ge.plotxl,ge.plotxr,ge.plotyb,ge.plotyt)

        taus=fts.keys()
        taus.sort()

        self.taus=taus

        self.platlons={}
        self.pvmax={}
        self.ppmin={}
        self.pdvmax={}
        self.pvmaxflg={}

        self.xys={}
        self.lineprop={}
        self.markprop={}

        otaus=[]
        
        n=0
        for tau in taus:

            try:
                plat=fts[tau][0]
                plon=fts[tau][1]
            except:
                print 'EEE gXplotTcFt plat exception: ',tau
                continue

            if(plon == None): continue

            landfrac=self.getLF(plat,plon)
            if(self.doland == 0 and landfrac > self.maxlandFrac): continue

            otaus.append(tau)
            
            try:    vmax=fts[tau][2]
            except: vmax=None
            
            try:    pmin=fts[tau][3]
            except: pmin=None
            
            try:    dvmax=fts[tau][4]
            except: dvmax=None
            
            try:     vmaxflg=fts[tau][5]
            except:  vmaxflg=0

            if(not(self.dovmaxflg)): vmaxflg=0

            if(self.verb): print 'eeeeeeeeeeeeeeeeeee',tau,plat,plon,vmax,pmin,dvmax,vmaxflg
            
            self.platlons[tau]=(plat,plon)
            self.pvmax[tau]=vmax
            self.ppmin[tau]=pmin
            self.pdvmax[tau]=dvmax
            self.pvmaxflg[tau]=vmaxflg

            self._cmd('q w2xy %f %f'%(plon,plat))
            self.xys[tau]=([float(self._cmd.rw(1,3)),float(self._cmd.rw(1,6))])

            n=n+1

        self.taus=otaus
        self.otimes=otaus


    def setLineProps(self):

        for tau in self.taus:
            try:
                dvmax=self.pdvmax[tau]
                vmaxflg=self.pvmaxflg[tau]
                self.setSegCol(tau,dvmax,vmaxflg)
            except:
                continue


    def setMarkProps(self):
        
        for tau in self.taus:
            ftsiz=self.msiz
            ftsym=self.msym
            ftcol=self.mcol
            ftthk=self.mthk

            self.markprop[tau]=(ftsym,ftsiz,ftcol,ftthk)


        
    def setPcutcols(self):
        
        pcuts=[-25,-20,-15,-10,-5,0,5,  10,  15,   20, 25]
        pcols=[41,43, 45, 47, 49,15,15, 29,  27,  25,  23,  21]
        pcols=[49,47, 45, 43, 41,15,15, 21,  23,  25,  27,  29]

        pcutsvmax=[  25,  35,  50,  65,  75,  85,  95,  105,  120]
        pcolsvmax=[15,  21,  22,  23,  24,  25,  26,  27,   28,  29]

        self.pcuts=pcuts
        self.pcols=pcols
        self._ge.setShades(pcuts,pcols)

    
    def setSegCol(self,tau,dvmax,vmaxflg):

        if(self.lcol == -1 or self.lcol == -2):
            olcoldef=75
            olthkdef=4
            olsty=self.lsty
            if(dvmax != None):
                if(vmaxflg == 1): olcol=self._ge.getShadeCol(dvmax) ; olthk=6
                elif(vmaxflg == 0): olcol=olcoldef ; olthk=olthkdef
                elif(vmaxflg == -1): olcol=self._ge.getShadeCol(dvmax) ; olthk=5
            else:
                olcol=olcoldef
                olthk=olthkdef
        else:
            olcol=self.lcol
            olsty=self.lsty
            olthk=self.lthk

        self.lineprop[tau]=(olcol,olsty,olthk)


    def cbarn(self,sf=1.0,vert=1,side=None):

        self._cmd("set clip 0 %6.3f 0 %6.3f"%(self._ge.pagex,self._ge.pagey))
        cb=cbarn(self._ga,self._ge,vert=vert,side=side,sf=sf)

 
    def setGradsData(self,tdtg,
                     dttime=None,
                     tname='fcvmax',
                     platlons=None,
                     tdir='/tmp',
                     undef=1e20,
                     maxtau=None,
                     ):
    
        cpath="%s/%s.%s.ctl"%(tdir,tname,tdtg)
        opath="%s/%s.%s.dat"%(tdir,tname,tdtg)
        
        bgtime=mf.dtg2gtime(tdtg)
        if(maxtau != None):
            tottime=maxtau
        else:
            tottime=self.otimes[-1]-self.otimes[0]

        if(len(self.otimes) > 1 and dttime == None):
            dttime=self.otimes[1]-self.otimes[0]
            
        nt=int(tottime/dttime)+1
        
        if(platlons == None):
            (rlat,rlon)=self.platlons[self.otimes[0]]
        else:
            (rlat,rlon)=platlons
        
        ctl="""dset %s
title %s
undef %10.0e
xdef 1  levels %6.1f
ydef 1  levels %5.1f
zdef 1  levels 1013
tdef %d linear %s %dhr
vars 1
fvm 0 0 %s
endvars"""%(opath,tname,undef,rlon,rlat,
            nt,bgtime,dttime,
            tname)
        
        MF.WriteString2Path(ctl,cpath)

        stnid='btvmax01'
        stndt=0.0
        
        oB=open(opath,'wb')
        
        for n in range(0,int(tottime/dttime)+1):
            otime=n*dttime
            if(otime in self.otimes): ovmax=self.pvmax[otime]
            else:                     ovmax=undef
            
            # -- 20180520 - case with aid not having Vmax
            #
            if(ovmax < 0.0): ovmax=undef
            stnrec = struct.pack('1f',ovmax)
            oB.write(stnrec)
        
        oB.close()
        



    
class gXplotTcFtVmax(gXplotTcFt):


    def set(self,
            fts,lcol=-1,lsty=1,lthk=7,
            msym=3,mcol=3,msiz=0.05,mthk=5,
            dovmaxflg=1,
            doland=0,
            verb=0,
            quiet=0,
            ):
        
        self.dovmaxflg=dovmaxflg
        self.doland=doland

        self.initLF()
        self.initVars(lcol,lsty,lthk,msym,mcol,msiz,mthk,verb)
        self.setPcutcols()
        self.initProps(fts)
        self.setLineProps()
        self.setMarkProps()


    def setLineProps(self):

        for tau in self.taus:
            vmax=self.pvmax[tau]
            self.setSegCol(tau,vmax)

    def setPcutcols(self):
        
        pcuts=[  25,  35,  50,  65,  90,  120]
        pcols=[15,   7,   4,  3,    2,   14,   2]

        self.pcuts=pcuts
        self.pcols=pcols
        self._ge.setShades(pcuts,pcols)

    
    def setSegCol(self,tau,vmax):

        if(vmax != None and self.lcol == -1):
            if(vmax >= 65.0): olcol=self._ge.getShadeCol(vmax) ; olthk=6
            else: olcol=self._ge.getShadeCol(vmax) ; olthk=5
            olsty=self.lsty
        else:
            olcol=self.lcol
            olsty=self.lsty
            olthk=self.lthk
            
        self.lineprop[tau]=(olcol,olsty,olthk)

    
class gXpolyCircle(MFbase):

    def __init__(self,ga,ge,cmd):

        self._ga=ga
        self._cmd=cmd
        self._ge=ge


    def set(self,clat,clon,radii,
            dtheta=10,
            dodisplay=0,
            hemiDir=None,
            ):
        
        from tcbase import rumltlg

        self.clat=clat
        self.clon=clon

        self.platlons=[]
        dtau=12.0
        spdc=radii/dtau
        

        for theta in range(0,360+1,dtheta):
            (plat,plon)=rumltlg(theta,spdc,dtau,clat,clon)
            self.platlons.append([plat,plon])

        if(dodisplay):
            self._cmd('set cmax -1000')
            self._cmd('d lat')

        self.xys=[]
        for (plat,plon) in self.platlons:
            if(plat == None): continue
            self._cmd('q w2xy %f %f'%(plon,plat))
            self.xys.append([float(self._ga.rword(1,3)),float(self._ga.rword(1,6))])

        if(hemiDir != None):
            self.xysh=[]
            for theta in [hemiDir,hemiDir+180]:
                (plat,plon)=rumltlg(theta,spdc,dtau,clat,clon)
                if(plat == None): continue
                self._cmd('q w2xy %f %f'%(plon,plat))
                self.xysh.append([float(self._ga.rword(1,3)),float(self._ga.rword(1,6))])



    def fill(self,lcol=1):

        self._cmd("set line %d"%(lcol))
        pcmd='draw polyf '

        for (x,y) in self.xys:
            pcmd=pcmd+"%6.3f %6.3f"%(x,y)

        print pcmd
        self._cmd(pcmd)

        
    def border(self,lcol=1,lsty=1,lthk=5):

        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))
        
        for n in range(1,len(self.xys)):
            (x0,y0)=self.xys[n-1]
            (x1,y1)=self.xys[n]
            
            cmd="draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1)
            self._cmd(cmd)

    def hemiline(self,hemidir,lcol=1,lsty=1,lthk=5):

        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))

        for n in range(1,len(self.xysh)):
            (x0,y0)=self.xysh[n-1]
            (x1,y1)=self.xysh[n]
            
            cmd="draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1)
            self._cmd(cmd)

class gXarrow(MFbase):

    def __init__(self,ga,ge,cmd):

        self._ga=ga
        self._cmd=cmd
        self._ge=ge


    def set(self,latc,lonc,len,dir,
            arrang=30.0,
            arrscl=0.20,
            lab=None,labopt=None,
            dodisplay=0,
            verb=0,
            ):
        
        from tcbase import rumltlg

        self.len=len
        self.dir=dir

        self.lab=lab
        self.labopt=labopt

        self._cmd('q w2xy %f %f'%(lonc,latc))

        x=float(self._ga.rword(1,3))
        y=float(self._ga.rword(1,6))

        dd=deg2rad*dir
        arrlen=len*arrscl

        xl=sin(dd)*len
        yl=cos(dd)*len

        da1=(dir+arrang)*deg2rad
        da2=(dir-arrang)*deg2rad
        
        xa1=sin(da1)*arrlen
        ya1=cos(da1)*arrlen
        
        xa2=sin(da2)*arrlen
        ya2=cos(da2)*arrlen
        
        xa1=x+xl-xa1
        ya1=y+yl-ya1
        
        xa2=x+xl-xa2
        ya2=y+yl-ya2
        
        x1=x+xl
        y1=y+yl

        if(verb):
            print 'arrow: '
            print '            x,y: ',x,y
            print '          x1,y1: ',x1,y1
            print 'xa1,ya1,xa2,ya2: ',xa1,ya1,xa2,ya2
            
        self.x=x
        self.y=y
        self.x1=x1
        self.y1=y1
        self.xa1=xa1
        self.ya1=ya1
        self.xa2=xa2
        self.ya2=ya2

        return


    def draw(self,lcol=1,lsty=1,lthk=5,doblackout=0,doblackin=0):

        # -- set outside black
        #
        if(doblackout):
            self._cmd("set line %d %d %d"%(0,lsty,20))
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)

        # -- draw the arrow
        #
        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))
        pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
        pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
        pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)

        # -- set inside black
        #
        if(doblackin):
            self._cmd("set line %d %d %d"%(0,lsty,3))
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)



class gXcbarn(MFbase):


    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge


    def draw(self,
                 sf=1.0,
                 vert=-1,
                 side=None,
                 xmid=None,
                 ymid=None,
                 sfstr=1.0,
                 pcuts=None,
                 pcols=None,
                 quiet=0,
                 ):

        ge=self._ge
        
        ge.getGxinfo()

        if(pcuts != None and pcols != None):
            ge.setShades(pcuts,pcols)

        # -- check if ge has colbar -- 20130816 -- not sure why I did this
        # -- 20150311 -- because ge.setShades adds colbar var to ge.
        #
        elif(hasattr(ge,'colbar')):
            print 'III(ga2.gXcbarn.ge.setShades: ',ge.colbar
            None    
        else:
            # -- get shades if not set above adds ge.colbar
            ge.getShades()


        xsiz= ge.pagex
        ysiz= ge.pagey
        ylo=  ge.plotyb
        yhi=  ge.plotyt
        xhi=  ge.plotxr
        xlo=  ge.plotxl
        xd= xsiz-xhi

        ylolim=0.6*sf
        xdlim1=1.0*sf
        xdlim2=1.5*sf  
        barsf=0.8*sf
        yoffset=0.3*sf
        stroff=0.05*sf
        strxsiz=0.12*sf*sfstr
        strysiz=0.13*sf*sfstr

        if(ylo < ylolim and xd < xdlim1):
            print "Not enough room in plot for a colorbar"
            return
        
        #
        #  Decide if horizontal or vertical color bar
        #  and set up constants.
        #
        cnum=ge.nshades
        #
        #	logic for setting the bar orientation with user overides
        #
        if(ylo<ylolim or xd>xdlim1):
            vchk=1
        else:
            vchk=0

        if(vert >= 0): vchk=vert

        if(vchk == 1):
            
            #
            #	vertical bar
            #
            if(xmid == None): xmid=xhi+xd/2
            if(side == 'left'):
                xmid=0.0+xlo*0.35
            
            xwid=0.2*sf
            ywid=0.5*sf
            xl=xmid-xwid/2
            xr=xl+xwid

            if(ywid*cnum > ysiz*barsf): 
                ywid=ysiz*barsf/cnum
                
            if(ymid == None): ymid=ysiz/2
            yb=ymid-ywid*cnum/2
            self._cmd('set string 1 l 5 0')
            vert=1
            
        else:
            
            #
            #	horizontal bar
            #
            
            ywid=0.2*sf
            xwid=0.6*sf

            if(ymid == None): ymid=ylo/2-ywid/2
            yt=ymid+yoffset
            yb=ymid
            if(xmid == None): xmid=xsiz/2
            if(xwid*cnum > xsiz*barsf):
                xwid=xsiz*barsf/cnum
            xl=xmid-xwid*cnum/2
            self._cmd('set string 1 tc 5 0')
            vert=0

        #
        #  Plot colorbar
        #


        self._cmd("set strsiz %f %f"%(strxsiz,strysiz))

        num=0
        while (num<cnum):

            (col,minval,maxval)=ge.colbar[num]
            hi="%g"%(maxval)

            if(vert): 
                yt=yb+ywid
            else :
                xr=xl+xwid
                yt=yb+ywid

            if(num != 0 and  num != cnum-1):
                self._cmd('set line %d'%(col))
                self._cmd('draw recf %f %f %f %f'%(xl,yb,xr,yt))

                self._cmd('set line 1 1 5')
                self._cmd('draw rec %f %f %f %f'%(xl,yb,xr,yt))
                
            if(num < cnum-1):
                if(vert): 
                    xp=xr+stroff
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))


            if(num == 0):

                if(vert):
                    xm=(xl+xr)*0.5

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,yt,xm,yb,xr,yt,xl,yt))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,yt,xm,yb))
                    self._cmd('draw line %f %f %f %f'%(xm,yb,xr,yt))
                    self._cmd('draw line %f %f %f %f'%(xr,yt,xl,yt))

                else:

                    ym=(yb+yt)*0.5
                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,ym,xr,yb,xr,yt,xl,ym))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,ym,xr,yb))
                    self._cmd('draw line %f %f %f %f'%(xr,yb,xr,yt))
                    self._cmd('draw line %f %f %f %f'%(xr,yt,xl,ym))

            if(num < cnum-1):
                if(vert):
                    xp=xr+stroff 
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))

            if(num == cnum-1 ):

                if( vert):

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,yb,xm,yt,xr,yb,xl,yb))

                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,yb,xm,yt))
                    self._cmd('draw line %f %f %f %f'%(xm,yt,xr,yb))
                    self._cmd('draw line %f %f %f %f'%(xr,yb,xl,yb))

                else:

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xr,ym,xl,yb,xl,yt,xr,ym))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xr,ym,xl,yb))
                    self._cmd('draw line %f %f %f %f'%(xl,yb,xl,yt))
                    self._cmd('draw line %f %f %f %f'%(xl,yt,xr,ym))

            
            if(num<cnum-1):
                if(vert): 
                    xp=xr+stroff
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))

            num=num+1
            if(vert):
                yb=yt
            else:
                xl=xr




class gXtitle(MFbase):


    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()


    def set(self,
            scale=1.0,
            t1col=1,
            t2col=1,
            t3col=1,
            t2scale=0.80,
            t3scale=0.70,
            t1thk=5,
            t2thk=5,
            t3thk=5,
            ):
        
        self.scale=scale
        self.t1col=t1col
        self.t2col=t2col
        self.t3col=t3col
        self.t2scale=t2scale
        self.t3scale=t3scale
        self.t1thk=t1thk
        self.t2thk=t2thk
        self.t3thk=t3thk
        
    def clip(self):

        self._ge.getGxinfo()
        self._cmd("set clip 0 %6.3f 0 %6.3f"%(self._ge.pagex,self._ge.pagey))
        

    def top(self,t1,t2=None,t3=None,doclip=1):

        if(doclip): self.clip()
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
            t3scale=1.05
        else:
            t2scale=self.t2scale
            t3scale=self.t3scale
            
        xr=self._ge.pagex
        xl=0
        y1=self._ge.pagey-0.15
        xs=(xr-xl)*0.5
        tsiz=0.15
        
        tsiz=tsiz*self.scale
        t2siz=tsiz*t2scale
        y2=self._ge.pagey-0.15-tsiz*1.5

        t3siz=tsiz*t3scale
        y3=y2-tsiz*1.5

        self._cmd('set strsiz %f'%(tsiz))
        self._cmd('set string %d c %d 0'%(self.t1col,self.t1thk))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set string %d c %d 0'%(self.t2col,self.t2thk))
            self._cmd('set strsiz %f'%(t2siz))
            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))

        if(t3 != None):
            self._cmd('set string %d c %d 0'%(self.t3col,self.t3thk))
            self._cmd('set strsiz %f'%(t3siz))
            self._cmd('draw string %f %f `0%s`0'%(xs,y3,t3))

        


    def bottom(self,t1,t2=None,sopt=None,doclip=1):

        if(doclip): self.clip()
        
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
        else:
            t2scale=0.80
            
        xr=self._ge.pagex
        xl=0
        y1=0.22
        y2=0.08
        
        if(sopt == 'left'):
            xs=0.2
        elif(sopt == 'right'):
            xs=0.2
            xs=xr-xs
        else:
            xs=xl+(xr-xl)*0.5

        tsiz=0.09
        
        tsiz=tsiz*self.scale
        t2siz=tsiz*t2scale

        self._cmd('set strsiz %f'%(tsiz))
        if(sopt == 'left'):
            self._cmd('set string %d l 6 0'%(self.t1col))
        elif(sopt == 'right'):
            self._cmd('set string %d r 6 0'%(self.t1col))
        else:
            self._cmd('set string %d c 6 0'%(self.t1col))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set strsiz %f'%(t2siz))
            if(sopt == 'left'):
                self._cmd('set string %d l 8 0'%(self.t2col))
            elif(sopt == 'right'):
                self._cmd('set string %d r 8 0'%(self.t2col))
            else:
                self._cmd('set string %d c 8 0'%(self.t2col))

            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))


    def plot(self,t1,t2=None,sopt=None,doclip=1):

        if(doclip): self.clip()
        
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
        else:
            scale=self.scale
            t2scale=0.80

        dxs=self._ge.plotxl
        dyt=self._ge.pagey-self._ge.plotyt

        tsiz=0.09
        xoff=0.75

        tsiz=tsiz*scale
        t2siz=tsiz*t2scale

        yoffscale=1.3
        yoff=tsiz*yoffscale

        xs=self._ge.plotxl-xoff-tsiz
        xm=(self._ge.plotxl+self._ge.plotxr)*0.5
        ys=(self._ge.plotyb+self._ge.plotyb)*0.5

        angle=90
        tt=tsiz+yoff

        if(tt < dyt):
            xs=xm
            ys=self._ge.plotyt+yoff+tsiz/2 
            angle=0

        y2=ys
        y1=ys
        if(t2 != None):
            y1=ys+yoff
            y2=y1-yoff*yoffscale
            
        #self._cmd('set line 0')
        self._cmd('set strsiz %f'%(tsiz))
        if(sopt == 'left'):
            self._cmd('set string %d l 6 0'%(self.t1col))
        elif(sopt == 'right'):
            self._cmd('set string %d r 6 0'%(self.t1col))
        else:
            self._cmd('set string %d c 6 0'%(self.t1col))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set strsiz %f'%(t2siz))
            if(sopt == 'left'):
                self._cmd('set string %d l 8 0'%(self.t2col))
            elif(sopt == 'right'):
                self._cmd('set string %d r 8 0'%(self.t2col))
            else:
                self._cmd('set string %d c 8 0'%(self.t2col))

            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))


class gxout(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        
    def shaded(self):
        self._cmd('set gxout shaded')

    def contour(self):
        self._cmd('set gxout contour')

class gxset(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        self._rl=ga.rline
        self._nL=ga.nLines
        

    def latlon(self,lat1=-90,lat2=90,lon1=0,lon2=360):
        self._cmd("set lat %f %f"%(lat1,lat2))
        self._cmd("set lon %f %f"%(lon1,lon2))
        
    def latlonA(self,area):
        self._cmd("set lat %f %f"%(area.lat1,area.lat2))
        self._cmd("set lon %f %f"%(area.lon1,area.lon2))        
        
    def lev(self,lev1=500,lev2=None):
        if(lev2 == None): lev2=lev1
        self._cmd("set lev %f %f"%(lev1,lev2))


    def time(self,time=None):

        if(time == None):
            self._cmd('q time')
            card=self._rl(self._nL)

        self._cmd("set time %s"%(time))


    def dtg(self,dtg=None):

        name="%s.%s"%(self.__module__,'gxset.dtg')
        if(dtg == None):
            print 'WWW dtg must be set in: ',name
        else:
            gtime=mf.dtg2gtime(dtg)
            if(gtime != None):
                self._cmd("set time %s"%(gtime))
            else:
                print 'EEE invalid dtg in: ',name

class gxGxout(MFbase):

    def __init__(self,g1s,g1v,g2s,g2v,stn):
        self.g1s=g1s
        self.g1v=g1v
        self.g2s=g2s
        self.g2v=g2v
        self.stn=stn
        
            


class gxget(MFbase):


    def __init__(self,ga,verb=0):
        self._cmd=ga.cmd
        self.ga=ga
        self.verb=verb
        

    def scorr(self,var1,var2,area):

        expr="scorr(%s,%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,var2,
                                                         area.lon1,area.lon2,
                                                         area.lat1,area.lat2)

        self.ga('d %s'%(expr))
        scorr=float(self.ga.rword(1,4))
        if(self.verb): print 'scorr: ',scorr

        return(scorr)

    def asum(self,var1,area):

        expr="asum(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)
        self.ga('d %s'%(expr))
        asum=float(self.ga.rword(1,4))
        if(self.verb): print 'asum:    ',asum 
        return(asum)

    def aave(self,var1,area):

        expr="aave(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)
        self.ga('d %s'%(expr))
        aave=float(self.ga.rword(1,4))
        if(self.verb): print 'aave:    ',aave
        return(aave)


    def asumg(self,var1,area):

        expr="asumg(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)

        self.ga('d %s'%(expr))
        asumg=float(self.ga.rword(1,4))
        if(self.verb): print 'asumg:   ',asumg

        return(asumg)


    def stat(self,expr):

        # get the current graphics and rank of display grid
        rank=len(self.ga.coords().shape)
        cgxout=self.gxout()

        # set gxout to stats; display expression
        self.ga.cmdQ('set gxout stat')
        self.ga.cmdQ('d %s'%(expr))
        cards=self.ga.Lines
        stats=gxStats(cards)

        # reset the original gxout
        if(rank == 1): self.ga.cmdQ('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self.ga.cmdQ('set gxout %s'%(cgxout.g2s))

        return(stats)


    def gxout(self):
        
        self.ga.cmdQ('q gxout')
        g1s=self.ga.rword(2,6)
        g1v=self.ga.rword(3,6)
        g2s=self.ga.rword(4,6)
        g2v=self.ga.rword(5,6)
        stn=self.ga.rword(6,4)
        gxout=gxGxout(g1s,g1v,g2s,g2v,stn)
        return(gxout)
        
        

class gxdefvar(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        self._rl=ga.rline
        self._nL=ga.nLines

    def var(self,var,expr):

        cmd="""%s=%s"""%(var,expr)
        self._cmd(cmd)
        return(cmd)
        
    def re2(self,var,expr,dx=2.5,dy=2.5,method='ba'):

        cmd="""%s=re2(%s,%f,%f,%s)"""%(var,expr,dx,dy,method)
        self._cmd(cmd)
        return(cmd)
        
    def regrid(self,var,expr,reargs):

        cmd="""%s=re(%s,%s)"""%(var,expr,reargs)
        self._cmd(cmd)
        return(cmd)


    def dregrid(self,var,expr,reargs):

        cmd="""d re(%s,%s)"""%(expr,reargs)
        self._cmd(cmd)
        return(cmd)

    def dregrid0(self,var,expr,reargs,undef=0):

        cmd="""d const(re(%s,%s),%s,-u)"""%(expr,reargs,str(undef))
        self._cmd(cmd)
        return(cmd)

    def dundef0(self,expr,undef=0):

        cmd="""d const(%s,%s,-u)"""%(expr,str(undef))
        self._cmd(cmd)
        return(cmd)

        
    def writef77(self,var):
        
        cmd="""set gxout fwrite
d %s"""%(var)
        self._cmd(cmd)

        # set gxout to standard
        self._cmd('set gxout contour')
        
        
    def sh_filt(self,var,expr,nwaves=20):

        cmd="""%s=sh_filt(%s,%d)"""%(var,expr,nwaves)
        self._cmd(cmd)
        
# -- CCCCCCCCCCCCCCCCCCCC -- models


class Model(MFbase):

    def DoGribmap(self,gmpverb=0):

        if(self.gribtype == 'grb1'): xgribmap='gribmap'
        if(self.gribtype == 'grb2'): xgribmap='gribmap'
        xgopt='-i'
        if(gmpverb):
            xgopt='-v -i'

        cmd="%s %s %s"%(xgribmap,xgopt,self.ctlpath)
        mf.runcmd(cmd)



class Model2(Model):

    #addir=w2.Nwp2DataMassStore
    models=Nwp2ModelsAll
    allmodels=Nwp2ModelsAll
    models=Nwp2ModelsActive
    modelsW2=Nwp2ModelsActiveW2flds

    geodir=sbtGeogDatDir
    bdir2=Nwp2DataBdir
    d2dir='/dat2/nwp2'
    archdir='/dat5/dat/nwp2'
    archdirDat6='/dat6/dat/nwp2'

    d2dir='/data/global/dat/nwp2'
    archdir='/data/global/dat/nwp2'
    archdirDat6='/data/global/dat/nwp2'

    modelrestitle=None
    modelDdtg=None
    modelgridres=None
    modelprvar=None
    modelpslvar=None
    modeltitleAck1=None
    modeltitleFullmod=None

    dofimlsgrib=1

    btau=0
    etau=168
    dtau=6

    warn=0

    myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) ESRL/GSD/AMB, Boulder, CO"
    modeltitleAck2=myname
    
    def __init__(self,model='ecm2',center='ecmwf',useAll=0,gribver=1,chkm2=1,bdir2=None):

        if(chkm2 and not(self.IsModel2(model))):
            print 'M2 -- invalid m2 model: ',model
            sys.exit()

        #
        # defaults
        #

        self.model=model
        self.dmodel=model
        self.dirmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'
        self.nfields=999
        self.nfieldsW2flds=999
        self.dmodelType=None        

        self.gmask=None
        self.grbpaths=[]

        self.xwgrib='wgrib'
        self.location='kishou'

        self.rundtginc=6

        name2tau=None  # force these three methods to be set
        setxwgrib=None
        setgmask=None
        

    def initModelCenter(self,center):
        self.center=center
        self.modelcenter="%s/%s"%(self.center,self.dirmodel)
        self.bddir="%s/%s"%(self.bdir2,self.modelcenter)
        self.bddirarch="%s/%s"%(self.archdir,self.modelcenter)
        self.bddirarchDat6="%s/%s"%(self.archdirDat6,self.modelcenter)
        self.w2fldsSrcDir="%s/w2flds/dat/%s"%(self.bdir2,self.model)
        self.w2fldsArchDir="/dat4/nwp2/w2flds/dat/%s"%(self.model)
        # -- temp location to free up the internal /dat4 drive
        self.w2fldsArchDir="/FWV1/dat2/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDir="/Volumes/FWV2/dat2/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDir="/dat5/dat/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDirDat6="/dat6/dat/nwp2/w2flds/dat/%s"%(self.model)

        self.rtfimSrcDir="%s/rtfim/dat"%(self.bdir2)
        self.rtfimArchDir="/Volumes/FWV2/dat2/nwp2/rtfim/dat"
        self.rtfimArchDir="/dat4/nwp2/rtfim/dat"
        self.rtfimArchDir2="/Volumes/FWV2/dat2/nwp2/rtfim/dat"

    def getRtfimModelsByDtg(self,dtg,sdir=None):

        rtmodels=[]
        if(sdir == None):   sdir=self.rtfimSrcDir

        smask="%s/*/%s"%(sdir,dtg)
        mm=glob.glob(smask)
        for m in mm:
            tt=m.split('/')
            ltt=len(tt)
            model=tt[ltt-2]
            rtmodels.append(model)
        return(rtmodels)


    def initGribVer(self,gribver):
        self.gribver=gribver
        self.gribtype='grb%d'%(self.gribver)

    def IsModel2(self,value):
        rc=0
        if(value in self.allmodels): rc=1
        return(rc)

    def IsModel1(self,value):
        rc=0
        if(value in self.models): rc=1
        return(rc)

    def getEtau(self,dtg=None):
        if(dtg == None):
            return(self.etau)
        else:
            return(self.etau)

    def getDtau(self,dtg=None):
        if(dtg == None):
            return(self.dtau)
        else:
            return(self.dtau)



    def Put2Arch(self,sbdir=None,tbdir=None,tdir=None,dtg=None,dtgs=None,rmsrc=0,ropt=''):

        rc=0
        if(tbdir == None): tbdir="%s"%(self.archdir)
        if(sbdir == None): sbdir=self.bddir
        if(dtg == None and dtgs == None): dtgs=self.ddtgs
        if(dtg != None and dtgs == None): dtgs=[dtg]

        for dtg in dtgs:
            sdir="%s/%s"%(sbdir,dtg)
            if(tdir == None):
                tdir="%s/%s"%(tbdir,self.modelcenter)

            mf.ChkDir(tdir,'mk')
            cmd="rsync -av %s %s"%(sdir,tdir)
            mf.runcmd(cmd,ropt)

            if(rmsrc):
                cmd="rm -r %s"%(sdir)
                mf.runcmd(cmd,ropt)

        print 'SSS(sbdir): ',sbdir
        print ' TTT(tdir): ',tbdir
        return(rc)


    def setDbase(self,dtg,dtype=None,warn=0):
        

        if(self.IsModel2(self.model) or self.IsModel1(self.model)):
            if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

            if(dtype == 'w2flds'):
                self.dmodel=self.model
                self.lmodel=self.model

            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)
            self.dbasedirarchDat6="%s/%s"%(self.bddirarchDat6,dtg)

            self.dmodelType=dtype

            self.bddirNWP2=self.bddir
            
            if(dtype != None):
                self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtg,dtype)
                if(dtype == 'w2flds'):
                    self.bddir=self.w2fldsSrcDir
                    self.dbasedir="%s/%s"%(self.bddir,dtg)
                    self.dbase="%s/%s/%s.%s.%s"%(self.bddir,dtg,self.lmodel,dtype,dtg)

            else:
                self.dbase="%s/%s.%s"%(self.dbasedir,self.lmodel,dtg)
                self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)

            self.dpath="%s.ctl"%(self.dbase)

            self.dpathexists=os.path.exists(self.dpath)


        elif(mf.find(self.model,'geo')):
            self.dbasedir=self.geodir
            if(self.model == 'geo05'):
                self.dpath="%s/lf.gfs.05deg.ctl"%(self.geodir)
            else:
                self.dpath=None

        elif(mf.find(self.model,'tctrk')):
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            mask="%s/*.ctl"%(dbasedir)
            self.dpaths=glob.glob(mask)
            if(len(self.dpaths) > 0):
                self.dpaths=dpaths
            else:
                self.dpaths=[]
                self.ddtgs=[]

        else:
            print 'EEE could not set M2.setDbase.dbase  model: ',self.model,'dtg: ',dtg,' dtype: ',self.dtype,' or maybe because model not in w2localvars.py Nwp2ModelsAll...'
            sys.exit()

        self.tdatbase=self.dbase


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar=modelprvar.replace('pr','pr(t+1)')
        return(modelprvar)



    def DataPath(self,dtgopt,dtype=None,getFromMss=0,dowgribinv=1,dofilecheck=1,override=0,ropt='',
                 diag=0,
                 useglob=0,
                 doDATage=0,
                 verb=1):


        if(hasattr(self,'doDATage')): doDATage=self.doDATage
        dpaths=[]
        statuss={}

        self.dtype=dtype

        dtgs=mf.dtg_dtgopt_prc(dtgopt)

        inV=None
        if(hasattr(self,'iV')): inV=self.iV.hash
        
        dataDtgs=[]

        for dtg in dtgs:
            
            # -- find tau offset
            #
            dataDtg=dtg
            if(MF.is0618Z(dtg) and self.modelDdtg == 12):
                self.tauOffset=6
                dataDtg=mf.dtginc(dtg,-6)
                
            dataDtgs.append(dataDtg)
            
            status={}

            self.setDbase(dataDtg,dtype=dtype)
            
            try:
                dthere=os.path.exists(self.dpath)
            except:
                dthere=0

            if(dthere):
                siz=MF.GetPathSiz(self.dpath)
                dpaths.append(self.dpath)

            elif(getFromMss):
                if(not(hasattr(self,'archmodelcenter'))): self.archmodelcenter=self.modelcenter
                mssdpath="%s/%s/%s.%s.tar"%(self.addir,self.archmodelcenter,self.dmodel,dataDtg)
                rc=os.popen('mssLs %s'%(mssdpath)).readlines()
                print 'getFromMss rc: ',rc

                if(len(rc) == 1):
                    tarball=rc[0]
                    mf.ChangeDir(self.bddir)
                    mf.runcmd(cmd,ropt)

                dthere=os.path.exists(self.dpath)
                if(dthere):
                    dpaths.append(self.dpath)

            # check file status...doesn't work!!!
            #
            #if(dofilecheck == 0):
            #    self.statuss=statuss
            #    return(self)

            if(dtype != None and not(hasattr(self,'dmodelType'))): self.dmodelType=dtype

            self.setxwgrib(dataDtg)
            if(hasattr(self,'setgmask')): self.setgmask(dtg)

            # -- special case for navgem from ncep
            #
            if(hasattr(self,'dsetMaskOverride') and self.dsetMaskOverride):
                
                def name2tau(ffile,dtg):
                    
                    try:
                        tau=ffile.split('.')[-2][-3:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                
                self.name2tau=name2tau
                
            
            elif(hasattr(self,'dmodelType') and self.dmodelType == 'w2flds' and self.tautype != 'alltau'):
                
                self.dmask=self.dmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                if(hasattr(self,'dsetmask')):
                    self.dsetmask=self.dsetmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                def name2tau(file,dtg):
                    try:
                        tau=file.split('.')[3][1:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                self.name2tau=name2tau


                
            self.datmask="%s/%s"%(self.dbasedir,self.dmask)

            self.datpaths=glob.glob(self.datmask)
            self.datpaths.sort()
            
            self.grbmask="%s/%s"%(self.dbasedir,self.gmask)
            self.grbpaths=glob.glob(self.grbmask)
            self.grbpaths.sort()
            
            if( len(self.datpaths) == 0 and len(self.grbpaths) > 0):
                print 'WWW(Model2.DataPath): len(self.datpaths): ',len(self.datpaths),' but grbpaths there'

                for grbpath in self.grbpaths:
                    grbsiz=MF.GetPathSiz(grbpath)
                    if(grbsiz == 0):
                        print 'WWW(Model2.DataPath): zero length source grb: ',grbpath,' delete'
                        os.unlink(grbpath)
                    else:
                        if(hasattr(self,'gname2tau')):
                            ctau="%03d"%(self.gname2tau(grbpath,dataDtg))
                            if(hasattr(self,'doLn') and self.doLn):
                                lmfile="%s.f%s.%s"%(self.tdatbase,ctau,self.gribtype)
                                cmd="ln -s -f %s %s"%(grbpath,lmfile)
                                mf.runcmd(cmd,ropt)

                self.datpaths=glob.glob(self.datmask)


            if ( len(self.datpaths) > 0):

                for datpath in self.datpaths:

                    (fdir,ffile)=os.path.split(datpath)
                    (base,ext)=os.path.splitext(datpath)
                    tau=self.name2tau(ffile,dtg)

                    gotit=0
                    if(inV != None and not(override)):
                        try:
                            (datpath,age,nf)=inV[self.model,dtg,tau]
                            status[tau]=(age,nf)
                            gotit=1
                        except:
                            None

                    if(gotit): continue


                    # -- bypass zero length files
                    #
                    if(MF.GetPathSiz(datpath) == 0):
                        if(self.warn): print 'WWW MF.GetPathSiz(datpath) == 0',MF.GetPathSiz(datpath)
                        continue


                    # old forms of the wgribpaths...
                    #
                    if(self.tautype == 'alltau' and dtype != 'w2flds'):
                        owgribpath="%s/%s.wgrib.txt"%(dir,base)
                    else:
                        owgribpath="%s/%s.%s.%03d.wgrib.txt"%(dir,self.model,dataDtg,tau)


                    #if(self.tautype == 'alltau'):
                    #    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)
                    #else:
                    (base,ext)=os.path.splitext(datpath)
                    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)

                    #if(os.path.exists(owgribpath)):
                    #    cmd="mv %s %s"%(owgribpath,wgribpath)
                    #    mf.runcmd(cmd,'')

                    if(dowgribinv):
                        try:
                            datsize=os.path.getsize(datpath)
                        except:
                            datsize=-999

                        if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0 and datsize > 0) or override):
                            cmd="%s %s > %s"%(self.xwgrib,datpath,wgribpath)
                            if(diag):  mf.runcmd(cmd)
                            else:      mf.runcmd(cmd,'quiet')    
                            
                    if(os.path.exists(wgribpath)):
                        if(doDATage):
                            age=MF.PathCreateTimeDtgdiff(dataDtg,datpath)
                        else:
                            age=MF.PathCreateTimeDtgdiff(dataDtg,wgribpath)
                            
                        if(age >= 1000.0): age=999.9
                        cards=open(wgribpath).readlines()
                        nf=len(cards)
                        status[tau]=(age,nf)

                        if(inV != None):
                            rc=(datpath,age,nf)
                            if(verb): print 'PPP putting rc: ',self.model,dataDtg,tau,nf
                            inV[self.model,dtg,tau]=rc


            else:
                status={}

            statuss[dtg]=status

        #
        # outside  dtg loop -- single dtg
        #

        self.ctlpath="%s.ctl"%(self.tdatbase)

        self.dpaths=dpaths
        self.ddtgs=dataDtgs
        self.statuss=statuss

        if(self.dmodelType != None and self.dmodelType == 'w2flds'):
            self.nfields=self.nfieldsW2flds
        else:
            self.nfields=self.nfields
            
        if(hasattr(self,'iV')): self.iV.put()


        return(self)


    def GetDataStatus(self,dtg,checkNF=0,mintauNF=5):

        if(hasattr(self,'bddirNWP2')):
            tdir="%s/%s"%(self.bddirNWP2,dtg)
        else:
            tdir="%s/%s"%(self.bddir,dtg)

        NFmin=self.nfields
        if(checkNF): NFmin=self.nfields-mintauNF

        lastTau=None
        latestTau=None
        latestCompleteTau=None
        earlyTau=None
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        mask="%s/gribmap.status.*.txt"%(tdir)
        gmps=glob.glob(mask)
        gmps.sort()

        gmpAge=0.0
        if(len(gmps) >= 1):
            for gmpspath in gmps:
                age=MF.PathCreateTimeDtgdiff(dtg,gmpspath)
                if(age > gmpAge):
                    gmpAge=age
                    latestgmpPath=gmpspath

            (dir,file)=os.path.split(latestgmpPath)
            tt=file.split('.')

            if(len(tt) >= 6):
                gmplastdogribmap=int(tt[3])
                gmplatestTau=int(tt[4])
                gmplastTau=int(tt[5])


        if(len(self.statuss) == 0):
            return(self)

        status=self.statuss[dtg]
        itaus=status.keys()
        itaus.sort()
        
        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            # -- >= because for taus having the same age
            #
            if(ages[itau] >= oldest):
                oldest=ages[itau]
                latestTau=itau

        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau

        if(hasattr(self,'dattaus')):
            datataus=self.dattaus
        else:
            datataus=Model2DataTaus(self.model,dtg)

        # -- forward search thru target data taus
        # 

        ndt=len(datataus)

        if(self.tautype == 'alltau'):
            latestCompleteTau=datataus[-1]
            
        else:
            for n in range(0,ndt):
                datatau=datataus[n]
                gotit=0
                for itau in itaus:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTau=datatau
                        break
    
    
                if(gotit == 0):  break


        # -- backward search (default)
        #

        latestCompleteTauBackward=-999

        if(self.tautype == 'alltau' and self.dmodelType == None):
            None
        else:
            for n in range(ndt-1,0,-1):
                datatau=datataus[n]
                gotit=0
                for itau in itaus[-1:0:-1]:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTauBackward=datatau
                        break
        
                if(gotit == 1):  break
        
        self.dstdir=tdir
        self.dsitaus=itaus
        self.dslastTau=lastTau
        self.dsgmpAge=gmpAge
        self.dsoldestTauAge=oldest
        self.dslatestTau=latestTau
        self.dsyoungest=youngest
        self.dsearlyTau=earlyTau
        self.dsgmplastdogribmap=gmplastdogribmap
        self.dsgmplatestTau=gmplatestTau
        self.dsgmplastTau=gmplastTau
        self.dslatestCompleteTau=latestCompleteTau
        self.dslatestCompleteTauBackward=latestCompleteTauBackward

        return(self)


    def makeCtl(self,dtg):

        if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel
        if(not(hasattr(self,'dsetmask'))): self.dsetmask=self.dmask

        gmppath="%s.gmp"%(self.tdatbase)
        gmpfile="%s.%s.gmp"%(self.lmodel,dtg)

        gtime=mf.dtg2gtime(dtg)
        nt=(self.etau/self.dtau)+1

        self.ctl='''dset ^%s
index ^%s.%s.gmp
tdef % 3d linear %s %shr
%s
'''%(self.dsetmask,self.lmodel,dtg,nt,gtime,self.dtau,self.ctlgridvar)


    def doGrib(self,dtg,verb=0):

        # -- first set up the gribtype, etc
        self.setxwgrib(dtg)
        self.setctlgridvar(dtg)
        self.makeCtl(dtg)

        self.WriteCtl()  # from Model in M
        self.DoGribmap(gmpverb=verb) # from Model in M


    #def setInventory(self,dtype='w2flds',override=0,unlink=0):

        #dbname='nwp2Inv-%s'%(dtype)
        ##tbdir=w2.Nwp2DataBdir
        ##self.iV=InvHash(dbname,tbdir,override=override)

        #tbdir=w2.Nwp2DataDSsBdir
        #self.iV=InvHash(dbname,tbdir,override=override,unlink=unlink)


    def Model2PlotMinTau(self,dtg):
        mintauPlot=144
        return(mintauPlot)


class Era5(Model2):

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=12
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    modelZgVar='zg/%f'%(gravity)
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of ERA project"
    modeltitleFullmod="ECMWF(ERA5)"

    model='era5'
    center='ecmwf'

    dmodel='era5'
    pmodel='er5'

    pltdir='plt_ecmwf_%s'%(pmodel)

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)
    regridTracker=0.5


    def __init__(self,bdir2=None,gribver=2):

        self.dirmodel=self.dmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='wxmap2'

        self.tautype='alltau'
        self.gribtype='grb2'

        self.nfields=94
        self.nfieldsW2flds=66

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='era5'
        self.tryarch=0
        
    def name2tau(self,ffile,dtg):
        tau=240
        return(tau)

    def setDbase(self,dtg,dtype='w2flds',warn=0):

        if(self.IsModel2(self.model) or self.IsModel1(self.model)):
            if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

            if(dtype == 'w2flds'):
                self.dmodel=self.model
                self.lmodel=self.model
                
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)

            byear=dtg[0:4]
            self.bddir="%s/%s"%(self.w2fldsSrcDir,byear)
            self.useBddir=1
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbase="%s/%s/%s-%s-%s-ua"%(self.bddir,dtg,self.lmodel,dtype,dtg)
            self.dmask="%s-%s-%s-ua.%s"%(self.lmodel,dtype,dtg,self.gribtype)

            self.dpath="%s.ctl"%(self.dbase)

            self.dpathexists=os.path.exists(self.dpath)

            # -- try dat5
            #
            if(not(self.dpathexists) and self.tryarch):
                if(warn): print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIII M2.Model2.setDbase tryarch=1 -- trying the archive on: ',self.dbasedirarch,self.dtype
                self.dbasedir=self.dbasedirarch
                if(self.dtype == 'w2flds'):
                    self.bddir=self.w2fldsArchDir
                    self.dbasedir="%s/%s"%(self.bddir,dtg)
                    self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtype,dtg)
                    self.dmask="%s.%s.%s.f???.%s"%(self.lmodel,dtype,dtg,self.gribtype)
                    
                    self.dpath="%s.ctl"%(self.dbase)
                    self.dpathexists=os.path.exists(self.dpath)
            
        else:
            print 'EEE-M2.Era5.setDbase could not set M2.setDbase.dbase  model: ',self.model,'dtg: ',dtg,' dtype: ',self.dtype,' or maybe because model not in w2localvars.py Nwp2ModelsAll...'
            sys.exit()

        self.tdatbase=self.dbase

    def GetDataStatus(self,dtg,checkNF=0,mintauNF=5):

        if(hasattr(self,'bddirNWP2')):
            tdir="%s/%s"%(self.bddirNWP2,dtg)
        else:
            tdir="%s/%s"%(self.bddir,dtg)

        NFmin=self.nfields
        if(checkNF): NFmin=self.nfields-mintauNF

        lastTau=None
        latestTau=None
        latestCompleteTau=None
        earlyTau=None
        gmpAge=None
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        datataus=Model2DataTaus(self.model,dtg)
        
        # -- for single tau in era5/ecm5 ... get the age from the single data file
        #
        stat=self.statuss[dtg]
        itaus=stat.keys()
        
        if(len(itaus) == 1):
            itau=itaus[0]
            (age,siz)=stat[itau]
        else:
            age=-999
            siz=-999
        
        for tau in datataus:
            nf=self.nfieldsW2flds
            self.statuss[dtg][tau]=(age,nf)
        
        status=self.statuss[dtg]
        itaus=status.keys()
        itaus.sort()
        
        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            # -- >= because for taus having the same age
            #
            if(ages[itau] >= oldest):
                oldest=ages[itau]
                latestTau=itau

        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau


        # -- forward search thru target data taus
        # 

        ndt=len(datataus)

        if(self.tautype == 'alltau'):
            latestCompleteTau=datataus[-1]
            
        else:
            for n in range(0,ndt):
                datatau=datataus[n]
                gotit=0
                for itau in itaus:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTau=datatau
                        break
    
    
                if(gotit == 0):  break


        # -- backward search (default)
        #

        latestCompleteTauBackward=-999

        if(self.tautype == 'alltau' and self.dmodelType == None):
            None
        else:
            for n in range(ndt-1,0,-1):
                datatau=datataus[n]
                gotit=0
                for itau in itaus[-1:0:-1]:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTauBackward=datatau
                        break
        
                if(gotit == 1):  break
        
        self.dstdir=tdir
        self.dsitaus=itaus
        self.dslastTau=lastTau
        self.dsgmpAge=gmpAge
        self.dsoldestTauAge=oldest
        self.dslatestTau=latestTau
        self.dsyoungest=youngest
        self.dsearlyTau=earlyTau
        self.dsgmplastdogribmap=gmplastdogribmap
        self.dsgmplatestTau=gmplatestTau
        self.dsgmplastTau=gmplastTau
        self.dslatestCompleteTau=latestCompleteTau
        self.dslatestCompleteTauBackward=latestCompleteTauBackward

        return(self)

    def getDataTaus(self,dtg):
        taus=range(0,120+1,6)+range(132,240+1,12)
        return(taus)


    # -- set prvar method to set dependence on tau
    #
    def setprvar2(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau >= 6 and tau <= 120):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
        elif(tau > 120):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-2),0,-u) )*2)'"""
            
        return(modelprvar)
    
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        
        #if(tau >= 0 and tau <= 120):
        if(tau == 0):
            prl='''(const(prl.2(t+1),0,-u)-const(prl.2(t-0),0,-u))'''
            prc='''(const(prc.2(t+1),0,-u)-const(prc.2(t-0),0,-u))'''
            modelprvar="""_prvar='(( %s + %s )*4*1000)'"""%(prl,prc)

        elif(tau == 6):
            prl='''(const(prl.2(t+0),0,-u))'''
            prc='''(const(prc.2(t+0),0,-u))'''
            prl='''(const(prl.2(t+0),0,-u)-const(prl.2(t-1),0,-u))'''
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-1),0,-u))'''
            modelprvar="""_prvar='(( %s + %s )*4*1000)'"""%(prl,prc)

        elif(tau >= 12 and tau <= 120):
            prl='''(const(prl.2(t+0),0,-u)-const(prl.2(t-1),0,-u))'''
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-1),0,-u))'''
            modelprvar="""_prvar='(( %s + %s )*4*1000)'"""%(prl,prc)

        elif(tau > 120):
            prl='''(const(prl.2(t+0),0,-u)-const(prl.2(t-2),0,-u))'''
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-2),0,-u))'''
            modelprvar="""_prvar='(( %s + %s )*2*1000)'"""%(prl,prc)
            
        return(modelprvar)

    def setprvarc(self,dtg=None,tau=None):
        
        #if(tau >= 0 and tau <= 120):
        if(tau == 0):
            prc='''(const(prc.2(t+1),0,-u)-const(prc.2(t-0),0,-u))'''
            modelprvar="""_prvar='(( %s )*4*1000)'"""%(prc)

        elif(tau == 6):
            prc='''(const(prc.2(t+0),0,-u))'''
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-1),0,-u))'''
            modelprvar="""_prvar='(( %s )*4*1000)'"""%(prc)

        elif(tau >= 12 and tau <= 120):
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-1),0,-u))'''
            modelprvar="""_prvar='(( %s )*4*1000)'"""%(prc)

        elif(tau > 120):
            prc='''(const(prc.2(t+0),0,-u)-const(prc.2(t-2),0,-u))'''
            modelprvar="""_prvar='(( %s )*2*1000)'"""%(prc)
            
        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)

    def setgmask(self,dtg):
        self.gmask="%s-w2flds-%s-ua*"%(self.dmodel,dtg)


    def setxwgrib(self,dtg):

        self.xwgrib='wgrib2'
        self.dmask="%s-w2flds-%s-ua.%s"%(self.dmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg):

        latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

        if(self.gribtype == 'grb1'):
            optiondtype='''options yrev template
dtype grib
zdef 14 levels 1000 925 850 700 500 400 300 250 200 150 100 50 20 10'''

        elif(self.gribtype == 'grb2'):
            optiondtype='''options yrev template pascals
dtype grib2'''


        self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars'''%(optiondtype,latlongrid)


        allvarsnew='''vars 30
10FGsfc  0 49,1,0  ** Wind gust at 10 metres [m s**-1]
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
BLHsfc  0 159,1,0  ** Boundary layer height [m]
CAPEsfc  0 59,1,0  ** Convective available potential energy [J kg**-1]
CIsfc  0 31,1,0  ** Sea-ice cover [(0-1)]
CPsfc  0 143,1,0  ** Convective precipitation [m]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
LSPsfc  0 142,1,0  ** Stratiform precipitation [m]
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
SFsfc  0 144,1,0  ** Snowfall (convective + stratiform) [m of water equivalent]
SPhbl  0 134,109,1  ** Surface pressure [Pa]
SSTKsfc  0 34,1,0  ** Sea surface temperature [K]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TCWsfc  0 136,1,0  ** Total column water [kg m**-2]
TPsfc  0 228,1,0  ** Total precipitation [m]
TTRsfc  0 179,1,0  ** Top thermal radiation [W m**-2 s]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]
Wprs  0 135,100,700  ** Vertical velocity [Pa s**-1]
var121sfc  0 121,1,0  ** undefined
var122sfc  0 122,1,0  ** undefined
var123sfc  0 123,1,0  ** undefined'''

        allvarsold='''vars 15
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TPsfc  0 228,1,0  ** Total precipitation [m]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]'''
