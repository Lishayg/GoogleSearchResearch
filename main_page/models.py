# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class ParticipantsManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Basicterms(models.Model):
    id = models.CharField(
        max_length=20,
        default='CS' + str(models.AutoField(primary_key=True)),
        unique=True,
        primary_key=True,
        editable=False
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    categoryid = models.ForeignKey('Categories', models.DO_NOTHING, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    contextExample = models.CharField(max_length=250, blank=True, null=True, db_column='contextUse')

    class Meta:
        managed = False
        db_table = 'BasicTerms'
        verbose_name_plural = "Basic Terms"


class Categories(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'

    class Meta:
        managed = False
        db_table = 'Categories'
        verbose_name_plural = "Categories"


class Countries(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    countrycode = models.CharField(db_column='countryCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Countries'


class Languages(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    langcode = models.CharField(db_column='langCode', max_length=10, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Languages'


class Languageswithcountries(models.Model):
    languageid = models.ForeignKey(Languages, models.DO_NOTHING, db_column='languageId', blank=True, null=True)  # Field name made lowercase.
    countryid = models.ForeignKey(Countries, models.DO_NOTHING, db_column='countryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LanguagesWithCountries'
        verbose_name_plural = "Languages With Countries"


class Links(models.Model):
    link = models.CharField(max_length=500, blank=True, null=True)
    translatedtermid = models.ForeignKey('Translatedterms', models.DO_NOTHING, db_column='translatedTermId', blank=True, null=True)  # Field name made lowercase.
    stopcodinglink = models.BooleanField(db_column='stopCodingLink', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.link

    class Meta:
        managed = False
        db_table = 'Links'


class Participants(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    profile_avatar = models.CharField(db_column='profileAvatar', max_length=200, default='profile_imgs/DefaultProfilePhoto.png')
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(db_column='email', max_length=254, blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='userType', max_length=40, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(blank=True, null=True)
    langcountryid = models.ForeignKey(Languageswithcountries, models.DO_NOTHING, db_column='langCountryId')  # Field name made lowercase.
    proficiencylevel = models.IntegerField(db_column='proficiencyLevel')  # Field name made lowercase.
    academiclevel = models.CharField(db_column='academicLevel', max_length=60)  # Field name made lowercase.
    scienceeducationlevel = models.CharField(db_column='scienceEducationLevel', max_length=60)  # Field name made lowercase.
    trainedcategories = models.CharField(db_column='trainedCategories', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=128, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField('admin access', default=False)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField()

    USERNAME_FIELD = "username"

    objects = ParticipantsManager()

    class Meta:
        managed = False
        db_table = 'Participants'
        verbose_name_plural = 'Participants'

    def has_perm(self, perm, obj=None):
        return True  # self.is_admin

    def has_module_perms(self, app_label):
        return True


User = get_user_model()


class Searchresults(models.Model):
    CHOICE_LIST = [
        ('suggested', 'suggested'),
        ('approved', 'approved'),
        ('declined', 'declined'),
    ]
    userid = models.ForeignKey(User, models.CASCADE, db_column='userId', blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True, choices=CHOICE_LIST)
    codingdate = models.DateField(db_column='codingDate', blank=True, null=True, default=datetime.date.today)  # Field name made lowercase.
    resultnumber = models.IntegerField(db_column='resultNumber', blank=True, null=True)  # Field name made lowercase.
    linkid = models.ForeignKey(Links, models.DO_NOTHING, db_column='linkId', blank=True, null=True)  # Field name made lowercase.
    freeaccess = models.IntegerField(db_column='freeAccess', blank=True, null=True)  # Field name made lowercase.
    sitetype = models.IntegerField(db_column='siteType', blank=True, null=True)  # Field name made lowercase.
    contentproducer = models.IntegerField(db_column='contentProducer', blank=True, null=True)  # Field name made lowercase.
    recentinformation = models.IntegerField(db_column='recentInformation', blank=True, null=True)  # Field name made lowercase.
    authorbackground = models.IntegerField(db_column='authorBackground', blank=True, null=True)  # Field name made lowercase.
    scientificbackground = models.IntegerField(db_column='scientificBackground', blank=True, null=True)  # Field name made lowercase.
    scientificterms = models.IntegerField(db_column='scientificTerms', blank=True, null=True)  # Field name made lowercase.
    explanations = models.IntegerField(blank=True, null=True)
    scientificerrors = models.IntegerField(db_column='scientificErrors', blank=True, null=True)  # Field name made lowercase.
    scientificerrorssureness = models.IntegerField(db_column='scientificErrorsSureness', blank=True, null=True)  # Field name made lowercase.
    scientificaccuracy = models.IntegerField(db_column='scientificAccuracy', blank=True, null=True)  # Field name made lowercase.
    scientificaccuracysureness = models.IntegerField(db_column='scientificAccuracySureness', blank=True, null=True)  # Field name made lowercase.
    availablesources = models.CharField(db_column='availableSources', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lifereferences = models.IntegerField(db_column='lifeReferences', blank=True, null=True)  # Field name made lowercase.
    localexamples = models.IntegerField(db_column='localExamples', blank=True, null=True)  # Field name made lowercase.
    contentpresent = models.IntegerField(db_column='contentPresent', blank=True, null=True)  # Field name made lowercase.
    conspiracytheory = models.IntegerField(db_column='conspiracyTheory', blank=True, null=True)  # Field name made lowercase.
    maliciousmeaning = models.IntegerField(db_column='maliciousMeaning', blank=True, null=True)  # Field name made lowercase.
    scientificexplanations = models.IntegerField(db_column='scientificExplanations', blank=True, null=True)  # Field name made lowercase.
    enemypresented = models.IntegerField(db_column='enemyPresented', blank=True, null=True)  # Field name made lowercase.
    codingtime = models.FloatField(db_column='codingTime', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SearchResults'
        verbose_name_plural = "Search Results"


class Suggestedcategories(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    numberofusers = models.IntegerField(db_column='numberOfUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SuggestedCategories'
        verbose_name_plural = "Suggested Categories"


class Suggestedterms(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    numberofusers = models.IntegerField(db_column='numberOfUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SuggestedTerms'
        verbose_name_plural = "Suggested Terms"


class Suggestedtranslatedterms(models.Model):
    CHOICE_LIST = [
        ('suggested', 'suggested'),
        ('approved', 'approved'),
        ('declined', 'declined'),
    ]
    name = models.CharField(max_length=100, blank=True, null=True)
    basictermid = models.ForeignKey(Basicterms, models.DO_NOTHING, db_column='basicTermId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.CASCADE, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=10, blank=True, null=True, choices=CHOICE_LIST)

    class Meta:
        managed = False
        db_table = 'SuggestedTranslatedTerms'
        verbose_name_plural = "Suggested Translated Terms"


class Traininganswers(models.Model):
    linkid = models.ForeignKey(Links, models.DO_NOTHING, db_column='linkId', blank=True, null=True)  # Field name made lowercase.
    sitetype = models.IntegerField(db_column='siteType', blank=True, null=True)  # Field name made lowercase.
    sitetypeexplain = models.CharField(db_column='siteTypeExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    contentproducer = models.IntegerField(db_column='contentProducer', blank=True, null=True)  # Field name made lowercase.
    contentproducerexplain = models.CharField(db_column='contentProducerExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    freeaccess = models.IntegerField(db_column='freeAccess', blank=True, null=True)  # Field name made lowercase.
    freeaccessexplain = models.CharField(db_column='freeAccessExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    recentinformation = models.IntegerField(db_column='recentInformation', blank=True, null=True)  # Field name made lowercase.
    recentinformationexplain = models.CharField(db_column='recentInformationExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    authorbackground = models.IntegerField(db_column='authorBackground', blank=True, null=True)  # Field name made lowercase.
    authorbackgroundexplain = models.CharField(db_column='authorBackgroundExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    scientificbackground = models.IntegerField(db_column='scientificBackground', blank=True, null=True)  # Field name made lowercase.
    scientificbackgroundexplain = models.CharField(db_column='scientificBackgroundExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    scientificterms = models.IntegerField(db_column='scientificTerms', blank=True, null=True)  # Field name made lowercase.
    scientifictermsexplain = models.CharField(db_column='scientificTermsExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    explanations = models.IntegerField(blank=True, null=True)
    explanationsexplain = models.CharField(db_column='explanationsExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    scientificerrors = models.IntegerField(db_column='scientificErrors', blank=True, null=True)  # Field name made lowercase.
    scientificerrorsexplain = models.CharField(db_column='scientificErrorsExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    scientificaccuracy = models.IntegerField(db_column='scientificAccuracy', blank=True, null=True)  # Field name made lowercase.
    scientificaccuracyexplain = models.CharField(db_column='scientificAccuracyExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    availablesources = models.CharField(db_column='availableSources', max_length=30, blank=True, null=True)  # Field name made lowercase.
    availablesourcesexplain = models.CharField(db_column='availableSourcesExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    lifereferences = models.IntegerField(db_column='lifeReferences', blank=True, null=True)  # Field name made lowercase.
    lifereferencesexplain = models.CharField(db_column='lifeReferencesExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    localexamples = models.IntegerField(db_column='localExamples', blank=True, null=True)  # Field name made lowercase.
    localexamplesexplain = models.CharField(db_column='localExamplesExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    contentpresent = models.IntegerField(db_column='contentPresent', blank=True, null=True)  # Field name made lowercase.
    contentpresentexplain = models.CharField(db_column='contentPresentExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    conspiracytheory = models.IntegerField(db_column='conspiracyTheory', blank=True, null=True)  # Field name made lowercase.
    conspiracytheoryexplain = models.CharField(db_column='conspiracyTheoryExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    maliciousmeaning = models.IntegerField(db_column='maliciousMeaning', blank=True, null=True)  # Field name made lowercase.
    maliciousmeaningexplain = models.CharField(db_column='maliciousMeaningExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    scientificexplanations = models.IntegerField(db_column='scientificExplanations', blank=True, null=True)  # Field name made lowercase.
    scientificexplanationsexplain = models.CharField(db_column='scientificExplanationsExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.
    enemypresented = models.IntegerField(db_column='enemyPresented', blank=True, null=True)  # Field name made lowercase.
    enemypresentedexplain = models.CharField(db_column='enemyPresentedExplain', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrainingAnswers'


class Translatedterms(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    basictermid = models.ForeignKey(Basicterms, models.DO_NOTHING, db_column='basicTermId', blank=True, null=True)  # Field name made lowercase.
    langcountryid = models.ForeignKey(Languageswithcountries, models.DO_NOTHING, db_column='langCountryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TranslatedTerms'
        verbose_name_plural = "Translated Terms"


class FAQ(models.Model):
    CHOICE_LIST = [
        (1, 'About the project'),
        (2, 'Technicalities'),
        (3, 'Using the site'),
        (4, 'Suggestions and problems'),
    ]
    question = models.CharField(max_length=200, unique=True)
    answer = models.CharField(max_length=500)
    title = models.IntegerField(choices=CHOICE_LIST)

    class Meta:
        managed = True
        db_table = 'FAQ'
        verbose_name_plural = "FAQ"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ParticipantsGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='participants_id')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Participants_groups'
        unique_together = (('user', 'group'),)


class ParticipantsPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='participants_id')
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Participants_user_permissions'
        unique_together = (('user', 'permission'),)


class Numtoanswer(models.Model):
    num = models.IntegerField(primary_key=True)
    freeaccess = models.CharField(db_column='freeAccess', max_length=150, blank=True, null=True)  # Field name made lowercase.
    sitetype = models.CharField(db_column='siteType', max_length=150, blank=True, null=True)  # Field name made lowercase.
    contentproducer = models.CharField(db_column='contentProducer', max_length=150, blank=True, null=True)  # Field name made lowercase.
    recentinformation = models.CharField(db_column='recentInformation', max_length=150, blank=True, null=True)  # Field name made lowercase.
    authorbackground = models.CharField(db_column='authorBackground', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scientificbackground = models.CharField(db_column='scientificBackground', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scientificterms = models.CharField(db_column='scientificTerms', max_length=150, blank=True, null=True)  # Field name made lowercase.
    explanations = models.CharField(max_length=150, blank=True, null=True)
    scientificerrors = models.CharField(db_column='scientificErrors', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scientificaccuracy = models.CharField(db_column='scientificAccuracy', max_length=150, blank=True, null=True)  # Field name made lowercase.
    availablesources = models.CharField(db_column='availableSources', max_length=150, blank=True, null=True)  # Field name made lowercase.
    lifereferences = models.CharField(db_column='lifeReferences', max_length=150, blank=True, null=True)  # Field name made lowercase.
    localexamples = models.CharField(db_column='localExamples', max_length=150, blank=True, null=True)  # Field name made lowercase.
    contentpresent = models.CharField(db_column='contentPresent', max_length=150, blank=True, null=True)  # Field name made lowercase.
    conspiracytheory = models.CharField(db_column='conspiracyTheory', max_length=150, blank=True, null=True)  # Field name made lowercase.
    maliciousmeaning = models.CharField(db_column='maliciousMeaning', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scientificexplanations = models.CharField(db_column='scientificExplanations', max_length=150, blank=True, null=True)  # Field name made lowercase.
    enemypresented = models.CharField(db_column='enemyPresented', max_length=150, blank=True, null=True)  # Field name made lowercase.
    accuracysurness = models.CharField(db_column='accuracySureness', max_length=150, blank=True, null=True)  # Field name made lowercase.
    errorssureness = models.CharField(db_column='errorsSureness', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NumToAnswer'
        verbose_name_plural = "Num To Answer"


class Forum(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    comment = models.CharField(max_length=1000)
    date = models.DateField()
    category = models.CharField(max_length=150)
    answer = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'Forum'


class MapInformation(models.Model):
    basictermid = models.ForeignKey(Basicterms, models.DO_NOTHING, db_column='basicTermId', blank=True, null=True)  # Field name made lowercase.
    langcountryid = models.ForeignKey(Languageswithcountries, models.DO_NOTHING, db_column='langCountryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MapInformation'
        verbose_name_plural = "Information for Map"


