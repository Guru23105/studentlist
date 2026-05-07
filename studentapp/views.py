from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Student

import csv
import openpyxl


# HOME PAGE
@login_required
def home(request):
    students = Student.objects.all()
    return render(request, 'home.html', {'students': students})


# ADD STUDENT
@login_required
def add_student(request):

    if request.method == 'POST':

        name = request.POST['name']
        age = request.POST['age']
        course = request.POST['course']

        Student.objects.create(
            name=name,
            age=age,
            course=course
        )

        return redirect('/')

    return render(request, 'add.html')


# UPDATE STUDENT
@login_required
def update_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == 'POST':

        student.name = request.POST['name']
        student.age = request.POST['age']
        student.course = request.POST['course']

        student.save()

        return redirect('/')

    return render(request, 'update.html', {'student': student})


# DELETE STUDENT
@login_required
def delete_student(request, id):

    student = Student.objects.get(id=id)

    student.delete()

    return redirect('/')


# DOWNLOAD EXCEL/CSV
@login_required
def download_students(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)

    writer.writerow(['Name', 'Age', 'Course'])

    students = Student.objects.all()

    for student in students:
        writer.writerow([
            student.name,
            student.age,
            student.course
        ])

    return response


# UPLOAD EXCEL/CSV
@login_required
def upload_excel(request):

    if request.method == 'POST':

        file = request.FILES['file']

        filename = file.name

        # CSV FILE
        if filename.endswith('.csv'):

            decoded_file = file.read().decode('utf-8').splitlines()

            reader = csv.reader(decoded_file)

            next(reader)

            for row in reader:

                Student.objects.create(
                    name=row[0],
                    age=row[1],
                    course=row[2]
                )

        # EXCEL FILE
        elif filename.endswith('.xlsx'):

            workbook = openpyxl.load_workbook(file)

            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):

                name, age, course = row

                Student.objects.create(
                    name=name,
                    age=age,
                    course=course
                )

        return redirect('/')

    return render(request, 'upload.html')