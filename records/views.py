from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import connection
from .models import Person, PersonPhoneNumber, Patient, Doctor, Appointment, MedicalRecord, Prescription, Billing
from datetime import datetime

def index(request):
    """Main menu view"""
    # Check if database is initialized
    is_initialized = Person.objects.exists()
    return render(request, 'records/index.html', {'is_initialized': is_initialized})


def create_tables(request):
    """Create and populate tables with sample data"""
    if request.method == 'POST':
        # Clear existing data
        Billing.objects.all().delete()
        Prescription.objects.all().delete()
        MedicalRecord.objects.all().delete()
        Appointment.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        PersonPhoneNumber.objects.all().delete()
        Person.objects.all().delete()

        # Create Persons
        person1 = Person.objects.create(person_id=1, first_name='John', last_name='Doe', 
                                       email='john.doe@email.com', phone_number='416-555-0101')
        person2 = Person.objects.create(person_id=2, first_name='Jane', last_name='Smith', 
                                       email='jane.smith@email.com', phone_number='416-555-0102')
        person3 = Person.objects.create(person_id=3, first_name='Sarah', last_name='Johnson', 
                                       email='dr.johnson@hospital.com', phone_number='416-555-0201')
        person4 = Person.objects.create(person_id=4, first_name='Michael', last_name='Brown', 
                                       email='dr.brown@hospital.com', phone_number='416-555-0202')
        person5 = Person.objects.create(person_id=5, first_name='Emily', last_name='Davis', 
                                       email='emily.davis@email.com', phone_number='416-555-0103')

        # Create Person Phone Numbers
        PersonPhoneNumber.objects.create(person=person1, phone_number='416-555-0101')
        PersonPhoneNumber.objects.create(person=person1, phone_number='647-555-0101')
        PersonPhoneNumber.objects.create(person=person2, phone_number='416-555-0102')
        PersonPhoneNumber.objects.create(person=person3, phone_number='416-555-0201')
        PersonPhoneNumber.objects.create(person=person4, phone_number='416-555-0202')
        PersonPhoneNumber.objects.create(person=person5, phone_number='416-555-0103')

        # Create Patients
        patient1 = Patient.objects.create(person=person1, age=35, date_of_birth='1989-05-15',
                                         street='123 Main St', city='Toronto', postal_code='M5V 2T6')
        patient2 = Patient.objects.create(person=person2, age=42, date_of_birth='1982-08-22',
                                         street='456 Oak Ave', city='Toronto', postal_code='M4W 1A1')
        patient3 = Patient.objects.create(person=person5, age=28, date_of_birth='1996-12-10',
                                         street='789 Elm St', city='Mississauga', postal_code='L5B 3Y4')

        # Create Doctors
        doctor1 = Doctor.objects.create(person=person3, specialization='Cardiology')
        doctor2 = Doctor.objects.create(person=person4, specialization='General Practice')

        # Create Appointments
        apt1 = Appointment.objects.create(appointment_id=1, appointment_date='2024-11-25',
                                         reason='Annual Checkup', patient=patient1, doctor=doctor1)
        apt2 = Appointment.objects.create(appointment_id=2, appointment_date='2024-11-26',
                                         reason='Follow-up Visit', patient=patient2, doctor=doctor2)
        apt3 = Appointment.objects.create(appointment_id=3, appointment_date='2024-11-27',
                                         reason='Consultation', patient=patient3, doctor=doctor1)

        # Create Medical Records
        record1 = MedicalRecord.objects.create(record_id=1, record_date='2024-11-25',
                                              treatment='Blood Pressure Medication',
                                              diagnosis='Hypertension', patient=patient1, appointment=apt1)
        record2 = MedicalRecord.objects.create(record_id=2, record_date='2024-11-26',
                                              treatment='Physical Therapy',
                                              diagnosis='Back Pain', patient=patient2, appointment=apt2)

        # Create Prescriptions
        Prescription.objects.create(prescription_id=1, medicine_name='Lisinopril',
                                   dosage='10mg', duration='30 days', record=record1)
        Prescription.objects.create(prescription_id=2, medicine_name='Ibuprofen',
                                   dosage='400mg', duration='14 days', record=record2)

        # Create Billings
        Billing.objects.create(bill_id=1, amount=150.00, payment_status='Paid', appointment=apt1)
        Billing.objects.create(bill_id=2, amount=200.00, payment_status='Pending', appointment=apt2)
        Billing.objects.create(bill_id=3, amount=175.00, payment_status='Paid', appointment=apt3)

        return JsonResponse({'status': 'success', 'message': 'Database initialized with sample data!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def drop_tables(request):
    """Drop all tables (delete all data)"""
    if request.method == 'POST':
        Billing.objects.all().delete()
        Prescription.objects.all().delete()
        MedicalRecord.objects.all().delete()
        Appointment.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        PersonPhoneNumber.objects.all().delete()
        Person.objects.all().delete()
        
        return JsonResponse({'status': 'success', 'message': 'All tables dropped successfully!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def query_tables(request):
    """Query and search tables"""
    table = request.GET.get('table', 'person')
    search = request.GET.get('search', '')

    data = []
    
    if table == 'person':
        queryset = Person.objects.all()
        if search:
            queryset = queryset.filter(first_name__icontains=search) | queryset.filter(last_name__icontains=search) | queryset.filter(email__icontains=search)
        data = list(queryset.values())
    
    elif table == 'patient':
        queryset = Patient.objects.select_related('person').all()
        if search:
            queryset = queryset.filter(person__first_name__icontains=search) | queryset.filter(person__last_name__icontains=search) | queryset.filter(city__icontains=search)
        data = [{'person_id': p.person.person_id, 'name': str(p.person), 'age': p.age, 
                 'date_of_birth': p.date_of_birth, 'street': p.street, 'city': p.city, 
                 'postal_code': p.postal_code} for p in queryset]
    
    elif table == 'doctor':
        queryset = Doctor.objects.select_related('person').all()
        if search:
            queryset = queryset.filter(person__first_name__icontains=search) | queryset.filter(person__last_name__icontains=search) | queryset.filter(specialization__icontains=search)
        data = [{'person_id': d.person.person_id, 'name': str(d.person), 
                 'specialization': d.specialization} for d in queryset]
    
    elif table == 'appointment':
        queryset = Appointment.objects.select_related('patient__person', 'doctor__person').all()
        if search:
            queryset = queryset.filter(reason__icontains=search)
        data = [{'appointment_id': a.appointment_id, 'appointment_date': a.appointment_date,
                 'reason': a.reason, 'patient': str(a.patient.person), 
                 'doctor': str(a.doctor.person)} for a in queryset]
    
    elif table == 'medical_record':
        queryset = MedicalRecord.objects.select_related('patient__person', 'appointment').all()
        if search:
            queryset = queryset.filter(diagnosis__icontains=search) | queryset.filter(treatment__icontains=search)
        data = [{'record_id': m.record_id, 'record_date': m.record_date,
                 'treatment': m.treatment, 'diagnosis': m.diagnosis,
                 'patient': str(m.patient.person), 'appointment_id': m.appointment.appointment_id} for m in queryset]
    
    elif table == 'prescription':
        queryset = Prescription.objects.select_related('record').all()
        if search:
            queryset = queryset.filter(medicine_name__icontains=search)
        data = [{'prescription_id': p.prescription_id, 'medicine_name': p.medicine_name,
                 'dosage': p.dosage, 'duration': p.duration, 
                 'record_id': p.record.record_id} for p in queryset]
    
    elif table == 'billing':
        queryset = Billing.objects.select_related('appointment').all()
        if search:
            queryset = queryset.filter(payment_status__icontains=search)
        data = [{'bill_id': b.bill_id, 'amount': str(b.amount),
                 'payment_status': b.payment_status, 
                 'appointment_id': b.appointment.appointment_id} for b in queryset]

    return JsonResponse({'data': data})


def manage_records(request):
    """View for managing records"""
    return render(request, 'records/manage.html')


def add_person(request):
    """Add a new person record"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        
        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone
        )
        
        return JsonResponse({'status': 'success', 'message': 'Person added successfully!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def delete_person(request, person_id):
    """Delete a person record"""
    if request.method == 'POST':
        person = get_object_or_404(Person, person_id=person_id)
        person.delete()
        return JsonResponse({'status': 'success', 'message': 'Person deleted successfully!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})