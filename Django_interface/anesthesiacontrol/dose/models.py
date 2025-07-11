from django.db import models
from django.utils import timezone

class PatientRecord(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    code = models.CharField(max_length=10, unique=True, blank=True)
    co2_levels = models.JSONField(default=list)
    heart_rate = models.JSONField(default=list)
    respiration_rate = models.JSONField(default=list)
    spo2_levels = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.code} - {self.name} (Age: {self.age})"

    def save(self, *args, **kwargs):
        if not self.code:  # Generate code only if it doesn't exist
            name_part = self.name[:2].upper()
            base_code = f"{name_part}{self.age}"
            self.code = base_code

            # Ensure the code is unique
            counter = 1
            while PatientRecord.objects.filter(code=self.code).exists():
                self.code = f"{base_code}{counter}"
                counter += 1
        super().save(*args, **kwargs)  # Call the parent save method