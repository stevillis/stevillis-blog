import random
import re

from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from home.models import Blog


# Create your views here.
def index(request):
    recent_blogs = Blog.objects.all().order_by("-created_at")[:3]
    context = {"recent_blogs": recent_blogs}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def thanks(request):
    return render(request, "thanks.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        invalid_input = ["", " "]
        if (
            name in invalid_input
            or email in invalid_input
            # or phone in invalid_input
            or message in invalid_input
        ):
            messages.error(request, "Um ou mais campos estão vazios!")
        else:
            email_pattern = re.compile(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            )
            # phone_pattern = re.compile(r"^[0-9]{10}$")

            if email_pattern.match(email):
                form_data = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "message": message,
                }

                message = f"""
                From:\n\t\t{form_data["name"]}\n
                Message:\n\t\t{form_data["message"]}\n
                Email:\n\t\t{form_data["email"]}\n
                Phone:\n\t\t{form_data["phone"]}\n
                """

                send_mail(
                    subject="Alguém te mandou um email via site!",
                    from_email=email,
                    message=message,
                    recipient_list=["stevillis@hotmail.com"],
                )

                messages.success(request, "Mensagem enviada com sucesso!")
                # return HttpResponseRedirect('/thanks')
            else:
                messages.error(request, "Email ou telefone inválido!")

    return render(request, "contact.html")


def projects(request):
    return render(request, "projects.html")


def blog(request):
    blogs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs, 10)
    page = request.GET.get("page")
    blogs = paginator.get_page(page)
    context = {"blogs": blogs}

    return render(request, "blog.html", context)


def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by("-created_at")
    if not category_posts:
        message = f"Nenhum post encontrado para a categoria: '{category}'."
        context = {"message": message}

        return render(request, "category.html", context)

    paginator = Paginator(category_posts, 3)
    page = request.GET.get("page")
    category_posts = paginator.get_page(page)
    context = {"category": category, "category_posts": category_posts}

    return render(request, "category.html", context)


def categories(request):
    categories = Blog.objects.values("category").distinct().order_by("category")

    context = {"categories": categories}

    return render(request, "categories.html", context)


def search(request):
    query = request.GET.get("q")
    query_list = query.split()
    results = Blog.objects.none()

    for word in query_list:
        results = results | Blog.objects.filter(
            Q(title__contains=word) | Q(content__contains=word)
        ).order_by("-created_at")

    paginator = Paginator(results, 3)
    page = request.GET.get("page")
    results = paginator.get_page(page)

    message = ""
    if len(results) == 0:
        message = f"Nenhum resultado encontrado para a busca: '{query}'."

    context = {"query": query, "results": results, "message": message}

    return render(request, "search.html", context)


def blogpost(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
        context = {"blog": blog}

        return render(request, "blogpost.html", context)
    except Blog.DoesNotExist:
        context = {"message": "Post não encontrado."}
        return render(request, "404.html", context, status=404)


def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)


def custom_server_error(request):
    return render(request, "500.html", status=500)
