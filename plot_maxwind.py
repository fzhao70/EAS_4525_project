import numpy as np
import pandas as pd
import Ngl

def read_xls(filename):
    dfs = pd.read_excel(filename, sheet_name="Sheet1").to_numpy()
    return dfs

#track_name = "Charley-Track"
#track_name = "Katrina-Track"
track_name = "Wilma-Track"

#for track_name in ["Charley-Track", "Katrina-Track", "Wilma-Track"]:
dfs = read_xls(track_name+".xls")
lon_c = dfs[:, 1]
lat_c = dfs[:, 2]

lon = np.load("lon.npy")
lat = np.load("lat.npy")
grid = np.load(track_name + ".npy")
count = np.zeros_like(lon)
dim = grid.shape
maxwind = np.amax(grid, 0)

wks = Ngl.open_wks("png", track_name)
resources = Ngl.Resources()
resources.cnFillOn = True
resources.cnLinesOn = False
resources.cnLineLabelsOn        = False
resources.cnInfoLabelOn         = False
resources.mpLimitMode = "LatLon"    # Limit the map view.
resources.mpMinLonF   = np.min(lon)
resources.mpMaxLonF   = np.max(lon)
resources.mpMinLatF   = np.min(lat)
resources.mpMaxLatF   = np.max(lat)
resources.mpPerimOn   = True        # Turn on map perimeter.
resources.nglFrame = False
resources.nglDraw  = False
resources.mpOutlineBoundarySets = "GeophysicalAndUSStates"
resources.mpLandFillColor        = 16
resources.mpFillOn               = True
resources.sfXArray = lon
resources.sfYArray = lat
resources.cnFillPalette = "WhViBlGrYeOrRe"
resources.cnLevelSelectionMode = "ExplicitLevels"
resources.cnLevels  = np.arange(1, 100, 10)
resources.tiMainString = track_name + " maxwind "
resources.lbTitleString = "Knots"
#resources.lbTitlePosition = "Right"
resources.lbLabelFontHeightF = 0.02
resources. lbTitleFontHeightF = 0.02
resources.cnFillMode = "RasterFill"


mpid = Ngl.contour_map(wks, np.transpose(maxwind), resources)
#mpid = Ngl.contour_map(wks, np.transpose(grid), resources)

mkres = Ngl.Resources()
mkres.gsMarkerIndex = 1
mkres.gsMarkerColor = "Black"
mkres.gsMarkerSizeF =  15
dum = Ngl.add_polymarker(wks, mpid, lon_c, lat_c, mkres)

Ngl.draw(mpid)
Ngl.frame(wks)

Ngl.end()
