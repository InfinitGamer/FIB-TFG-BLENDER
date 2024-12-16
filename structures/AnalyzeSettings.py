import bpy

class AnalyzeSettings(bpy.types.PropertyGroup):
   type: bpy.props.EnumProperty(
        items=[
            (
                "AVERAGEDISTORTION",
                "Average Distorsion",
                "Average distorsion from the whole object",
            ),
            ("AREADISTORTED", "Area Distorted", "Area distorted expressed in parts per units"),
        ],
        default="AREADISTORTED",
    ) 