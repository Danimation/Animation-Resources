## Reloads existing maya file ##

from maya import cmds
sFile = cmds.file(q=True, sceneName=True)
cmds.file(sFile, open=True, force=True)

## This reloading of the file can help when testing out changes and resetting things back to the defualt ##