#!/usr/bin/python
# -*- coding: utf-8 -*-
from plone.app.z3cform.layout import wrap_form
from plone.z3cform.fieldsets import group as plonegroup
from z3c.form import form, field, group, button
from zope.interface import Interface
import zope.i18n

from collective.noticeboard import _
from collective.noticeboard.interfaces import INoticeboardSettings
from collective.noticeboard.settings import NoticeboardSettings


class INothing(Interface):

    pass


class MainSettingsGroup(plonegroup.Group):

    fields = field.Fields(INoticeboardSettings)
    label = _(u'Main')


class NoticeBoardSettingsForm(group.GroupForm, form.EditForm):
    """ The page that holds all the noticeboard settings
    """

    fields = field.Fields(INothing)
    groups = [MainSettingsGroup]

    label = _(u'heading_noticeboard_settings_form',
              default=u'Noticeboard')
    description = _(u'description_noticeboard_settings_form',
                    default=u'Configure the settings of this noticeboard.')
    successMessage = _(u'successMessage_noticeboard_settings_form',
                       default=u'Noticeboard settings saved.')
    noChangesMessage = _(u'noChangesMessage_noticeboard_settings_form',
                 default=u'There are no changes in the Noticeboard settings.')

    def add_fields_to_group(self, type_, groupname):
        group = None
        for g in self.groups:
            if groupname == g.label:
                group = g

        if group is None:
            g = plonegroup.GroupFactory(groupname,
                                        field.Fields(type_.schema))
            self.groups.append(g)
        else:
            fields = field.Fields(type_.schema)
            toadd = []
            for f in fields._data_values:
                if f.__name__ not in group.fields.keys():
                    toadd.append(f)

            group.fields = field.Fields(group.fields, *toadd)

    def update(self):
        super(NoticeBoardSettingsForm, self).update()

    def set_status_message(self, settings, has_changes):
        msg = has_changes and self.successMessage \
            or self.noChangesMessage
        msg = zope.i18n.translate(msg)

        self.status = msg

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        settings = NoticeboardSettings(self.context)

        has_changes = False
        if changes:
            settings = NoticeboardSettings(self.context)
            has_changes = True

        self.set_status_message(settings, has_changes)
        return self.request.response.redirect(self.context.absolute_url())


NoticeboardSettingsView = wrap_form(NoticeBoardSettingsForm)
