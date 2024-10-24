from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import FriendForm
from .models import Friend

from django.views import View

def indexView(request):
    form = FriendForm()
    friends = Friend.objects.all()
    return render(request, "index.html", {"form": form, "friends": friends})


def postFriend(request):
    # Verificar si el método es POST
    if request.method == "POST":
        # Obtener los datos del formulario
        form = FriendForm(request.POST)
        
        # Validar el formulario
        if form.is_valid():
            # Guardar el objeto y obtener la instancia
            instance = form.save()
            # Serializar el nuevo amigo en JSON
            ser_instance = serializers.serialize('json', [instance])
            # Enviar la respuesta JSON al cliente
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # Devolver los errores de formulario
            return JsonResponse({"error": form.errors}, status=400)

    # Si no es un POST
    return JsonResponse({"error": "Método no permitido"}, status=400)


def checkNickName(request):
    # Agregar mensajes de depuración
    print(f"Request method: {request.method}")
    print(f"Request GET data: {request.GET}")

    # Verificar que sea una solicitud GET
    if request.method == "GET":
        # Obtener el nick_name desde la solicitud
        nick_name = request.GET.get("nick_name", None)
        print(f"Nick name: {nick_name}")

        if nick_name:
            # Verificar si el nickname ya existe en la base de datos
            if Friend.objects.filter(nick_name=nick_name).exists():
                return JsonResponse({"valid": False}, status=200)
            else:
                return JsonResponse({"valid": True}, status=200)

    # Si no se recibe correctamente el nick_name o hay un error en la solicitud
    return JsonResponse({"error": "Solicitud inválida"}, status=400)


# Clase FriendView (Class Based View)
class FriendView(View):
    form_class = FriendForm
    template_name = "index.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name, 
                      {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        # Verificar que la solicitud sea AJAX y el método sea POST
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' and self.request.method == "POST":
            # Obtener los datos del formulario
            form = self.form_class(self.request.POST)
            # Guardar los datos y luego obtener la instancia creada
            if form.is_valid():
                instance = form.save()
                # Serializar la nueva instancia en JSON
                ser_instance = serializers.serialize('json', [instance])
                # Enviar al lado del cliente
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # Ocurrieron errores en el formulario
                return JsonResponse({"error": form.errors}, status=400)

        # Si algo falla, devolver error
        return JsonResponse({"error": ""}, status=400)
