from dao.products_dao import ProductDAO
from dao.orders_dao import OrderDAO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dao.products_dao import ProductDAO


#string_con = f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine("postgresql://postgres:lasnessk@localhost:5433/elecronic_equipment_store1")
session = Session(engine)



def show_products():
    product_dao = ProductDAO(session)
    products = product_dao.get_all_products()

    for product in products:
        print(f'\nID товара: {product.product_id}')
        print(f'Название: {product.name}')
        print(f'Описание: {product.description}')
        print(f'Цена: {product.price}')
        print(f'Количество: {product.quantity}')
        print(f'Категория: {product.category.name}')
        print(f'Бренд: {product.brand.name}, {product.brand.country}')
        print(f'Добавлен: {product.created_at}')
        print('------------------------')

def show_orders():
    order_dao = OrderDAO(session)
    orders = order_dao.get_all_orders()
    for order in orders:
        print(f'\nID заказа: {order.order_id}')
        print(f'Клиент (Имя, email): {order.customer.first_name}, {order.customer.email}')
        print(f'Дата заказа: {order.order_date}')
        print(f'Сумма: {order.total_amount}')
        print(f'Адрес: {order.address}')
        print(f'Ожидаемая дата доставки: {order.expected_delivery}')
        print(f'Фактическая дата доставки: {order.actual_delivery}')
        print(f'Статус: {order.status.status}')
        print(f'Метод оплаты: {order.payment_method.method_name}')
        print('------------------------')


def add_product():
    from rich.table import Table
    from rich.console import Console
    from models.brand import Brand
    from models.category import Category

    console = Console()


    def show_brands():
        brands = session.query(Brand).all()
        table = Table(title="Список брендов")
        table.add_column("ID", style="cyan")
        table.add_column("Название", style="green")
        table.add_column("Страна", style="magenta")
        for brand in brands:
            table.add_row(str(brand.brand_id), brand.name, brand.country)
        console.print(table)

    def show_categories():
        categories = session.query(Category).all()
        table = Table(title="Список категорий")
        table.add_column("ID", style="cyan")
        table.add_column("Название", style="green")
        for category in categories:
            table.add_row(str(category.category_id), category.name)
            console.print(table)



    print('Справочник:')
    show_categories()
    print('\n')
    show_brands()

    product_dao = ProductDAO(session)
    new_product = product_dao.create_product(
        name=input('Введите название: '),
        description=input('Введите описание: '),
        price=float(input('Введите цену: ')),
        quantity=int(input('Введите количество: ')),
        category_id=int(input('Введите ID категории: ')),
        brand_id=int(input(f'Введите ID бренда: '))

    )

def add_menu():
    while True:
        print("\nЧто хотите добавить?")
        print('1. Товар')
        print('2. Заказ')
        print('3. Пользователя')
        print('4. Бренд')
        print('5. Категорию')
        print('0. Выход\n')

        choice = int(input('Введите: '))

        if choice == 1:
            add_product()
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 0:
            break


def main_menu():
    try:
        while True:
            print("\n===Главное меню===")
            print("1. Показать товары")
            print("2. Просмотр текущих заказов")
            print("3. Добавить...")
            print("0. Выход\n")

            choice = input("Выберите: ")

            if choice == "1":
                show_products()
            elif choice == "2":
                show_orders()
            elif choice == "3":
                add_menu()
            elif choice == "4":
                SystemFacade.list_records()
            elif choice == "0":
                break
    finally:
        print('сессия завершена')



if __name__ == "__main__":
    main_menu()

