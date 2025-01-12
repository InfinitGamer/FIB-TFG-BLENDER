import bpy

class AnalyzeSettings(bpy.types.PropertyGroup):
   type: bpy.props.EnumProperty(
        items=[
            (
                "AVERAGEDISTORTION",
                "Average Distorsion",
                "Average distorsion from the whole object",
            ),
            (
                "AREADISTORTED",
                "Area Distorted",
                "Area distorted expressed in parts per units",
            ),
            ("RATIODISTORTED",
             "Ratio Distorted",
             "Image representing for each ratio of distorsion the number of polygons that have that ratio")
        ],
        default="AREADISTORTED",
    )
   
   path: bpy.props.StringProperty()