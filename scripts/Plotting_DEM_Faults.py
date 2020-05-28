#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 20:40:02 2020

@author: github.com/ryanign

Basic to plot an elevation data and a tectonic fault shapefile
--combination pygmt and cartopy
"""
import numpy as np
import pygmt
import shapefile

def reading_shapefile(infile):
    shp = open(infile+'.shp','rb')
    dbf = open(infile+'.dbf','rb')
    shpfile = shapefile.Reader(shp=shp,dbf=dbf)
    return shpfile


def main():
    ###files needed
    dem = '../data/dem_gebco2014_cut.grd'
    faults = '../data/Tectonic_faults'
    
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
    
    ###Extract shapefile data
    flt = reading_shapefile(faults)
    Nfeatures = len(flt)                                                ## Number of features
    #Nfeatures = 1
    for i in range(Nfeatures):
        gmtry = flt.shape(i)                                            ## Extract shapefile geometry
        rcrds = flt.record(i)                                           ## Extract shapefile record/attribute
        lon  = np.empty(len(gmtry.points))
        lat  = np.empty(len(gmtry.points))
        for j in range(len(gmtry.points)):                              ## Extract feature vertices
            lon[j]  = gmtry.points[j][0]
            lat[j]  = gmtry.points[j][1]
        
        if rcrds.Mechanism == 'Thrust':                                 ## Read fault mechanism
            style = 'f1+r+t'
            pen   = '0.5p'
        elif rcrds.Mechanism == 'Normal':
            style = 'f1+r+b'
            pen   = '0.5p'
        elif rcrds.Mechanism == 'Trough':
            style = 'f1/0.00001'
            pen   = '0.5p,-'
        else:
            style = 'f1/0.00001'
            pen   = '0.5p'
        
        fig.plot(x=lon,y=lat,style=style,color='black',pen=pen)         ## Plot mechanism in GMT
        
    fig.savefig('../outputs/image.png',dpi=300)

if __name__ == "__main__":
    main()

