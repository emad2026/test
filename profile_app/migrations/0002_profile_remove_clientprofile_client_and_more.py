# Generated by Django 4.2.17 on 2024-12-26 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_client_user_permissions'),
        ('profile_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(default='+20', max_length=5)),
                ('captain', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_app_profile', to='accounts.captain')),
                ('client', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_app_profile', to='accounts.client')),
            ],
        ),
        migrations.RemoveField(
            model_name='clientprofile',
            name='client',
        ),
        migrations.DeleteModel(
            name='CaptainProfile',
        ),
        migrations.DeleteModel(
            name='ClientProfile',
        ),
    ]
