from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Searchresults, MapInformation, Suggestedtranslatedterms, Translatedterms, Links


@receiver(post_save, sender=Searchresults)
def approve_coding(sender, instance, **kwargs):
    if instance.status == 'approved':
        langCountryId = instance.userid.langcountryid
        basicTermId = instance.linkid.translatedtermid.basictermid

        # Update data for Map
        MapInformation.objects.create(langcountryid=langCountryId, basictermid=basicTermId)

        # Update stopCodingLing to True if 2 codings approved
        try:
            approved_codings = Searchresults.objects.filter(status='approved', linkid=instance.linkid)
            result_count = approved_codings.count()
            if result_count == 2:
                related_link = Links.objects.get(id=instance.linkid.id)
                related_link.stopcodinglink = 1
                related_link.save()
        except Searchresults.DoesNotExist:
            pass


@receiver(post_save, sender=Suggestedtranslatedterms)
def approve_translation(sender, instance, **kwargs):
    if instance.status == 'approved':
        translation = instance.name
        basicTermId = instance.basictermid
        langCountryId = instance.userid.langcountryid

        # Update Translated Terms
        Translatedterms.objects.create(name=translation, basictermid=basicTermId, langcountryid=langCountryId)


