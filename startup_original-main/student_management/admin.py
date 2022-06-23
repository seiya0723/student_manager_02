from django.contrib import admin
from .models import Building, Student

from django.utils.html import format_html

class BuildingAdmin(admin.ModelAdmin):
    #指定したフィールドを表示、編集ができる
    list_display = ["id", "name", "dt", "description", "count_students", "student_list_format_html"]
    list_editable = ["name", "dt", "description"]

    
    #校舎に所属する生徒を表示させる時、関数を呼び出す。
    def student_list_format_html(self, building):

        students    = building.student_list()
        text        = students.replace("\n","<br>")

        #ul liタグを使って一覧表示のように仕立てる事ができる。
        return format_html("<div>" + text + "</div>")



    #指定したフィールドの検索と絞り込みができる
    search_fields = ["name", "description"]
    list_filter  = ["name", "dt"]

    #日付ごとに絞り込む、ドリルナビゲーションの設置
    date_hierarchy = "dt"


class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "dt", "building"]
    list_editable = ["name", "dt", "building"]

    search_fields = ["name", "building"]
    list_filter  = ["name", "dt", "building"]

    date_hierarchy = "dt"


admin.site.register(Building, BuildingAdmin)
admin.site.register(Student, StudentAdmin)
