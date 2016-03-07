# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, types, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# base for declaring a mapping
BASE = declarative_base()


class Transcript(BASE):

    """Set of non-overlapping exons.

    A :class:`Transcript` can *only* be related to a single gene.

    Args:
        id (str): unique transcript id (e.g. CCDS)
        gene_id (str): related gene
        chromosome (str): related contig id
        lenght (int): number of exon bases in transcript
    """

    __tablename__ = 'transcript'

    id = Column(types.String(32), primary_key=True)
    gene_id = Column(types.String(32), index=True, nullable=False)
    chromosome = Column(types.String(10))
    length = Column(types.Integer)


class Sample(BASE):

    """Metadata for a single sample.

    Args:
        id (str): unique sample id
        group_id (str): unique group id
        source (str): path to coverage source Sambamba output/BAM file
        created_at (DateTime): date of addition to database
    """

    __tablename__ = 'sample'

    id = Column(types.String(32), primary_key=True)
    group_id = Column(types.String(32), index=True)
    source = Column(types.String(256))
    created_at = Column(types.DateTime, default=datetime.now)


class TranscriptStat(BASE):

    """Statistics on transcript level, related to sample and transcript.

    Args:
        sample_id (str): link to sample record
        sample (Sample): parent Sample record
        transcript_id (str): link to transcript record
        transcript (Transcript): parent transcript record
        mean_coverage (Float): mean coverage across all exons
        completeness_XX (Float): percentage of exon bases coverage at XX
        _incomplete_exons (str): comma separated list of exon ids
    """

    __tablename__ = 'transcript_stat'
    __table_args__ = (UniqueConstraint('sample_id', 'transcript_id',
                                       name='_sample_transcript_uc'),)

    id = Column(types.Integer, primary_key=True)
    sample_id = Column(types.String(32), ForeignKey('sample.id'),
                       nullable=False)
    sample = relationship(Sample, backref=backref('stats'))
    transcript_id = Column(types.String(32), ForeignKey('transcript.id'),
                           nullable=False)
    transcript = relationship(Transcript, backref=backref('stats'))
    mean_coverage = Column(types.Float, nullable=False)
    completeness_10 = Column(types.Float)
    completeness_15 = Column(types.Float)
    completeness_20 = Column(types.Float)
    completeness_50 = Column(types.Float)
    completeness_100 = Column(types.Float)

    threshold = Column(types.Integer)
    _incomplete_exons = Column(types.Text)

    @property
    def incomplete_exons(self):
        """Return a list of exons ids."""
        return self._incomplete_exons.split(',') if self._incomplete_exons else []

    @incomplete_exons.setter
    def incomplete_exons(self, value):
        self._incomplete_exons = ','.join(value)
