#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.sql import func, session

Base = declarative_base()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs')


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies')

    @classmethod
    def oldest_company(cls, session):
        oldest_company = session.query(cls).order_by(cls.founding_year).first()
        return oldest_company

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    dev = relationship('Dev', back_populates='freebies')

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def give_away(self, new_dev):
        if self.dev == new_dev:
            self.dev = new_dev
            session.commit()

