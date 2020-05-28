#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 20:40:02 2020

@author: github.com/ryanign

Basic to plot an elevation data and a tectonic fault shapefile
--combination pygmt and cartopy
"""

import pygmt


###files needed
dem = '../data/dem_gebco2014_cut.grd'

###Prepare basemap using pygmt
with pygmt.clib.Session() as session:
    session.call_module('gmtset', 'MAP_FRAME_TYPE plain')           ## A simple frame
    session.call_module('gmtset', 'FONT 10p')                       ## Fontsize for frame
    
fig = pygmt.Figure()
fig.basemap(region=[125,135,-10,0],projection='M0/0/5i',frame=True)  ## Set region and projection

###Colormap
demcpt = "dem.cpt"
pygmt.makecpt(cmap='globe', series="-10000/10000/100", output=demcpt )

###Plot data
fig.grdimage(dem,cmap=demcpt)
fig.grdcontour(dem, interval="2000", limit="-10000/-10", annotation=(True,"f6p"), 
               pen="0.2p")
fig.grdcontour(dem, interval="10000", pen="0.3p")

fig.savefig('../outputs/image.png',dpi=300)


