from tabnanny import verbose
from django.db import models
from django.utils import timezone

class Building(models.Model):
    name = models.CharField(verbose_name="校舎名",max_length=200)

    # timezone.now()で実行するが()で実行してはいけない
    dt = models.DateTimeField(verbose_name="登録日時",default=timezone.now)
    
    description = models.CharField(verbose_name="備考", max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    def count_students(self):
        return Student.objects.filter(building=self.id).count()


    count_students.short_description = "在籍生徒数" # adminサイトでのlist_displayのヘッダ名変更

    # def student_list(self):
    #     return Student.objects.filter(building=self.id).all()

    def student_list(self):
        student_list = Student.objects.filter(building=self.id).all()

        list = ""
        for student in student_list:
            list += str(student) + "\n"
        return list
        #return Student.objects.filter(building=self.id).all()


    student_list.short_description = "生徒一覧"




class Student(models.Model):
    name = models.CharField(verbose_name="生徒名",max_length=50)

    dt = models.DateTimeField(verbose_name="登録日時",default=timezone.now)

    building = models.ForeignKey(Building, verbose_name="所属校舎", on_delete=models.PROTECT)

    def __str__(self):
        return self.name

