from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('terms', models.BooleanField(default=1)),
                ('terms', models.BooleanField(default=0)),
                ('agreement', models.BooleanField(default=0)),
                ('invitation_code', models.CharField(max_length=15)),
                ('point', models.IntegerField(default=0)),
                ('postal_code', models.CharField(max_length=20, null=True)),
                ('road_address', models.CharField(max_length=100, null=True)),
                ('detail_address', models.CharField(max_length=100, null=True)),
                ('discount', models.IntegerField(default=1)),
                ('mobile_agreement', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=30)),
                ('auth_number', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'authentications',
            },
        ),
        migrations.CreateModel(
            name='PointImageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'point_image_lists',
            },
        ),
        migrations.CreateModel(
            name='PointProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.CharField(max_length=45)),
                ('hashtag', models.CharField(max_length=45)),
                ('image_url', models.URLField(max_length=2000)),
                ('detail', models.TextField()),
                ('brand', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'point_products',
            },
        ),
        migrations.CreateModel(
            name='Recommender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Account')),
            ],
            options={
                'db_table': 'recommenders',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Account')),
            ],
            options={
                'db_table': 'prescriptions',
            },
        ),
    ]
