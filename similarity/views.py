from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,JsonResponse

from django.contrib.auth import authenticate


from utils import zipmanager as ziputil
from utils import calc_ngram as calc_ngram
from utils import process as process

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def similarity_tool(request):
    # user = authenticate(username='user', password='user12345')
    # if user is not None:
    return render(request, 'index.html')
    # else:
    #     return render(request, 'login.html')

def uploadfiles(request):
    
    zipfile = request.FILES['zipfile']

    fs = FileSystemStorage()
    # isexist = fs.exists('uploads/' + zipfile.name)
    # if isexist == True:
    #     fs.delete('uploads/' + zipfile.name)

    ziputil.delete_files('uploads/origfiles')
    ziputil.delete_files('uploads')
    ziputil.delete_files('result')
    ziputil.delete_files('static/result')

    filename = fs.save('uploads/' + zipfile.name, zipfile)

    if ziputil.unzip('uploads/' + zipfile.name, 'uploads/origfiles') == False:
        success = 2
    else:
        success = 1
        global valuemax
        valuemax = calc_ngram.filecount()

    data = {
        'success': success
    }

    return JsonResponse(data)

def startprocess(request):
    print('start process')
    result_file_name = process.startprocess()
    success = 1
    
    data = {
        'success': success,
        'result_file_name': result_file_name
    }

    return JsonResponse(data)
    print('check process')    


def checkprocess(request):
    process_status = process.checkprocess()
    
    data = {
        'success': 1,
        'check_process': process_status
    }
    return JsonResponse(data)


def deletefiles(request):
    ziputil.delete_files('uploads/origfiles')
    ziputil.delete_files('uploads')
    ziputil.delete_files('result')
    ziputil.delete_files('static/result')

    data = {
        'success': 1
    }
    return JsonResponse(data)

def calcngram(request):
    success = 1
    if calc_ngram.create_gram_file() == False:
        success = 2
    data = {
        'success': success
    }
    return JsonResponse(data)

def ngramprocess(request):
    global valuemax
    valuenow = calc_ngram.checkprocess()

    data = {
        'success': 1,
        'valuemax': valuemax,
        'valuenow': valuenow
    }
    return JsonResponse(data)