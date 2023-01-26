import bpy

#  Convierte tiempo en frame  
def aFrame(min,seg):
    fmin = min*60*60
    fseg = seg*60
    return fmin+fseg  

# Intervalos de tiempos a eliminar

datos = [[0, 0 , 0, 37],[1,44, 2, 8], [2,51,2,56], [3,50,3,55],[4,4,4,11],[4,22,4,35],[ 4,44, 4,49],[ 4,57, 5,9],[ 5,25, 5,32],[ 6,33 ,6,42],[ 7,2, 7,9],[ 7,16, 8,36],[ 9,32 ,9,38],[ 10,8 ,10,18],[ 10,42 ,10,54],[ 11,19, 13,46],[ 14,24, 14,33],[ 15,9 ,15,12],[ 15,19, 15,27],[ 15,44 ,15,49],[ 15,52 ,16,1],[ 16,21 ,16,28],[ 16,45, 16,57],[ 17,13, 17,16],[ 17,55 ,18,4],[ 18,53, 18,57],[ 20,21, 20,48],[ 21,3 ,21,13],[ 21,39, 21,53],[ 22,27, 22,36],[ 23,13, 23,23],[ 23,37, 23,44],[ 24,43, 24,46],[ 25,48, 25,58],[ 26,18, 26,30],[ 26,41, 26,56],[ 27,7, 27,13],[ 27,22, 27,34]]
#  [ minuto inicial, seg inicial, minuto final, segundo final ] 

# Proceso de recortes en video 
filas = len(datos)
for i in range(filas):
    j = filas - i -1
    bpy.ops.sequencer.select_all()
    bpy.ops.sequencer.split(frame=aFrame(datos[j][0],datos[j][1]), channel=2, type='SOFT', side='RIGHT')
    bpy.ops.sequencer.split(frame=aFrame(datos[j][2],datos[j][3]), channel=2, type='SOFT', side='LEFT')
    bpy.ops.sequencer.delete()
  