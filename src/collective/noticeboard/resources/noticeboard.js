/*jslint nomen: true */
(function init(noticeboard, $, _, Backbone) {
    "use strict"; /*global _: true, jQuery: true, Backbone: true, window: true */
    noticeboard.init = function (canvas, template) {
        var Note = Backbone.Model.extend({

        }),
            Notes = Backbone.Collection.extend({
                model: Note

            }),
            NoteView = Backbone.View.extend({
                events: {},
                template: Mustache.compile(template.html()),
                initialize: function () {
                    this.model.bind("change", this.render, this);
                    this.model.bind("destroy", this.remove, this);
                },
                render: function () {
                    var data = {
                        text: "No text"
                    };
                    $.extend(data, this.model.toJSON());
                    if(data.image_url){
                        data.image_url = '<img src="' + data.image_url + '" />'
                    }
                    data.css = "position: absolute; left:" + this.model.get("position_x") + "px ;top:" + this.model.get("position_y") + "px;"
                    this.$el.html(this.template(data));
                    return this;
                }

            }),
            App = Backbone.View.extend({
                el: canvas,
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
                }
            }),
            app = new App();
    };

}(window.noticeboard = window.noticeboard || {}, jQuery, _, Backbone));