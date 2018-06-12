from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import HttpResponse, redirect
from crm import models
from crm.models import UserProfile
from crm.used_forms import UserProfileForms


# Register your models here.



class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserProfileForms.UserProfileChangeForm
    add_form = UserProfileForms.UserProfileCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('PersonalInfo', {'fields': ('name','stu_account')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_permissions', 'groups', 'roles')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions', 'groups', 'roles')


# Now register the new UserAdmin...

class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "course_record", "attendance", "score"]
    list_filter = ["course_record"]


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ["cls", "day_num", "teacher", "has_homework", "homework_title", "date"]

    actions = ['initialize_studyrecords']

    def initialize_studyrecords(self, req, queryset):
        if len(queryset) > 1:
            return HttpResponse("只能选择一个班级！")
        student_list = []
        for enroll_obj in queryset[0].cls.enrollment_set.all():
            student_list.append(
                models.StudyRecord(
                    student=enroll_obj,
                    course_record=queryset[0],
                    attendance=0,
                    score=0,
                )
            )
        try:
            models.StudyRecord.objects.bulk_create(student_list)
        except Exception as e:
            return HttpResponse("初始化失败，请检查是否有相应记录存在！")
        return redirect("/admin/crm/studyrecord/?course_record__id__exact=%s" % queryset[0].id)

    initialize_studyrecords.short_description = "所以学生学习记录初始化"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'qq', 'derive', 'consultant', 'status', 'date')
    list_filter = ('derive', 'consultant', 'date')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)
    list_per_page = 5

    actions = ['test_one', ]

    def test_one(self, args1, args2):
        print(self)
        print(args1)
        print(args2)


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Tag)
admin.site.register(models.CustomerFollowUp)

admin.site.register(models.Role)
admin.site.register(models.Course)
admin.site.register(models.Branch)
admin.site.register(models.Cls)
admin.site.register(models.Enrollment)
admin.site.register(models.Payment)
admin.site.register(models.CourseRecord, CourseRecordAdmin)
admin.site.register(models.StudyRecord, StudyRecordAdmin)
admin.site.register(models.Menu)
admin.site.register(models.ContractTemplate)

admin.site.register(UserProfile, UserProfileAdmin)
