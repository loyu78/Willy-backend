# Generated by Django 3.0.6 on 2020-05-19 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20200519_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'order_status',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]