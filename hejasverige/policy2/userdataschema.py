# -*- coding: utf-8 -*-

from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from zope.interface import Invalid
from hejasverige.policy2 import _
from zope.schema import ValidationError
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from plone import api

import logging
logger = logging.getLogger(__name__)


class ToShortPersonalId(ValidationError):
    __doc__ = _(u"Ogiltig längd. Personnumret måste vara 12 tecken")


class IllegalCheckDigit(ValidationError):
    __doc__ = _(u"Ogiltig checksiffra")


class PersonalIdAlreadyRegistered(ValidationError):
    __doc__ = _(u"Det angivna personnumret finns redan. Om du har angivit ditt eget personnummer och får detta fel, kontakta Heja Sverige")


class TermsNotAccepted(ValidationError):
    __doc__ = _(u'Du måste acceptera allmänna villkor för att kunna registrera ett konto')


def personal_id_check_digit(p):
    a,p=[0,2,4,6,8,1,3,5,7,9],[int(i) for i in p]
    return (10-(a[p[0]]+p[1]+a[p[2]]+p[3]+a[p[4]]+p[5]+a[p[6]]+p[7]+a[p[8]]))%10


def personal_id_already_registered(value):
    portal = getUtility(ISiteRoot)

    mtool = getToolByName(portal, 'portal_membership')
    members = [member for member in mtool.listMembers()
               if member.getProperty('personal_id') == value 
               and member != api.user.get_current()]

    if members:
        return True
    return False

def validateAccept(value):
    if not value:
        raise TermsNotAccepted(value)
    return True

def validatePersonalId(value):
    # check that the personal id conforms to the standard in lenght and that check digit is correct
    if value:
        if len(value) != 12:
            raise ToShortPersonalId(value)
        elif personal_id_check_digit(value[2:]) != int(value[11:]):
            # verify that checkdigit is ok
            raise IllegalCheckDigit(value)
        elif personal_id_already_registered(value):
            raise PersonalIdAlreadyRegistered(value)
    return True

def getCommonTerms():
    #import pdb; pdb.set_trace()
    #context_state = getMultiAdapter((context.context, context.request),
    #                                name=u'plone_context_state')

    #commonterms_actions = None

    #try: # Plone 4+
    #    commonterms_actions = context_state.actions(category="hejasverige.commonterms")
    #except TypeError: # Plone 3
    #    commonterms_actions = context_state.actions().get('hejasverige.commonterms', ())    

    #if not commonterms_actions:
    commonterms_actions = 'dokument/avtal-och-villkor/avtalsvillkor-medlem/allmanna/allmana-villkor-medlem'

    return commonterms_actions

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        #logger.info('Executed getSchema...')
        return IEnhancedUserDataSchema

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    address1 = schema.TextLine(
        title=_(u'label_address1', default=u'Adress 1'),
        description=_(u'help_address1',
                      default=u"Storgatan 1"),
        required=False,
        )

    address2 = schema.TextLine(
        title=_(u'label_address2', default=u'Adress 2'),
        description=_(u'help_address1',
                      default=u""),
        required=False,
        )

    postal_code = schema.TextLine(
        title=_(u'label_postal_code', default=u'Postnummer'),
        description=_(u'help_postal_code',
                      default=u"123 45"),
        required=False,
        )

    city = schema.TextLine(
        title=_(u'label_city', default=u'Ort'),
        description=_(u'help_city',
                      default=u"Storstan"),
        required=False,
        )

    personal_id = schema.TextLine(
        title=_(u'label_personal_id', default=u'Personnummer'),
        description=_(u'help_personal_id',
                      default=u"För att identifiera dig behöver vi ditt personnummer (ÅÅÅÅMMDDNNNN)"),
        required=True,
        constraint=validatePersonalId,
        )

    kollkoll = schema.Bool(
        title=_(u'label_kollkoll', default=u'Hämta köp automatiskt'),
        description=_(u'help_kollkoll',
                      default=u"Markera detta val för att Heja Sverige ska hämta dina korttransaktioner från vanliga köp. För att Heja Sverige ska kunna göra detta behöver du registrera ditt bankkonto."),
        required=False,
        )

    accept = schema.Bool(
        title=_(u'label_accept', default=u'Acceptera användarvillkor'),
        description=_(u'help_accept',
                      default=u"De finns <a id='commonterms' target='_blank' href='" + getCommonTerms() + "'>h&auml;r!</a>"), 
        required=True,
        constraint=validateAccept,
        )
