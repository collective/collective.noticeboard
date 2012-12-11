collective.noticeboard
======================

A fancy noticeboard.

collective.noticeboard transforms folders or collections into a fancy noticeboard where users can add and modify notes.
Notes display the content of a content-type (by default a News Item) and are editable in overlays. They are draggable, resizeable and can change color.

In the configuration you can:

 - select the default type used for notes
 - select types that should be displayed
 - enable adding notes by clicking on the canvas
 - enable auto-publishing of notes
 - select if notes should be hidden after a number of days after the last change
 - display a link to a help-page

Items that are excluded from navigation are not shown on the noticeboard (e.g. you might want to exclude the help-page)

collective.noticeboard works with Archetypes and Dexterity.


Installation
------------
Add this line in the eggs section of your buildout.cfg

eggs=
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

Written by:

[Starzel.de](http://www.starzel.de)

Sponsored by:

[DIPF](http://www.dipf.de)


Contributors
------------

[Philip Bauer](bauer@starzel.de)
[Patrick Gerken](gerken@starzel.de)

