from Components.Button import Button
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.PluginList import resolveFilename
from Components.Task import Task, Job, job_manager, Condition
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.TaskView import JobView
from Tools.Downloader import downloadWithProgress
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, SCOPE_PLUGINS
import urllib2
import os
import shutil
import math
from boxbranding import getBoxType, getMachineBuild, getImageVersion, getBrandOEM

class NFR4XChooseOnLineImage(Screen):
    skin = '<screen name="NFR4XChooseOnLineImage" position="center,center" size="880,620" title="NFR4XBoot - Download OnLine Images" >\n\t\t\t  <widget source="list" render="Listbox" position="10,0" size="870,610" scrollbarMode="showOnDemand" transparent="1">\n\t\t\t\t  <convert type="TemplatedMultiContent">\n\t\t\t\t  {"template": [\n\t\t\t\t  MultiContentEntryText(pos = (0, 10), size = (830, 30), font=0, flags = RT_HALIGN_RIGHT, text = 0),\n\t\t\t\t  MultiContentEntryPixmapAlphaBlend(pos = (10, 0), size = (480, 60), png = 1),\n\t\t\t\t  MultiContentEntryText(pos = (0, 40), size = (830, 30), font=1, flags = RT_VALIGN_TOP | RT_HALIGN_RIGHT, text = 3),\n\t\t\t\t  ],\n\t\t\t\t  "fonts": [gFont("Regular", 28),gFont("Regular", 20)],\n\t\t\t\t  "itemHeight": 65\n\t\t\t\t  }\n\t\t\t\t  </convert>\n\t\t\t  </widget>\n\t\t  </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        returnValue = self.sel[2]
        if returnValue is not None:
            self.session.openWithCallback(self.quit, DownloadOnLineImage, returnValue)
        return

    def updateList(self):
        self.list = []
        mypath = resolveFilename(SCOPE_PLUGINS)
        mypath = mypath + 'Extensions/NFR4XBoot/images/'
        mypixmap = mypath + 'opennfr.png'
        png = LoadPixmap(mypixmap)
        name = _('NFR')
        desc = _('Download latest NFR Image')
        idx = 'opennfr'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'openvix.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenVIX')
        desc = _('Download latest OpenVIX Image')
        idx = 'openvix'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'opendroid.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenDroid')
        desc = _('Download latest OpenDroid Image')
        idx = 'opendroid'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'egami.png'
        png = LoadPixmap(mypixmap)
        name = _('Egami')
        desc = _('Download latest Egami Image')
        idx = 'egami'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'openatv.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenATV-5.2')
        desc = _('Download latest OpenATV Image')
        idx = 'openatv-5.2'
        res = (name,
         png,
         idx,
         desc) 
        self.list.append(res)
        mypixmap = mypath + 'openatv.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenATV-5.3')
        desc = _('Download latest OpenATV Image')
        idx = 'openatv-5.3'
        res = (name,
         png,
         idx,
         desc) 
        self.list.append(res)
        mypixmap = mypath + 'openpli.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenPLi')
        desc = _('Download latest OpenPLi Image')
        idx = 'openpli'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'openhdf.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenHDF')
        desc = _('Download latest OpenHDF Image')
        idx = 'openhdf'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'openmips.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenMIPS')
        desc = _('Download latest OpenMIPS Image')
        idx = 'openmips'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        mypixmap = mypath + 'openeight.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenEight')
        desc = _('Download latest OpenEight Image')
        idx = 'openeight'
        res = (name,
         png,
         idx,
         desc)
        self.list.append(res)
        self['list'].list = self.list

    def quit(self):
        self.close()


class DownloadOnLineImage(Screen):
    skin = '\n\t<screen position="center,center" size="560,500" title="NFR4XBoot - Download Image">\n\t\t<ePixmap position="0,460"   zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />\n\t\t<ePixmap position="140,460" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />\n\t\t<widget name="key_red" position="0,460" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t<widget name="key_green" position="140,460" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t<widget name="imageList" position="10,10" zPosition="1" size="550,450" font="Regular;20" scrollbarMode="showOnDemand" transparent="1" />\n\t</screen>'

    def __init__(self, session, distro):
        Screen.__init__(self, session)
        self.session = session
        ImageVersion = getImageVersion()
        Screen.setTitle(self, _('NFR4XBoot - Download Image'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Exit'))
        self.filename = None
        self.imagelist = []
        self.simulate = False
        self.imagePath = '/media/nfr4xboot/NFR4XBootUpload'
        self.distro = distro
        if self.distro == 'egami':
            self.feed = 'egami'
            self.feedurl = 'http://image.egami-image.com'
        elif self.distro == 'opennfr':
            self.feed = 'opennfr'
            self.feedurl = 'http://dev.nachtfalke.biz/nfr/feeds/%s/images' %ImageVersion
        elif self.distro == 'openatv-5.2':
            self.feed = 'openatv'
            self.feedurl = 'http://images1.mynonpublic.com/openatv/5.2'    
        elif self.distro == 'openatv-5.3':
            self.feed = 'openatv'
            self.feedurl = 'http://images.mynonpublic.com/openatv/5.3'
        elif self.distro == 'openvix':
            self.feed = 'openvix'
            self.feedurl = 'http://openvix.co.uk'
        elif self.distro == 'opendroid':
            self.feed = 'opendroid'
            self.feedurl = 'http://images.opendroid.org/5.3/'
        elif self.distro == 'openpli':
            self.feed = 'openpli'
            self.feedurl = 'http://openpli.org/download'
        elif self.distro == 'openhdf':
            self.feed = 'openhdf'
            self.feedurl1 = 'http://images.hdfreaks.cc'
            self.feedurl = 'http://images.hdfreaks.cc/menu.html'
        elif self.distro == 'openmips':
            self.feed = 'openmips'
            self.feedurl = 'http://image.openmips.com/5.3'
        elif self.distro == 'openeight':
            self.feed = 'openeight'
            self.feedurl = 'http://openeight.de'
        else:
            self.feed = 'opennfr'
            self.feedurl = 'http://dev.nachtfalke.biz/nfr/feeds/5.3/images'
        self['imageList'] = MenuList(self.imagelist)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'green': self.green,
         'red': self.quit,
         'cancel': self.quit}, -2)
        self.onLayoutFinish.append(self.layoutFinished)
        return

    def quit(self):
        self.close()

    def box(self):
        box = getBoxType()
        urlbox = getBoxType()
        if self.distro == 'openatv-5.2' or self.distro == 'openatv-5.3' or self.distro == 'opennfr' or self.distro == 'egami' or self.distro == 'openmips' or self.distro == 'openhdf':
            if box in ('xpeedlx1', 'xpeedlx2'):
                    box = 'xpeedlx'
            req = urllib2.Request(self.feedurl)
            stb = 'no Image for this Box on this Side'
            try:
                    response = urllib2.urlopen(req)
                    tmp = response.readlines()
                    for line in tmp:
                        if '<a href="' in line:
                            if box in line:
                                stb = '1'
                                break
            except:
                    stb = 'no Image for this Box on this Side'
        if self.distro == 'openvix':
            if box in ('xpeedlx1', 'xpeedlx2', 'xpeedlx3', 'vusolo2', 'vusolose', 'vuduo2', 'vusolo4k', 'mutant2400', 'gbquadplus', 'gb800ueplus', 'gb800seplus', 'osmini', 'spycat', 'uniboxeco'):
                if box in ('xpeedlx1', 'xpeedlx2'):
                    box = 'xpeedlx'
                    urlbox = 'GI-Xpeed-LX'
                    stb = '1'
                elif box in ('xpeedlx3'):
                    box = 'xpeedlx3'
                    urlbox = 'GI-Xpeed-LX3'
                    stb = '1'
                elif box in ('vusolo2'):
                    box = 'vusolo2'
                    urlbox = 'Vu+Solo2'
                    stb = '1'
                elif box in ('vusolo4k'):
                    box = 'vusolo4k'
                    urlbox = 'Vu+Solo4K'
                    stb = '1'   
                elif box in ('vusolose'):
                    box = 'vusolose'
                    urlbox = 'Vu+Solo-SE'
                    stb = '1'
                elif box in ('vuduo2'):
                    box = 'vuduo2'
                    urlbox = 'Vu+Duo2'                    
                    stb = '1'
                elif box in ('mutant2400'):
                    box = 'mutant2400'
                    urlbox = 'Mutant-HD2400'                    
                    stb = '1'
                elif box in ('gbquadplus'):
                    box = 'gbquadplus'
                    urlbox = 'GiGaBlue-HD-QUAD-PLUS'                    
                    stb = '1'
                elif box in ('gb800ueplus'):
                    box = 'gb800ueplus'
                    urlbox = 'GiGaBlue-HD800UE-PLUS'                    
                    stb = '1'
                elif box in ('gb800seplus'):
                    box = 'gb800seplus'
                    urlbox = 'GiGaBlue-HD800SE-PLUS'                    
                    stb = '1'
                elif box in ('osmini'):
                    box = 'osmini'
                    urlbox = 'OS-mini'                    
                    stb = '1'
                elif box in ('spycat'):
                    box = 'spycat'
                    urlbox = 'Spycat'                    
                    stb = '1'
                elif box in ('uniboxhde'):
                    box = 'uniboxhde'
                    urlbox = 'Venton-Unibox-HDeco-PLUS'                    
                    stb = '1'     
            else:   
                stb = 'no Image for this Box on this Side' 
        elif self.distro == 'opendroid':
            if box in ('gbquadplus', 'gb800ueplus', 'gb800seplus'):
                box = 'GigaBlue'
                urlbox = getBoxType()               
                stb = '1'
            elif box in ('xpeedlx1', 'xpeedlx2'):
                box = 'GoldenInterstar'
                urlbox = 'xpeedlx'                
                stb = '1'
            elif box in ('xpeedlx3'):
                box = 'GoldenInterstar'
                urlbox = 'xpeedlx3'                
                stb = '1'
            elif box in ('optimussos1', 'optimussos2', 'optimussos1plus', 'optimussos2plus', 'optimussos3plus', 'osmini'):
                box = 'Edision'
                urlbox = getBoxType()                
                stb = '1'
            elif box in ('vusolose', 'vusolo2', 'vuduo2'):
                box = getBrandOEM()
                urlbox = getBoxType()
                stb = '1'
	    elif box in ('atemionemesis'):
                box = 'Atemio'
                urlbox = 'atemionemesis'                
                stb = '1'
	    elif box in ('atemio6200'):
                box = 'Atemio'
                urlbox = 'atemio6200'                
                stb = '1'    
	    elif box in ('atemio6000'):
                box = 'Atemio'
                urlbox = 'atemio6000'                
                stb = '1'
            elif box in ('atemio6100'):
                box = 'Atemio'
                urlbox = 'atemio6100'                
                stb = '1'
            elif box in ('formuler4', 'formuler3', 'formuler1'):
                box = 'Formuler'
                urlbox = getBoxType()                
                stb = '1'    
            elif box in ('uniboxhde'):
                box = 'Venton-Unibox'
                urlbox = 'uniboxhde'                
                stb = '1'
                                
            else:   
                stb = 'no Image for this Box on this Side'
        elif self.distro == 'openeight':
            if box in ('sf208', 'sf228', 'sf108', 'sf3038', 'sf98'):
               if box in ('sf228'):
               		box = 'sf228'
                	urlbox = getBoxType()               
                	stb = '1'
               elif box in ('sf208'):
               		box = 'sf208'
                	urlbox = getBoxType()               
                	stb = '1'
               elif box in ('sf98'):
               		box = 'sf98'
                	urlbox = getBoxType()               
                	stb = '1'
               elif box in ('sf3038'):
               		box = 'sf3038'
                	urlbox = getBoxType()               
                	stb = '1'
               elif box in ('sf108'):
                    box = 'sf108'
                    urlbox = getBoxType() 
                    stb = '1' 
               elif box in ('sf128'):
                    box = 'sf128'
                    urlbox = getBoxType() 
                    stb = '1'
               elif box in ('sf138'):
                    box = 'sf138'
                    urlbox = getBoxType() 
                    stb = '1'			
                
            else:   
                stb = 'no Image for this Box on this Side'    
        elif self.distro == 'openpli':
            if box in ('vusolo2', 'vusolo4k', 'vusolose', 'vuduo2', 'osmini', 'mutant2400', 'quadbox2400', 'formuler4', 'formuler1', 'formuler3'):
               if box in ('vusolo2'):
                    box = 'vusolo2'
                    urlbox = 'vuplus/vusolo2/' 
                    stb = '1'
               elif box in ('vusolo4k'):
                    box = 'vusolo4k'
                    urlbox = 'vuplus/vusolo4k/' 
                    stb = '1'                    
               elif box in ('vusolose'):
                    box = 'vusolose'
                    urlbox = 'vuplus/vusolose/' 
                    stb = '1'
               elif box in ('vuduo2'):
                    box = 'vuduo2'
                    urlbox = 'vuplus/vuduo2/' 
                    stb = '1'
               elif box in ('mutant2400'):
                    box = 'hd2400'
                    urlbox = 'mutant/hd2400/' 
                    stb = '1'
               elif box in ('quadbox2400'):
                    box = 'hd2400'
                    urlbox = 'mutant/hd2400/' 
                    stb = '1'
               elif box in ('formuler1'):
                    box = 'formuler1'
                    urlbox = 'formuler/formuler1/' 
                    stb = '1'
               elif box in ('formuler3'):
                    box = 'formuler3'
                    urlbox = 'formuler/formuler3/' 
                    stb = '1'
               elif box in ('formuler4'):
                    box = 'formuler4'
                    urlbox = 'formuler/formuler4/' 
                    stb = '1'     
               elif box in ('osmini'):
                    box = 'osmini'
                    urlbox = 'edision/osmini/' 
                    stb = '1' 
               elif box in ('spycatmini'):
                    box = 'spycatmini'
                    urlbox = 'spycat/spycatmini/' 
                    stb = '1'
               elif box in ('spycat'):
                    box = 'spycat'
                    urlbox = 'spycat/spycat/' 
                    stb = '1'                      
            else:   
                stb = 'no Image for this Box on this Side'        
        return (box, urlbox, stb)

    def green(self, ret = None):
        sel = self['imageList'].l.getCurrentSelection()
        if sel == None:
            print 'Nothing to select !!'
            return
        else:
            file_name = self.imagePath + '/' + sel
            self.filename = file_name
            self.sel = sel
            box = self.box()
            self.hide()
            if self.distro == 'openvix':
                print "url=", self.feedurl + '/openvix-builds/' + box[1]
                url = self.feedurl + '/openvix-builds/' + box[1] + '/' + sel 
            elif self.distro == 'openpli':
                url = 'http://downloads.pli-images.org/builds/' + box[0] + '/' + sel
            elif self.distro == 'openeight':
                url = self.feedurl + '/images/' + box[0] + '/' + sel
            elif self.distro == 'openhdf':
                url = 'http://images.hdfreaks.cc/' + box[0] + '/' + sel
            elif self.distro == 'opendroid':
                url = self.feedurl + '/' + box[0] + '/' + box[1] + '/' + sel            
            else:
                url = self.feedurl + '/' + box[0] + '/' + sel
            print '[NFR4XBoot] Image download url: ', url
            try:
                u = urllib2.urlopen(url)
            except:
                self.session.open(MessageBox, _('The URL to this image is not correct !!'), type=MessageBox.TYPE_ERROR)
                self.close()

            f = open(file_name, 'wb')
            f.close()
            meta = u.info()
            file_size = int(meta.getheaders('Content-Length')[0])
            print 'Downloading: %s Bytes: %s' % (sel, file_size)
            job = ImageDownloadJob(url, file_name, sel)
            job.afterEvent = 'close'
            job_manager.AddJob(job)
            job_manager.failed_jobs = []
            self.session.openWithCallback(self.ImageDownloadCB, JobView, job, backgroundable=False, afterEventChangeable=False)
            return

    def ImageDownloadCB(self, ret):
        if ret:
            return
        elif job_manager.active_job:
            job_manager.active_job = None
            self.close()
            return
        else:
            if len(job_manager.failed_jobs) == 0:
                self.session.openWithCallback(self.startInstall, MessageBox, _('Do you want to install this image now?'), default=False)
            else:
                self.session.open(MessageBox, _('Download Failed !!'), type=MessageBox.TYPE_ERROR)
            return

    def startInstall(self, ret = None):
        if ret:
            from Plugins.Extensions.NFR4XBoot.plugin import NFR4XBootImageInstall
            self.session.openWithCallback(self.quit, NFR4XBootImageInstall)
        else:
            self.close()

    def layoutFinished(self):
        box = self.box()[0]
        urlbox = self.box()[1]
        stb = self.box()[2]
        print '[NFR4XBoot] FEED URL: ', self.feedurl
        print '[NFR4XBoot] BOXTYPE: ', box
        print '[NFR4XBoot] URL-BOX: ', urlbox        
        self.imagelist = []
        if stb != '1':
            url = self.feedurl
        elif self.distro in ('egami', 'openmips', 'openatv-5.2', 'openatv-5.3','openeight'):
            url = '%s/index.php?open=%s' % (self.feedurl, box)
        elif self.distro == 'openvix':
            url = '%s/openvix-builds/%s' % (self.feedurl, urlbox)
        elif self.distro == 'opendroid':
            url = '%s/%s/index.php?dir=%s' % (self.feedurl, box, urlbox)       
        elif self.distro == 'openpli':
            url = '%s/%s' % (self.feedurl, urlbox)
        elif self.distro == 'opennfr':
            url = '%s/%s' % (self.feedurl, box)
        elif self.distro == 'openhdf':
            url = '%s/%s' % (self.feedurl1, box)
            
	else:
            url = self.feedurl
        print '[NFR4XBoot] URL: ', url
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError as e:
            print 'URL ERROR: %s' % e
            return

        try:
            the_page = response.read()
        except urllib2.HTTPError as e:
            print 'HTTP download ERROR: %s' % e.code
            return

        lines = the_page.split('\n')
        
        tt = len(box)
        if stb == '1':
            for line in lines:
                if self.feed == "openeight":
                    if line.find("/images/%s/" % box) > -1:
                    		t = line.find('/images/%s/' % box)
                    		self.imagelist.append(line[t+tt+9:t+tt+tt+40])
                    elif line.find("<a href='%s/" % box) > -1:
                    		t = line.find("<a href='%s/" % box)
                    		t2 = line.find("'>egami")
                    		if self.feed in 'openatv':
                    			self.imagelist.append(line[t + tt + 10:t + tt + tt + 39])
                    		elif self.feed in 'egami':
                    			self.imagelist.append(line[t + tt + 10:t2])
                    		elif self.feed in 'openmips':
                    			line = line[t + tt + 10:t + tt + tt + 40]
                    			self.imagelist.append(line)
                    	
                elif line.find("<a href='%s/" % urlbox) > -1:
                    ttt = len(urlbox)
                    t = line.find("<a href='%s/" % urlbox) 
                    t5 = line.find(".zip'")
                    self.imagelist.append(line[t + ttt + 10 :t5 + 4])                        
                elif line.find('href="openvix-') > -1:
                    t4 = line.find('openvix-')
                    t5 = line.find('.zip"')
                    self.imagelist.append(line[t4 :t5+4])
                elif line.find('file=openvixhd-') > -1:
                    t4 = line.find('file=')
                    self.imagelist.append(line[t4 + 5:-2])
                elif line.find('<a href="http://downloads.pli-images.org/builds/' + box + '/') > -1:
                    line = line[-43 - tt:-9]
                    self.imagelist.append(line)
                elif line.find('<a href="download.php?file=' + box + '/') > -1:
                    t4 = line.find('file=' + box)
                    t5 = line.find('.zip" class="')
                    self.imagelist.append(line[t4 + len(box) + 6:t5 + 4])
                elif line.find('href="opennfr-') > -1:
                    t4 = line.find('opennfr-')
                    t5 = line.find('.zip"')
                    self.imagelist.append(line[t4 :t5+4])
                elif line.find('href="http://downloads.pli-images.org' ) > -1:
                    t4 = line.find('OpenPLi-')
                    t5 = line.find('.zip"')
                    self.imagelist.append(line[t4 :t5+4])    
                elif line.find('href="openhdf-') > -1:
                    t4 = line.find('openhdf-')
                    t5 = line.find('.zip"')
                    self.imagelist.append(line[t4 :t5+4])
                                
        else:
            self.imagelist.append(stb)
        self['imageList'].l.setList(self.imagelist)


class ImageDownloadJob(Job):

    def __init__(self, url, filename, file):
        Job.__init__(self, _('Downloading %s' % file))
        ImageDownloadTask(self, url, filename)


class DownloaderPostcondition(Condition):

    def check(self, task):
        return task.returncode == 0

    def getErrorMessage(self, task):
        return self.error_message


class ImageDownloadTask(Task):

    def __init__(self, job, url, path):
        Task.__init__(self, job, _('Downloading'))
        self.postconditions.append(DownloaderPostcondition())
        self.job = job
        self.url = url
        self.path = path
        self.error_message = ''
        self.last_recvbytes = 0
        self.error_message = None
        self.download = None
        self.aborted = False
        return

    def run(self, callback):
        self.callback = callback
        self.download = downloadWithProgress(self.url, self.path)
        self.download.addProgress(self.download_progress)
        self.download.start().addCallback(self.download_finished).addErrback(self.download_failed)
        print '[ImageDownloadTask] downloading', self.url, 'to', self.path

    def abort(self):
        print '[ImageDownloadTask] aborting', self.url
        if self.download:
            self.download.stop()
        self.aborted = True

    def download_progress(self, recvbytes, totalbytes):
        if recvbytes - self.last_recvbytes > 10000:
            self.progress = int(100 * (float(recvbytes) / float(totalbytes)))
            self.name = _('Downloading') + ' ' + '%d of %d kBytes' % (recvbytes / 1024, totalbytes / 1024)
            self.last_recvbytes = recvbytes

    def download_failed(self, failure_instance = None, error_message = ''):
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        Task.processFinished(self, 1)
        return

    def download_finished(self, string = ''):
        if self.aborted:
            self.finish(aborted=True)
        else:
            Task.processFinished(self, 0)
