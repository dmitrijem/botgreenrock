from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, create_engine, func, text, JSON, Text, select
import main

DATABASE_URL = "sqlite:///use.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    user_id = Column(Integer, unique=True, nullable=False) 
    firstname = Column(String, nullable=True)
    username = Column(String, nullable=True)
    status = Column(String, nullable=False)
    inn = Column(String, nullable=True)
    name = Column(String, nullable=True)
    money = Column(Integer, nullable=False)
    costs_on_birge = Column(Integer)
    crypto_on_birge = Column(Integer)
class oper(Base):
    __tablename__ = 'operations'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    user_id = Column(Integer, nullable=False)
    inn_from = Column(String)
    operation = Column(String)
    payme = Column(Integer)
    one_cost = Column(Integer, nullable=True)
    costs = Column(Integer)
    inn_to = Column(String)
    status = Column(String, nullable=True)
class birge(Base):
    __tablename__ = 'birge'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String)
    user_id = Column(Integer, nullable=False)
    inn_from = Column(String)
    payme = Column(Integer)
    one_cost = Column(Integer, nullable=True)
    costs = Column(Integer)
    type = Column(String)
class costs(Base):
    __tablename__ = 'costs'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True,  nullable=True)
    invest_name = Column(String)
    have_cost = Column(Text)
class crypto(Base):
    __tablename__ = 'crypto'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True,  nullable=True)
    invest_name = Column(String)
    have_crypto = Column(Text)
class orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, unique=True,  nullable=False)
    user_id = Column(Integer)
    invest_name = Column(String)
    cost_company_name = Column(String)
    money_one_cost = Column(Integer)
    num_cost = Column(Integer)
    st_order = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
def get_logi_one_costs() -> str:
    with SessionLocal() as session:
        id = session.query(oper).order_by(oper.id.desc()).first()
        if id:
            return (f"{id.one_cost}")
        else:
            return None
def get_last_costs() -> str:
    with SessionLocal() as session:
        return session.query(birge).filter(birge.type == "cost").all()
def get_last_crypto() -> str:
    with SessionLocal() as session:
        return session.query(birge).filter(birge.type == "crypto").all()
def get_logi_costs() -> str:
    with SessionLocal() as session:
        id = session.query(oper).order_by(oper.id.desc()).first()
        if id:
            return (f"{id.costs}")
        else:
            return None
def get_birge_inn() -> str:
    with SessionLocal() as session:
        id = session.query(birge).order_by(birge.id.desc()).first()
        if id:
            return (f"{id.inn_from}")
        else:
            return None
def get_all_stocks() -> str:
    with SessionLocal() as session:
        stocks = session.query(birge).all()
        return stocks
def get_birge_one_costs() -> str:
    with SessionLocal() as session:
        id = session.query(birge).order_by(birge.id.desc()).first()
        if id:
            return (f"{id.one_cost}")
        else:
            return None
def get_birge_costs() -> str:
    with SessionLocal() as session:
        id = session.query(birge).order_by(birge.id.desc()).first()
        if id:
            return (f"{id.costs}")
        else:
            return None
def user_exist(user_id: int) -> bool:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user is not None
def get_user_status(user_id: int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.status}")
        else:
            return None
def get_user_payme(user_id: int) -> str:
    with SessionLocal() as session:
        id = session.query(oper).order_by(oper.id.desc()).first()
        if id:
            return (f"{id.payme}")
        else:
            return None
def get_user_logi_id():
    with SessionLocal() as session:
        id = session.query(oper).order_by(oper.id.desc()).first()
        if id:
            return (f"{id.user_id}")
        else:
            return None
def get_inn_log(user_id: int) -> str:
    with SessionLocal() as session:
        id = session.query(oper).order_by(oper.id.desc()).first()
        if id:
            return (f"{id.inn_to}")
        else:
            return None
def get_user_money(user_id: int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.money}")
        else:
            return None
def get_username(user_id: int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.username}")
        else:
            return None
def get_user_inn(user_id:int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.inn}")
        else:
            return None
def get_user_name(user_id:int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.name}")
        else:
            return None
def get_user_first(user_id:int) -> str:
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return (f"{user.firstname}")
        else:
            return None



