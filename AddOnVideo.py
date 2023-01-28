import bpy, os

# Intervalos de tiempos a eliminar
datos = [[0, 0 , 0, 37],[1,44, 2, 8], [2,51,2,56], [3,50,3,55],[4,4,4,11],[4,22,4,35],[ 4,44, 4,49],[ 4,57, 5,9],[ 5,25, 5,32],[ 6,33 ,6,42],[ 7,2, 7,9],[ 7,16, 8,36],[ 9,32 ,9,38],[ 10,8 ,10,18],[ 10,42 ,10,54],[ 11,19, 13,46],[ 14,24, 14,33],[ 15,9 ,15,12],[ 15,19, 15,27],[ 15,44 ,15,49],[ 15,52 ,16,1],[ 16,21 ,16,28],[ 16,45, 16,57],[ 17,13, 17,16],[ 17,55 ,18,4],[ 18,53, 18,57],[ 20,21, 20,48],[ 21,3 ,21,13],[ 21,39, 21,53],[ 22,27, 22,36],[ 23,13, 23,23],[ 23,37, 23,44],[ 24,43, 24,46],[ 25,48, 25,58],[ 26,18, 26,30],[ 26,41, 26,56],[ 27,7, 27,13],[ 27,22, 27,34]]
 #  [ minuto inicial, seg inicial, minuto final, segundo final ] 

#########################################################
##  Procedimiento para subir videos a linea del tiempo
class insertVideo(bpy.types.Operator):
    bl_idname = "scene.invideo"
    bl_label = "Insert Video"

    def execute(self, context):
        episode_path = bpy.path.abspath( "/home/jluis/Vídeos/PingPong23/21Enero23/")
        episode_list = os.listdir(episode_path)
        episode_sort = sorted(episode_list)
        first_frame=0
        last_frame=0
        for v in [f for f in episode_sort if f.endswith('.mp4')]:
            movs = os.path.join(episode_path,v)
            start_frame = last_frame+first_frame
            bpy.ops.sequencer.movie_strip_add(filepath=movs, frame_start=start_frame, channel=1)
            first_frame = bpy.context.scene.sequence_editor.sequences_all[v].frame_start
            last_frame = bpy.context.scene.sequence_editor.sequences_all[v].frame_final_duration
        return{'FINISHED'}
 
############################################
##   Procedimiento para recortar el video
## 
class recorta(bpy.types.Operator):
    bl_idname = "scene.recorta"
    bl_label = "recorta"


    def execute(self, context):
        
        def aFrame(min,seg):
            fmin = min*60*60
            fseg = seg*60
            return fmin+fseg

        filas = len(datos)
        for i in range(filas):
            j = filas - i -1
            bpy.ops.sequencer.select_all()
            bpy.ops.sequencer.split(frame=aFrame(datos[j][0],datos[j][1]), channel=2, type='SOFT', side='RIGHT')
            bpy.ops.sequencer.split(frame=aFrame(datos[j][2],datos[j][3]), channel=2, type='SOFT', side='LEFT')
            bpy.ops.sequencer.delete()

        return{'FINISHED'}
########################################################
###   Procedimiento para colocar marcadores 
class marcador(bpy.types.Operator):
    bl_idname = "scene.marcador"
    bl_label = "marcador"
    

    def execute(self, context):
        def aFrame(min,seg):
            fmin = min*60*60
            fseg = seg*60
            return fmin+fseg
        
       
        for i in range(len(datos)-1):
            fi = aFrame(datos[i][2],datos[i][3])
            ff = aFrame(datos[i+1][0],datos[i+1][1])
            bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start=fi, frame_end=ff, channel=3)
            bpy.context.active_sequence_strip.text = "Hola  "+str(i)

        return{'FINISHED'}
 
 
#######################################################
##  Codigo principal para dar formato a este complemento
class MyPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mis Herramientas de video"
    bl_idname = "my.panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Pasos a seguir")       
        row = layout.row()
        row.operator("scene.invideo", text="Insertar videos")
        row = layout.row()
        row.operator("scene.recorta", text="Recortar")
        row = layout.row()
        row.operator("scene.marcador", text="Marcador")
    
      

def register():
    bpy.utils.register_class(MyPanel)
    bpy.utils.register_class(insertVideo)
    bpy.utils.register_class(recorta)
    bpy.utils.register_class(marcador)


def unregister():
    bpy.utils.unregister_class(MyPanel)
    bpy.utils.unregister_class(insertVideo)
    bpy.utils.unregister_class(recorta)
    bpy.utils.unregister_class(marcador)


if __name__ == "__main__":
    register()