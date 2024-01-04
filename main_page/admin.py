from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import F

from .models import Searchresults, Suggestedterms, Suggestedcategories, Suggestedtranslatedterms, Basicterms, \
    Categories, Translatedterms, Participants, Numtoanswer, Languageswithcountries
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resources import SearchResultsResource, NumToAnswersResource, TranslatedTermsResource, \
    SuggestedtranslatedtermsResource
from .views import FAQ


class ParticipantsAdmin(UserAdmin):
    readonly_fields = ['username', 'profile_avatar', 'first_name', 'last_name', 'email', 'usertype', 'age',
                       'langcountryid', 'proficiencylevel', 'academiclevel', 'scienceeducationlevel',
                       'trainedcategories', 'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
                       'last_login']

    list_display = [field.name for field in Participants._meta.fields if
                    field.name != 'profile_avatar' and field.name != 'password' and field.name != 'id']

    langcountryid_index = list_display.index('langcountryid')
    list_display = list_display[:langcountryid_index] + ['language', 'country'] + list_display[langcountryid_index + 1:]

    list_display_links = None

    list_filter = ('is_active', 'is_staff')

    actions = ['change_to_admin', 'change_to_superuser', 'remove_admin_from_user']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']

        if not request.user.is_superuser:
            # Actions for non-superusers
            actions = []

        return actions

    @admin.action(description="Change selected to admin users")
    def change_to_admin(self, request, queryset):
        queryset.filter(is_staff=False).update(is_staff=True)
        queryset.update(usertype='admin')

    @admin.action(description="Change selected to admin super users")
    def change_to_superuser(self, request, queryset):
        queryset.filter(is_staff=False).update(is_staff=True)
        queryset.filter(is_superuser=False).update(is_superuser=True)
        queryset.update(usertype='admin')

    @admin.action(description="Change selected to registered users from admin")
    def remove_admin_from_user(self, request, queryset):
        queryset.filter(is_staff=True).update(is_staff=False)
        queryset.filter(is_superuser=True).update(is_superuser=False)
        queryset.update(usertype='registered')

    def language(self, obj):
        return obj.langcountryid.languageid.name

    def country(self, obj):
        return obj.langcountryid.countryid.name

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class searchResultsAdmin(ImportExportModelAdmin, ExportActionMixin):
    search_fields = ['userid__username']
    list_display = [field.name for field in Searchresults._meta.fields]
    resource_class = SearchResultsResource
    list_display = list_display[:3] + ['termid', 'term', 'language', 'country'] + list_display[3:]

    def language(self, obj):
        if obj.userid:
            return obj.userid.langcountryid.languageid.name
        return None

    def country(self, obj):
        if obj.userid:
            return obj.userid.langcountryid.countryid.name
        return None

    def termid(self, obj):
        return obj.linkid.translatedtermid.basictermid.id

    def term(self, obj):
        return obj.linkid.translatedtermid.basictermid.name

    actions = ['change_to_approved', 'change_to_declined']

    @admin.action(description="Approve coding")
    def change_to_approved(self, request, queryset):
        queryset.update(status='approved')

        # Save the objects after updating the status
        for obj in queryset:
            obj.save()

    @admin.action(description="Decline coding")
    def change_to_declined(self, request, queryset):
        queryset.update(status='declined')


class suggestedTermsAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = [field.name for field in Suggestedterms._meta.fields[1:]]


class suggestedCategoriesAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = [field.name for field in Suggestedcategories._meta.fields[1:]]


class suggestedTranslatedTermsAdmin(ImportExportModelAdmin, ExportActionMixin):
    search_fields = ['userid__username']
    resource_class = SuggestedtranslatedtermsResource
    list_display = [field.name for field in Suggestedtranslatedterms._meta.fields]

    list_select_related = ['basictermid', 'userid__langcountryid__languageid', 'userid__langcountryid__countryid']

    actions = ['change_to_approved', 'change_to_declined']

    @admin.action(description="Approve suggesting")
    def change_to_approved(self, request, queryset):
        queryset.update(status='approved')

        # Save the objects after updating the status
        for obj in queryset:
            obj.save()

    @admin.action(description="Decline suggesting")
    def change_to_declined(self, request, queryset):
        queryset.update(status='declined')

    def basicterm(self, obj):
        return obj.basictermid.name

    def language(self, obj):
        return obj.userid.langcountryid.languageid.name

    def country(self, obj):
        return obj.userid.langcountryid.countryid.name

    # Set the list_display fields to include the custom methods
    basicterm_index = list_display.index('basictermid')
    list_display = list_display[:basicterm_index] + ['basicterm', 'language', 'country'] + list_display[basicterm_index+1:]

    # Use annotate and F expression to make the 'basicterm' field available for ordering
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(basicterm_name=F('basictermid__name'))


class basicTermsAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Basicterms._meta.fields]


class categoriesAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Categories._meta.fields]


class translatedTermsAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = [field.name for field in Translatedterms._meta.fields[1:]]
    list_select_related = ['basictermid', 'langcountryid__languageid', 'langcountryid__countryid']
    resource_class = TranslatedTermsResource

    def basicterm(self, obj):
        return obj.basictermid.name

    def language(self, obj):
        return obj.langcountryid.languageid.name

    def country(self, obj):
        return obj.langcountryid.countryid.name

    # Set the list_display fields to include the custom methods instead of 'langcountryid'
    basicterm_index = list_display.index('basictermid')
    list_display = list_display[:basicterm_index] + ['basicterm', 'language', 'country']

    # Use annotate and F expression to make the 'basicterm' field available for ordering
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(basicterm_name=F('basictermid__name'))

    # Set the ordering fields inside the get_queryset method
    ordering = ['basictermid', 'langcountryid__languageid', 'langcountryid__countryid']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'get_title_display']

    def get_queryset(self, request):
        # Retrieve the unmanaged objects using a custom queryset
        queryset = FAQ.objects.all()

        return queryset

    def get_title_display(self, obj):
        # Return the mapped title value
        return dict(FAQ.CHOICE_LIST)[int(obj.title)]

    get_title_display.short_description = 'Title'


class NumToAnswerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Numtoanswer._meta.fields[:]]
    resource_class = NumToAnswersResource

    def get_ordering(self, request):
        return ['num']


class LanguagesWithCountriesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Languageswithcountries._meta.fields]


admin.site.register(Searchresults, searchResultsAdmin)
admin.site.register(Suggestedterms, suggestedTermsAdmin)
admin.site.register(Suggestedcategories, suggestedCategoriesAdmin)
admin.site.register(Suggestedtranslatedterms, suggestedTranslatedTermsAdmin)
admin.site.register(Basicterms, basicTermsAdmin)
admin.site.register(Categories, categoriesAdmin)
admin.site.register(Translatedterms, translatedTermsAdmin)
admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Numtoanswer, NumToAnswerAdmin)
admin.site.register(Languageswithcountries, LanguagesWithCountriesAdmin)

admin.site.unregister(Group)
