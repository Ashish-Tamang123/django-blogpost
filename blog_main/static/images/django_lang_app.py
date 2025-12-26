"""
Django Language Learning Application - Minimal Runnable Version

SETUP INSTRUCTIONS:
1. Create a new directory and save this file as 'setup_app.py'
2. Run: python setup_app.py
3. Follow the prompts to create the Django project structure
4. Run migrations: python manage.py migrate
5. Create superuser: python manage.py createsuperuser
6. Load sample data: python manage.py loaddata initial_data.json
7. Run server: python manage.py runserver
8. Visit: http://127.0.0.1:8000/

This script will create a complete Django project structure with:
- User authentication
- Vocabulary management
- Flashcard practice
- Progress tracking
- Admin interface
"""

import os
import sys
import json

def create_project_structure():
    """Create the Django project directory structure"""
    
    # Project structure
    structure = {
        'language_app': {
            '__init__.py': '',
            'settings.py': SETTINGS_PY,
            'urls.py': URLS_PY,
            'wsgi.py': WSGI_PY,
        },
        'vocabulary': {
            '__init__.py': '',
            'models.py': MODELS_PY,
            'views.py': VIEWS_PY,
            'urls.py': VOCABULARY_URLS_PY,
            'admin.py': ADMIN_PY,
            'forms.py': FORMS_PY,
        },
        'templates': {
            'base.html': BASE_HTML,
            'vocabulary': {
                'word_list.html': WORD_LIST_HTML,
                'practice.html': PRACTICE_HTML,
                'progress.html': PROGRESS_HTML,
            },
            'registration': {
                'login.html': LOGIN_HTML,
                'register.html': REGISTER_HTML,
            }
        },
        'static': {
            'css': {
                'style.css': STYLE_CSS,
            },
            'js': {
                'practice.js': PRACTICE_JS,
            }
        }
    }
    
    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, 'w') as f:
                    f.write(content)
    
    # Create base directory
    if not os.path.exists('language_learning_project'):
        os.makedirs('language_learning_project')
    
    os.chdir('language_learning_project')
    
    # Create manage.py
    with open('manage.py', 'w') as f:
        f.write(MANAGE_PY)
    
    os.chmod('manage.py', 0o755)
    
    # Create structure
    create_structure('.', structure)
    
    # Create initial data fixture
    os.makedirs('vocabulary/fixtures', exist_ok=True)
    with open('vocabulary/fixtures/initial_data.json', 'w') as f:
        f.write(INITIAL_DATA)
    
    print("✓ Project structure created successfully!")
    print("\nNext steps:")
    print("1. cd language_learning_project")
    print("2. pip install django")
    print("3. python manage.py migrate")
    print("4. python manage.py createsuperuser")
    print("5. python manage.py loaddata initial_data.json")
    print("6. python manage.py runserver")
    print("\nThen visit: http://127.0.0.1:8000/")


# File contents as constants

MANAGE_PY = '''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
'''

SETTINGS_PY = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dev-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vocabulary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'language_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'language_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
'''

URLS_PY = '''
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('vocabulary.urls')),
    path('', RedirectView.as_view(url='/vocabulary/', permanent=False)),
]
'''

WSGI_PY = '''
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_app.settings')
application = get_wsgi_application()
'''

MODELS_PY = '''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Word(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    pronunciation = models.CharField(max_length=200, blank=True)
    example_sentence = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['difficulty', 'word']
    
    def __str__(self):
        return f"{self.word} - {self.translation}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    mastery_level = models.IntegerField(default=0)  # 0-5
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(default=timezone.now)
    next_review = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'word']
        ordering = ['next_review']
    
    def __str__(self):
        return f"{self.user.username} - {self.word.word} (Level {self.mastery_level})"
    
    @property
    def success_rate(self):
        total = self.correct_count + self.incorrect_count
        if total == 0:
            return 0
        return int((self.correct_count / total) * 100)
    
    def update_progress(self, is_correct):
        """Update progress using simplified spaced repetition"""
        from datetime import timedelta
        
        if is_correct:
            self.correct_count += 1
            self.mastery_level = min(5, self.mastery_level + 1)
            # Increase interval: 1 day, 3 days, 7 days, 14 days, 30 days, 60 days
            intervals = [1, 3, 7, 14, 30, 60]
            days = intervals[self.mastery_level]
        else:
            self.incorrect_count += 1
            self.mastery_level = max(0, self.mastery_level - 1)
            days = 1  # Review again tomorrow
        
        self.last_reviewed = timezone.now()
        self.next_review = timezone.now() + timedelta(days=days)
        self.save()

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    words_practiced = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def accuracy(self):
        if self.words_practiced == 0:
            return 0
        return int((self.correct_answers / self.words_practiced) * 100)
'''

VIEWS_PY = '''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Avg, Sum
from .models import Word, UserProgress, StudySession, Language
import random

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('word_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def word_list(request):
    difficulty = request.GET.get('difficulty', '')
    
    words = Word.objects.all()
    if difficulty:
        words = words.filter(difficulty=difficulty)
    
    # Get user progress for each word
    user_progress = {
        p.word_id: p for p in UserProgress.objects.filter(user=request.user)
    }
    
    words_with_progress = []
    for word in words:
        progress = user_progress.get(word.id)
        words_with_progress.append({
            'word': word,
            'progress': progress
        })
    
    context = {
        'words_with_progress': words_with_progress,
        'current_difficulty': difficulty,
    }
    return render(request, 'vocabulary/word_list.html', context)

@login_required
def practice(request):
    # Get words due for review or new words
    due_words = UserProgress.objects.filter(
        user=request.user,
        next_review__lte=timezone.now()
    ).select_related('word')[:10]
    
    # If not enough due words, add new ones
    learned_word_ids = UserProgress.objects.filter(user=request.user).values_list('word_id', flat=True)
    new_words = Word.objects.exclude(id__in=learned_word_ids)[:10 - len(due_words)]
    
    words = list(due_words) + [
        type('obj', (object,), {'word': word, 'mastery_level': 0})() 
        for word in new_words
    ]
    
    if not words:
        return render(request, 'vocabulary/practice.html', {'no_words': True})
    
    # Start a new study session
    session = StudySession.objects.create(user=request.user)
    
    context = {
        'words': [w if isinstance(w, UserProgress) else w.word for w in words],
        'session_id': session.id,
    }
    return render(request, 'vocabulary/practice.html', context)

@login_required
def check_answer(request):
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        user_answer = request.POST.get('answer', '').strip().lower()
        session_id = request.POST.get('session_id')
        
        word = get_object_or_404(Word, id=word_id)
        is_correct = user_answer == word.translation.lower()
        
        # Update or create progress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            word=word,
        )
        progress.update_progress(is_correct)
        
        # Update session
        session = StudySession.objects.get(id=session_id)
        session.words_practiced += 1
        if is_correct:
            session.correct_answers += 1
        session.save()
        
        return JsonResponse({
            'correct': is_correct,
            'correct_answer': word.translation,
            'mastery_level': progress.mastery_level,
            'example': word.example_sentence,
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def progress_view(request):
    progress_items = UserProgress.objects.filter(user=request.user).select_related('word')
    
    # Calculate statistics
    total_words = progress_items.count()
    avg_mastery = progress_items.aggregate(Avg('mastery_level'))['mastery_level__avg'] or 0
    
    sessions = StudySession.objects.filter(user=request.user).order_by('-start_time')[:10]
    
    # Words by mastery level
    mastery_distribution = {}
    for i in range(6):
        mastery_distribution[i] = progress_items.filter(mastery_level=i).count()
    
    context = {
        'progress_items': progress_items,
        'total_words': total_words,
        'avg_mastery': round(avg_mastery, 1),
        'sessions': sessions,
        'mastery_distribution': mastery_distribution,
    }
    return render(request, 'vocabulary/progress.html', context)
'''

VOCABULARY_URLS_PY = '''
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('vocabulary/', views.word_list, name='word_list'),
    path('practice/', views.practice, name='practice'),
    path('check-answer/', views.check_answer, name='check_answer'),
    path('progress/', views.progress_view, name='progress'),
]
'''

ADMIN_PY = '''
from django.contrib import admin
from .models import Language, Word, UserProgress, StudySession

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'language', 'difficulty', 'created_at']
    list_filter = ['language', 'difficulty']
    search_fields = ['word', 'translation']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'mastery_level', 'success_rate', 'last_reviewed', 'next_review']
    list_filter = ['mastery_level', 'user']
    search_fields = ['user__username', 'word__word']

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'words_practiced', 'accuracy']
    list_filter = ['user', 'start_time']
'''

FORMS_PY = '''
from django import forms
from .models import Word

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['language', 'word', 'translation', 'pronunciation', 'example_sentence', 'difficulty']
'''

BASE_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Language Learning App{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <h1 class="nav-logo">🌍 LangLearn</h1>
            {% if user.is_authenticated %}
            <ul class="nav-menu">
                <li><a href="{% url 'word_list' %}">Vocabulary</a></li>
                <li><a href="{% url 'practice' %}">Practice</a></li>
                <li><a href="{% url 'progress' %}">Progress</a></li>
                <li><a href="{% url 'logout' %}">Logout ({{ user.username }})</a></li>
            </ul>
            {% else %}
            <ul class="nav-menu">
                <li><a href="{% url 'login' %}">Login</a></li>
                <li><a href="{% url 'register' %}">Register</a></li>
            </ul>
            {% endif %}
        </div>
    </nav>
    
    <main class="container">
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <script src="/static/js/practice.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

WORD_LIST_HTML = '''{% extends 'base.html' %}

{% block title %}Vocabulary List{% endblock %}

{% block content %}
<div class="page-header">
    <h2>Vocabulary</h2>
    <a href="{% url 'practice' %}" class="btn btn-primary">Start Practice</a>
</div>

<div class="filter-bar">
    <a href="{% url 'word_list' %}" class="filter-btn {% if not current_difficulty %}active{% endif %}">All</a>
    <a href="?difficulty=beginner" class="filter-btn {% if current_difficulty == 'beginner' %}active{% endif %}">Beginner</a>
    <a href="?difficulty=intermediate" class="filter-btn {% if current_difficulty == 'intermediate' %}active{% endif %}">Intermediate</a>
    <a href="?difficulty=advanced" class="filter-btn {% if current_difficulty == 'advanced' %}active{% endif %}">Advanced</a>
</div>

<div class="word-grid">
    {% for item in words_with_progress %}
    <div class="word-card">
        <div class="word-header">
            <h3>{{ item.word.word }}</h3>
            <span class="difficulty-badge difficulty-{{ item.word.difficulty }}">{{ item.word.get_difficulty_display }}</span>
        </div>
        <p class="translation">{{ item.word.translation }}</p>
        {% if item.word.pronunciation %}
        <p class="pronunciation">🔊 {{ item.word.pronunciation }}</p>
        {% endif %}
        {% if item.word.example_sentence %}
        <p class="example">💬 {{ item.word.example_sentence }}</p>
        {% endif %}
        {% if item.progress %}
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {{ item.progress.mastery_level|mul:20 }}%"></div>
        </div>
        <p class="mastery-text">Mastery: {{ item.progress.mastery_level }}/5 ({{ item.progress.success_rate }}% success)</p>
        {% else %}
        <p class="new-word">🆕 New word</p>
        {% endif %}
    </div>
    {% empty %}
    <p class="no-data">No words found. Contact admin to add vocabulary.</p>
    {% endfor %}
</div>
{% endblock %}
'''

PRACTICE_HTML = '''{% extends 'base.html' %}

{% block title %}Practice{% endblock %}

{% block content %}
{% if no_words %}
<div class="empty-state">
    <h2>No words to practice!</h2>
    <p>You've mastered everything or there are no words available.</p>
    <a href="{% url 'word_list' %}" class="btn btn-primary">View Vocabulary</a>
</div>
{% else %}
<div class="practice-container" id="practiceContainer">
    <div class="practice-header">
        <h2>Practice Session</h2>
        <div class="practice-stats">
            <span id="currentWord">1</span> / <span id="totalWords">{{ words|length }}</span>
            <span class="score">Score: <span id="score">0</span></span>
        </div>
    </div>
    
    <div class="flashcard" id="flashcard">
        <div class="flashcard-content">
            <h3 class="word-prompt" id="wordPrompt"></h3>
            <input type="text" id="answerInput" class="answer-input" placeholder="Type your answer..." autocomplete="off">
            <button onclick="checkAnswer()" class="btn btn-primary btn-check">Check Answer</button>
        </div>
        
        <div class="feedback" id="feedback" style="display: none;">
            <div class="feedback-content">
                <h3 id="feedbackTitle"></h3>
                <p id="feedbackText"></p>
                <p id="exampleSentence" class="example"></p>
                <button onclick="nextWord()" class="btn btn-primary">Next Word</button>
            </div>
        </div>
    </div>
</div>

<script>
    const words = {{ words|safe|escapejs }};
    const sessionId = {{ session_id }};
    let currentIndex = 0;
    let score = 0;
    
    const wordsData = [
        {% for word in words %}
        {
            id: {{ word.id }},
            word: "{{ word.word|escapejs }}",
            translation: "{{ word.translation|escapejs }}",
            example: "{{ word.example_sentence|escapejs }}"
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];
    
    function loadWord() {
        if (currentIndex >= wordsData.length) {
            showComplete();
            return;
        }
        
        const word = wordsData[currentIndex];
        document.getElementById('wordPrompt').textContent = `Translate: ${word.word}`;
        document.getElementById('answerInput').value = '';
        document.getElementById('answerInput').focus();
        document.getElementById('feedback').style.display = 'none';
        document.getElementById('currentWord').textContent = currentIndex + 1;
    }
    
    function checkAnswer() {
        const answer = document.getElementById('answerInput').value;
        const word = wordsData[currentIndex];
        
        fetch('{% url "check_answer" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: `word_id=${word.id}&answer=${encodeURIComponent(answer)}&session_id=${sessionId}`
        })
        .then(response => response.json())
        .then(data => {
            const feedback = document.getElementById('feedback');
            const feedbackTitle = document.getElementById('feedbackTitle');
            const feedbackText = document.getElementById('feedbackText');
            const exampleSentence = document.getElementById('exampleSentence');
            
            if (data.correct) {
                feedbackTitle.textContent = '✅ Correct!';
                feedbackTitle.className = 'feedback-correct';
                feedbackText.textContent = `Great job!`;
                score++;
                document.getElementById('score').textContent = score;
            } else {
                feedbackTitle.textContent = '❌ Incorrect';
                feedbackTitle.className = 'feedback-incorrect';
                feedbackText.textContent = `The correct answer is: ${data.correct_answer}`;
            }
            
            if (data.example) {
                exampleSentence.textContent = `Example: ${data.example}`;
                exampleSentence.style.display = 'block';
            } else {
                exampleSentence.style.display = 'none';
            }
            
            feedback.style.display = 'flex';
        });
    }
    
    function nextWord() {
        currentIndex++;
        loadWord();
    }
    
    function showComplete() {
        const container = document.getElementById('practiceContainer');
        const accuracy = Math.round((score / wordsData.length) * 100);
        container.innerHTML = `
            <div class="practice-complete">
                <h2>🎉 Session Complete!</h2>
                <div class="complete-stats">
                    <p>Words Practiced: ${wordsData.length}</p>
                    <p>Correct: ${score}</p>
                    <p>Accuracy: ${accuracy}%</p>
                </div>
                <a href="{% url 'practice' %}" class="btn btn-primary">Practice Again</a>
                <a href="{% url 'progress' %}" class="btn btn-secondary">View Progress</a>
            </div>
        `;
    }
    
    document.getElementById('answerInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkAnswer();
        }
    });
    
    loadWord();
</script>
{% endif %}
{% endblock %}
'''

PROGRESS_HTML = '''{% extends 'base.html' %}

{% block title %}Your Progress{% endblock %}

{% block content %}
<h2>Your Learning Progress</h2>

<div class="stats-grid">
    <div class="stat-card">
        <h3>{{ total_words }}</h3>
        <p>Words Learning</p>
    </div>
    <div class="stat-card">
        <h3>{{ avg_mastery }}</h3>
        <p>Avg Mastery Level</p>
    </div>
    <div class="stat-card">
        <h3>{{ sessions.count }}</h3>
        <p>Practice Sessions</p>
    </div>
</div>

<h3>Mastery Distribution</h3>
<div class="mastery-chart">
    {% for level, count in mastery_distribution.items %}
    <div class="mastery-bar">
        <span class="mastery-label">Level {{ level }}</span>
        <div class="mastery-bar-fill" style="width: {% if total_words %}{{ count|mul:100|div:total_words }}{% else %}0{% endif %}%">
            {{ count }}
        </div>
    </div>
    {% endfor %}
</div>

<h3>Recent Sessions</h3>
<div class="sessions-list">
    {% for session in sessions %}
    <div class="session-card">
        <p><strong>{{ session.start_time|date:"M d, Y H:i" }}</strong></p>
        <p>Words: {{ session.words_practiced }} | Accuracy: {{ session.accuracy }}%</p>
    </div>
    {% empty %}
    <p class="no-data">No practice sessions yet. Start practicing!</p>
    {% endfor %}
</div>

<h3>Your Vocabulary</h3>
<table class="progress-table">
    <thead>
        <tr>
            <th>Word</th>
            <th>Translation</th>
            <th>Mastery</th>
            <th>Success Rate</th>
            <th>Next Review</th>
        </tr>
    </thead>
    <tbody>
        {% for progress in progress_items %}
        <tr>
            <td>{{ progress.word.word }}</td>
            <td>{{ progress.word.translation }}</td>
            <td>
                <div class="progress-mini">
                    <div class="progress-bar" style="width: {{ progress.mastery_level|mul:20 }}%"></div>
                </div>
                {{ progress.mastery_level }}/5
            </td>
            <td>{{ progress.success_rate }}%</td>
            <td>{{ progress.next_review|date:"M d, H:i" }}</td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="5" class="no-data">Start practicing to track your progress!</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
'''

LOGIN_HTML = '''{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="auth-container">
    