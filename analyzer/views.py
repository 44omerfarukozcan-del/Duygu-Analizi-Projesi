from django.shortcuts import render, redirect
from .models import Feedback
from transformers import pipeline

# Modeli belleğe alıyoruz (Sadece bir kez yüklenir)
print("🚀 Yapay Zeka Modeli Aktif Ediliyor...")
sentiment_model = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

def dashboard(request):
    # Eğer form gönderildiyse (Yeni veri eklendiyse)
    if request.method == 'POST':
        category = request.POST.get('category')
        text = request.POST.get('text')
        
        if text and category:
            # 1. Metni Yapay Zekaya Gönder
            analiz = sentiment_model(text)[0]
            label = analiz['label'].lower()
            
            # 2. İngilizce etiketleri Türkçeye çevir
            if 'pos' in label:
                sentiment_tr = 'Olumlu'
            elif 'neg' in label:
                sentiment_tr = 'Olumsuz'
            else:
                sentiment_tr = 'Nötr'
                
            # 3. Yüzdelik güven skorunu hesapla
            score_percent = round(analiz['score'] * 100, 2)
            
            # 4. Veritabanına Kaydet
            Feedback.objects.create(
                category=category, 
                text=text, 
                sentiment=sentiment_tr, 
                score=score_percent
            )
            
            # İşlem bitince sayfayı yenile
            return redirect('dashboard')

    # Sayfa normal yüklendiğinde veritabanındaki verileri çek
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # İstatistikleri hesapla
    context = {
        'feedbacks': feedbacks,
        'total': feedbacks.count(),
        'pos_count': feedbacks.filter(sentiment='Olumlu').count(),
        'neg_count': feedbacks.filter(sentiment='Olumsuz').count(),
        'neu_count': feedbacks.filter(sentiment='Nötr').count(),
    }
    
    return render(request, 'analyzer/dashboard.html', context)