from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:12345@localhost/npl_auction_system"
)