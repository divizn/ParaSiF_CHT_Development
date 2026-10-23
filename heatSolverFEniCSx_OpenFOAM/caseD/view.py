import os
from paraview.simple import *

case = os.getcwd()  # run from caseD

fluid = OpenFOAMReader(FileName=os.path.join(case, "fluid/fluid.foam"))
fluid.CellArrays = ["T"]
solid = Xdmf3ReaderS(FileName=[os.path.join(case, "solid/output/fenicsx_solid_data.xdmf")])

view = GetActiveViewOrCreate("RenderView")
lut = GetColorTransferFunction("T")

fluid_display = Show(fluid, view)
fluid_display.Representation = "Surface With Edges"
ColorBy(fluid_display, ("CELLS", "T"))
fluid_display.LookupTable = lut

solid_display = Show(solid, view)
solid_display.Representation = "Surface With Edges"
ColorBy(solid_display, ("POINTS", "f"))
solid_display.LookupTable = lut
lut.AutomaticRescaleRangeMode = "Never"
lut.RescaleTransferFunction(273.15, 274.15)

fluid_display.SetScalarBarVisibility(view, True)
bar = GetScalarBar(lut, view)
bar.Title = "T (K)"
bar.RangeLabelFormat = "{:.2f}"
bar.WindowLocation = "Any Location"
bar.Position = [0.85, 0.25]
bar.TitleFontSize = 14
bar.LabelFontSize = 12

GetAnimationScene().UpdateAnimationUsingDataTimeSteps()
GetAnimationScene().AnimationTime = 0

view.InteractionMode = "2D"
view.CameraPosition = [0.6, 0.5, 3]
view.CameraFocalPoint = [0.6, 0.5, 0]
view.CameraViewUp = [0, 1, 0]
view.ResetCamera()
Render()
