# Generated by Django 4.0.3 on 2022-04-19 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_visitors_remove_user_password1_remove_user_password2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitors',
            name='gender',
            field=models.CharField(max_length=25),
        ),
    ]
