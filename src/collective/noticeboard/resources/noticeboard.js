/*jslint nomen: true */
(function init(noticeboard, $, _, Backbone) {
    "use strict"; /*global _: true, jQuery: true, Backbone: true, window: true, Mustache: true, TinyMCEConfig: true, InitializedTinyMCEInstances: true  */
    Backbone.emulateHTTP = true;
    noticeboard.init = function (canvas, template) {
        var Note = Backbone.Model.extend({
            url: function () {
                return this.collection.itemurl + '/' + this.id + '/json';
            }

        }),
            Notes = Backbone.Collection.extend({
                initialize: function () {
                    this.on("updateZIndex", this.updateZIndex);
                },
                model: Note,
                updateZIndex: function () {
                    _.each(_.sortBy(this.models, function (note) {
                        return note.get("zIndex");
                    }), function (note, index) {
                        note.set({
                            zIndex: index
                        });
                        note.save();
                    });
                }
            }),
            NoteView = Backbone.View.extend({
                className: "note",
                template: Mustache.compile(template.html()),
                initialize: function () {
                    this.model.bind("change", this.render, this);
                    this.model.bind("destroy", this.remove, this);
                    _.bindAll(this);
                },
                update: function () {
                    this.model.fetch();
                },
                remove: function () {
                    this.$el.remove();
                },
                updateZIndex: function () {
                    var biggest = _.reduce($(".note"), function (a, b) {
                        return Math.max($(b).zIndex(), a);
                    }, 0);
                    console.log(biggest);
                    if(this.model.get("zIndex") !== biggest) {
                        this.model.set({
                            zIndex: biggest + 1
                        });
                        if(Math.random() * 1001 > 1000 || biggest > 30) {
                            this.model.trigger("updateZIndex");
                        } else {
                            this.model.save();
                        }
                    }

                },
                render: function () {
                    var data = {},
                        model = this.model,
                        color = this.model.get("color"),
                        position_x = this.model.get("position_x"),
                        position_y = this.model.get("position_y"),
                        width = this.model.get("width"),
                        height = this.model.get("height");
                    $.extend(data, this.model.toJSON());
                    this.$el.unbind();

                    this.$el.empty();
                    this.$el.removeClass("ui-resizable");
                    this.$el.removeClass("ui-draggable");
                    this.$el.removeData();
                    this.$el.html(this.template(data));
                    this.$el.zIndex(this.model.get("zIndex"));

                    this.$el.css("top", position_y);
                    this.$el.css("left", position_x);
                    this.$el.css("width", width);
                    this.$el.css("height", height);
                    this.$el.css("position", "absolute");
                    this.$el.addClass(color);



                    this.$el.draggable({
                        handle: "h3",
                        containment: "window",
                        cursor: "move",
                        stack: ".note",
                        stop: function (object, event) {
                            model.set({
                                position_x: event.position.left,
                                position_y: event.position.top,
                                zIndex: event.helper.zIndex()
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
                        minHeight: 150,
                        minWidth: 100,
                        autoHide: true,
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
                        afterpost: _.bind(this.update, this),
                        config: {
                            onLoad: function () {
                                var config = new TinyMCEConfig("text");
                                config.init();
                            },
                            onClose: function () {
                                delete InitializedTinyMCEInstances.text;
                            }
                        }
                    });
                    this.$el.bind("click.zindex", this.updateZIndex);
                    return this;
                }
            }),
            App = Backbone.View.extend({
                el: canvas,
                events: {
                    //                    "mousedown": "down"
                },
                initialize: function () {
                    var notes = this.notes = new Notes(),
                        update = this.update;
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
                        afterpost: this.update,
                        config: {
                            onLoad: function () {
                                var config = new TinyMCEConfig("text");
                                config.init();
                            },
                            onClose: function () {
                                delete InitializedTinyMCEInstances.text;
                            }
                        }
                    });
                    $("#notesettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form',
                        noform: 'close'
                    });
                    $("#viewsettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*'
                    });
                },
                addOne: function (note) {
                    var view = new NoteView({
                        model: note
                    });
                    this.$el.append(view.render().el);
                },
                reset: function () {
                    this.$el.empty();
                    this.notes.each(this.addOne, this);
                },
                update: function () {
                    this.notes.fetch();
                }
            }),
            app = new App();
    };

}(window.noticeboard = window.noticeboard || {}, jQuery, _, Backbone));