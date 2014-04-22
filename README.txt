collective.noticeboard
======================

A fancy noticeboard for Plone inspired by corkboard.me

This Plone-Addon allow suser to transform folders or collections into a fancy noticeboard where users can add and modify postit-like notes.
Notes display the content of a content-type (by default News Items) and are editable in overlays.
Notes are draggable, resizeable and can change color.

collective.noticeboard works with Archetypes and Dexterity. By default it displays

- Title
- Description
- Image (if one exists)
- Author
- Modification-Date

In the configuration you can:

- select the default type used for notes
- select types that should be displayed
- enable adding notes by clicking on the canvas
- enable auto-publishing of notes
- select if notes should be hidden when the were not updated for a certain number of days
- display a link to a help-page (with the id 'noticeboard-help')

Items that were excluded from the navigation are not shown on the noticeboard (you might want to exclude the help-page).

.. warning::

    In Plone, one needs delete permission on an object AND its parent folder
    to delete an item. Most often, a user has the edit permission on
    containing folders, so that does not matter.

    On a noticeboard though, it makes sense that users are only allowed to
    add notes and not to modify the noticeboard itself.

    To allow deletion of content, our delete functionality only checks for the
    delete permission on the object itself and not on the folder.

    This should not create any trouble for you, but we note it here because
    it is a small deviation from Plones default behavior.


Installation
------------

Add this line in the eggs section of your buildout.cfg::

    eggs =
        ...
        collective.noticeboard


Dependencies
------------

- collective.js.jqueryui
- collective.js.backbone
- collective.js.underscore

Take care to choose the right version of collective.js.jqueryui. They offer different versions for each minor Plone Release, so we cannot suggest minimum versions.

To get collective.noticeboard working on Plone 4.3.x you need at least ``collective.js.jqueryui = 1.10.3`` which is not pinned by Plone 4.3.2.

Noticeboard breaks with underscore 1.5.0, so we declared ``collective.js.underscore < 1.5.0`` as a dependency in setup.py.

Editing in overlays should work with the differnt version of Products.TinyMCE shipped with Plone 4.1, 4.2 and 4.3.



Credits
-------

Written by Starzel.de - http://www.starzel.de

Sponsored by DIPF - http://www.dipf.de


Contributors
------------

- Philip Bauer
- Patrick Gerken
