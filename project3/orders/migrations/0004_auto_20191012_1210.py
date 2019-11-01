# Generated by Django 2.2.5 on 2019-10-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20191012_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'addition',
                'verbose_name_plural': 'additions',
                'db_table': 'shop_addition',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='n_addition',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topping',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]