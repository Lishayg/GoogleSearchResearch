# Generated by Django 4.1.7 on 2023-08-03 19:17

import datetime
from django.db import migrations, models
import main_page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('profile_avatar', models.CharField(db_column='profileAvatar', default='images/profile_imgs/DefaultProfilePhoto.png', max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.CharField(blank=True, db_column='email', max_length=254, null=True)),
                ('usertype', models.CharField(blank=True, db_column='userType', max_length=40, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('proficiencylevel', models.IntegerField(db_column='proficiencyLevel')),
                ('academiclevel', models.CharField(db_column='academicLevel', max_length=60)),
                ('scienceeducationlevel', models.CharField(db_column='scienceEducationLevel', max_length=60)),
                ('trainedcategories', models.CharField(blank=True, db_column='trainedCategories', max_length=20, null=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, verbose_name='admin access')),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
                ('last_login', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Participants',
                'db_table': 'Participants',
                'managed': False,
            },
            managers=[
                ('objects', main_page.models.ParticipantsManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Basicterms',
            fields=[
                ('id', models.CharField(default='CS<django.db.models.fields.AutoField>', editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('contextExample', models.CharField(blank=True, db_column='contextUse', max_length=250, null=True)),
            ],
            options={
                'verbose_name_plural': 'Basic Terms',
                'db_table': 'BasicTerms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'Categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('countrycode', models.CharField(blank=True, db_column='countryCode', max_length=10, null=True)),
                ('latitude', models.FloatField(blank=True, db_column='Latitude', null=True)),
                ('longitude', models.FloatField(blank=True, db_column='Longitude', null=True)),
            ],
            options={
                'db_table': 'Countries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('comment', models.CharField(max_length=1000)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=150)),
                ('answer', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'Forum',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('langcode', models.CharField(blank=True, db_column='langCode', max_length=10, null=True)),
            ],
            options={
                'db_table': 'Languages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Languageswithcountries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Languages With Countries',
                'db_table': 'LanguagesWithCountries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('stopcodinglink', models.BooleanField(blank=True, db_column='stopCodingLink', null=True)),
            ],
            options={
                'db_table': 'Links',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MapInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Information for Map',
                'db_table': 'MapInformation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Numtoanswer',
            fields=[
                ('num', models.IntegerField(primary_key=True, serialize=False)),
                ('freeaccess', models.CharField(blank=True, db_column='freeAccess', max_length=150, null=True)),
                ('sitetype', models.CharField(blank=True, db_column='siteType', max_length=150, null=True)),
                ('contentproducer', models.CharField(blank=True, db_column='contentProducer', max_length=150, null=True)),
                ('recentinformation', models.CharField(blank=True, db_column='recentInformation', max_length=150, null=True)),
                ('authorbackground', models.CharField(blank=True, db_column='authorBackground', max_length=150, null=True)),
                ('scientificbackground', models.CharField(blank=True, db_column='scientificBackground', max_length=150, null=True)),
                ('scientificterms', models.CharField(blank=True, db_column='scientificTerms', max_length=150, null=True)),
                ('explanations', models.CharField(blank=True, max_length=150, null=True)),
                ('scientificerrors', models.CharField(blank=True, db_column='scientificErrors', max_length=150, null=True)),
                ('scientificaccuracy', models.CharField(blank=True, db_column='scientificAccuracy', max_length=150, null=True)),
                ('availablesources', models.CharField(blank=True, db_column='availableSources', max_length=150, null=True)),
                ('lifereferences', models.CharField(blank=True, db_column='lifeReferences', max_length=150, null=True)),
                ('localexamples', models.CharField(blank=True, db_column='localExamples', max_length=150, null=True)),
                ('contentpresent', models.CharField(blank=True, db_column='contentPresent', max_length=150, null=True)),
                ('conspiracytheory', models.CharField(blank=True, db_column='conspiracyTheory', max_length=150, null=True)),
                ('maliciousmeaning', models.CharField(blank=True, db_column='maliciousMeaning', max_length=150, null=True)),
                ('scientificexplanations', models.CharField(blank=True, db_column='scientificExplanations', max_length=150, null=True)),
                ('enemypresented', models.CharField(blank=True, db_column='enemyPresented', max_length=150, null=True)),
                ('accuracysurness', models.CharField(blank=True, db_column='accuracySureness', max_length=150, null=True)),
                ('errorssureness', models.CharField(blank=True, db_column='errorsSureness', max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'Num To Answer',
                'db_table': 'NumToAnswer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantsGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Participants_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantsPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Participants_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Searchresults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('suggested', 'suggested'), ('approved', 'approved'), ('declined', 'declined')], max_length=10, null=True)),
                ('codingdate', models.DateField(blank=True, db_column='codingDate', default=datetime.date.today, null=True)),
                ('resultnumber', models.IntegerField(blank=True, db_column='resultNumber', null=True)),
                ('freeaccess', models.IntegerField(blank=True, db_column='freeAccess', null=True)),
                ('sitetype', models.IntegerField(blank=True, db_column='siteType', null=True)),
                ('contentproducer', models.IntegerField(blank=True, db_column='contentProducer', null=True)),
                ('recentinformation', models.IntegerField(blank=True, db_column='recentInformation', null=True)),
                ('authorbackground', models.IntegerField(blank=True, db_column='authorBackground', null=True)),
                ('scientificbackground', models.IntegerField(blank=True, db_column='scientificBackground', null=True)),
                ('scientificterms', models.IntegerField(blank=True, db_column='scientificTerms', null=True)),
                ('explanations', models.IntegerField(blank=True, null=True)),
                ('scientificerrors', models.IntegerField(blank=True, db_column='scientificErrors', null=True)),
                ('scientificerrorssureness', models.IntegerField(blank=True, db_column='scientificErrorsSureness', null=True)),
                ('scientificaccuracy', models.IntegerField(blank=True, db_column='scientificAccuracy', null=True)),
                ('scientificaccuracysureness', models.IntegerField(blank=True, db_column='scientificAccuracySureness', null=True)),
                ('availablesources', models.CharField(blank=True, db_column='availableSources', max_length=30, null=True)),
                ('lifereferences', models.IntegerField(blank=True, db_column='lifeReferences', null=True)),
                ('localexamples', models.IntegerField(blank=True, db_column='localExamples', null=True)),
                ('contentpresent', models.IntegerField(blank=True, db_column='contentPresent', null=True)),
                ('conspiracytheory', models.IntegerField(blank=True, db_column='conspiracyTheory', null=True)),
                ('maliciousmeaning', models.IntegerField(blank=True, db_column='maliciousMeaning', null=True)),
                ('scientificexplanations', models.IntegerField(blank=True, db_column='scientificExplanations', null=True)),
                ('enemypresented', models.IntegerField(blank=True, db_column='enemyPresented', null=True)),
                ('codingtime', models.FloatField(blank=True, db_column='codingTime', null=True)),
            ],
            options={
                'verbose_name_plural': 'Search Results',
                'db_table': 'SearchResults',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Suggestedcategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('numberofusers', models.IntegerField(blank=True, db_column='numberOfUsers', null=True)),
            ],
            options={
                'verbose_name_plural': 'Suggested Categories',
                'db_table': 'SuggestedCategories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Suggestedterms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('numberofusers', models.IntegerField(blank=True, db_column='numberOfUsers', null=True)),
            ],
            options={
                'verbose_name_plural': 'Suggested Terms',
                'db_table': 'SuggestedTerms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Suggestedtranslatedterms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('suggested', 'suggested'), ('approved', 'approved'), ('declined', 'declined')], max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'Suggested Translated Terms',
                'db_table': 'SuggestedTranslatedTerms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Traininganswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitetype', models.IntegerField(blank=True, db_column='siteType', null=True)),
                ('sitetypeexplain', models.CharField(blank=True, db_column='siteTypeExplain', max_length=300, null=True)),
                ('contentproducer', models.IntegerField(blank=True, db_column='contentProducer', null=True)),
                ('contentproducerexplain', models.CharField(blank=True, db_column='contentProducerExplain', max_length=300, null=True)),
                ('freeaccess', models.IntegerField(blank=True, db_column='freeAccess', null=True)),
                ('freeaccessexplain', models.CharField(blank=True, db_column='freeAccessExplain', max_length=300, null=True)),
                ('recentinformation', models.IntegerField(blank=True, db_column='recentInformation', null=True)),
                ('recentinformationexplain', models.CharField(blank=True, db_column='recentInformationExplain', max_length=300, null=True)),
                ('authorbackground', models.IntegerField(blank=True, db_column='authorBackground', null=True)),
                ('authorbackgroundexplain', models.CharField(blank=True, db_column='authorBackgroundExplain', max_length=300, null=True)),
                ('scientificbackground', models.IntegerField(blank=True, db_column='scientificBackground', null=True)),
                ('scientificbackgroundexplain', models.CharField(blank=True, db_column='scientificBackgroundExplain', max_length=300, null=True)),
                ('scientificterms', models.IntegerField(blank=True, db_column='scientificTerms', null=True)),
                ('scientifictermsexplain', models.CharField(blank=True, db_column='scientificTermsExplain', max_length=300, null=True)),
                ('explanations', models.IntegerField(blank=True, null=True)),
                ('explanationsexplain', models.CharField(blank=True, db_column='explanationsExplain', max_length=300, null=True)),
                ('scientificerrors', models.IntegerField(blank=True, db_column='scientificErrors', null=True)),
                ('scientificerrorsexplain', models.CharField(blank=True, db_column='scientificErrorsExplain', max_length=300, null=True)),
                ('scientificaccuracy', models.IntegerField(blank=True, db_column='scientificAccuracy', null=True)),
                ('scientificaccuracyexplain', models.CharField(blank=True, db_column='scientificAccuracyExplain', max_length=300, null=True)),
                ('availablesources', models.CharField(blank=True, db_column='availableSources', max_length=30, null=True)),
                ('availablesourcesexplain', models.CharField(blank=True, db_column='availableSourcesExplain', max_length=300, null=True)),
                ('lifereferences', models.IntegerField(blank=True, db_column='lifeReferences', null=True)),
                ('lifereferencesexplain', models.CharField(blank=True, db_column='lifeReferencesExplain', max_length=300, null=True)),
                ('localexamples', models.IntegerField(blank=True, db_column='localExamples', null=True)),
                ('localexamplesexplain', models.CharField(blank=True, db_column='localExamplesExplain', max_length=300, null=True)),
                ('contentpresent', models.IntegerField(blank=True, db_column='contentPresent', null=True)),
                ('contentpresentexplain', models.CharField(blank=True, db_column='contentPresentExplain', max_length=300, null=True)),
                ('conspiracytheory', models.IntegerField(blank=True, db_column='conspiracyTheory', null=True)),
                ('conspiracytheoryexplain', models.CharField(blank=True, db_column='conspiracyTheoryExplain', max_length=300, null=True)),
                ('maliciousmeaning', models.IntegerField(blank=True, db_column='maliciousMeaning', null=True)),
                ('maliciousmeaningexplain', models.CharField(blank=True, db_column='maliciousMeaningExplain', max_length=300, null=True)),
                ('scientificexplanations', models.IntegerField(blank=True, db_column='scientificExplanations', null=True)),
                ('scientificexplanationsexplain', models.CharField(blank=True, db_column='scientificExplanationsExplain', max_length=300, null=True)),
                ('enemypresented', models.IntegerField(blank=True, db_column='enemyPresented', null=True)),
                ('enemypresentedexplain', models.CharField(blank=True, db_column='enemyPresentedExplain', max_length=300, null=True)),
            ],
            options={
                'db_table': 'TrainingAnswers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Translatedterms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Translated Terms',
                'db_table': 'TranslatedTerms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, unique=True)),
                ('answer', models.CharField(max_length=500)),
                ('title', models.IntegerField(choices=[(1, 'About the project'), (2, 'Technicalities'), (3, 'Using the site'), (4, 'Suggestions and problems')])),
            ],
            options={
                'verbose_name_plural': 'FAQ',
                'db_table': 'FAQ',
                'managed': True,
            },
        ),
    ]