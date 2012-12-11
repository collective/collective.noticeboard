collective.noticeboard
======================

A fancy noticeboard for Plone inspired by corkboard.me

This Plone-Addon allow suser to transform folders or collections into a fancy noticeboard where users can add and modify postit-like notes.
Notes display the content of a content-type (by default News Items) and are editable in overlays.
Notes are draggable, resizeable and can change color.

In the configuration you can:

- select the default type used for notes
- select types that should be displayed
- enable adding notes by clicking on the canvas
- enable auto-publishing of notes
- select if notes should be hidden when the were not updated for a number of days
- display a link to a help-page

Items that were excluded from the navigation are not shown on the noticeboard (you might want to exclude the help-page).

collective.noticeboard works with Archetypes and Dexterity.


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

Editing in overlays works with the version of Products.TinyMCE shipped with Plone 4.x as well as with the latest version compatible with IE9 (>= 1.3b7)


Credits
-------

Written by Starzel.de - http://www.starzel.de

Sponsored by DIPF - http://www.dipf.de


Contributors
------------

- Philip Bauer
- Patrick Gerken
