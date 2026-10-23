from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Feedback, Institution, UserProfile
from transformers import pipeline
import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail

print("🚀 Yapay Zeka Modeli Aktif Ediliyor...")
sentiment_model = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

def student_form(request):
    gonderildi = False
    takip_kodu = None
    hata_mesaji = None
    kurumlar = Institution.objects.filter(is_active=True)
    
    if request.method == 'POST':
        kurum_id = request.POST.get('institution')
        category = request.POST.get('category')
        text = request.POST.get('text')
        email = request.POST.get('email', '').strip()
        
        yasakli_domainler = ['yopmail.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com', 'mailinator.com', 'throwawaymail.com']
        
        if email:
            domain = email.split('@')[-1].lower()
            if domain in yasakli_domainler:
                hata_mesaji = "Geçici veya sahte e-posta adresleri kullanılamaz. Lütfen geçerli bir adres girin."
        
        if text and category and kurum_id and email and not hata_mesaji:
            secilen_kurum = Institution.objects.get(id=kurum_id)
            analiz = sentiment_model(text)[0]
            label = analiz['label'].lower()
            
            if 'pos' in label: sentiment_tr = 'Olumlu'
            elif 'neg' in label: sentiment_tr = 'Olumsuz'
            else: sentiment_tr = 'Nötr'
                
            score_percent = round(analiz['score'] * 100, 2)
            
            yeni_kayit = Feedback.objects.create(
                institution=secilen_kurum,
                category=category, 
                text=text, 
                sentiment=sentiment_tr, 
                score=score_percent,
                student_email=email
            )
            takip_kodu = yeni_kayit.tracking_code
            gonderildi = True
            
    return render(request, 'analyzer/student_form.html', {
        'gonderildi': gonderildi, 
        'takip_kodu': takip_kodu, 
        'kurumlar': kurumlar,
        'hata_mesaji': hata_mesaji
    })

def track_status(request):
    feedback = None
    error = None
    if request.method == 'POST':
        code = request.POST.get('tracking_code', '').strip().upper()
        try:
            feedback = Feedback.objects.get(tracking_code=code)
        except Feedback.DoesNotExist:
            error = "Bu takip numarasına ait bir kayıt bulunamadı."
    return render(request, 'analyzer/track_status.html', {'feedback': feedback, 'error': error})

@login_required(login_url='/login/')
def dashboard(request):
    try:
        kullanici_kurumu = request.user.profile.institution
        feedbacks = Feedback.objects.filter(institution=kullanici_kurumu).order_by('-created_at')
        kurum_adi = kullanici_kurumu.name
    except:
        feedbacks = Feedback.objects.none()
        kurum_adi = "Kurum Atanmamış!"

    total_count = feedbacks.count()
    category_data = feedbacks.values('category').annotate(count=Count('category')).order_by('-count')
    
    context = {
        'feedbacks': feedbacks,
        'total': total_count,
        'pos_count': feedbacks.filter(sentiment='Olumlu').count(),
        'neg_count': feedbacks.filter(sentiment='Olumsuz').count(),
        'neu_count': feedbacks.filter(sentiment='Nötr').count(),
        'category_data': category_data,
        'kurum_adi': kurum_adi,
    }
    return render(request, 'analyzer/dashboard.html', context)

@login_required(login_url='/login/')
def update_status(request, pk):
    if request.method == 'POST':
        feedback = Feedback.objects.get(id=pk)
        feedback.status = request.POST.get('status', 'Beklemede')
        feedback.admin_note = request.POST.get('admin_note', '')
        feedback.save()

        if feedback.status == 'Çözüldü' and feedback.student_email:
            try:
                subject = f"{feedback.institution.name} - Şikayetiniz Çözüldü ({feedback.tracking_code})"
                message = f"Merhaba,\n\nİletmiş olduğunuz bildirim yönetimimiz tarafından incelenmiş ve çözülmüştür.\n\nİletilen Mesaj: {feedback.text}\nYönetici Notu: {feedback.admin_note}\n\nİyi günler dileriz."
                send_mail(subject, message, 'noreply@saasmerkezi.com', [feedback.student_email])
                print(f"📧 Başarılı: {feedback.student_email} adresine mail gönderildi!")
            except Exception as e:
                print(f"❌ Mail Hatası: {e}")

    return redirect('dashboard')

@login_required(login_url='/login/')
def export_to_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sistem_analiz_raporu.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Tarih', 'Kurum', 'Takip Kodu', 'Durum', 'Kategori', 'Geri Bildirim', 'Karar', 'Skor'])
    
    try:
        feedbacks = Feedback.objects.filter(institution=request.user.profile.institution).order_by('-created_at')
    except:
        feedbacks = []

    for f in feedbacks:
        tarih = f.created_at.strftime("%Y-%m-%d %H:%M")
        writer.writerow([tarih, f.institution.name, f.tracking_code, f.status, f.category, f.text, f.sentiment, f.score])
    return response

@api_view(['POST'])
def api_analyze(request):
    text = request.data.get('text', '')
    if not text: return Response({'hata': 'Metin gönderin.'}, status=400)
    analiz = sentiment_model(text)[0]
    label = analiz['label'].lower()
    sentiment_tr = 'Olumlu' if 'pos' in label else ('Olumsuz' if 'neg' in label else 'Nötr')
    return Response({'metin': text, 'karar': sentiment_tr, 'skor': round(analiz['score'] * 100, 2)})