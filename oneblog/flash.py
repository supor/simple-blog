# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

@author: Nob
'''
from flask import flash as _flash, get_flashed_messages


class Flash(object):

    def __call__(self, errors, category):
        if not isinstance(errors, list):
            errors = [errors]
        for msg in errors:
            _flash(msg, category)

    def render(self):
        messages = get_flashed_messages(with_categories=True)
        if messages:
            html = '<div class="notifications">\n'
            for category, message in messages:
                html += '<p class="%s">%s</p>\n' % (category, message)
            html += '</div>'
            return html
        return ''

    __html__ = render


flash = Flash()
