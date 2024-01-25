## Cycles through all existing perspective cameras in your maya scene ##

import maya.cmds as cmds
import maya.mel as mel

currentCam = cmds.lookThru (q=1)
camType = cmds.camera (currentCam, q=1, o=1)
allPrespCams = cmds.listCameras (p=1)
if not camType: # See if camera is prespective
        i = allPrespCams.index( currentCam ) 
        countPCams = len(allPrespCams) - 1
        if currentCam == allPrespCams[countPCams]:
            i=0
            cmds.lookThru (allPrespCams[i])
        else:
            i +=1
            cmds.lookThru (allPrespCams[i])
else:
        i=0
        cmds.lookThru (allPrespCams[i])
mel.eval ('print ("Camera: " + `lookThru -q`)')
