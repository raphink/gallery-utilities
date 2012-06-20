#!/usr/bin/env python
#
#	FILE: mplayer-video-thumb.py -- A script to generate PNG thumbnails
#	from MPlayer playable video files for use by Nautilus...
#
#	Examples:
#		mplayer-video-thumb.py  -s 128 file:///home/user/video.avi /home/user/thumb.png
#		
#
#	Requirements:
#		mplayer - MPlayer Project ( http://www.mplayerhq.hu/ )
#		Python Python Image Module
#
# Last Updated: 18 December 2006
#
# Written By:	Ravinder Rathi <mes030581@gmail.com>
#		John Conroy <jconroy@gmail.com>
#		Stephen Kennedy <stevek@gnome.org>
#		Fedora Fat <?>
#               Bittu <?>
#
# All rights reserved.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import sys,os,Image,subprocess
from shutil import rmtree
from urllib import unquote
from tempfile import mkdtemp
from random import randint
import time, select, signal
Size="128" #default thumbnail size -really-quiet
Role="/usr/share/totem/flim-role.png"
TMP=mkdtemp('',"mvideothumb.","/tmp/")
CMD="nice -n 10 /usr/bin/mplayer  -nojoystick -nolirc -nortc -noautosub -framedrop -noconsolecontrols -nomouseinput -nocache -ni -nobps -nodouble -nograbpointer -vf scale -nosound -zoom -nostop-xscreensaver -nofs -nokeepaspect -monitorpixelaspect 1 -vo jpeg:outdir="+TMP+":quality=100 -slave -x "
#Follwing Python unix subprocess wrapper by PIAdraig Brady (http://code.activestate.com/recipes/576387/)
class subProcess:
    """Class representing a child process. It's like popen2.Popen3
       but there are three main differences.
       1. This makes the new child process group leader (using setpgrp())
          so that all children can be killed.
       2. The output function (read) is optionally non blocking returning in
          specified timeout if nothing is read, or as close to specified
          timeout as possible if data is read.
       3. The output from both stdout & stderr is read (into outdata and
          errdata). Reading from multiple outputs while not deadlocking
          is not trivial and is often done in a non robust manner."""

    def __init__(self, cmd, bufsize=8192):
        """The parameter 'cmd' is the shell command to execute in a
        sub-process. If the 'bufsize' parameter is specified, it
        specifies the size of the I/O buffers from the child process."""
        self.cleaned=False
        self.BUFSIZ=bufsize
        self.outr, self.outw = os.pipe()
        self.errr, self.errw = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            self._child(cmd)
        os.close(self.outw) #parent doesn't write so close
        os.close(self.errw)
        # Note we could use self.stdout=fdopen(self.outr) here
        # to get a higher level file object like popen2.Popen3 uses.
        # This would have the advantages of auto handling the BUFSIZ
        # and closing the files when deleted. However it would mean
        # that it would block waiting for a full BUFSIZ unless we explicitly
        # set the files non blocking, and there would be extra uneeded
        # overhead like EOL conversion. So I think it's handier to use os.read()
        self.outdata = self.errdata = ''
        self._outeof = self._erreof = 0

    def _child(self, cmd):
        # Note sh below doesn't setup a seperate group (job control)
        # for non interactive shells (hmm maybe -m option does?)
        os.setpgrp() #seperate group so we can kill it
        os.dup2(self.outw,1) #stdout to write side of pipe
        os.dup2(self.errw,2) #stderr to write side of pipe
        #stdout & stderr connected to pipe, so close all other files
        map(os.close,[self.outr,self.outw,self.errr,self.errw])
        try:
            cmd = ['/bin/sh', '-c', cmd]
            os.execvp(cmd[0], cmd)
        finally: #exit child on error
            os._exit(1)

    def read(self, timeout=None):
        """return 0 when finished
           else return 1 every timeout seconds
           data will be in outdata and errdata"""
        currtime=time.time()
        while 1:
            tocheck=[]
            if not self._outeof:
                tocheck.append(self.outr)
            if not self._erreof:
                tocheck.append(self.errr)
            ready = select.select(tocheck,[],[],timeout)
            if len(ready[0]) == 0: #no data timeout
                return 1
            else:
                if self.outr in ready[0]:
                    outchunk = os.read(self.outr,self.BUFSIZ)
                    if outchunk == '':
                        self._outeof = 1
                    self.outdata += outchunk
                if self.errr in ready[0]:
                    errchunk = os.read(self.errr,self.BUFSIZ)
                    if errchunk == '':
                        self._erreof = 1
                    self.errdata += errchunk
                if self._outeof and self._erreof:
                    return 0
                elif timeout:
                    if (time.time()-currtime) > timeout:
                        return 1 #may be more data but time to go

    def kill(self):
        os.kill(-self.pid, signal.SIGTERM) #kill whole group

    def cleanup(self):
        """Wait for and return the exit status of the child process."""
        self.cleaned=True
        os.close(self.outr)
        os.close(self.errr)
        pid, sts = os.waitpid(self.pid, 0)
        if pid == self.pid:
            self.sts = sts
        return self.sts

    def __del__(self):
        if not self.cleaned:
            self.cleanup()


def mkthumb( Size,IFile,OFile ):
	try:    
	        if (IFile[:7] == "file://"):
			IFile=IFile[7:]
		if (os.path.getsize(IFile) < 200000):
			cmd=CMD+str(Size)+" -y "+str((int(Size)*96)/128)+" -frames 2"
		else:
			Seek=randint(15,70)
			cmd="echo seek "+str(Seek)+" 1 | "+CMD+str(Size)+" -y "+str((int(Size)*96)/128)+" -frames 14"
		#os.system('%s "%s"' % (cmd,IFile))
		#runMplayer=subprocess.Popen(('%s "%s"' % (cmd,IFile)),shell=True)
		#runMplayer.wait()
		runMplayer = subProcess(('%s "%s"' % (cmd,IFile)))
		if (runMplayer.read(5) == 0): #Wait for at max 5 sec for geting frames
			if (os.path.getsize(IFile) < 200000):
				frame=TMP+"/00000002.jpg"
			else:
				frame=TMP+"/00000014.jpg"
			f=Image.open(frame)
			r=Image.open(Role)
			rr=r.resize((f.size))
			f.paste(rr,(0,0),rr)
			f.save(OFile,"PNG")
		else:
			print "Taking too much time"
			runMplayer.kill()
	except:
		print "Something gone wrong"
		pass
	print "Removing TMP dir"
        rmtree(TMP)
		
Instructions = "This script genrate thumbnail of video file \n"+\
               "e.g.:  python mplayer-video-thumb.py -s size input output \n"+\
               "e.g.:  python mplayer-video-thumb.py  input output \n"+\
               "default size is 128"

if __name__=="__main__":
    if len(sys.argv) == 5:
        mkthumb(sys.argv[2],unquote(sys.argv[3]),sys.argv[4])
    elif len(sys.argv) == 3:
    	mkthumb(Size,unquote(sys.argv[1]),sys.argv[2])
    else:
        print Instructions


