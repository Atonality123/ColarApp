# Generated by Django 4.2.3 on 2023-07-15 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solar_radiation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]