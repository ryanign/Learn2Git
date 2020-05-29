#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:41:34 2020

@author: github.com/ryanign

Basic to plot an elevation data and a tectonic fault shapefile
--cartopy
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs                                          ### Cartopy, set projection
import cmocean.cm as cmo                                            ### Cmocean colormap
from netCDF4 import Dataset                                         ### NetCDF4
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter ### Cartopy, tick formater


def main():
    ###files needed
    demfile = '../data/dem_gebco2014_cut.grd'
    faults  = '../data/Tectonic_faults'
    
    ###Reading dem file
    lons,lats,dem = reading_netcdf(demfile)
    X,Y = np.meshgrid(lons,lats)
    #X,Y = np.meshgrid(np.linspace(xr[0],xr[1],dmn[0]),np.linspace(yr[0],yr[1],dmn[1]))
    
    
    ###Plotting
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111,projection=ccrs.PlateCarree())
    elevation = ax.imshow(dem,extent=[lons[0],lons[-1],lats[0],lats[-1]],origin='lower',
                          cmap=cmo.topo,vmin=-10000,vmax=10000) ##cmo.topo
    contour = ax.contour(X,Y,dem,levels=[-6000,-4000,-2000,0],colors='black',
                         linewidths=0.25,transform=ccrs.PlateCarree(),linestyles='-')
    ax.clabel(contour,fmt='{:.0f}'.format,fontsize=4,inline_spacing=0.05)
    
    
    ax.set_xticks([126,128,130,132,134])
    ax.set_yticks([-10,-8,-6,-4,-2,0])
    lon_formatter = LongitudeFormatter(number_format='.0f')#'.0f')
    lat_formatter = LatitudeFormatter(number_format='.0f')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    ax.tick_params(axis='both',left=True,bottom=True,right=True,top=True,
                   labelleft=True,labelbottom=True,labelright=True,labeltop=True,
                   labelsize=7)
    
    ax.text(134.8,-9.8,'ignatiusryanpranantyo at gmail dot com [29/05/2020]',
            fontsize=4,ha='right',va='bottom',color=(0,0,1))
    
    fig.tight_layout()
    fig.savefig('../outputs/image-02.png',dpi=300)
    plt.close()
    
    return

def reading_netcdf(infile):
    data = Dataset(infile)
    lons = data.variables['lon'][:]
    lats = data.variables['lat'][:]
    vals = data.variables['z'][:]
    
    data.close()
    return lons,lats,vals

if __name__ == "__main__":
    main()

