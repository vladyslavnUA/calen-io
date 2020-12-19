import datetime
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import Calendar
from .forms import *
from .emails import *

def index(request):
    return HttpResponse('hello')

def send_email_attachment(request, title, description, start_time, end_time, send_to, message):
    user_email = request.user.email
    message = EmailMultiAlternatives(subject=title, body=description,from_email=user_email, to=[send_to])
    html_templ = get_template("cal/email.html").render({'title':title, 'description': description, "start_time":start_time, "end_time":end_time, "send_to":send_to, 'message':message,})
    message.attach_alternative(html_templ, "text/html")
    message.send()
    print("email sent")

def detail(request, event_id=None):
    context = {}
    print(event_id)
    print(request.user.email)
    template_name = 'cal/detail.html'

    if not request.user.is_authenticated:
        return HttpResponse('oops, 404')
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
        length = (event.start_time - event.end_time)
        # length.strtime('%Y-%m-%d')
        event.save()
        context['event'] = event
        context['length'] = length
        if request.method == 'GET':
            form = EmailForm(request.POST)
        if request.method == 'POST':
            form = EmailForm(request.POST)
        # all_files = request.FILES.getlist('files')
            if form.is_valid():
                obj = form.save(commit=False)
                # title, description, start_time, end_time, send_to
                obj.title = event.title
                obj.description = event.description
                obj.start_time = event.start_time
                obj.end_time = event.end_time
                obj.send_to = request.POST.get('to')
                obj.message = request.POST.get('message')
        #     recipient_list = [form.cleaned_data.get("to")]
        #     files = form.cleaned_data.get("all_files")
        #     subject = form.cleaned_data.get("subject")
        #     message = form.cleaned_data.get("message")
        #     message += str(files)
        #     email_from = 'welcome.amongus@gmail.com'

        #     obj.to = recipient_list
        #     obj.subject = subject
        #     obj.message = message
        #     obj.files = all_files
                obj.save()
                # title, description, start_time, end_time, send_to, message
                send_email_attachment(request, event.title, event.description, event.start_time, event.end_time, obj.send_to, obj.message)
            # htmly = get_template('cal/email.html')
            # send_email_attachment()
            # html_content = htmly.render({'order':order, "email":email, 'mattress': mattress})
            # send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                print('sent')
            else:
                form = EmailForm()
            context['form'] = form
        context['form'] = form
        #     return HttpResponse('404')
            # form = EmailForm()
    # if request.method == 'GET':
    #     return render(request, template_name, context)
    # context = {'form': form}
    


    # event = get_object_or_404(Event, pk=event_id)
    return render(request, template_name, context)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        today = datetime.now().date()
        context['today'] = today
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        # print(f'{event.get_html_url}')
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})