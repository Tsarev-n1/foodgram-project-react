# Generated by Django 4.1.3 on 2022-12-25 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_title_recipe_name_rename_title_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]
