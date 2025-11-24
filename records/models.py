from django.db import models

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'person'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonPhoneNumber(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)

    class Meta:
        db_table = 'person_phone_number'
        unique_together = ('person', 'phone_number')

    def __str__(self):
        return f"{self.person} - {self.phone_number}"


class Patient(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return str(self.person)


class Doctor(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f"Dr. {self.person}"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.appointment_date}"


class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    record_date = models.DateField()
    treatment = models.CharField(max_length=255, blank=True, null=True)
    diagnosis = models.CharField(max_length=255, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'medical_record'

    def __str__(self):
        return f"Record {self.record_id} - {self.patient}"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)

    class Meta:
        db_table = 'prescription'

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"


class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=255, blank=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing'

    def __str__(self):
        return f"Bill {self.bill_id} - ${self.amount}"