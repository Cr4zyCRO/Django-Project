# Generated by Django 4.2.1 on 2023-05-25 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_korisnik_role_alter_korisnik_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmeti',
            name='izborni',
            field=models.CharField(choices=[('da', 'da'), ('ne', 'ne')], max_length=50),
        ),
    ]
