"""
Generic Object-Level Actions for Django Admin

This module provides a reusable way to add object-level actions to Django admin change forms.

Usage:
    from app.object_actions import ObjectActionsMixin, object_action

    class MyModelAdmin(ObjectActionsMixin, admin.ModelAdmin):
        object_actions = ['publish', 'archive']

        @object_action(label='Publish', css_class='default')
        def publish(self, request, obj):
            obj.status = 'published'
            obj.save()
            self.message_user(request, f'{obj} published successfully!')

        @object_action(label='Archive', css_class='deletelink')
        def archive(self, request, obj):
            obj.is_archived = True
            obj.save()
            self.message_user(request, f'{obj} archived!')
"""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html


def object_action(label=None, css_class="default", confirm=None):
    """
    Decorator to mark a method as an object-level action.

    Args:
        label: The text to display on the button (defaults to method name)
        css_class: CSS class for styling. Options:
            - 'default': Default button style
            - 'addlink': Green add button style
            - 'changelink': Blue change button style
            - 'deletelink': Red delete button style
            - 'historylink': Gray history button style
        confirm: Optional confirmation message to show before executing
    """

    def decorator(func):
        func.is_object_action = True
        func.action_label = label or func.__name__.replace("_", " ").title()
        func.action_css_class = css_class
        func.action_confirm = confirm
        return func

    return decorator


class ObjectActionsMixin:
    """
    Mixin to add object-level actions to Django admin change forms.

    Add this mixin to your ModelAdmin class and define object_actions list.
    """

    object_actions = []
    change_form_template = "admin/object_actions_change_form.html"

    def get_object_actions(self, request, obj):
        """
        Get list of available object actions for this object.
        Override this method to conditionally show/hide actions.
        """
        actions = []
        for action_name in self.object_actions:
            method = getattr(self, action_name, None)
            if method and hasattr(method, "is_object_action"):
                actions.append(
                    {
                        "name": action_name,
                        "label": method.action_label,
                        "css_class": method.action_css_class,
                        "confirm": method.action_confirm,
                    }
                )
        return actions

    def get_urls(self):
        """Add custom URLs for each object action."""
        urls = super().get_urls()
        custom_urls = []

        for action_name in self.object_actions:
            custom_urls.append(
                path(
                    f"<path:object_id>/{action_name}/",
                    self.admin_site.admin_view(self._object_action_view),
                    name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_{action_name}",
                    kwargs={"action_name": action_name},
                ),
            )

        return custom_urls + urls

    def _object_action_view(self, request, object_id, action_name):
        """Generic view to handle object action execution."""
        obj = self.get_object(request, object_id)
        method = getattr(self, action_name, None)

        if not method or not hasattr(method, "is_object_action"):
            self.message_user(
                request, f'Action "{action_name}" not found.', level=messages.ERROR
            )
            return redirect(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                object_id,
            )

        # Execute the action
        result = method(request, obj)

        # If method returns a response, use it; otherwise redirect back
        if result:
            return result

        return redirect(
            "admin:%s_%s_change"
            % (self.model._meta.app_label, self.model._meta.model_name),
            object_id,
        )

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """Add object actions to the context."""
        extra_context = extra_context or {}

        if object_id:
            obj = self.get_object(request, object_id)
            if obj:
                extra_context["object_actions"] = self.get_object_actions(request, obj)

        return super().changeform_view(request, object_id, form_url, extra_context)
