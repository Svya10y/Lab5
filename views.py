from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ValidationError
from .models import Task


def archive(request):
    return render(request, 'archive.html', {"posts": Task.objects.all()})


def get_task(request, task_id):
    try:
        post = Task.objects.get(id=task_id)
        return render(request, 'task.html', {"post": post})
    except Task.DoesNotExist:
        raise Http404


def create_task(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # в словаре form хранится информация, введенная пользователем
            form = {
                'title': request.POST["title"],
                'client': request.POST["client"],
                'contact': request.POST["contact"],
                'department': request.POST["department"],
                'employee': request.POST["employee"],
                'issue_date': request.POST["issue_date"],
                'hours': request.POST["hours"],
                'hour_rate': request.POST["hour_rate"],
                'discount': request.POST["discount"],
                'text': request.POST["text"],
            }
            required = ['title', 'client', 'contact', 'department', 'employee', 'issue_date',
                        'hours', 'hour_rate', 'discount', 'text']
            if all(form[name] for name in required):
                # проверка уникальности названия задания
                if Task.objects.filter(title=form["title"]).exists():
                    form['errors'] = "Задание с таким названием уже существует"
                    return render(request, 'create_task.html', {'form': form})
                try:
                    # если поля заполнены без ошибок, создается новая запись
                    task = Task.objects.create(
                        title=form["title"],
                        client=form["client"],
                        contact=form["contact"],
                        department=form["department"],
                        employee=form["employee"],
                        issue_date=form["issue_date"],
                        hours=form["hours"],
                        hour_rate=form["hour_rate"],
                        discount=form["discount"],
                        text=form["text"],
                        author=request.user
                    )
                except (ValueError, ValidationError):
                    form['errors'] = "Проверьте правильность чисел и дат"
                    return render(request, 'create_task.html', {'form': form})
                # переход на страницу созданной записи
                return redirect('get_task', task_id=task.id)
            else:
                # если введенные данные некорректны
                form['errors'] = "Не все поля заполнены"
                return render(request, 'create_task.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_task.html', {})
    else:
        raise Http404
