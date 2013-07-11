# -*- coding: UTF-8 -*-

from flask.ext.wtf import \
        Form, \
        IntegerField, \
        FloatField, \
        RadioField, \
        BooleanField, \
        TextAreaField, \
        validators


class SubmitForm(Form):
    """Model of submit form of MultiNest web service."""
    #:Domain size in X (integer field).
    xsize = IntegerField(
        'X', [
            validators.NumberRange(
                min=10, max=10000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=100,
    )
    #:Domain size in Y (integer field).
    ysize = IntegerField(
        'Y', [
            validators.NumberRange(
                min=10, max=10000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=100,
    )
    #:Minimum number of nodes to generate (integer field).
    nodes_min = IntegerField(
        'Min', [
            validators.NumberRange(
                min=1, max=1000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=10,
    )
    #:Maximum number of nodes to generate (integer field).
    nodes_max = IntegerField(
        'Max', [
            validators.NumberRange(
                min=1, max=1000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=10,
    )
    #:Minimum sigma of a node (float field).
    sigma_min = FloatField(
        'Min', [
            validators.NumberRange(
                min=1, max=100,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=1,
    )
    #:Maximum sigma of a node (float field).
    sigma_max = FloatField(
        'Max', [
            validators.NumberRange(
                min=1, max=100,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=6,
    )
    #:Has user requested to use predefined data set (bool field)?
    use_sets = BooleanField(u'Użyj predefiniowanego zestawu zamiast przypadku losowego', default = False)
    #:Predefined data sets (radio field).
    sets = RadioField('Sets',
                      choices=[
                          ('set_x1',u'1 Maksimum'),
                          ('set_x10',u'10 Maksimów'),
                          ('set_x100',u'100 Maksimów'),
                          ('user_set',u'Maksima zdefiniowane przez użytkownika'),
                      ],
                      default = 'set_x1'
                      )
    #:User set (text field)
    user_set = TextAreaField(u'')
    #:Number of live points for MultiNest to use (integer field).
    n_live_points = IntegerField(
        'Live Points', [
            validators.NumberRange(
                min=10, max=100000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=1000,
    )
    #:Maximum number of modes to search for (integer field).
    max_modes = IntegerField(
        'Max Modes', [
            validators.NumberRange(
                min=1, max=1000,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=100,
    )
    #:MultiNest sampling efficiency (float field)
    sampling_efficiency = FloatField(
        'Sampling Efficiency', [
            validators.NumberRange(
                min=0, max=1,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=0.8,
    )
    #:MultiNest evidence tolerance (float field)
    evidence_tolerance = FloatField(
        'Evidence Tolerance', [
            validators.NumberRange(
                min=0, max=1,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=0.5,
    )
