import bpy
from mathutils.bvhtree import BVHTree
import bpy
from bpy import context as C
from bpy import data as D
import time
import math
import numpy as np
print("Started !")
leChar = bpy.data.objects["PiCar-Chassis-Assembly"]
##bpy.ops.screen. change_frame(frame=0.0,snap=True)
#bpy.data.scenes['Scene'].frame_set(0) bpy.data.scenes['Scene'].frame_set(0)
bpy.ops.anim.keyframe_insert(type="LocRotScale")
ACCMAX = 0.5 
VMAX = 0.736
frames = np.arange(0,1000,1)
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
vAct = 0
acc = 0
angle = 0
angleCalc = 0
precArrayPath = [0,0,1,0,0]
leChar.rotation_euler = [0,0,0]
leChar.location.x = 0
leChar.location.y = 0 
leChar.location.z = 0
        
for i in np.arange(0,1000,1):
    acc = ACCMAX
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
    
    vAct = acc * (i/24)
    
    if(vAct >= VMAX):
        vAct = VMAX
        acc = 0
    
    current_frame = frames[i] 
    bpy.data.scenes['Scene'].frame_set(current_frame)

    array_path = [0,0,0,0,0]
    if bvh_path.overlap(bvh_td):
        array_path[0] = 1
    if bvh_path.overlap(bvh_d):
        array_path[1] = 1
    if bvh_path.overlap(bvh_c):
        array_path[2] = 1
    if bvh_path.overlap(bvh_g):
        array_path[3] = 1
    if bvh_path.overlap(bvh_tg):
        array_path[4] = 1

    print("------" + str(i))
    print(array_path)
    print(vAct)
    print("location x: " + str(leChar.location.x))
    if array_path == [0,0,0,0,0]:
        array_path = precArrayPath
    if array_path == [1,1,1,1,1]:
        vAct = 0
        acc = 0
        
    if array_path == [0,1,1,0,0] or array_path == [0,0,1,1,0]:
        angleCalc = 15/24 
    elif array_path == [0, 1, 0, 0, 0] or array_path == [0, 0, 0, 1, 0]:
        angleCalc = 25/24
    elif array_path == [1, 1, 0, 0, 0] or array_path == [0, 0, 0, 1, 1]:
        angleCalc = 35/24
    elif array_path == [1, 0,0, 0, 0] or array_path == [0,0, 0, 0, 1]:
        angleCalc = 50/24
    
    if (array_path == [0, 0, 1, 1, 0] or array_path == [0, 0, 0, 1, 0] or array_path == [0, 0, 0, 1, 1] or array_path == [0, 0, 0, 0, 1]):
        angle += angleCalc
        leChar.rotation_euler = [0,0,math.radians(angle)]
    elif (array_path == [0, 1, 1, 0, 0] or array_path == [0, 1, 0, 0, 0] or array_path == [1, 1, 0, 0, 0] or array_path == [1, 0, 0, 0, 0]):
        angle -= angleCalc 
        leChar.rotation_euler = [0,0,math.radians(angle)]
    leChar.location.x = np.cos(math.radians(angle)) * ( vAct * (i/24) + 1/2 * acc * (i/24)**2) + leChar.location.x
    leChar.location.y = np.sin(math.radians(angle)) * ( vAct * (i/24) + 1/2 * acc * (i/24)**2) + leChar.location.y
    precArrayPath = array_path
    if i == 0:
        leChar.rotation_euler = [0,0,0]
        leChar.location.x = 0
        leChar.location.y = 0 
        leChar.location.z = 0
    bpy.ops.anim.keyframe_insert(type="LocRotScale")
#   bpy.context.scene.frame_set(i)     

bpy.ops.screen.animation_play() 