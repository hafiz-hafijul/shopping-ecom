# Generated by Django 3.1.7 on 2021-06-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('L', 'Laptop'), ('TW', 'TopWears'), ('BM', 'Bottomwears')], max_length=50),
        ),
    ]
