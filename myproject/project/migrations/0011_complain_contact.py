# Generated by Django 4.0.3 on 2022-04-20 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_visitors_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='none', max_length=50)),
                ('email', models.EmailField(max_length=25)),
                ('value', models.CharField(max_length=25, null=True)),
                ('message', models.TextField(default='none', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='none', max_length=50)),
                ('email', models.EmailField(max_length=25)),
                ('subject', models.CharField(max_length=100, null=True)),
                ('message', models.TextField(default='none', max_length=1000)),
            ],
        ),
    ]
