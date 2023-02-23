# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 09:02

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('ANSWER_ID', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.CharField(max_length=200)),
                ('correct_answer', models.BooleanField()),
                ('answer_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedQuestion',
            fields=[
                ('COMPLETEDQUESTION_ID', models.AutoField(primary_key=True, serialize=False)),
                ('cq_text', models.CharField(max_length=200)),
                ('mca', models.BooleanField(default=False)),
                ('correct_a', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedQuiz',
            fields=[
                ('COMPLETEDQUIZ_ID', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('COURSE_ID', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CourseAdministrator',
            fields=[
                ('COURSEADMINISTRATOR_ID', models.AutoField(primary_key=True, serialize=False)),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('ENROLLMENT_ID', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_professor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('QUESTION_ID', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=200)),
                ('multiple_correct_answers', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionIsEditedByTa',
            fields=[
                ('EDITED_BY_TA_ID', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Course')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('QUIZ_ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('due_date', models.DateTimeField()),
                ('active_from', models.DateTimeField(default='2017-01-01')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Course')),
            ],
        ),
        migrations.CreateModel(
            name='QuizIsCreatedByTa',
            fields=[
                ('CREATED_BY_TA_ID', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Course')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Quiz')),
            ],
        ),
        migrations.AddField(
            model_name='questioniseditedbyta',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Quiz'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Quiz'),
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Quiz'),
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='completedquestion',
            name='completed_quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.CompletedQuiz'),
        ),
        migrations.AddField(
            model_name='completedquestion',
            name='given_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Answer'),
        ),
        migrations.AddField(
            model_name='completedquestion',
            name='q_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buddy.Question'),
        ),
    ]