/*jslint nomen: true */
(function init(noticeboard, $, _, Backbone) {
    "use strict"; /*global _: true, jQuery: true, Backbone: true, window: true, Mustache: true */
    noticeboard.init = function (canvas, template) {
        var Note = Backbone.Model.extend({

        }),
            Notes = Backbone.Collection.extend({
                model: Note

            }),
            NoteView = Backbone.View.extend({
                events: {
                    "startmove": "startmove",
                    "stopmove": "stopmove",
                },
                template: Mustache.compile(template.html()),
                initialize: function () {
                    this.model.bind("change", this.render, this);
                    this.model.bind("destroy", this.remove, this);
                    _.bindAll(this);
                    $("#add a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form'
                    });
                    $("#notesettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form'
                    });
                    $("#viewsettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form'
                    });
                },
                render: function () {
                    var data = {
                        text: "No text"
                    };
                    $.extend(data, this.model.toJSON());
                    if (data.image_url) {
                        data.image_url = '<img src="' + data.image_url + '" />';
                    }
                    data.css = "position: absolute; left:" + this.model.get("position_x") + "px ;top:" + this.model.get("position_y") + "px;";
                    this.$el.html(this.template(data));
                    return this;
                },
                startmove: function (e) {
                    this.before_x = e.clientX;
                    this.before_y = e.clientY;
                    $(window).bind("mousemove", this.move);
                    $(window).bind("mouseup", this.stopmove);
                },
                stopmove: function (e) {
                    $(window).unbind("mousemove", this.move);
                    $(window).unbind("mouseup", this.stopmove);
                    this.model.save();
                },
                move: function (e) {
                    var delta_x = e.clientX - this.before_x,
                        delta_y = e.clientY - this.before_y;
                    this.before_x = e.clientX;
                    this.before_y = e.clientY;
                    this.model.set({
                        position_x: this.model.get("position_x") + delta_x,
                        position_y: this.model.get("position_y") + delta_y
                    });
                }

            }),
            App = Backbone.View.extend({
                el: canvas,
                events: {
                    "mousedown": "down"
                },
                initialize: function () {
                    this.notes = new Notes();
                    this.notes.url = this.$el.data('href');
                    this.notes.bind("add", this.addOne, this);
                    this.notes.bind("reset", this.addAll, this);
                    this.notes.bind("all", this.render, this);
                    this.notes.fetch();
                },
                addOne: function (note) {
                    var view = new NoteView({
                        model: note
                    });
                    this.$el.append(view.render().el);
                },
                addAll: function () {
                    this.notes.each(this.addOne, this);
                },
                down: function (e) {
                    var evt = $.Event("startmove");
                    evt.clientX = e.clientX;
                    evt.clientY = e.clientY;
                    $(e.target).trigger(evt);
                    return false;
                }
            }),
            app = new App();
    };

}(window.noticeboard = window.noticeboard || {}, jQuery, _, Backbone));