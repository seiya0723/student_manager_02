from django.db import models

#settings.pyにて指定したタイムゾーンを考慮したtimezoneをimport (awareとnative)
#Djangoサーバーの拠点が海外に存在したとしても日本時間で記録される。
from django.utils import timezone


#例外発動用
from django.core.exceptions import ValidationError


from django.contrib.auth.models import User
import datetime

class Building(models.Model):

    #ここにidフィールドがある(自動採番なので、クライアントは入力不要。)
    name        = models.CharField(verbose_name="校舎名",max_length=200)
    dt          = models.DateTimeField(verbose_name="登録日時",default=timezone.now)
    description = models.CharField(verbose_name="備考",max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.name

    #在籍生徒数
    #TODO:これよりも在籍生徒の全てのモデルオブジェクトをreturnするほうが良い。カウンターはテンプレート側でlengthフィルタを使えば良い。
    #更に、アクティブな生徒だけを表示させるべき
    #TODO:かと言って下記を消すと管理サイトまで影響が及ぶので、それらを修正した上で直したほうが良いだろう。
    def count_students(self):
        return Student.objects.filter(building=self.id).count()
    

    #在籍生徒のリストを出す。
    def exist_students(self):
        return Student.objects.filter(building=self.id, is_active=True).order_by("dt")


    #buildingから日付を指定し、その日に自習室に行ったどうかを調べる
    def logs(self):
        #TIPS:__を使うことで、外部キーで繋がっているフィールドに対して検索できる。
        return Log.objects.filter(student__building__id=self.id, date=timezone.localdate())


    #TODO:もし、今日以外の日付でデータを表示させたい場合
    #まず、上記のlogsに引数のdateを入れる。
    #ただし、テンプレート側から引数を指定してモデルのメソッドを実行することはできない。そのため、必然的にカスタムテンプレートタグを使う必要が出る。
    #さらに、カスタムテンプレートタグの中でも難度の高い埋め込み型のカスタムテンプレートタグになることが予想される。

    #TODO:◯日連続を表現するには？
    #上記のlogsをループして、生徒のidを取得。もう一度Logに対して検索を仕掛ける。日付が連続していれば、その数だけカウントして、辞書型に連続日数を付与する。


    def weekly_logs(self):
        #TIPS:__を使うことで、外部キーで繋がっているフィールドに対して検索できる。
        today       = timezone.localdate() 
        last_week   = today - datetime.timedelta(days=7)

        return Log.objects.filter(student__building__id=self.id, date__lte=today, date__gte=last_week )


    def usage(self):
        exist   = len(self.exist_students())

        #0除算になってしまうため。
        if exist:
            return ( len(self.logs()) / exist )*100
        else:
            return 0.0

    def weekly_usage(self):
        exist   = len(self.exist_students())

        #0除算になってしまうため。
        if exist:
            return ( len(self.weekly_logs()) / exist )*100
        else:
            return 0.0


    #管理サイトから呼び出す時のヘッダ名
    count_students.short_description      = "所属生徒数"
    

class Student(models.Model):

    name        = models.CharField(verbose_name="生徒名",max_length=50)
    dt          = models.DateTimeField(verbose_name="登録日時",default=timezone.now)

    building    = models.ForeignKey(Building,verbose_name="所属校舎",on_delete=models.PROTECT)

    #生徒が卒業もしくは離反した時にFalse。DBには0か1が入る
    is_active   = models.BooleanField(verbose_name="アクティブ",default=True)

    def __str__(self):
        return self.name

def validate_student_is_active(value):

    student = Student.objects.filter(id=value).first()
    print(student)

    if not student.is_active:
        #form.is_valid()でValidationErrorがraiseされると、Falseが返却され、save()が使えなくなるのでDBに保存できなくなる。
        raise ValidationError("この生徒はアクティブではありません。 " + student.name )

class Log(models.Model):

    class Meta:
        #https://noauto-nolife.com/post/django-same-user-operate-prevent/
        unique_together = ("date","student")

    date        = models.DateField(verbose_name="自習日")
    student     = models.ForeignKey(Student,verbose_name="生徒",on_delete=models.PROTECT, validators=[validate_student_is_active])
    user        = models.ForeignKey(User, verbose_name="投稿者",on_delete=models.SET_NULL,null=True)


