import tablib
from django.contrib.auth import get_user_model
from import_export import resources
from django.utils.html import format_html
from .models import Searchresults, Numtoanswer, Languageswithcountries, Translatedterms, Links, Basicterms,\
    Suggestedtranslatedterms
from import_export.admin import ExportActionMixin


class TranslatedTermsResource(ExportActionMixin, resources.ModelResource):

    # Define a threshold for the number of rows to trigger 'after_export'
    AFTER_EXPORT_THRESHOLD = 1000

    def after_export(self, queryset, data, *args, **kwargs):
        if queryset.count() <= self.AFTER_EXPORT_THRESHOLD:
            # Perform additional queries to include related fields
            new_data = tablib.Dataset()
            new_data.headers = ["Id", "Name", "Basic Term", "Language", "Country"]

            for row in data:
                # Unpack the tuple to access individual values
                id, name, basictermid, langcountryid = row

                # Fetch related data using the IDs from the exported data
                basicterm_name = Basicterms.objects.get(id=basictermid).name
                langcountry_instance = Languageswithcountries.objects.get(id=langcountryid)
                language_name = langcountry_instance.languageid.name
                country_name = langcountry_instance.countryid.name

                # Create a list with the related field data
                new_row = [id, name, basicterm_name, language_name, country_name]
                new_data.append(new_row)

            # Replace the original 'data' with the modified 'new_data'
            data._data = new_data._data
            data.headers = new_data.headers

    class Meta:
        model = Translatedterms


class SuggestedtranslatedtermsResource(ExportActionMixin, resources.ModelResource):

    # Define a threshold for the number of rows to trigger 'after_export'
    AFTER_EXPORT_THRESHOLD = 1000

    def after_export(self, queryset, data, *args, **kwargs):
        if queryset.count() <= self.AFTER_EXPORT_THRESHOLD:
            # Perform additional queries to include related fields
            new_data = tablib.Dataset()
            new_data.headers = ["Id", "Translation", "Basic Term", "Language", "Country", "Username", 'Status']

            for row in data:
                # Unpack the tuple to access individual values
                id, name, basictermid, userid, status = row

                # Fetch related data using the IDs from the exported data
                basicterm_name = Basicterms.objects.get(id=basictermid).name
                user = get_user_model().objects.filter(id=userid).first()
                username = user.username
                language_name = user.langcountryid.languageid.name
                country_name = user.langcountryid.countryid.name

                # Create a list with the related field data
                new_row = [id, name, basicterm_name, language_name, country_name, username, status]
                new_data.append(new_row)

            # Replace the original 'data' with the modified 'new_data'
            data._data = new_data._data
            data.headers = new_data.headers

    class Meta:
        model = Suggestedtranslatedterms


class SearchResultsResource(ExportActionMixin, resources.ModelResource):
    # Define a threshold for the number of rows to trigger 'after_export'
    AFTER_EXPORT_THRESHOLD = 1000

    class Meta:
        model = Searchresults

    def after_export(self, queryset, data, *args, **kwargs):
        if queryset.count() <= self.AFTER_EXPORT_THRESHOLD:

            custom_data = tablib.Dataset()
            headers = [field.name for field in Searchresults._meta.fields]
            headers = headers[:3] + ['termid', 'term', 'language', 'country'] + headers[3:]
            userid_idx = headers.index("userid")
            headers[userid_idx] = "username"
            custom_data.headers = headers
            for row in data:
                data_row = []
                user = get_user_model().objects.filter(id=row[1]).first() if row[1] != "" else None
                link = Links.objects.filter(id=row[5]).first() if row[5] != "" else None
                translated_term = Translatedterms.objects.filter(id=link.translatedtermid.id).first()
                term = Basicterms.objects.filter(id=translated_term.basictermid.id).first()
                for h in headers:
                    if h == 'username':
                        to_add = user.username if user else None
                    elif h == 'termid':
                        to_add = term.id
                    elif h == 'term':
                        to_add = term.name
                    elif h == 'language':
                        to_add = user.langcountryid.languageid.name if user else None
                    elif h == 'country':
                        to_add = user.langcountryid.countryid.name if user else None
                    else:
                        search_result_map = {
                            'id': row[0],
                            'status': row[2],
                            'codingdate': row[3],
                            'resultnumber': row[4],
                            'linkid': link.id,
                            'freeaccess': row[6],
                            'sitetype': row[7],
                            'contentproducer': row[8],
                            'recentinformation': row[9],
                            'authorbackground': row[10],
                            'scientificbackground': row[11],
                            'scientificterms': row[12],
                            'explanations': row[13],
                            'scientificerrors': row[14],
                            'scientificerrorssureness': row[15],
                            'scientificaccuracy': row[16],
                            'scientificaccuracysureness': row[17],
                            'availablesources': row[18],
                            'lifereferences': row[19],
                            'localexamples': row[20],
                            'contentpresent': row[21],
                            'conspiracytheory': row[22],
                            'maliciousmeaning': row[23],
                            'scientificexplanations': row[24],
                            'enemypresented': row[25],
                            'codingtime': row[26]
                        }
                        to_add = search_result_map[h]
                    data_row.append(to_add)

                custom_data.append(data_row)

            headers_map = [
                ('id', 'Coding Id'),
                ('status', 'Status'),
                ('codingdate', 'Coding Date'),
                ('resultnumber', 'Result Number'),
                ('linkid', 'Link'),
                ('freeaccess', 'Accessibility of the website'),
                ('sitetype', 'Site Type'),
                ('contentproducer', 'The Content Producer'),
                ('recentinformation', 'How recent is the information?'),
                ('authorbackground', 'What is the author background?'),
                ('scientificbackground',
                 'Is a scientific background (high school or above) required to understand the information?'),
                ('scientificterms', 'Are there any scientific terms that laypeople do not understand?'),
                ('explanations',
                 'If you answered No to the previous question, you may proceed to the next question. If you answered Yes, please answer: Are there any explanations for the scientific terms?'),
                ('scientificerrors', 'Are there major scientific errors in the link?'),
                ('scientificerrorssureness', 'How sure are you regarding your previous answer?'),
                ('scientificaccuracy', 'How accurate is the scientific content presented in the link?'),
                ('scientificaccuracysureness', 'How sure are you regarding the accuracy?'),
                ('availablesources', 'Are the following sources available in the link?'),
                ('lifereferences', 'Is there reference to everyday life?'),
                ('localexamples', 'Are there local examples in the content?'),
                ('contentpresent', 'Does the content present advantages and disadvantages or risks and benefits?'),
                ('conspiracytheory', 'Does the content reject or reinforce the discussed conspiracy theory'),
                ('maliciousmeaning', 'Is malicious meaning is alluded to in the text ("We are being tricked")'),
                ('scientificexplanations', 'Do claims contradict accepted scientific explanations?'),
                ('enemypresented',
                 'Are specific groups in society (pharma, Jews, Muslims etc.), institutions or governments are presented as the enemy?'),
            ]

            for i, h in enumerate(custom_data.headers):
                for header_map in headers_map:
                    if h == header_map[0]:
                        custom_data.headers[i] = format_html('{}', header_map[1])
                        break

            data._data = custom_data._data
            data.headers = custom_data.headers


class NumToAnswersResource(ExportActionMixin, resources.ModelResource):

    def get_export_headers(self):
        # Define a list of tuples that includes the original header name and its replacement name
        headers_map = [
            ('num', 'option number'),
            ('freeaccess', 'Accessibility of the website'),
            ('sitetype', 'Site Type'),
            ('contentproducer', 'The Content Producer'),
            ('recentinformation', 'How recent is the information?'),
            ('authorbackground', 'What is the author background?'),
            ('scientificbackground', 'Is a scientific background (high school or above) required to understand the information?'),
            ('scientificterms', 'Are there any scientific terms that laypeople do not understand?'),
            ('explanations', 'If you answered No to the previous question, you may proceed to the next question. If you answered Yes, please answer: Are there any explanations for the scientific terms?'),
            ('scientificerrors', 'Are there major scientific errors in the link?'),
            ('scientificerrorssureness', 'How sure are you regarding your previous answer?'),
            ('scientificaccuracy', 'How accurate is the scientific content presented in the link?'),
            ('scientificaccuracysureness', 'How sure are you regarding the accuracy?'),
            ('availablesources', 'Are the following sources available in the link?'),
            ('lifereferences', 'Is there reference to everyday life?'),
            ('localexamples', 'Are there local examples in the content?'),
            ('contentpresent', 'Does the content present advantages and disadvantages or risks and benefits?'),
            ('conspiracytheory', 'Does the content reject or reinforce the discussed conspiracy theory'),
            ('maliciousmeaning', 'Is malicious meaning is alluded to in the text ("We are being tricked")'),
            ('scientificexplanations', 'Do claims contradict accepted scientific explanations?'),
            ('enemypresented', 'Are specific groups in society (pharma, Jews, Muslims etc.), institutions or governments are presented as the enemy?'),
        ]

        headers = super().get_export_headers()
        for i, h in enumerate(headers):
            for header_map in headers_map:
                if h == header_map[0]:
                    headers[i] = format_html('{}', header_map[1])
                    break

        return headers

    class Meta:
        model = Numtoanswer

