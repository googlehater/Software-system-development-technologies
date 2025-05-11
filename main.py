import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dao.brand_dao import BrandDAO
from sqlalchemy import text
import sys
sys.stderr = open("error_log.txt", "w", encoding="utf-8")


load_dotenv()

string_con = f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine("postgresql://postgres:lasnessk@localhost:5433/elecronic_equipment_store1")

session = Session(engine)



# brand_dao = BrandDAO(session)

# usa_brands = brand_dao.find_by_country("USA")
# if usa_brands:
#     for brand in usa_brands:
#         print(brand.name, brand.country)
# else:
#     print('no brands found')
    