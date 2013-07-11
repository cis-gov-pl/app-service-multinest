# -*- coding: UTF-8 -*-

from flask.ext.wtf import Form, IntegerField, FloatField, validators


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
    #:Minimum sigma of a node (integer field).
    sigma_min = FloatField(
        'Min', [
            validators.NumberRange(
                min=1, max=100,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=1,
    )
    #:Maximum sigma of a node (integer field).
    sigma_max = FloatField(
        'Max', [
            validators.NumberRange(
                min=1, max=100,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=6,
    )
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
    sampling_efficiency = FloatField(
        'Sampling Efficiency', [
            validators.NumberRange(
                min=0, max=1,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=0.8,
    )
    evidence_tolerance = FloatField(
        'Evidence Tolerance', [
            validators.NumberRange(
                min=0, max=1,
                message="Wymaga liczby zawartej w <%(min)s, %(max)s>"
            )
        ],
        default=0.5,
    )
