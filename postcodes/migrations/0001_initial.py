import re

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Postcode',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, validators=[django.core.validators.RegexValidator(re.compile('^[ABCEGHJKLMNPRSTVXY]\\d[ABCEGHJKLMNPRSTVWXYZ]\\d[ABCEGHJKLMNPRSTVWXYZ]\\d$', 32))], serialize=False)),
                ('centroid', django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326, null=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('province', models.CharField(max_length=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostcodeConcordance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('boundary', models.TextField()),
                ('source', models.CharField(help_text='A description of the data source.', max_length=30)),
                ('code', models.ForeignKey(on_delete=models.CASCADE, to='postcodes.Postcode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='postcodeconcordance',
            unique_together={('code', 'boundary')},
        ),
    ]
