# Generated by Django 3.2.16 on 2023-10-22 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20231021_1830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('user',)},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('title',)},
        ),
    ]
