import maya.cmds as cmds

class BrokenFK():

    def __init__(self):
        self.window_name = "BrokenFKConstaints"

    def create(self):
        self.delete()
        self.window_name = cmds.window(self.window_name, t="Broken FK Constaints")
        self.column = cmds.columnLayout(p=self.window_name)
        self.constrainButton = cmds.button(p=self.column, label="Broken FK Constraints",
                                      command=lambda *args: self.Broken_FK_Constraints())
        cmds.showWindow(self.window_name)

    def delete(self):
        if (cmds.window(self.window_name, exists=True)):
            cmds.deleteUI(self.window_name)

    #Select parent->child->parent->child...
    def Broken_FK_Constraints(self, sels=[]):
        if len(sels) < 1:
            sels = cmds.ls(sl = True)
        if len(sels) > 1 or len(sels)%2==0:
            for i in range(0,len(sels), 2):
                self.Broken_FK_Constraints_Single(sels[i], sels[i+1])

    #select parent then child
    def Broken_FK_Constraints_Single(self, parentObj, childObj):
        constraintname = "%s_parentConstraint_translate" % childObj
        translateConstraint = cmds.parentConstraint(parentObj, childObj, maintainOffset=True,
                                                    skipRotate=['x', 'y', 'z'],
                                                    weight=1, name = constraintname)
        constraintname = "%s_parentConstraint_rotate" % childObj
        rotateConstraint = cmds.parentConstraint(parentObj, childObj, maintainOffset=True,
                                                    skipTranslate=['x', 'y', 'z'],
                                                    weight=1, name = constraintname)
        attributeControl = cmds.listRelatives(childObj, type='transform')
        childname = childObj[:-4]
        for ctrl in attributeControl:
            if ctrl == childname:
                cmds.addAttr(ctrl,longName="Translate", attributeType="float", minValue=0,
                             maxValue=1, keyable=True, defaultValue=1)
                cmds.addAttr(ctrl, longName="Rotate", attributeType="float", minValue=0,
                             maxValue=1, keyable=True, defaultValue=1)
                translateWeightName = translateConstraint[0] + "." + parentObj + "W0"
                translateAttribute = ctrl+".Translate"
                rotateAttribute = ctrl+".Rotate"
                cmds.connectAttr(translateAttribute, translateWeightName, f=True)
                rotateWeightName = rotateConstraint[0] + "." + parentObj + "W0"
                cmds.connectAttr(rotateAttribute, rotateWeightName, f=True)



rig = BrokenFK()
rig.create()
