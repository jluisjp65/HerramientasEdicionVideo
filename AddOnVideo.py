import bpy, os

fps = 30

Encabezado = "Torneo UNPA 2016"
JLocal = "Rodolfo  "
JVicta = "\nC. Raúl   "

# Intervalos de tiempos a eliminar
datos = [[0,0,0,5,0,11],[0,1,0,27,0,31],[1,1,0,34,0,38],[2,1,0,41,0,44],[3,1,0,47,0,51],[3,2,0,53,0,59],[3,3,1,2,1,6],[4,3,1,10,1,15],[4,4,1,22,1,26],[4,5,1,28,1,34],[5,5,1,38,1,41],[5,6,1,44,1,47],[5,7,1,51,1,55],[5,8,1,59,2,4],[5,9,2,7,2,11],[6,9,2,15,2,20],[7,9,2,23,2,29],[7,10,2,36,2,42],[7,11,2,43,2,47],[0,0,2,48,2,58],[0,1,3,6,3,11],[0,2,3,15,3,20],[0,3,3,32,3,39],[0,4,3,42,3,46],[1,4,3,53,3,56],[2,4,4,13,4,20],[2,5,4,23,4,27],[3,5,4,32,4,37],[3,6,4,42,4,45],[4,6,4,57,5,0],[4,7,5,11,5,15],[4,8,5,22,5,26],[4,9,5,30,5,34],[5,9,5,37,5,40],[6,9,5,43,5,46],[6,10,5,52,5,57],[6,11,5,58,6,6],[0,0,6,7,6,11],[1,0,6,14,6,17],[1,1,6,22,6,26],[1,2,6,28,6,32],[2,2,6,41,6,45],[3,2,6,50,6,57],[4,2,7,2,7,9],[4,3,7,17,7,20],[5,3,7,26,7,31],[6,3,7,42,7,47],[6,4,7,53,7,58],[7,4,8,2,8,6],[8,4,8,12,8,16],[8,5,8,18,8,21],[8,6,8,24,8,26],[8,7,8,29,8,33],[9,7,8,35,8,43],[9,8,8,51,8,55],[10,8,9,9,9,17],[11,8,9,18,9,26],[0,0,9,27,9,33],[0,1,9,38,9,43],[1,1,9,45,9,49],[2,1,9,50,9,54],[2,2,9,57,10,1],[3,2,10,4,10,11],[3,3,10,20,10,26],[4,3,10,28,10,32],[4,4,10,35,10,40],[4,5,10,44,10,47],[5,5,10,50,11,4],[6,5,11,8,11,12],[7,5,11,23,11,28],[8,5,11,31,11,38],[9,5,11,42,11,45],[10,5,11,51,11,56],[11,5,11,57,12,11],[0,0,12,12,12,18],[0,1,12,28,12,33],[1,1,12,54,12,59],[2,1,13,3,13,6],[2,2,13,8,13,13],[3,2,13,25,13,32],[4,2,13,35,13,41],[4,3,13,44,13,47],[5,3,13,49,13,55],[6,3,13,58,14,3],[7,3,14,7,14,12],[8,3,14,14,14,18],[8,4,14,21,14,28],[9,4,14,35,14,45],[9,5,14,51,14,56],[9,6,15,5,15,9],[10,6,15,13,15,19],[11,6,15,13,15,19],[11,6,15,20,15,40]]
#  [ LOCAL, VISITANTE, minuto inicial, seg inicial, minuto final, segundo final ] 
MFinal = "Rudy  3  7  6 11 11 11\nRaúl  2 11 11  8  5 6"
#########################################################
##  Procedimiento para subir videos a linea del tiempo
class insertVideo(bpy.types.Operator):
    bl_idname = "scene.invideo"
    bl_label = "Insert Video"
    
    def execute(self, context):
        episode_path = bpy.path.abspath( "/home/jluis/Vídeos/PPAntiguo")
        episode_list = os.listdir(episode_path)
        episode_sort = sorted(episode_list)
        first_frame=0
        last_frame=0
        for v in [f for f in episode_sort if f.endswith('.m4v')]:
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
      
        # antes de ejecutar deselecione todo en ventan de tiempo
        for i in range(len(datos)-1):
            bpy.ops.sequencer.select_all()
            fo = aFrame(datos[i][4],datos[i][5])
            ff = aFrame(datos[i+1][2], datos[i+1][3])
            if( (ff-fo) > fps*2 ):
                bpy.ops.sequencer.split(frame=fo, channel=2, type='SOFT', side='RIGHT')
                bpy.ops.sequencer.split(frame=ff, channel=2, type='SOFT', side='LEFT')
                bpy.ops.sequencer.delete()

        return{'FINISHED'}
########################################################
###   Procedimiento para colocar marcadores 
class marcador(bpy.types.Operator):
    bl_idname = "scene.marcador"
    bl_label = "marcador"
    

    def execute(self, context):
        
        
        setL = 0
        setV = 0
        for i in range(len(datos)-1):
            fi = aFrame(datos[i][2],datos[i][3])
            ff = aFrame(datos[i+1][2],datos[i+1][3])
            bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start=fi, frame_end=ff, channel=3)
            bpy.context.active_sequence_strip.text = JLocal+str(setL)+" "+str(datos[i][0])+JVicta+str(setV)+" "+str(datos[i][1])
            bpy.context.active_sequence_strip.location=[0.25,0.2]
            if(datos[i][0] > 10 and (datos[i][0]-datos[i][1])>1):  
                setL = setL + 1
            if(datos[i][1] > 10 and (datos[i][1]-datos[i][0])>1):  
                setV = setV + 1
            
        bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start=0, frame_end=300, channel=3)
        param = bpy.context.active_sequence_strip
        param.text = Encabezado
        param.location=[0.5,0.5]
        param.font_size = 100
        param.use_bold = True
        param.use_box = True
        param.box_color = (0.0862986, 0.103902, 0.2, 0.7)

        bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start=0, frame_end=300, channel=3)
        param= bpy.context.active_sequence_strip
        param.text = MFinal
        param.location=[0.5,0.5]
        param.font_size = 80
        param.use_bold = True
        param.use_box = True
        param.box_color = (0.0862986, 0.103902, 0.2, 0.7)

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
    
def aFrame(min,seg):
    fmin = min*60*fps
    fseg = seg*fps
    return fmin+fseg      

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