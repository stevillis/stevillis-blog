from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from home.forms import ContactForm
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
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            subject = f"Contato do site - {name}"
            body = (
                f"Nome: {name}\nEmail: {email}\nTelefone: {phone}\nMensagem: {message}"
            )

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL_RECIPIENT],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    "Mensagem enviada com sucesso! Em breve entrarei em contato com você. 😊",
                )

                return redirect("contact")
            except Exception:
                messages.error(
                    request, "Erro ao enviar e-mail. Por favor, tente novamente."
                )

                return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


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
