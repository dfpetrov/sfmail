from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .models import Letter, SentLetter

def index(request):
    context = {}
    return render(request, 'appmain/index.html', context)


def plan(request):
    letter_qs = Letter.objects.all().order_by('-created')[0:10]
    letters = []
    for letter in letter_qs:
        sent_letter = SentLetter.objects.filter(letter=letter)
        if sent_letter:
            from datetime import datetime, timedelta
            letters.append({'letter': letter, 'plan_date': letter.created+timedelta(seconds=letter.delay), 'status': sent_letter[0].status})
        else:
            from datetime import datetime, timedelta
            letters.append({'letter': letter, 'plan_date': letter.created+timedelta(seconds=letter.delay), 'status': 'не отправлено'})

    context = {
        'letters': letters
    }
        
    return render(request, 'appmain/plan.html', context)


def add_new_mail(request):
    """
    Функция добавляет письмо в базу
    """
    mail_data = {
        'subject': 'Тестовое письмо',
        'email': request.POST.get('email'),
        'message': request.POST.get('message'),
        'delay': int(request.POST.get('delay')),
    }

    if mail_data['email'] and mail_data['message']:
        
        # создаем письмо
        Letter.objects.create(
            subject=f"Тестовое письмо. Задержка {mail_data['delay']} сек",
            email=mail_data['email'], 
            message=mail_data['message'],
            delay=mail_data['delay'],
        )

        # запускаем отправку всех писем
        sent_all_mails()

        return HttpResponseRedirect(reverse_lazy('appmain:plan'))
    else:
        return JsonResponse('Не все поля заполнены')

def sent_all_mails():
    
    import threading
    
    # создаем список тредов
    threads = []

    # получаем все письма из базы
    letters = Letter.objects.all()

    for letter in letters:
        
        if not SentLetter.objects.filter(letter=letter):
            
            # добавляем письмо в отправленные
            sent_letter = SentLetter.objects.create(letter=letter, status='ожидает отправки')

            # открываем тред для отправки письма
            t = threading.Thread(target=sent_mail, args=(letter, sent_letter, ))
            
            # добавляем тред в список тредов
            threads.append(t)

            # стартуем тред
            t.start()
            

    # закрываем все треды
    for t in threads:
        t.join()


def sent_mail(letter, sent_letter):
    """
    Функция для отправки письма
    """
    
    import time

    # Cпим. Время сна = задержка из письма (поле delay)
    time.sleep(letter.delay)
    
    # после сна отправляем письмо
    send_mail(
        letter.subject,
        letter.message,
        'dfpetrov@mail.ru',
        [letter.email],
    )

    sent_letter.status = 'отправлено'
    sent_letter.save()

    return JsonResponse({'response': 'ok'})
