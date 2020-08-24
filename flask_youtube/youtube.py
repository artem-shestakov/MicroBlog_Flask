from flask import Blueprint, Markup, render_template


class Video(object):
    def __init__(self, video_id, cls="youtube"):
        self.video_id = video_id
        self.cls = cls

    @property
    def html(self):
        return Markup("<iframe "
                      "id = 'ytplayer'"
                      "type = 'text/html'"
                      "width = '640'"
                      "height = '360'"
                      f"src = 'http://www.youtube.com/embed/{self.video_id}'"
                      "frameborder = '0'>"
                      "</iframe>")


def youtube(*args, **kwargs):
    video = Video(*args, **kwargs)
    return video.html


class YouTube(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_template_global(youtube)
