# Generated by Django 3.1.4 on 2021-01-10 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_auto_20201228_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('students', models.ManyToManyField(to='homepage.Student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='book',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.book'),
        ),
        migrations.AddField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(to='homepage.Teacher'),
        ),
    ]