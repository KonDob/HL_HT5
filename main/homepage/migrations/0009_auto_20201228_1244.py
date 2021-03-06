# Generated by Django 2.2.6 on 2020-12-28 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_auto_20201228_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='description',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='surname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
