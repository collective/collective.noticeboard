from Products.CMFCore.WorkflowCore import WorkflowException
from collective.noticeboard.settings import NoticeboardSettings
from collective.noticeboard.interfaces import INoticeboard
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent
import logging

logger = logging.getLogger("collective.noticeboard")

def auto_publish(note, event):
    if INoticeboard.providedBy(event.newParent):
        settings = NoticeboardSettings(event.newParent)
        if settings.publish_on_creation:
            workflowTool = getToolByName(note, "portal_workflow")
            try:
                workflowTool.doActionFor(note, "publish")
            except WorkflowException:
                logger.info("Could not publish:" + str(note.getId()))
