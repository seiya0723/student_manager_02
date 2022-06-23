from django.shortcuts import render,redirect
from django.views import View

from .models import Document
from .forms import DocumentForm


from django.http import FileResponse

from django.conf import settings


import datetime


class IndexView(View):
    def get(self, request, *args, **kwargs):

        context = {}
        context["documents"]    = Document.objects.order_by("-id")

        return render(request,"excel/index.html",context)
    
    def post(self, request, *args, **kwargs):

        form    = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("excel:index")

index   = IndexView.as_view()


#TODO:ここにダウンロード時の処理を書く。

import openpyxl as px

class DownloadView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):

        #https://docs.djangoproject.com/en/4.0/ref/request-response/#fileresponse-objects

        pk          = kwargs["pk"]
        document    = Document.objects.filter(id=pk).first()

        print(settings.MEDIA_ROOT)
        print(document.content)

        path        = str(settings.MEDIA_ROOT) + "/" + str(document.content) 
        print(path)


        #ここでエクセル読み込み、編集してバイナリデータでFileResponseの引数に入れる。
        wb  = px.load_workbook(path)
        ws  = wb.worksheets[0]

        rows    = ws.iter_rows()

        for row in rows:
            for cell in row:
                print(cell.value)

                #結合されたセルに対しては書き換えできないため、スルーする。
                if type(cell).__name__ == 'MergedCell':
                    continue

                #TODO:ここでコマンドを検知して実行(例えば、command:date を検知して今日の日付を表示させるなど) 
                cell.value  = "書き換えた"


        #一時的に記憶する専用のストレージパスへファイルを保存。FileResponseにてPATHを指定して読み込ませる。
        file_name           = str(datetime.datetime.now()) + ".xlsx"
        temporarily_path    = str(settings.MEDIA_ROOT) + "/temp/" + file_name

        wb.save(temporarily_path)  

        #HACK:一次記憶用のストレージへファイルを保存し続けると、いずれパンクするので、管理サイトか常駐スクリプトから一定時間後に削除させるべきでは？
        return FileResponse( open( temporarily_path, mode="rb" ))


download    = DownloadView.as_view()

