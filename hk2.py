#!/usr/bin/env python3
# /opt/anaconda/bin/python
#

import numpy as np
import string
import datetime
from datetime import datetime
import matplotlib.pyplot as pl
import matplotlib.dates as mdates
import argparse

def confloat(str):
	if (str != "N/A"):
		cf = float(str)
	elif (str == "N/A"):
		cf = 99999.
	return cf

parser=argparse.ArgumentParser(description='MODS HK')

parser.add_argument('isislog',type=str,help='ISIS logfile')

args = parser.parse_args()

isislog = args.isislog

pngfile = isislog.strip(".log") + ".png"

bhk = []
rhk = []

bk = 0
rk = 0
with open(isislog,'r') as read_file: 
     for line in read_file: 
          if "ESTATUS" in line: 
               if "RC" in line: 
                  #if rk == 0:
                     #ncolr = len(line.split()) 
                  ncolr = 20
                  #discard lines which are truncated before the optional last column
                  if rk > 0 and (len(line.split())) >= ncolr:
                        rhk.append(line.strip()) 
                  rk += 1
               if "BC" in line: 
                  #if bk == 0:
                     #ncolb = len(line.split())
                  ncolb = 20
                  if bk > 0 and (len(line.split())) >= ncolb:
                        bhk.append(line.strip()) 
                  bk += 1

abhk = np.empty((len(bhk),(ncolb)),dtype=np.dtype('U100'))
arhk = np.empty((len(rhk),(ncolr)),dtype=np.dtype('U100'))

for i in range(len(bhk)):
     abhk[i,:] = np.array(bhk[i].split()[:20])

for i in range(len(rhk)):
     arhk[i,:] = np.array(rhk[i].split()[:20])

b_ngood=len(abhk)
r_ngood=len(arhk)

b_dewpres=np.zeros(b_ngood)
b_ctempin=np.zeros_like(b_dewpres)
b_ctempout=np.zeros_like(b_dewpres)
b_hstemp=np.zeros_like(b_dewpres)
b_hebtemp=np.zeros_like(b_dewpres)
b_p24v=np.zeros_like(b_dewpres)
b_p5v=np.zeros_like(b_dewpres)
b_ccdtemp=np.zeros_like(b_dewpres)
b_dewtemp=np.zeros_like(b_dewpres)
b_m15=np.zeros_like(b_dewpres)
b_p12fan=np.zeros_like(b_dewpres)
b_ts = []
b_ddate = []

r_dewpres=np.zeros(r_ngood)
r_ctempin=np.zeros_like(r_dewpres)
r_ctempout=np.zeros_like(r_dewpres)
r_hstemp=np.zeros_like(r_dewpres)
r_hebtemp=np.zeros_like(r_dewpres)
r_p24v=np.zeros_like(r_dewpres)
r_p5v=np.zeros_like(r_dewpres)
r_ccdtemp=np.zeros_like(r_dewpres)
r_dewtemp=np.zeros_like(r_dewpres)
r_m15=np.zeros_like(r_dewpres)
r_p12fan=np.zeros_like(r_dewpres)
r_ts = []
r_ddate = []

for i in range(r_ngood):
     dt = datetime.strptime((arhk[i,0]),"%Y-%m-%dT%H:%M:%S.%f")
     r_ts.append(datetime.strptime((arhk[i,0]),"%Y-%m-%dT%H:%M:%S.%f"))
     r_ddate.append((((float(dt.strftime("%j"))-0)) + (float(dt.strftime("%H")) + (float(dt.strftime("%M"))/60.) + (float(dt.strftime("%S"))/3600.))/24.))
     r_dewpres[i] = confloat(str.split(arhk[i,7],"=")[1]) 
     r_ctempin[i] = confloat(str.split(arhk[i,8],"=")[1])
     r_ctempout[i] = confloat(str.split(arhk[i,9],"=")[1])
     r_hstemp[i] = confloat(str.split(arhk[i,10],"=")[1])
     r_hebtemp[i] = confloat(str.split(arhk[i,11],"=")[1])
     r_p24v[i] = confloat(str.split(arhk[i,12],"=")[1])
     r_p5v[i] = confloat(str.split(arhk[i,13],"=")[1])
     r_ccdtemp[i] = confloat(str.split(arhk[i,14],"=")[1])
     r_m15[i] = confloat(str.split(arhk[i,15],"=")[1])
     r_dewtemp[i] = confloat(str.split(arhk[i,16],"=")[1])

for i in range(b_ngood):
     dt = datetime.strptime((abhk[i,0]),"%Y-%m-%dT%H:%M:%S.%f")
     b_ts.append(datetime.strptime((abhk[i,0]),"%Y-%m-%dT%H:%M:%S.%f"))
     b_ddate.append((((float(dt.strftime("%j"))-0)) + (float(dt.strftime("%H")) + (float(dt.strftime("%M"))/60.) + (float(dt.strftime("%S"))/3600.))/24.))
     b_dewpres[i] = confloat(str.split(abhk[i,7],"=")[1]) 
     b_ctempin[i] = confloat(str.split(abhk[i,8],"=")[1])
     b_ctempout[i] = confloat(str.split(abhk[i,9],"=")[1])
     b_hstemp[i] = confloat(str.split(abhk[i,10],"=")[1])
     b_hebtemp[i] = confloat(str.split(abhk[i,11],"=")[1])
     b_p24v[i] = confloat(str.split(abhk[i,12],"=")[1])
     b_p5v[i] = confloat(str.split(abhk[i,13],"=")[1])
     b_ccdtemp[i] = confloat(str.split(abhk[i,14],"=")[1])
     b_m15[i] = confloat(str.split(abhk[i,15],"=")[1])
     b_dewtemp[i] = confloat(str.split(abhk[i,16],"=")[1])
#
pl.figure(figsize=(15,10))


# HEB temperature
ax1 = pl.subplot(2,1,1)

ax1.tick_params("x",rotation=90,labelsize=7)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax1.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))

ax1.set_xlim(r_ts[0],r_ts[-1])
ax1.set_yscale("log")
ax1.plot(r_ts,(r_dewpres),'r',linestyle="solid",marker=".",label="MODS2R")
ax1.plot(b_ts,(b_dewpres),'b',linestyle="solid",marker=".",label="MODS2B")
ax1.grid(True,which='both',axis='x')
pl.ylabel("Dewar Pressure [Torr]")
ax1.legend()
#

# Dewar and CCD temperature plot
ax2 = pl.subplot(2,1,2)
ax2.tick_params("x",rotation=90,labelsize=7)
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax2.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
ax2.set_xlim(r_ts[0],r_ts[-1])
ax2.set_ylim(-200, 0)
ax2.plot(b_ts,b_dewtemp,'b',linestyle="solid",marker=".",label="MODS2B Dewar Temp")
ax2.plot(r_ts,r_dewtemp,'r',linestyle="solid",marker=".",label="MODS2R Dewar Temp")
ax2.plot(b_ts,b_ccdtemp,'b',linestyle="dotted",marker=".",label="MODS2B CCD Temp")
ax2.plot(r_ts,r_ccdtemp,'r',linestyle="dotted",marker=".",label="MODS2R CCD Temp")
ax2.grid(True,which='both',axis='x')
ax2.legend()
pl.ylabel("Dewar (solid) and CCD (dotted) Temperature [K]")
pl.xlabel("Date UT") 

title = ("%s" % isislog)
pl.suptitle(title)

pl.savefig(pngfile)

# show the plots
pl.show()
