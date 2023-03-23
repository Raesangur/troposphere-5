import bpy
from mathutils.bvhtree import BVHTree

print("tarted")
ligne_tres_droite = bpy.data.objects["ligne_tres_droite"]
ligne_droite = bpy.data.objects["ligne_droite"]
ligne_centre = bpy.data.objects["ligne_centre"]
ligne_gauche = bpy.data.objects["ligne_gauche"]
ligne_tres_gauche = bpy.data.objects["ligne_tres_gauche"]
path = bpy.data.objects["chemin"]

mat_td = ligne_tres_droite.matrix_world
mat_d = ligne_droite.matrix_world
mat_c = ligne_centre.matrix_world
mat_g = ligne_gauche.matrix_world
mat_tg = ligne_tres_gauche.matrix_world
mat_path = path.matrix_world


vert_td = [mat_td @ v.co for v in ligne_tres_droite.data.vertices] 
poly_td = [p.vertices for p in ligne_tres_droite.data.polygons]

vert_d = [mat_d @ v.co for v in ligne_droite.data.vertices] 
poly_d = [p.vertices for p in ligne_droite.data.polygons]

vert_c = [mat_c @ v.co for v in ligne_centre.data.vertices] 
poly_c = [p.vertices for p in ligne_centre.data.polygons]

vert_g = [mat_g @ v.co for v in ligne_gauche.data.vertices] 
poly_g = [p.vertices for p in ligne_gauche.data.polygons]

vert_tg = [mat_tg @ v.co for v in ligne_tres_gauche.data.vertices] 
poly_tg = [p.vertices for p in ligne_tres_gauche.data.polygons]

vert_path = [mat_path @ v.co for v in path.data.vertices] 
poly_path = [p.vertices for p in path.data.polygons]



bvh_td = BVHTree.FromPolygons( vert_td, poly_td )
bvh_d = BVHTree.FromPolygons( vert_d, poly_d )
bvh_c = BVHTree.FromPolygons( vert_c, poly_c)
bvh_g = BVHTree.FromPolygons( vert_g, poly_g)
bvh_tg = BVHTree.FromPolygons( vert_tg, poly_tg)
bvh_path = BVHTree.FromPolygons( vert_path, poly_path)

if bvh_path.overlap(bvh_td):
    print( "Overlap tres droite" )
if bvh_path.overlap(bvh_d):
    print( "Overlap droite" )
if bvh_path.overlap(bvh_c):
    print( "Overlap centre" )
if bvh_path.overlap(bvh_g):
    print( "Overlap gauche" )
if bvh_path.overlap(bvh_tg):
    print( "Overlap Tres gauche" )