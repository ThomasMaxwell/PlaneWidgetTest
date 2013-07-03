

import vtk
import math

import shapefile
sf = shapefile.Reader("/home/winstonzhou/data/coastline/high/ne_10m_coastline.shp")
shapes = sf.shapes()


points = vtk.vtkPoints()

print(len(shapes))
lines = vtk.vtkCellArray()  
for x in range(len(shapes)):
    shape =  shapes[x] 
    nPts = len( shape.points )
    lines.InsertNextCell(nPts) 
    for iPt in range(nPts):
        pt = shape.points[iPt]
        ptIndex=points.InsertNextPoint(pt[0], pt[1], 0.0 )
        lines.InsertCellPoint(ptIndex)  

       

polygon = vtk.vtkPolyData()
polygon.SetPoints(points)
polygon.SetLines(lines)
 

polygonMapper = vtk.vtkPolyDataMapper()
polygonMapper.SetInputConnection(polygon.GetProducerPort())
 

polygonActor = vtk.vtkActor()
polygonActor.SetMapper(polygonMapper)
 
ren1 = vtk.vtkRenderer()
ren1.AddActor(polygonActor)
ren1.SetBackground(0.1, 0.2, 0.4)

ren1.ResetCamera()
 
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)
 

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
 