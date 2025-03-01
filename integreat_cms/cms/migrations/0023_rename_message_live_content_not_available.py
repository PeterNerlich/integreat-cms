# Generated by Django 3.2.13 on 2022-05-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Renames the 'message_live_content_not_available' field to 'message_content_not_available'
    """

    dependencies = [
        ("cms", "0022_rename_media_directories"),
    ]

    operations = [
        migrations.RenameField(
            model_name="language",
            old_name="message_live_content_not_available",
            new_name="message_content_not_available",
        ),
        migrations.AlterField(
            model_name="language",
            name="message_content_not_available",
            field=models.CharField(
                default="This page does not exist in the selected language. It is however available in these languages:",
                help_text="This is shown to the user when a page is not available in their language.",
                max_length=250,
                verbose_name='"This page does not exist in the selected language. It is however available in these languages:" in this language',
            ),
        ),
    ]
