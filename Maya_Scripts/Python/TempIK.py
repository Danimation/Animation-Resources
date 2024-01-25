#create a temporary IK chain
#SELECT FOUR OBJECTS TO MAKE AN IK CHAIN WITH (The last three selected will be the chain, the first selected is the parent)
#made by Martin Chang, 2020
import maya.cmds as cmds

objects = cmds.ls ( orderedSelection = True, long = False)

if len(objects) == 4:
    #put selected controls into variables and get the time range
    ik_parent = objects[0]
    ik_top = objects[1]
    ik_mid = objects[2]
    ik_bot = objects[3]
    objects = cmds.ls ( orderedSelection = True)
    temp_ik_grp = cmds.group(name=objects[1]+'_tempIK_grp', empty=True)
    cmds.select(clear=True)
    startTime = cmds.playbackOptions( q=True, minTime=True )
    endTime = cmds.playbackOptions( q=True, maxTime=True )
    
    cmds.currentTime(startTime)
    
    #create joint chain
    ik_jnt_top = cmds.joint(name=ik_top+'_IK_jnt')
    cmds.matchTransform(ik_jnt_top, ik_top, position=True, rotation=True)
    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True)
    cmds.select(ik_jnt_top)
    ik_jnt_mid = cmds.joint(name=ik_mid+'_IK_jnt')
    cmds.matchTransform(ik_jnt_mid, ik_mid, position=True, rotation=True)
    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True)
    cmds.select(ik_jnt_mid)
    ik_jnt_bot = cmds.joint(name=ik_bot+'_IK_jnt')
    cmds.matchTransform(ik_jnt_bot, ik_bot, position=True, rotation=True)
    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True)
    
    #create IK handle
    ik_handle, ik_effector = cmds.ikHandle(name=ik_top+'_IK_TEMP', startJoint=ik_jnt_top, endEffector=ik_jnt_bot)
    cmds.hide(ik_handle, ik_jnt_top)
    
    #create temp controls
    loc_top = cmds.spaceLocator(name=ik_top+'ik_temp_loc')
    loc_top_grp = cmds.group(loc_top, name=ik_top+'_loc_top_grp')
    cmds.parentConstraint(ik_parent, loc_top_grp)
    pv_mid = cmds.spaceLocator(name=ik_mid+'ik_temp_loc')
    loc_bot = cmds.spaceLocator(name=ik_bot+'ik_temp_loc')
    cmds.poleVectorConstraint(pv_mid, ik_handle)
    cmds.hide(loc_top)
    cmds.parent(ik_jnt_top, temp_ik_grp)
    cmds.parent(ik_handle, temp_ik_grp)
    cmds.parent(loc_top_grp, temp_ik_grp)
    cmds.parent(pv_mid, temp_ik_grp)
    cmds.parent(loc_bot, temp_ik_grp)
    
    constraintList=[]
    #match temp controls to main controls
    constraint = cmds.parentConstraint(ik_top, loc_top, mo=False)
    constraintList.append(constraint)
    constraint = cmds.parentConstraint(ik_mid, pv_mid, mo=False)
    constraintList.append(constraint)
    constraint = cmds.parentConstraint(ik_bot, loc_bot, mo=False)
    constraintList.append(constraint)
    
    cmds.bakeResults(loc_bot, pv_mid, loc_top, time=(startTime,endTime), simulation=False, preserveOutsideKeys=True)
    cmds.cutKey(pv_mid, attribute = ['rx', 'ry', 'rz'], clear=True)
    cmds.matchTransform( pv_mid, ik_mid, rotation=True)
    for attr in ['.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
        cmds.setAttr(pv_mid[0] + attr, lock=True)    


    for c in constraintList:
        cmds.delete(c)
    
    del constraintList
    del constraint
    
    #constrain joints
    cmds.pointConstraint(loc_top, ik_jnt_top)
    cmds.hide(loc_top)
    cmds.pointConstraint(loc_bot, ik_handle)
    cmds.orientConstraint(loc_bot, ik_jnt_bot)
    
    #constrain controls
    #cmds.cutKey(ik_top, ik_mid, ik_bot, clear=True)
    
    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(ik_top, locked=True, scalar=True)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())
    cmds.parentConstraint(ik_jnt_top, ik_top, skipTranslate=lockedPos, skipRotate=lockedRot, maintainOffset=True)

    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(ik_mid, locked=True, scalar=True)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())
    cmds.parentConstraint(ik_jnt_mid, ik_mid, skipTranslate=lockedPos, skipRotate=lockedRot, maintainOffset=True)

    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(ik_bot, locked=True, scalar=True)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())       
    cmds.orientConstraint(loc_bot, ik_bot, skip=lockedRot, maintainOffset=True)
    
    cmds.select(loc_bot, pv_mid)
    cmds.filterCurve()