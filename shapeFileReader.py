#Winston Zhou


import vtk
import math
import os.path
import shapefile
from vtk import *

class shapeFileReader:
    
    def __init__(self):
        self._rgb=[ 0.5, 0.7, 0.1 ]
        self._linewidth=5
        self._reader=multiRoSShape()
        
        
    #sets the color of vtk    
    def setColors(self,rgb):    
       self._rgb=rgb
        
    #sets length of vtk
    def setWidth(self, linewidth):
       self._linewidth=linewidth
    
    #looks for resolution of the file, connects directory paths and then
    #creates a VTK model of land    
    def getLine(self,roi, mrsDefFilePath ): 
        
        
        xr=roi[1]-roi[0]
        yr=roi[3]-roi[2]
        r=max(xr,yr)

        ##checks roi and determines the resolution of requested file
        if r<50:
            resFile="high"
        if r>=50 and r<=100:
            resFile="medium"
        else:
            resFile="high"

        directory=self._reader.openFile(resFile,mrsDefFilePath)
        print(directory)
        print('1')
        #rel_coastFilePath=self._reader.read(resFile, mrsDefFilePath)
        root_path=os.path.abspath( os.path.dirname( mrsDefFilePath ) )
        print(root_path)
        #combines two directories together 
        full_coastFilePath=os.path.join( root_path, directory)
        sf = shapefile.Reader(full_coastFilePath)
        shapes = sf.shapes()
        
        
        
 
        points = vtk.vtkPoints()

        lines = vtk.vtkCellArray()
        for x in range(len(shapes)):
            
            shape =  shapes[x] 
            nPts = len( shape.points )
            idList=vtk.vtkIdList()
            for iPt in range(nPts):
                pt = shape.points[iPt]
                if pt[0]>roi[0] and pt[0]<roi[1]: 
                    if pt[1]>roi[2] and pt[1]<roi[3]:
                        ptIndex=points.InsertNextPoint(pt[0], pt[1], 0.0 ) 
                        idList.InsertNextId(ptIndex) 
            lines.InsertNextCell(idList)
        polygon = vtk.vtkPolyData()
        polygon.SetPoints(points)
        polygon.SetLines(lines)
        polygonMapper = vtk.vtkPolyDataMapper()
        polygonMapper.SetInputConnection(polygon.GetProducerPort())
        polygonActor = vtk.vtkActor()
        polygonActor.SetMapper(polygonMapper)
        
        property = vtk.vtkProperty()
        property.SetColor(self._rgb)
        property.SetLineWidth(self._linewidth)
        polygonActor.SetProperty(property)
        return polygonActor

#finds path of directory 
class multiRoSShape:
    
     def __init__(self):       
        self.FileMap = {}
        
     def openFile( self, res, textFilePath ):
         if(not ((self.FileMap.has_key(textFilePath))):
             self.FileMap[textFilePath]=self.read(textFilePath)
             
         self.FileMap[textFilePath] = self.read( textFilePath)
         resDict =  self.FileMap[textFilePath]
         return resDict[res]
         
     def read(self, textFilePath):
        resDict ={}
        f=open(textFilePath, 'r')
        lines=f.readlines()

        for line in lines:
            lineE=line.split('=')
            if(len(lineE)>1):
                resDict[ lineE[0].strip() ]  = lineE[1].strip()  
        return resDict
        
            
roi=[-80,80,-50,50]
rgb=[5.30, 1.0, 0.20 ]
linewidth=4
#reader=multiRoSShape()
textFilePath="/home/winstonzhou/data/coastline/coastline.txt"
#file=reader.openfile(file, halfDirec)

s=shapeFileReader()
s.setColors(rgb)
s.setWidth(linewidth)

polygonActor=s.getLine(roi,textFilePath)

ren1 = vtk.vtkRenderer()
ren1.AddActor(polygonActor)
ren1.SetBackground(0.46, 0.77, 0.99)

ren1.ResetCamera()

renWin = vtk.vtkRenderWindow()

renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()

iren.Start()