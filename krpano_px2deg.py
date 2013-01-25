import argparse
"""
    A simple tool to convert a pixel coordinate to a degree-coordinate
    for krpano hotspots needed in tour.xml
"""

parser = argparse.ArgumentParser(description='Calculate ath/vth for krpano hotspots')

parser.add_argument('--x', dest='coord_x', type=float, required=True)
parser.add_argument('--y', dest='coord_y', type=float, required=True)
parser.add_argument('--w', dest='image_width', type=float, default=22896.0)
parser.add_argument('--h', dest='image_height', type=float, default=11448.0)
parser.add_argument('--dir', dest='direction', action='store_true', default=False)

args = parser.parse_args()

ath = 360.0/args.image_width*args.coord_x
atv = 180.0/args.image_height* ((args.image_height/2.0)-args.coord_y)

if args.coord_x < (args.image_width/2.0):
    atv = atv+180.0

print '<point ath="%f" atv="%f" />' % (ath,atv)
