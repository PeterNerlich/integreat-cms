# Generated by Django 3.2.13 on 2022-05-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Support last week for monthly recurring events
    """

    dependencies = [
        ("cms", "0026_alter_poi_location_on_map"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recurrencerule",
            name="week_for_monthly",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "First week"),
                    (2, "Second week"),
                    (3, "Third week"),
                    (4, "Fourth week"),
                    (5, "Last week"),
                ],
                help_text="If the frequency is monthly, this field determines on which week of the month the event takes place",
                null=True,
                verbose_name="week",
            ),
        ),
    ]
