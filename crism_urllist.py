import os, sys, glob
from shapefile import shapefile

if not os.path.exists("download"):
    os.makedirs("download")

footprintfile = 'footprints/mars_mro_crism_trdrddrfrt07_c0a.shp'
shp = shapefile("read", footprintfile)
urls = []
for feat in shp.features:
    attr_dict = shp.attr_dict(feat)
    LabelURL = attr_dict["LabelURL"]
    LabelURL = LabelURL.strip()
    LabelURL = LabelURL.replace(".lbl", ".img")
    urls.append(LabelURL)
shp.finish()

for productidfile in glob.glob('regions/*.txt'):
    f = open(productidfile,"r")
    wgetdownloadlist = 'download/' + os.path.basename(productidfile)[:-4] + '_urllist.txt'
    o = open(wgetdownloadlist,'w')
    for productid in f:
        productid = productid.strip().lower()[:17]
        if "_if" in productid:
            for url in urls:
                ddrid = productid[:-2] + "de"
                if productid in url or ddrid in url:
                    o.write("%s\n" % (url))
                    o.write("%s\n" % (url[:-4] + ".lbl"))
    f.close()
    o.close()
    print "Written:", wgetdownloadlist
