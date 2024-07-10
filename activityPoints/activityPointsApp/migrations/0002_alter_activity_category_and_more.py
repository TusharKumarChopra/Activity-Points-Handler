# Generated by Django 5.0.6 on 2024-07-10 11:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activityPointsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.ForeignKey(default='Social Work', on_delete=django.db.models.deletion.CASCADE, to='activityPointsApp.activitycategory'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date_completed',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date_started',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('activity_link', models.URLField(blank=True, null=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activityPointsApp.teacher')),
            ],
        ),
    ]
