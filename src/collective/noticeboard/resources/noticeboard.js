/*jslint nomen: true */
(function init(noticeboard, $, _, Backbone) {
    "use strict"; /*global _: true, jQuery: true, Backbone: true, window: true, Mustache: true, TinyMCEConfig: true, InitializedTinyMCEInstances: true, copyDataForSubmit: true  */
    Backbone.emulateHTTP = true;
    noticeboard.init = function (canvas) {
        var Note = Backbone.Model.extend({
            url: function () {
                return this.collection.itemurl + '/' + this.id + '/json';
            }

        }),
            Notes = Backbone.Collection.extend({
                initialize: function () {
                    this.on("updateZIndex", this.updateZIndex);
                    this.on("hide_edit", this.hideEdit);
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
                },
                hideEdit: function () {
                    this.each(function (note) {
                        if (note.get("show_edit")) {
                            note.set({
                                show_edit: 0
                            });
                        }
                    });
                }
            }),
            NoteView = Backbone.View.extend({
                className: "note",
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
                    if (this.model.get("zIndex") !== biggest) {
                        this.model.set({
                            zIndex: biggest + 1
                        });
                        if (Math.random() * 1001 > 1000 || biggest > 1000) {
                            this.model.trigger("updateZIndex");
                        } else {
                            this.model.save();
                        }
                    }

                },
                updateEditBar: function () {
                    this.model.trigger("hide_edit");
                    this.model.set({
                        'show_edit': 1
                    });
                },
                delete1: function () {
                    var model = this.model;
                    this.$el.find(".delete_confirm").show("slide", {
                        direction: "right"
                    }, function () {
                        var $this = $(this);
                        $this.find(".question, .not_confirm").click(function () {
                            model.trigger("hide_edit");
                            return false;
                        });
                        $this.find(".confirm").click(function () {
                            var href = $(this).attr("href");
                            $.get(href, function (reply) {
                                var token = $(reply).find("input[name=_authenticator]").val();
                                $.post(href, {
                                    _authenticator: token,
                                    "form.submitted": 1
                                }, function () {
                                    model.destroy();
                                });
                            });
                        });
                    });
                    return false;
                },
                render: function () {
                    var data = {},
                        model = this.model,
                        color = this.model.get("color"),
                        position_x = this.model.get("position_x"),
                        position_y = this.model.get("position_y"),
                        width = this.model.get("width"),
                        height = this.model.get("height"),
                        template = this.model.collection.note_template,
                        publish_link;
                    if (position_x === "25%" && this.model.collection.anon_new_position !== undefined) {
                        this.model.set({
                            "position_x": this.model.collection.anon_new_position.x,
                            "position_y": this.model.collection.anon_new_position.y
                        });
                        this.model.save();
                        return this;
                    }
                    $.extend(data, this.model.toJSON());
                    this.$el.unbind();

                    this.$el.empty();
                    this.$el.removeClass("ui-resizable");
                    this.$el.removeClass("ui-draggable");
                    this.$el.removeData();
                    this.$el.html(Mustache.render(template, data));
                    this.$el.zIndex(this.model.get("zIndex"));
                    if (this.model.get("show_edit")) {
                        this.$el.find(".actions_first").show();
                    }

                    this.$el.css("top", position_y);
                    this.$el.css("left", position_x);
                    this.$el.css("width", width);
                    this.$el.css("height", height);
                    this.$el.css("position", "absolute");
                    if (this.model.get("old_color")) {
                        this.$el.removeClass(this.model.get("old_color"));
                    }
                    this.$el.addClass(color);
                    this.repair_css();
                    this.fix_links();

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

                    this.$el.find(".change_color a").click(function (event) {
                        var possible_colors = ['yellow',
                                               'blue',
                                               'green',
                                               'pink',
                                               'purple',
                                               'lightblue',
                                               'grey',
                                               'beige'],
                            color = model.get('color'),
                            color_index = possible_colors.indexOf(color),
                            next_color = possible_colors[(color_index + 1) % (possible_colors.length)];
                        event.preventDefault();
                        model.set({
                            old_color: color
                        });
                        model.set({
                            color: next_color
                        });
                        model.save();
                    });
                    this.$el.find(".deletex a").prepOverlay({
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
                            onLoad: function (event) {
                                event.stopPropagation();
                                var config,
                                    tiny;
                                if (window.TinyMCEConfig) {
                                    config = new TinyMCEConfig("text");
                                    config.init();
                                } else {
                                    tiny = event.currentTarget.getOverlay().find(".mce_editable");
                                    config = tiny.data('mce-config');
                                    tiny.tinymce(config);
                                }
                                event.currentTarget.getOverlay().find('.ArchetypesKeywordWidget select').multiSelect();
                                try {
                                    copyDataForSubmit("form-widgets-display_types");
                                } catch (err) {}
                            },
                            onClose: function () {
                                if (window.InitializedTinyMCEInstances) {
                                    delete InitializedTinyMCEInstances.text;
                                }
                            },
                            closeOnClick: false,
                            fixed: true,
                            speed: 'fast'
                        }
                    });
                    publish_link = this.$el.find(".publish");
                    if (this.model.get("review_state") === 'published') {
                        publish_link.hide();
                    } else {
                        this.$el.find(".publish a").click(function (event) {
                            var $this = $(this);
                            event.preventDefault();
                            $.post(this.href, function () {
                                model.set({
                                    review_state: 'published'
                                });
                            });
                        });
                    }
                    this.$el.bind("click.zindex", this.updateZIndex);
                    this.$el.bind("click.edit", this.updateEditBar);
                    this.$el.find(".delete a").click(this.delete1);
                    return this;
                },
                repair_css: function () {
                    var note_height = this.$el.innerHeight(),
                        h3_height = this.$el.find("h3").innerHeight();
                    if (h3_height) {
                        this.$el.find(".notecontent").height((note_height - h3_height) / note_height * 100 + "%");
                    }
                },
                fix_links: function () {
                    this.$el.find(".notecontent a").attr("target", "_blank");
                }
            }),
            App = Backbone.View.extend({
                el: canvas,
                events: {
                    "click": "addAnonymous"
                },
                initialize: function () {
                    var notes = this.notes = new Notes(),
                        update = this.update,
                        config,
                        tiny;
                    this.notes.url = this.$el.data('href');
                    this.notes.itemurl = this.$el.data('hrefitem');
                    this.notes.bind("add", this.addOne, this);
                    this.notes.bind("reset", this.reset, this);
                    this.notes.bind("all", this.render, this);
                    _.bindAll(this);
                    $(".add_note a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form[name=edit_form]',
                        noform: 'close',
                        afterpost: this.update,
                        config: {
                            onLoad: function (event) {
                                if (window.TinyMCEConfig) {
                                    config = new TinyMCEConfig("text");
                                    config.init();
                                } else {
                                    tiny = event.currentTarget.getOverlay().find(".mce_editable");
                                    config = tiny.data('mce-config');
                                    tiny.tinymce(config);
                                }
                                event.currentTarget.getOverlay().find('.ArchetypesKeywordWidget select').multiSelect();
                                try {
                                    copyDataForSubmit("form-widgets-display_types");
                                } catch (err) {}
                            },
                            onClose: function () {
                                if (window.InitializedTinyMCEInstances) {
                                    delete InitializedTinyMCEInstances.text;
                                }
                            },
                            closeOnClick: false,
                            fixed: true,
                            speed: 'fast'
                        }
                    });
                    $("#notesettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*',
                        formselector: 'form',
                        noform: 'reload',
                        config: {
                            onLoad: function (event) {
                                try {
                                    copyDataForSubmit("form-widgets-display_types");
                                } catch (err) {}
                            }
                        }
                    });
                    $("#viewsettings a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*'
                    });
                    $("#notes_archive a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*'
                    });
                    $("#noticeboard-help a").prepOverlay({
                        subtype: 'ajax',
                        filter: '#content>*'
                    });
                    $.get(this.$el.data("notetemplatehref"), function (data) {
                        notes.note_template = data;
                        notes.fetch();
                    });
                },
                addOne: function (note) {
                    var view = new NoteView({
                        model: note
                    });
                    this.$el.append(view.render().el);
                    view.repair_css();
                },
                addAnonymous: function (event) {
                    if (event.target.id !== 'noticeboardcanvas') {
                        return true;
                    }
                    if ($(event.target).data("addanonymous") !== "True") {
                        $(".actions_first:visible").hide();
                        return true;
                    }
                    var add_link = $(".add_note a").attr("href"),
                        update = this.update,
                        pos_x = event.pageX,
                        pos_y = event.pageY,
                        notes = this.notes;
                    notes.anon_new_position = {
                        x: event.pageX,
                        y: event.pageY
                    };
                    $.get(add_link, function (response) {
                        var edit_form = $(response).find("form[name=edit_form]");
                        edit_form.find("input[name=title]").val($(".anonymoustitle").text());
                        $.get(edit_form.attr("action") + "?" + edit_form.serialize(), function () {
                            update();
                        });
                    });
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
