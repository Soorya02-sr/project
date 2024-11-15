from django.contrib import admin
from django.utils import timezone
from .models import Patient, Appointment, Doctor, Notification, Feedback
from django import forms
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'get_username','age', 'mobile', 'gender', 'place']
    search_fields = ('mobile',)
    list_filter = ('place',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['app_id', 'token','patient', 'doctor', 'case', 'date','time','slot', 'status']
    search_fields = ('doctor','status')
    list_filter = ('date', 'doctor','time')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'get_username', 'doc_name', 'email', 'phone', 'special', 'Dept', 'quali','exp', 'status']
    search_fields = ('special',)
    list_filter = ('Dept',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if this is a new notification
            obj.created_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_reviewed')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('user__username', 'message')
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)
    mark_as_reviewed.short_description = "Mark selected feedback as reviewed"






# @admin.register(Prescription)
# class PrescriptionAdmin(admin.ModelAdmin):
#     list_display = ('patient', 'diagnosis', 'created_at')
#     search_fields = ('patient__user__username', 'diagnosis')
#     fields = ('patient', 'diagnosis', 'chief_complaint', 'treatment_plan')
#     readonly_fields = ('created_at',)
# class PrescriptionAdmin(admin.ModelAdmin):
#     fields = ('patient', 'diagnosis', 'chief_complaint', 
#               'quadrant_1_tooth', 'quadrant_2_tooth', 
#               'quadrant_3_tooth', 'quadrant_4_tooth')

#     class Media:
#         css = {
#             'all': ('css/custom.css',)
#         }
#         js = ('js/custo
from django import forms
from django.contrib import admin
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

    # Optionally override the __init__ method if you need to customize field choices
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No need to manually reverse the choices here

# class PrescriptionAdmin(admin.ModelAdmin):
#     form = PrescriptionForm
#     fieldsets = (
#         (None, {
#             'fields': ('patient', 'diagnosis', 'chief_complaint', 'treatment_plan')
#         }),
#         ('Treatment Plan - Quadrants', {
#             'fields': (('quadrant_1_tooth', 'quadrant_2_tooth'), ('quadrant_3_tooth', 'quadrant_4_tooth')),
#             'description': 'Select tooth representation for each quadrant',
#         }),
#         ('Additional Info', {
#             'fields': ('created_at',)
#         }),
#     )
#     readonly_fields = ('created_at',)

#     # Dynamically reverse choices for quadrant_1_tooth and quadrant_3_tooth
#     def formfield_for_choice_field(self, db_field, request, **kwargs):
#         formfield = super().formfield_for_choice_field(db_field, request, **kwargs)

#         if db_field.name == 'quadrant_1_tooth':
#             # Reverse the choices for quadrant_1_tooth (8-1) and use buttons
#             formfield.choices = [(8 , str(8 - i)) for i in range(1, 9)]
#         elif db_field.name == 'quadrant_3_tooth':
#             # Reverse the choices for quadrant_3_tooth (8-1) and use buttons
#             formfield.choices = [(8 , str(8 - i)) for i in range(1, 9)]

#         # Use buttons instead of the dropdown
#         formfield.widget = forms.RadioSelect()

#         return formfield

#     class Media:
#         css = {
#             'all': ('css/custom.css',)
#         }
#         js = ('js/custom.js',)

# admin.site.register(Prescription, PrescriptionAdmin)
class PrescriptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('patient', 'diagnosis', 'chief_complaint')
        }),
        ('Treatment Plan - Quadrants', {
            'fields': (('quadrant_1_tooth', 'quadrant_2_tooth'), ('quadrant_3_tooth', 'quadrant_4_tooth')),
            'description': 'Select tooth representation for each quadrant',
        }),
        ('Additional Info', {
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ('created_at',)
    
admin.site.register(Prescription, PrescriptionAdmin)
