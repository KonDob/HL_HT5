# Generated by Django 3.1.4 on 2021-01-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0011_remove_student_teachers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=999)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]