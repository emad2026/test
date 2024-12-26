# Generated by Django 4.2.17 on 2024-12-26 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_client_user_permissions'),
        ('profile_app', '0002_profile_remove_clientprofile_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='captain',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_app_captain_profile', to='accounts.captain'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='client',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_app_client_profile', to='accounts.client'),
        ),
    ]
