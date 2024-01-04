import json
import time

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe
from .TokenGenerator import email_verification_token
from .forms import UserRegistrationForm, UserUpdateForm
from django.http import JsonResponse, HttpResponse

from GoogleSearchResearch import settings
from django.contrib.auth import login, get_user_model
from .models import Searchresults, Links, Suggestedterms, Translatedterms, \
    Suggestedcategories, Countries, Languages, Categories, Basicterms, Participants, Languageswithcountries, \
    Traininganswers, Suggestedtranslatedterms, FAQ, Numtoanswer, Forum
from django.core.mail import send_mail, EmailMessage
from django.db.models import Subquery
from datetime import datetime


@never_cache
def home_page(request):
    return render(request, 'homePage.html')


@never_cache
def about(request):
    return render(request, 'about.html')


@never_cache
def faq(request):
    about_questions = FAQ.objects.filter(title=1)
    technicalities_questions = FAQ.objects.filter(title=2)
    using_questions = FAQ.objects.filter(title=3)
    suggest_questions = FAQ.objects.filter(title=4)

    questions = {
        'about_questions': about_questions,
        'technicalities_questions': technicalities_questions,
        'using_questions': using_questions,
        'suggest_questions': suggest_questions,
    }
    return render(request, 'FAQ.html', questions)


# ==========================
# Forum Section
@never_cache
def forum(request):
    return render(request, 'forum.html')


@never_cache
def discussions(request, category):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        question_id = request.POST.get('question_id')
        if question_id:
            try:
                question = Forum.objects.get(pk=question_id)
                question.answer = answer
                question.save()
            except Forum.DoesNotExist:
                pass

    category = category
    forum_discuss = Forum.objects.filter(category=category).all()
    discuss = []
    for item in forum_discuss:
        name = item.name
        comment = item.comment
        date = item.date
        answer = item.answer
        my_string = str(date) + ' From: ' + name + '<br>Comment: ' + comment
        if answer:
            my_string += '<br><strong>Answer:</strong> ' + answer
        my_string = mark_safe(my_string)
        discuss.append((item.id, my_string, answer))

    return render(request, 'discussions.html', {'category': category, 'discussions': discuss})


@never_cache
def add_comment(request):
    category = request.POST.get('category')
    name = request.POST.get('name')
    email = request.POST.get('email')
    comment = request.POST.get('comment')
    date = datetime.now()
    # Add your logic to save the comment for the selected category
    new_comment = Forum()
    new_comment.name = name
    new_comment.email = email
    new_comment.comment = comment
    new_comment.date = date
    new_comment.category = category
    new_comment.save()
    return render(request, 'discussions.html', {'category': category, 'discussions': []})
# ===========================


# ===========================
# Registration Section
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send confirmation mail
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            current_site = get_current_site(request)
            mail_subject = 'Confirm Your Registration'
            message = render_to_string('registration/confirmation_email_registration.html', {
                'user': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[user_email]
            )
            email.send()
            return redirect('register_email_confirmation')

    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {'form': form})


def register_email_confirmation(request):
    return render(request, 'registration/register_email_confirmation.html')


def activate_registration(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('registration_submitted')
    else:
        return HttpResponse('Activation link is invalid.')


def guest_registration(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        science_ed = request.POST.get('science_ed')
        country = request.POST.get('country')
        education = request.POST.get('education')
        language_proficiency = request.POST.get('language_proficiency')
        lang_obj = Languages.objects.get(id=language)
        country_obj = Countries.objects.get(id=country)
        try:
            langCountryId = Languageswithcountries.objects.get(languageid=lang_obj, countryid=country_obj)
        except Languageswithcountries.DoesNotExist:
            langCountryId = Languageswithcountries.objects.create(languageid=lang_obj, countryid=country_obj)

        # adding the values to the participants  table
        new_guest = Participants(username='guest' + str((Participants.objects.count()) + 1),
                                 usertype='guest',
                                 langcountryid=langCountryId,
                                 proficiencylevel=language_proficiency,
                                 academiclevel=education,
                                 scienceeducationlevel=science_ed,
                                 is_superuser=0,
                                 is_staff=0,
                                 is_active=1,
                                 date_joined=datetime.now(),
                                 last_login=datetime.now()
                                 )

        # adding the new guest to the database
        new_guest.save()
        # login
        login(request, new_guest, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('registration_submitted')

    else:
        languages = Languages.objects.all().order_by('name')
        countries = Countries.objects.all().order_by('name')
        return render(request, "registration/guest_registration.html", {'languages': languages, 'countries': countries})


@never_cache
def registration_submitted(request):
    return render(request, 'registration/registration_submitted.html')
# ===========================


# ===========================
# Training Section
def get_training_answers(training_num):
    if training_num == 7 or training_num == 8:
        database_variables = ['freeaccess', 'contentproducer', 'authorbackground', 'scientificterms', 'sitetype',
                              'recentinformation', 'scientificbackground', 'scientificerrors',
                              'scientificaccuracy', 'lifereferences', 'localexamples',
                              'contentpresent', 'conspiracytheory', 'maliciousmeaning', 'scientificexplanations',
                              'enemypresented']
        explainations_attr = ['freeaccessexplain', 'contentproducerexplain', 'authorbackgroundexplain',
                              'scientifictermsexplain',
                              'sitetypeexplain', 'recentinformationexplain', 'scientificbackgroundexplain',
                              'scientificerrorsexplain',
                              'scientificaccuracyexplain', 'lifereferencesexplain', 'localexamplesexplain',
                              'contentpresentexplain',
                              'conspiracytheoryexplain', 'maliciousmeaningexplain', 'scientificexplanationsexplain',
                              'enemypresentedexplain']
    else:
        database_variables = ['freeaccess', 'contentproducer', 'authorbackground', 'scientificterms', 'sitetype',
                              'recentinformation', 'scientificbackground', 'scientificerrors',
                              'scientificaccuracy', 'lifereferences', 'localexamples',
                              'contentpresent']
        explainations_attr = ['freeaccessexplain', 'contentproducerexplain', 'authorbackgroundexplain',
                              'scientifictermsexplain',
                              'sitetypeexplain', 'recentinformationexplain', 'scientificbackgroundexplain',
                              'scientificerrorsexplain',
                              'scientificaccuracyexplain', 'lifereferencesexplain',
                              'localexamplesexplain', 'contentpresentexplain']
    answers = Traininganswers.objects.filter(id=training_num).first()
    return answers, database_variables, explainations_attr


def redirect_link(training_num):
    return reverse('training', args=[training_num])


@login_required
@never_cache
def training(request, training_num):
    correct_answers, database_variables, explain_attr = get_training_answers(training_num)
    results = {}
    user = request.user
    explain = None
    answer = None
    correct_answer = None
    if request.method == 'POST':
        counter = 0
        url = redirect_link(training_num + 1)
        success = False
        num_questions = len(request.POST) - 2
        results['explanations'] = None
        i = 0
        post_data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        for field_name in post_data:
            is_correct = False
            if field_name == 'sources':
                sources_list = request.POST.getlist('sources')
                selected_values = []
                selected_texts = []
                answer_list = []

                for source in sources_list:
                    text = Numtoanswer.objects.filter(num=source).values('availablesources')[0]['availablesources']
                    selected_values.append(source)
                    selected_texts.append(source + ' - ' + text)

                # Join the selected values into a string separated by a comma
                selected_value = ", ".join(selected_values)
                correct_answer = getattr(correct_answers, 'availablesources')
                correct = correct_answer.split(', ')
                for s in correct:
                    answer_list.append(
                        s + ' - ' + Numtoanswer.objects.filter(num=s).values('availablesources')[0]['availablesources'])

                answer = ", ".join(answer_list)
                selected_text = ("& ".join(selected_texts)).split('& ')
                explain = getattr(correct_answers, 'availablesourcesexplain')
                explain = explain.split('\\n')

            elif field_name == 'explanations':
                selected_value = request.POST.get(field_name)
                selected_text = Numtoanswer.objects.filter(num=selected_value).values('explanations')[0]['explanations']
                correct_answer = getattr(correct_answers, 'explanations')
                answer = Numtoanswer.objects.filter(num=correct_answer).values('explanations')[0]['explanations']
                explain = getattr(correct_answers, 'explanationsexplain')

            else:
                selected_value = request.POST.get(field_name)
                selected_text = Numtoanswer.objects.filter(num=selected_value).values(database_variables[i])[0][
                    database_variables[i]]

            if field_name != 'explanations' and field_name != 'sources':
                correct_answer = getattr(correct_answers, database_variables[i])
                answer = Numtoanswer.objects.filter(num=correct_answer).values(database_variables[i])[0][
                    database_variables[i]]
                explain = getattr(correct_answers, explain_attr[i])
                i += 1

            if str(selected_value) == str(correct_answer):
                counter += 1
                is_correct = True

            results[field_name] = (selected_text, is_correct, answer, explain)

        if counter >= 0.8 * num_questions:
            success = True
            if user.trainedcategories is None:
                user.trainedcategories = str((training_num - 1) // 2 + 1)
            else:
                trained_list = user.trainedcategories.split(", ")
                trained_list.append(str((training_num - 1) // 2 + 1))
                user.trainedcategories = ", ".join(list(set(trained_list)))

            user.save()

        return render(request, 'training_section/trainingResults.html', {'results': results, 'success': success, 'url': url,
                                                        'training_num': training_num})

    else:
        answers_text = Numtoanswer.objects.all()
        category_index = (training_num - 1) // 2
        categories = Categories.objects.all()
        category_names = [category.name for category in categories]
        related_link = correct_answers.linkid
        context = {
            'article_link': related_link.link,
            'article_link_text': 'click here',
            'training_num': training_num,
            'category': category_names[category_index],
            'answers_text': answers_text
        }

        return render(request, 'training_section/training.html', context)


@never_cache
def training_explanations(request, training_num):
    correct_answers, database_variables, explain_attr = get_training_answers(training_num)
    related_link = correct_answers.linkid
    results = {}
    fields_names = ['free_access', 'content_producer', 'author', 'dont_understand', 'site_type', 'recent',
                    'scientific_background', 'errors', 'accuracy', 'everyday', 'examples',
                    'risk_contribute', 'theory', 'malicious', 'scientific_explanations', 'enemy']

    results['explanations'] = None
    i = 0

    answer_list = []

    # Join the selected values into a string separated by a comma
    correct_answer = getattr(correct_answers, 'availablesources')
    correct = correct_answer.split(', ')
    for s in correct:
        answer_list.append(
            s + ' - ' + Numtoanswer.objects.filter(num=s).values('availablesources')[0]['availablesources'])

    answer = ", ".join(answer_list)
    explain = getattr(correct_answers, 'availablesourcesexplain')
    explain = explain.split('\\n')

    results['sources'] = (answer, explain)

    if getattr(correct_answers, 'scientificterms') == 1:
        correct_answer = getattr(correct_answers, 'explanations')
        answer = Numtoanswer.objects.filter(num=correct_answer).values('explanations')[0]['explanations']
        explain = getattr(correct_answers, 'explanationsexplain')

        results['explanations'] = (answer, explain)

    for field_name in fields_names:
        if i < len(database_variables):
            correct_answer = getattr(correct_answers, database_variables[i])
            answer = Numtoanswer.objects.filter(num=correct_answer).values(database_variables[i])[0][
                database_variables[i]]
            explain = getattr(correct_answers, explain_attr[i])

            i += 1

        results[field_name] = (answer, explain)

    category_index = (training_num - 1) // 2
    categories = Categories.objects.all()
    category_names = [category.name for category in categories]

    context = {
        'article_link': related_link.link,
        'results': results,
        'training_num': training_num,
        'category': category_names[category_index]
    }

    return render(request, 'training_section/trainingExplanations.html', context)
# ===========================


# ===========================
# Coding Section
def get_related_links_ids(request):
    term_id = request.GET.get('term_id')
    data = []
    try:
        links = Links.objects.filter(translatedtermid=term_id, stopcodinglink=0)
        counter = 1
        for link in links:
            data.append({
                'num': counter,
                'id': link.id,
            })
            counter += 1
    except Links.DoesNotExist:
        return JsonResponse({'links': data})

    return JsonResponse({'links': data})


def get_related_link_url(request):
    link_id = request.GET.get('link_id')
    name = request.GET.get('name')
    link = Links.objects.filter(id=link_id).first()
    data = [{
        'url': link.link,
        'name': name,
    }]
    return JsonResponse({'link': data})


def get_translated_terms(request):
    data = []
    category_id = request.GET.get('category')
    user = request.user
    user_details = Participants.objects.get(username=user.username)
    langCountryId = user_details.langcountryid
    basic_terms = Basicterms.objects.filter(categoryid=category_id)
    for term in basic_terms:
        try:
            translated_term = Translatedterms.objects.filter(langcountryid=langCountryId, basictermid=term.id).first()
            if translated_term is not None:
                data.append({'id': translated_term.id, 'term': translated_term.name})
        except Translatedterms.DoesNotExist:
            continue

    return JsonResponse({'translated_terms': data})


@login_required
@never_cache
def before_coding(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        translated_term_id = request.POST.get('translated_terms')
        # for passing the translated term to get_stop_coding
        request.session['term'] = translated_term_id
        link_choosing = request.POST.get('link_using_check')
        if link_choosing != 'on':
            link_id = request.POST.get('related-links')
            context = {
                "category": category,
                "translated_term_id": translated_term_id,
                "link_id": link_id,
                "time_start": time.time()
            }
            json_data = json.dumps(context)

            url = f"/coding/?data={json_data}"
            return redirect(url)

        context = {
            "category": category,
            "translated_term_id": translated_term_id,
            "time_start": time.time()
        }
        json_data = json.dumps(context)

        url = f"/coding/?data={json_data}"
        return redirect(url)

    else:
        user = Participants.objects.get(username=request.user.username)
        trained_categories = user.trainedcategories
        categories = []
        if trained_categories is None or len(trained_categories) == 0:
            return render(request, "training_section/trainBeforeCoding.html")
        for cat in trained_categories.split(', '):
            categories.append(Categories.objects.get(id=int(cat)))
        return render(request, "site_contributions/before_coding.html", {'categories': categories})


def get_stop_coding(request):
    link = request.GET.get('res_link')
    # get the term from before_coding
    term_id = request.session['term']
    try:
        exist_link = Links.objects.filter(translatedtermid=term_id, link=link).first()
        if exist_link.stopcodinglink == 1:
            return JsonResponse({'stop': True})
        else:
            return JsonResponse({'stop': False})
    except:
        return JsonResponse({'stop': False})


@login_required
@never_cache
def coding(request):
    data = request.GET.get('data')
    data_dict = json.loads(data)
    category = data_dict['category']
    translated_term_id = data_dict['translated_term_id']
    link_id = None
    if 'link_id' in data_dict:
        link_id = data_dict['link_id']

    if request.method == 'POST':
        term_id = Translatedterms.objects.filter(id=translated_term_id).first()
        user = request.user
        if link_id is None:
            result_link = request.POST.get('res_link')
            result_num = int(request.POST.get('res_number'))

        else:
            result_link = Links.objects.get(id=link_id).link
            result_num = None

        free_access = int(request.POST.get('free_access'))
        if free_access == 1:
            site_type = int(request.POST.get('site_type'))
            content_producer = int(request.POST.get('content_producer'))
            recent_information = int(request.POST.get('recent'))
            author_background = int(request.POST.get('author'))
            scientific_background = int(request.POST.get('scientific_background'))
            scientific_terms = int(request.POST.get('dont_understand'))
            explanations = None
            if scientific_terms == 1:
                explanations = int(request.POST.get('explanations'))
            scientific_errors = int(request.POST.get('errors'))
            scientific_errors_sureness = int(request.POST.get('sureness_errors'))
            scientific_accuracy = int(request.POST.get('accuracy'))
            scientific_accuracy_sureness = int(request.POST.get('sureness_accuracy'))
            sources_list = request.POST.getlist('sources')
            available_sources = ", ".join(sources_list)
            life_references = int(request.POST.get('everyday'))
            local_examples = int(request.POST.get('examples'))
            content_present = int(request.POST.get('risk_contribute'))
            conspiracy_theory = None
            malicious_meaning = None
            scientific_explanations = None
            enemy_presented = None
            if int(category) == 4:
                conspiracy_theory = int(request.POST.get('theory'))
                malicious_meaning = int(request.POST.get('malicious'))
                scientific_explanations = int(request.POST.get('scientific_explanations'))
                enemy_presented = int(request.POST.get('enemy'))

            try:
                related_link = Links.objects.get(link=result_link, translatedtermid=term_id)
            except Links.DoesNotExist:
                related_link = Links.objects.create(link=result_link,
                                                    translatedtermid=term_id,
                                                    stopcodinglink=0)
            time_end = time.time()
            time_start = data_dict['time_start']
            new_coding_result = Searchresults(userid=user,
                                              resultnumber=result_num,
                                              linkid=related_link,
                                              freeaccess=free_access,
                                              sitetype=site_type,
                                              contentproducer=content_producer,
                                              recentinformation=recent_information,
                                              authorbackground=author_background,
                                              scientificbackground=scientific_background,
                                              scientificterms=scientific_terms,
                                              explanations=explanations,
                                              scientificerrors=scientific_errors,
                                              scientificerrorssureness=scientific_errors_sureness,
                                              scientificaccuracy=scientific_accuracy,
                                              scientificaccuracysureness=scientific_accuracy_sureness,
                                              availablesources=available_sources,
                                              lifereferences=life_references,
                                              localexamples=local_examples,
                                              contentpresent=content_present,
                                              conspiracytheory=conspiracy_theory,
                                              maliciousmeaning=malicious_meaning,
                                              scientificexplanations=scientific_explanations,
                                              enemypresented=enemy_presented,
                                              codingtime=(time_end-time_start)/60)

        else:
            try:
                related_link = Links.objects.get(link=result_link, translatedtermid=term_id)
            except Links.DoesNotExist:
                related_link = Links.objects.create(link=result_link,
                                                    translatedtermid=term_id,
                                                    stopcodinglink=1)
            new_coding_result = Searchresults(resultnumber=result_num,
                                              linkid=related_link,
                                              freeaccess=free_access)

        new_coding_result.save()
        return redirect('coding_submitted')

    translated_term = Translatedterms.objects.filter(id=translated_term_id).first()
    answers_text = Numtoanswer.objects.all()
    context = {'translated_term': translated_term, 'category': category,
               'link_id': link_id, 'answers_text': answers_text}

    return render(request, 'site_contributions/coding.html', context)


@never_cache
def coding_submitted(request):
    return render(request, 'site_contributions/coding_submitted.html')
# ===========================


# ===========================
# Suggesting Section
@login_required
@never_cache
def suggesting(request):
    if request.method == 'GET':
        # Filtering Suggestedterms objects where numberofusers > 5
        suggested_terms = Suggestedterms.objects.filter(numberofusers__gt=5)
        # Filtering Suggestedcategories objects where numberofusers > 5
        suggested_categories = Suggestedcategories.objects.filter(numberofusers__gt=5)
        return render(request, 'site_contributions/suggesting.html',
                      {'suggested_terms': suggested_terms, 'suggested_categories': suggested_categories})


def support_suggestion(request, suggestion_id, suggestion_type):
    suggestion = None
    if suggestion_type == 'Category':
        suggestion = get_object_or_404(Suggestedcategories, pk=suggestion_id)
    elif suggestion_type == 'Term':
        suggestion = get_object_or_404(Suggestedterms, pk=suggestion_id)
    else:
        # Handle invalid suggestion types here (optional)
        pass

    # Increment the numberofusers field by 1
    suggestion.numberofusers += 1
    suggestion.save()

    return redirect('suggesting')


@never_cache
def suggestion_submitted(request):
    suggest_name = request.POST.get('suggest')
    if request.POST.get('suggest_type') == 'Term':
        try:
            term = Suggestedterms.objects.get(name=suggest_name)
            term.numberofusers += 1
            term.save()
        except Suggestedterms.DoesNotExist:
            new_suggested_term = Suggestedterms()
            new_suggested_term.name = suggest_name
            new_suggested_term.numberofusers = 1
            new_suggested_term.save()

    elif request.POST.get('suggest_type') == 'Category':
        try:
            category = Suggestedcategories.objects.get(name=suggest_name)
            category.numberofusers += 1
            category.save()
        except Suggestedcategories.DoesNotExist:
            new_suggested_category = Suggestedcategories()
            new_suggested_category.name = suggest_name
            new_suggested_category.numberofusers = 1
            new_suggested_category.save()

    return render(request, 'site_contributions/suggestion_submitted.html')
# ===========================


# ===========================
# Translating Section
def get_basic_terms_to_translate(request):
    user = Participants.objects.get(username=request.user.username)
    category_id = request.GET.get('category')
    translated_terms = Translatedterms.objects.filter(langcountryid=user.langcountryid).values('basictermid')
    basic_terms = Basicterms.objects.filter(categoryid=category_id).exclude(id__in=Subquery(translated_terms))
    data = [{'id': term.id, 'name': term.name, 'helpText': term.contextExample} for term in basic_terms]
    return JsonResponse({'terms': data})


@login_required
@never_cache
def translating(request):
    user = Participants.objects.get(username=request.user.username)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('term'):
                term_id = key.split('_')[1]
                basic_term_obj = Basicterms.objects.filter(id=term_id).first()
                translation = value.lower()

                try:
                    suggested_translation = Suggestedtranslatedterms.objects.get(name=translation,
                                                                                 basictermid=basic_term_obj,
                                                                                 status='declined' or 'approved')
                # Handle the case when status is declined
                except Suggestedtranslatedterms.DoesNotExist:
                    Suggestedtranslatedterms.objects.create(name=translation,
                                                            basictermid=basic_term_obj,
                                                            userid=user,
                                                            status='suggested')

        return redirect('translating_submitted')
    else:
        categories = Categories.objects.all().order_by('name')
        return render(request, "site_contributions/translating.html", {'categories': categories, 'language': user.langcountryid.languageid})


@never_cache
def translating_submitted(request):
    return render(request, 'site_contributions/translating_submitted.html')
# ===========================


# ===========================
# Contact Us Section
# ===========================
@never_cache
def contact_submitted(request):
    name = str(request.POST.get('name'))
    phone = str(request.POST.get('phone'))
    email = request.POST.get('email')
    message = request.POST.get('message')
    send_mail('You received an email From ' + name,  # title
              'Dear researches,\n' + message + '\nYou can contact me on that number: ' + phone
              + '\n Or contact me at my mail: ' + email + '\nSincerely,' + name,  # message
              email,
              [settings.EMAIL_HOST_USER],
              fail_silently=False,
              )
    return render(request, 'contact_submitted.html')
# ===========================


# ===========================
# Profile Section
@login_required
@never_cache
def profile_page(request, username):
    if request.method == 'POST':
        user = request.user
        original_email = user.email
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            user_email = user.email
            if original_email != user_email:
                # Send confirmation mail
                user.is_active = False
                user.save()

                username = user.username
                current_site = get_current_site(request)
                mail_subject = 'Confirm Your Registration'
                message = render_to_string('registration/confirmation_email_change.html', {
                    'user': username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                })
                email = EmailMessage(
                    mail_subject, message, to=[user_email]
                )
                email.send()
                return redirect('change_email_confirmation')

            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()

    if user:
        form = UserUpdateForm(instance=user)

        trained_categories = user.trainedcategories
        categories = []
        categories_names = []
        if (trained_categories is not None) and (trained_categories != ''):
            for cat in trained_categories.split(', '):
                categories.append(Categories.objects.get(id=int(cat)))
                categories_names.append(Categories.objects.get(id=int(cat)).name)

        langCountryId = user.langcountryid
        countryName = langCountryId.countryid.name
        langName = langCountryId.languageid.name

        return render(request, "profile_section/profile_page.html", {'form': form, 'categories': categories,
                                                     'categories_names': categories_names,
                                                     'countryName': countryName,
                                                     'langName': langName})

    return redirect("home")


@never_cache
def change_email_confirmation(request):
    return render(request, 'registration/change_email_confirmation.html')


def activate_email_change(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'{user.username}, Your profile has been updated!')
        return redirect('profile', user.username)
    else:
        return HttpResponse('Activation link is invalid.')


@never_cache
def edit_profile_picture(request):
    if request.method == 'POST':
        user = request.user
        user.profile_avatar = request.POST.get("profile_photo")
        user.save()
        return redirect('profile', user.username)

    icon_list_women = [f"images/profile_imgs/Women/ProfilePhoto{i}.png" for i in range(1, 10)]
    icon_list_men = [f"images/profile_imgs/Men/ProfilePhoto{i}.png" for i in range(1, 10)]
    return render(request, 'profile_section/edit_profile_picture.html', {'icon_list_women': icon_list_women,
                                                         'icon_list_men': icon_list_men})
# ===========================


# ===========================
# Logout Section
@login_required
@never_cache
def logout(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        if user.usertype == 'guest':
            user.is_active = False
            user.save()
    auth.logout(request)
    request.session.flush()
    return redirect('custom_logout')


def custom_logout(request):
    return render(request, 'registration/logged_out.html')
# ===========================
