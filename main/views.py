from django.shortcuts import render
from .forms import ReclamoForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

user_states = {}

def home(request):
    return render(request, 'pantallas/index.html')

def pantalla2(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        name = request.POST.get('name')
        return render(request, 'pantallas/screen2.html', {'rut': rut, 'name': name})
    return render(request, 'pantallas/screen2.html')

def atencion_cliente(request):
    return render(request, 'pantallas/atencion.html')

def atenciondos(request):
    numero = request.GET.get('numero')
    opcion = request.GET.get('opcion')
    return render(request, 'pantallas/atencion2.html', {'numero': numero, 'opcion': opcion})

def chat_ia(request):
    return render(request, 'pantallas/chat-ia.html')

def reclamo(request):
    return render(request, 'pantallas/reclamo.html')

def reclamo(request):
    form = ReclamoForm()

    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            descripcion = form.cleaned_data['descripcion']
            
            to = 'reclamos@atlasxd.online'
            subject = 'Nuevo Reclamo - Atlas XD'
            message = f"Nuevo reclamo recibido:\n\nNombre: {nombre}\nCorreo: {email}\nDescripción:\n{descripcion}\n"
            headers = {'Reply-To': email}
            
            send_mail(subject, message, email, [to], headers=headers)
            
            return render(request, 'pantallas/reclamo.html', {'form': ReclamoForm(), 'success': True})

    return render(request, 'pantallas/reclamo.html', {'form': form})


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").lower()
            user_id = request.session.session_key
            
            if user_id not in user_states:
                user_states[user_id] = {"step": 0, "data": {}}

            state = user_states[user_id]

            if state["step"] == 0:
                state["step"] += 1
                response = "Hola, ¿qué malestar o dolor tienes?"
            elif state["step"] == 1:
                state["data"]["symptom"] = user_message
                state["step"] += 1
                response = "¿Cuántos años tienes?"
            elif state["step"] == 2:
                if not user_message.isdigit():
                    response = "Por favor, ingresa un número válido para tu edad."
                else:
                    state["data"]["age"] = int(user_message)
                    state["step"] += 1
                    response = "¿Tienes alguna enfermedad crónica como hipertensión o diabetes?"
            elif state["step"] == 3:
                state["data"]["chronic_conditions"] = user_message
                state["step"] += 1
                response = "¿Eres alérgico a algún medicamento?"
            elif state["step"] == 4:
                state["data"]["allergies"] = user_message
                state["step"] += 1
                response = "¿Tienes fiebre o algún otro síntoma?"
            elif state["step"] == 5:
                state["data"]["other_symptoms"] = user_message

                recommendation = generate_recommendation(state["data"])
                response = recommendation

                user_states[user_id] = {"step": 0, "data": {}}

                return JsonResponse({"response": response, "final_step": True})

            return JsonResponse({"response": response, "final_step": False})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Solicitud no válida"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def generate_recommendation(data):
    symptom = data.get("symptom", "").lower()
    age = data.get("age", 0)
    chronic_conditions = data.get("chronic_conditions", "").lower()
    allergies = data.get("allergies", "").lower()
    other_symptoms = data.get("other_symptoms", "").lower()

    if "cabeza" in symptom:
        if "alérgico" in allergies and "ibuprofeno" in allergies:
            return "Para el dolor de cabeza, puedes tomar Paracetamol (500mg). Consulta a un médico si el dolor persiste."
        if "hipertensión" in chronic_conditions:
            return "Para el dolor de cabeza, evita medicamentos como Ibuprofeno. Puedes tomar Paracetamol (500mg). Consulta a un médico si el dolor persiste."
        return "Para el dolor de cabeza, puedes tomar Ibuprofeno (400mg). Consulta a un médico si el dolor persiste."

    if "fiebre" in symptom or "fiebre" in other_symptoms:
        if age < 12:
            return "Para la fiebre en niños, consulta a un médico antes de administrar medicamentos. Puedes aplicar compresas frías y mantener una buena hidratación."
        if "diabetes" in chronic_conditions:
            return "Para la fiebre, toma Paracetamol (500mg cada 6 horas) y asegúrate de controlar tus niveles de glucosa. Consulta a un médico si la fiebre no baja."
        return "Para la fiebre, toma Paracetamol (500mg cada 6 horas). Asegúrate de hidratarte bien y consulta a un médico si la fiebre no baja."

    if "garganta" in symptom:
        if age > 60:
            return "Para el dolor de garganta en personas mayores, mantente hidratado con líquidos tibios y consulta a un médico si el dolor persiste. Evita auto medicarte."
        return "Para el dolor de garganta, puedes hacer gárgaras con agua tibia y sal. Si el dolor persiste, consulta a un médico."

    if "muscular" in symptom or "músculo" in symptom:
        if "hipertensión" in chronic_conditions:
            return "Para el dolor muscular, evita Ibuprofeno si tienes hipertensión. Aplica compresas calientes y consulta a un médico si el dolor persiste."
        if "alérgico" in allergies and "ibuprofeno" in allergies:
            return "Para el dolor muscular, aplica compresas calientes en la zona afectada. Consulta a un médico si el dolor persiste."
        return "Para el dolor muscular, puedes tomar Ibuprofeno (400mg) y aplicar compresas calientes. Consulta a un médico si el dolor persiste."

    if "estómago" in symptom or "estomacal" in symptom:
        if "reflujo" in chronic_conditions or "gastritis" in chronic_conditions:
            return "Para el malestar estomacal, evita comidas pesadas y ácidas. Consulta a un médico para evaluar el uso de un antiácido seguro."
        return "Para el malestar estomacal, evita comidas pesadas y mantente hidratado. Puedes tomar un antiácido si tienes acidez. Consulta a un médico si el malestar continúa."

    if "tos" in symptom:
        if "asma" in chronic_conditions:
            return "Para la tos, asegúrate de utilizar tu inhalador según las indicaciones médicas. Consulta a un médico si la tos persiste."
        if age > 60:
            return "Para la tos en personas mayores, consulta a un médico. Bebe líquidos tibios y usa un humidificador si tienes congestión."
        return "Para la tos, bebe líquidos tibios como té con miel. Si tienes congestión, un humidificador puede ayudarte. Consulta a un médico si la tos persiste más de 3 días."

    return "Lo siento, no tengo suficiente información para darte una recomendación. Por favor consulta a un médico."
