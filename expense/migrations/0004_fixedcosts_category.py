# Generated by Django 3.2.3 on 2021-05-20 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_auto_20210519_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixedcosts',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.fixedcostsourcecategory'),
        ),
    ]