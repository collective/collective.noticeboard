/*jslint nomen: true */
(function init(noticeboard, $, _, Backbone) {
    "use strict"; /*global _: true, jQuery: true, Backbone: true, window: true, Mustache: true */
    Backbone.emulateHTTP = true;
    noticeboard.init = function (canvas, template) {
        var Note = Backbone.Model.extend({
                url: function(){
                    return this.collection.itemurl + '/' + this.id + '/json';
                }

        }),
            Notes = Backbone.Collection.extend({
                model: Note

            }),
            NoteView = Backbone.View.extend({
                events: {
                    //                    "startmove": "startmove",
                    //                    "stopmove": "stopmove",
                },
                className: "note",
                template: Mustache.compile(template.html()),
                initialize: function () {
                    this.model.bind("change", this.render, this);
                    this.model.bind("destroy", this.remove, this);
                },
                update: function(){
                    this.model.fetch();
                },
                remove: function(){
                    this.$el.remove();
                },
                render: function () {
                    console.log("render" + this.cid);
                    var data = {},
                        model = this.model;
                    $.extend(data, this.model.toJSON());
                    var position_x = this.model.get("position_x");
                    var position_y = this.model.get("position_y");
                    var width = this.model.get("width");
                    var height = this.model.get("height");

                    this.$el.empty();
                    this.$el.removeClass("ui-resizable");
                    this.$el.removeClass("ui-draggable");
                    this.$el.removeData();
                    this.$el.html(this.template(data));
                    this.$el.css("top", position_y);
                    this.$el.css("left", position_x);
                    this.$el.css("width", width);
                    this.$el.css("height", height);
                    this.$el.css("position", "absolute");



                    this.$el.draggable({
                        handle: "h3",
                        stop: function (object, event) {
                            console.log(event.position.left);
                            console.log(event.position.top);
                            model.set({
                                position_x: event.position.left,
                                position_y: event.position.top
                            }, {
                                silent: true
                            });
                            model.save();
                        }
                    });
                    this.$el.data('draggable').position = this.$el.data('draggable').offset = {
                        top: position_y,
                        left: position_y
                    };
                    this.$el.resizable({
                        stop: function (object, event) {
                            model.set({
                                width: event.size.width,
                                height: event.size.height
                            }, {
                                silent: true
                            });
                            model.save();
                        }
                    });
                    this.$el.find(".delete a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        noform: 'close',
                        formselector: 'form#delete_confirmation',
                        afterpost: _.bind(this.remove, this)
                    });
                    this.$el.find(".edit a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form[name=edit_form]',
                        noform: 'close',
                        afterpost: _.bind(this.update, this)
                    });

                    return this;
                }
            }),
            App = Backbone.View.extend({
                el: canvas,
                events: {
                    //                    "mousedown": "down"
                },
                initialize: function () {
                    var notes = this.notes = new Notes();
                    this.notes.url = this.$el.data('href');
                    this.notes.itemurl = this.$el.data('hrefitem');
                    this.notes.bind("add", this.addOne, this);
                    this.notes.bind("reset", this.reset, this);
                    this.notes.bind("all", this.render, this);
                    _.bindAll(this);
                    this.notes.fetch();
                    $("#add a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form[name=edit_form]',
                        noform: 'close',
                        afterpost: this.update
                    });
                    $("#notesettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form',
                        noform: 'close'
                    });
                    $("#viewsettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                    });
                },
                addOne: function (note) {
                    var view = new NoteView({
                        model: note
                    });
                    console.log(note.cid);
                    this.$el.append(view.render().el);
                },
                reset: function () {
                    this.$el.empty();
                    this.notes.each(this.addOne, this);
                },
                update: function(){
                    this.notes.fetch();
                }
            }),
            app = new App();
    };

}(window.noticeboard = window.noticeboard || {}, jQuery, _, Backbone));