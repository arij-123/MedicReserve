from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Medecin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    governorate = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialty})"

    class Meta:
      #  managed = False  # ❗ Django ne crée/modifie pas la table
        db_table = 'medecin'  # nom exact de ta table dans pgAdmin

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class RendezVous(models.Model):
    id_RDV = models.AutoField(primary_key=True, db_column='id_RDV')
    id_patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rendezvous",
        db_column='id_patient'
    )
    id_med = models.ForeignKey(
        Medecin,
        on_delete=models.CASCADE,
        related_name="rendezvous",
        db_column='id_med'
    )
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rdv'

    def __str__(self):
        return f"RDV {self.id_patient} avec {self.id_med} le {self.date} à {self.time}"
