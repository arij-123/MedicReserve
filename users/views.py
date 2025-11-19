from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Medecin,RendezVous
# Create your views here.




def index(request):
    return render(request, 'users/index.html', {'user': request.user})

def departments_view(request):
    medecins = Medecin.objects.all()
    print("Nombre de médecins :", medecins.count())  # Debug

    return render(request, 'users/departments.html', {'medecins': medecins})

User = get_user_model()

def login_view(request):
    error_msg = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authentifier directement avec email
        user = User.objects.filter(email=email).first()  # cherche l'utilisateur
        if user:
            # vérifier le mot de passe
            if user.check_password(password):
                auth_login(request, user)   # connecte l'utilisateur
                return redirect('index')  # va directement à la page d'accueil
            else:
                error_msg = "Mot de passe incorrect."
        else:
            error_msg = "Email non trouvé."

    return render(request, 'users/login.html', {'error_msg': error_msg})



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Vérifier si les mots de passe correspondent
        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'users/register.html')

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'users/register.html')

        # Créer l'utilisateur
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
        return redirect('login')  # Redirige vers login après inscription

    return render(request, 'users/register.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')






def details_view(request, specialty):
    medecins = Medecin.objects.filter(specialty=specialty)
    return render(request, 'users/details.html', {
        'medecins': medecins,
        'specialty': specialty
    })


# views.py
def reserver_rdv(request, med_id):
    medecin_instance = get_object_or_404(Medecin, id=med_id)
    horaires_morinig = "09:00,09:30,10:00,10:30,11:00,11:30,12:00,12:30".split(',')
    horaires_evening = "15:00,15:30,16:00,16:30,17:00,17:30,18:00,18:30".split(',')
    if request.method == "POST":
        selected_time = request.POST.get('time')
        selected_date = request.POST.get('date')
        # ici tu peux enregistrer la réservation
        pass

    return render(request, 'users/reservation.html', {
        'medecin': medecin_instance,
        'horaires_mor': horaires_morinig,
        'horaires_even': horaires_evening
    })

#def appointment(request, med_id):
    medecin_instance = get_object_or_404(Medecin, id=med_id)

    horaires = "07:00,08:00,09:00,10:00,11:00,12:00,13:00,14:00,15:00,16:00,17:00,18:00".split(',')

    if request.method == "POST":
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')

        # --- Enregistrer le RDV dans PostgreSQL ---
        rdv = RendezVous.objects.create(
            medecin=medecin_instance,
            date=selected_date,
            time=selected_time
        )

        # Message ou redirection
        messages.success(request, "Your appointment has been successfully booked!")
        return redirect('home')   # ou vers une page de confirmation

    return render(request, 'users/reservation.html', {
        'medecin': medecin_instance,
        'horaires': horaires
    })

 
def verifier_user(request, medecin_id):
    medecin = get_object_or_404(Medecin, id=medecin_id)

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        date = request.POST.get("date")
        time = request.POST.get("time")

        try:
            user = User.objects.get(first_name=firstname, last_name=lastname)
        except User.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé.")
            return render(request, "users/verif_user.html", {"medecin": medecin})

        # Créer le rendez-vous
        RendezVous.objects.create(
            id_patient=user,
            id_med=medecin,
            date=date,
            time=time
        )

        messages.success(request, f"Rendez-vous réservé avec {medecin} le {date} à {time}")
        return redirect('reservation_success')

    # GET → afficher le formulaire
    return render(request, "users/verif_user.html", {"medecin": medecin})


# Traitement du formulaire

   


def reservation_success(request):
    return render(request, "users/success.html")