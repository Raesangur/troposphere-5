import bpy
from bpy import context as C
from bpy import data as D
import time
import numpy as np
print("Started !")

bpy.data.objects["PiCar-Chassis-Assembly"].select_set(True)
 
leChar = bpy.context.active_object
leChar.location.x = 0
##bpy.ops.screen. change_frame(frame=0.0,snap=True)
#bpy.data.scenes['Scene'].frame_set(0)

bpy.data.scenes['Scene'].frame_set(0)
leChar.location.x = 0
bpy.ops.anim.keyframe_insert(type="LocRotScale")    

frames = np.arange(0,900,1)
for i in range(900):
    current_frame = frames[i] 
    bpy.data.scenes['Scene'].frame_set(current_frame)
    leChar.location.x = (i * i)  * 150
    bpy.ops.anim.keyframe_insert(type="LocRotScale")    
#   bpy.context.scene.frame_set(i)     
#    
#    


bpy.ops.screen.animation_play()

#leChar.location.x = 0