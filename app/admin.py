from django.contrib import admin
from .models import *
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.


class SkillInlines(admin.TabularInline):
    model = Skill


class RequirmentInlines(admin.TabularInline):
    model = Requirment


class SectionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class VideoAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    autocomplete_fields = ["section"]


class VideoInlines(admin.TabularInline):
    model = Video
    fk_name = "course"
    # to modify extra

    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        return extra


class CheckoutItemInlines(admin.TabularInline):
    model = CheckoutItem


class CheckoutAdmin(admin.ModelAdmin):
    inlines = [CheckoutItemInlines]


class AdminMixins:

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class CourseAdmin(admin.ModelAdmin):
    inlines = (SkillInlines, RequirmentInlines, VideoInlines)
    list_display = [
        "upper_case_title",
        "author",
        "total_price",
        "rating",
        "status",
    ]
    search_fields = ["title"]
    view_on_site = False
    # list_display_links = None

    # make fields editable
    # list_editable=['status']

    # to display fields inside object
    # fields=('title','price')

    # to add action methods
    actions = ["make_draft", "make_published"]

    ordering = ("-date_created",)
    # to filter products with date
    date_hierarchy = "date_created"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields["price"].disabled = True
            form.base_fields["title"].disabled = True
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(status="DRAFT")

    """
    make function to return object title with upper

    """

    @admin.display(description="title")
    def upper_case_title(self, obj):
        return obj.title.upper()

    """
    make function to return total price after dicount

    """

    @admin.display
    def total_price(self, obj):
        if obj.discount:
            return obj.get_total
        return obj.price

    @admin.display
    def rating(self, obj):
        return obj.get_rating

    @admin.action(description="Mark selected courses as draft")
    def make_draft(self, request, queryset):
        updated = queryset.update(status="DRAFT")
        self.message_user(
            request,
            ngettext(
                "%d course was successfully marked as DRAFT.",
                "%d courses were successfully marked as DRAFT.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected courses as publish")
    def make_published(self, request, queryset):
        updated = queryset.update(status="PUBLISH")
        self.message_user(
            request,
            ngettext(
                "%d course was successfully marked as PUBLISH",
                "%d courses were successfully marked as PUBLISH",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
admin.site.register(Skill)
admin.site.register(Requirment)
admin.site.register(Section, SectionAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Language)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(CheckoutItem)
admin.site.register(ShopCart)
admin.site.register(CommentCourse)
admin.site.register(CommentVideo)
admin.site.register(Question)
