# Generated by Django 2.0.3 on 2018-05-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_remove_userprofile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='crm.Tag'),
        ),
    ]
