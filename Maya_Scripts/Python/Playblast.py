import maya.cmds as cmds

# Define the output path for the playblast
output_path = 'path_to_output_directory/output_filename.mov'

# Save the current scene
cmds.file(save=True)

# Get the render resolution width and height from the render settings
render_width = cmds.getAttr("defaultResolution.width")
render_height = cmds.getAttr("defaultResolution.height")

# Set playblast options
playblast_options = {
    'format': 'qt',
    'compression': 'H.264',
    'quality': 100,
    'widthHeight': (render_width, render_height),
    'filename': output_path,
}

# Create the playblast
cmds.playblast(**playblast_options)

print(f"Playblast created in QuickTime H.264 format with resolution {render_width}x{render_height} and saved to {output_path}.")
