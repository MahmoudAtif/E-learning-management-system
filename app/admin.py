from django.contrib import admin
from django.forms import Textarea
from .models import *
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.admin import SimpleListFilter
from .object_actions import ObjectActionsMixin, object_action

# Register your models here.


class PriceFilter(SimpleListFilter):
    title = "price"
    parameter_name = "price"
    template = "admin/price_filter.html"

    def lookups(self, request, model_admin):
        # Return a dummy tuple to make the filter appear
        return (("", ""),)

    def queryset(self, request, queryset):
        if self.value():
            try:
                price_value = int(self.value())
                return queryset.filter(price=price_value)
            except ValueError:
                return queryset
        return queryset


class AuthorFilter(SimpleListFilter):
    title = "author"
    parameter_name = "author"
    template = "admin/author_filter.html"

    def lookups(self, request, model_admin):
        # Return all authors
        authors = Author.objects.all()
        return [(author.id, author.name) for author in authors]

    def queryset(self, request, queryset):
        # Handle multiple author IDs separated by commas
        if self.value():
            author_ids = self.value().split(",")
            return queryset.filter(author__id__in=author_ids)
        return queryset


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


class CourseAdmin(ObjectActionsMixin, admin.ModelAdmin):
    inlines = (SkillInlines, RequirmentInlines, VideoInlines)
    list_display = [
        # "upper_case_title",
        "title",
        "author",
        "total_price",
        "rating",
        "status",
        "ceritficated",
    ]
    # filter_horizontal = ["author"]
    # sortable_by = ("title", "total_price", "status")
    search_fields = ["title"]
    # raw_id_fields = ("author",)
    autocomplete_fields = ("author",)
    # view_on_site = False
    prepopulated_fields = {"slug": ["title"]}
    list_filter = ["certificate", "language", PriceFilter]
    # list_display_links = None
    formfield_overrides = {
        "description": {"widget": Textarea(attrs={"rows": 2, "cols": 20})},
    }

    # Define object-level actions
    object_actions = ["publish_course", "make_draft_course"]

    # make fields editable
    # list_editable = ["status"]

    # to display fields inside object
    # fields=('title','price')

    # to add action methods
    actions = ["make_draft", "make_published"]

    ordering = ("-date_created",)
    # to filter products with date
    date_hierarchy = "date_created"

    def get_readonly_fields(self, request, obj=None, *args, **kwargs):
        read_only_fileds = list(super().get_readonly_fields(request, obj))
        is_superuser = request.user.is_superuser
        if not is_superuser:
            read_only_fileds.extend(["price"])
        return read_only_fileds

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(status="DRAFT")

    @object_action(
        label="Publish Course",
        confirm="Are you sure you want to make this course a publish?",
    )
    def publish_course(self, request, obj):
        """Publish the course"""
        obj.status = "PUBLISH"
        obj.save()
        self.message_user(
            request,
            f"Course '{obj.title}' has been published successfully.",
            messages.SUCCESS,
        )

    @object_action(
        label="Make Draft",
        css_class="deletelink",
        confirm="Are you sure you want to make this course a draft?",
    )
    def make_draft_course(self, request, obj):
        """Make the course a draft"""
        obj.status = "DRAFT"
        obj.save()
        self.message_user(
            request, f"Course '{obj.title}' has been moved to draft.", messages.WARNING
        )

    @admin.display(description="title")
    def upper_case_title(self, obj):
        """
        make function to return object title with upper

        """
        return obj.title.upper()

    @admin.display
    def total_price(self, obj):
        """
        make function to return total price after dicount

        """
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
                f"{updated} course was successfully marked as DRAFT.",
                f"{updated} courses were successfully marked as DRAFT.",
                updated,
            ),
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

    @admin.display(description="Ceritficated", boolean=True, ordering="certificate")
    def ceritficated(self, obj):
        return obj.certificate == "Yes" or False


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
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
