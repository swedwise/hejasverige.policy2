# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('hejasverige.policy2-various.txt') is None:
        return
    portal = context.getSite()
    disable_actions(portal)

def disable_actions(portal):
    """ Remove unneeded Plone actions
    @param portal Plone instance
    """
    # import pdb;pdb.set_trace()
    # getActionObject takes parameter category/action id
    # For ids and categories please refer to portal_actins in ZMI

    actionInformation = portal.portal_actions.getActionObject("user/mystuff")

    # See ActionInformation.py / ActionInformation for available edits
    if actionInformation:
    	actionInformation.edit(visible=False)
    else:
    	logger.error('Unable to get action object for user/mystuff')