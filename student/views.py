from django.shortcuts import render, HttpResponse
from crm import models
from PerfectCRM import settings
import os
import json
import time


# Create your views here.

def my_course(req):
    return render(req, "students/mycourse.html")
    pass


def studyrecords(req, enroll_obj_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_obj_id)

    return render(req, "students/studyrecords.html", {"enroll_obj": enroll_obj})
    pass


def homework_detail(req, study_record_id):
    study_record_obj = models.StudyRecord.objects.get(id=study_record_id)

    homework_path = "{base_dir}/{class_id}/{course_record_id}/{study_record_id}/".format(
        base_dir=settings.HOMEWORK_DATA,
        class_id=study_record_obj.student.cls_id,
        course_record_id=study_record_obj.course_record_id,
        study_record_id=study_record_obj.id)
    file_lists = []
    if req.method == "GET":
        if os.path.isdir(homework_path):
            for file_name in os.listdir(homework_path):
                f_path = "%s/%s" % (homework_path, file_name)
                modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f_path).st_mtime))
                file_lists.append([file_name, os.stat(f_path).st_size, modify_time])

    if req.is_ajax():
        if not os.path.isdir(homework_path):
            os.makedirs(homework_path, exist_ok=True)
        for k, file in req.FILES.items():
            with open('%s/%s' % (homework_path, file.name), 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        if os.path.isdir(homework_path):
            for file_name in os.listdir(homework_path):
                f_path = "%s/%s" % (homework_path, file_name)
                modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f_path).st_mtime))
                file_lists.append([file_name, os.stat(f_path).st_size, modify_time])

        return HttpResponse(json.dumps({"status":0,"msg":"file upload success","file_lists":file_lists}))

    return render(req, "students/homework_detail.html", {"study_record": study_record_obj,"file_lists":file_lists})
    pass
