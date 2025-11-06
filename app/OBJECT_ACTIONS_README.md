# Object-Level Actions for Django Admin

A generic, reusable system for adding custom action buttons to Django admin change forms.

## Quick Start

### 1. Import the required components

```python
from app.object_actions import ObjectActionsMixin, object_action
```

### 2. Add the mixin to your ModelAdmin

```python
class MyModelAdmin(ObjectActionsMixin, admin.ModelAdmin):
    # ... your existing configuration ...
    pass
```

### 3. Define your object actions

```python
class MyModelAdmin(ObjectActionsMixin, admin.ModelAdmin):
    # List the action method names
    object_actions = ['publish', 'archive']

    @object_action(label='Publish', css_class='addlink')
    def publish(self, request, obj):
        """Publish this object"""
        obj.status = 'published'
        obj.save()
        self.message_user(request, f'{obj} published successfully!')

    @object_action(
        label='Archive',
        css_class='deletelink',
        confirm='Are you sure you want to archive this?'
    )
    def archive(self, request, obj):
        """Archive this object"""
        obj.is_archived = True
        obj.save()
        self.message_user(request, f'{obj} archived!')
```

## Decorator Options

The `@object_action` decorator accepts the following parameters:

### `label` (str, optional)
The text to display on the button. Defaults to the method name with underscores replaced by spaces and title-cased.

```python
@object_action(label='Custom Button Text')
def my_action(self, request, obj):
    pass
```

### `css_class` (str, optional)
CSS class for button styling. Available options:
- `'default'`: Default gray button (default)
- `'addlink'`: Green button (for positive actions like publish, approve)
- `'changelink'`: Blue button (for neutral actions like edit, update)
- `'deletelink'`: Red button (for destructive actions like delete, archive)
- `'historylink'`: Gray button (for history-related actions)

```python
@object_action(label='Delete', css_class='deletelink')
def delete_action(self, request, obj):
    pass
```

### `confirm` (str, optional)
If provided, shows a JavaScript confirmation dialog before executing the action.

```python
@object_action(
    label='Delete Forever',
    css_class='deletelink',
    confirm='This action cannot be undone. Are you sure?'
)
def hard_delete(self, request, obj):
    pass
```

## Action Method Signature

Your action methods must follow this signature:

```python
def action_name(self, request, obj):
    """
    Args:
        request: The HttpRequest object
        obj: The model instance being acted upon

    Returns:
        Optional: HttpResponse to redirect/render, or None to redirect back to change form
    """
    # Your action logic here
    obj.do_something()
    obj.save()

    # Show message to user
    self.message_user(request, 'Action completed!')

    # Optional: return a custom response
    # return redirect('some-url')
```

## Advanced Usage

### Conditional Actions

Override `get_object_actions()` to conditionally show/hide actions:

```python
class MyModelAdmin(ObjectActionsMixin, admin.ModelAdmin):
    object_actions = ['publish', 'unpublish']

    def get_object_actions(self, request, obj):
        """Only show relevant actions based on object state"""
        actions = super().get_object_actions(request, obj)

        # Filter actions based on object state
        if obj.status == 'published':
            return [a for a in actions if a['name'] == 'unpublish']
        else:
            return [a for a in actions if a['name'] == 'publish']
```

### Custom Response

Return a custom HttpResponse to control what happens after the action:

```python
from django.shortcuts import redirect

@object_action(label='View Report')
def view_report(self, request, obj):
    """Generate and view a report"""
    report = obj.generate_report()
    # Redirect to a custom view
    return redirect('report-view', report_id=report.id)
```

### Permission Checks

Add permission checks within your action methods:

```python
@object_action(label='Approve', css_class='addlink')
def approve(self, request, obj):
    """Approve this item (requires staff permission)"""
    if not request.user.is_staff:
        self.message_user(
            request,
            'You do not have permission to approve.',
            level=messages.ERROR
        )
        return

    obj.approved = True
    obj.save()
    self.message_user(request, 'Approved successfully!')
```

## Complete Example

```python
from django.contrib import admin
from app.object_actions import ObjectActionsMixin, object_action
from django.contrib import messages

class CourseAdmin(ObjectActionsMixin, admin.ModelAdmin):
    list_display = ['title', 'status', 'author']
    object_actions = ['publish', 'archive', 'duplicate']

    @object_action(label='Publish Course', css_class='addlink')
    def publish(self, request, obj):
        """Publish the course"""
        obj.status = 'published'
        obj.published_date = timezone.now()
        obj.save()
        self.message_user(
            request,
            f'Course "{obj.title}" has been published!',
            messages.SUCCESS
        )

    @object_action(
        label='Archive Course',
        css_class='deletelink',
        confirm='Are you sure you want to archive this course?'
    )
    def archive(self, request, obj):
        """Archive the course"""
        obj.status = 'archived'
        obj.save()
        self.message_user(
            request,
            f'Course "{obj.title}" has been archived.',
            messages.WARNING
        )

    @object_action(label='Duplicate', css_class='changelink')
    def duplicate(self, request, obj):
        """Create a duplicate of this course"""
        new_course = Course.objects.create(
            title=f"{obj.title} (Copy)",
            description=obj.description,
            author=obj.author,
            status='draft'
        )
        self.message_user(
            request,
            f'Created duplicate: {new_course.title}',
            messages.SUCCESS
        )
        # Redirect to the new course
        return redirect('admin:app_course_change', new_course.id)

admin.site.register(Course, CourseAdmin)
```

## Benefits

1. **Easy to Use**: Just add the mixin and decorate your methods
2. **Reusable**: Write once, use across all your admin classes
3. **Consistent**: All actions appear in the same location (top-right toolbar)
4. **Flexible**: Support for custom styling, confirmations, and responses
5. **Maintainable**: Centralized logic in one place
