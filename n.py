from dao.products_dao import ProductDAO
from dao.orders_dao import OrderDAO
from sqlalchemy import create_engine
from sqlalchemy.orm import Session 
from dao.products_dao import ProductDAO
from patterns.strategy.strategy import CardPayment, CashByDelivery, InstallmentPlanPayment


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

    # Реализовать показ только что созданного товара (мб + отмену действия)

def add_order(): # доделать
    # тут будет использован паттерн фасад
    from patterns.facade.facade import OrderFacade
    from models.customers import Customer
    from models.product import Product
    from rich.table import Table
    from rich.console import Console



    customers = session.query(Customer).all()
    console = Console()
    table = Table(title='Список клиентов: ')
    table.add_column('ID', style='cyan')
    table.add_column('Имя')
    table.add_column('Фамилия')
    table.add_column('email: ', style='green')
    table.add_column('phone: ', style='magenta')
    for customer in customers:
        table.add_row(
            str(customer.customer_id), 
            customer.first_name, 
            customer.last_name, 
            customer.email, 
            customer.phone
            )
    console.print(table)


    products = session.query(Product).all()
    table = Table(title='Доступные товары')
    table.add_column('ID', style='cyan')
    table.add_column('Название')
    table.add_column('Цена')
    for product in products:
        table.add_row(
            str(product.product_id),
            product.name,
            str(product.price)
        )
    console.print(table)

    customer_id1 = int(input('Введите ID клиента: '))
    print(f'Введите ID товара или 0 для завершения: ')
    product_ids = []
    while True:
        choice = int(input())
        if choice == 0:
            break

        product_ids.append(choice)

    address = input('Введите адрес доставки: ')
    
    facade = OrderFacade(session)

    facade.place_order(
        customer_id=customer_id1,
        product_ids=product_ids,
        address=address
    )
    print('good')



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
            add_order()
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 0:
            break

def pay_order():
    from rich.table import Table
    from rich.console import Console
    from rich.prompt import Prompt 
    from dao.orders_dao import OrderDAO
    from models.customers import Customer
    from models.order import Order
    from patterns.observer.observer import EmailNotification, SMSNotification


    console = Console()
    order_dao = OrderDAO(session)
    orders = order_dao.get_all_orders()

    def show_orders():
        '''Показывает заказы, доступные для оплаты'''

        orders = session.query(Order).filter(Order.status_id != 3).all()
        table = Table(title="Orders")
        table.add_column("ID заказа", style="cyan")
        table.add_column(f"Клиент: ")
        table.add_column("Дата заказа: ")
        table.add_column("Сумма: ")
        table.add_column("Статус: ")
        table.add_column("Метод оплаты: ")
        for order in orders:
            table.add_row(
                str(order.order_id),
                f'{order.customer.first_name}, {order.customer.last_name}\n{order.customer.email}',
                order.order_date.strftime("%d.%m.%Y"),
                f'{order.total_amount:.2f}',
                order.status.status,
                order.payment_method.method_name
            )
        console.print(table)
        return orders
    
    
        

    payable_orders = show_orders()
    print(f'\nДоступные заказы:\n')
    
    order_id = Prompt.ask(
        '[bold]Введите ID заказа, который хотите оплатить[/bold]',
        choices=[str(o.order_id) for o in payable_orders]
    )
    order = next(o for o in payable_orders if o.order_id == int(order_id))

    print('Выберите метод оплаты:')
    print('1. card\n2. cash\n3. InstallPayment\n')
    payment_method = int(input('Ввод: '))

    if payment_method == 1:
        order.set_payment_strategy(CardPayment())
    elif payment_method == 2:
        order.set_payment_strategy(CashByDelivery())
    elif payment_method == 3:
        order.set_payment_strategy(InstallmentPlanPayment())
    else: 
       print(f'некорректно выбран метод. По умолчанию будет использоваться Card')

    '''Observer'''
    # создаем наблюдателей
    email_notifier = EmailNotification()
    sms_notifier = SMSNotification()

    # подписываем наблюдателей
    order.attach(email_notifier)
    order.attach(sms_notifier)


    # Подтверждение
    confirm = Prompt.ask(
        f"Оплатить заказ #{order_id} на сумму {order.total_amount:.2f}?",
        choices=["y", "n"],
        default="n"
    )

    if confirm == 'y':
        order.next_status(session)
        console.print(f'\n[green]Заказ №{order_id} успешно оплачен[/green]\n')
    else:
        console.print(f'[red]Операция отменена![/red]')

def main_menu():
    try:
        while True:
            print("\n===Главное меню===")
            print("1. Показать товары")
            print("2. Просмотр текущих заказов")
            print("3. Оплатить заказ")
            print("4. Добавить...")
            print("0. Выход\n")

            choice = input("Выберите: ")

            if choice == "1":
                show_products()
            elif choice == "2":
                show_orders()
            elif choice == "3":
                pay_order()
            elif choice == "4":
                add_menu()
            elif choice == "0":
                break
    finally:
        print('сессия завершена')



if __name__ == "__main__":
    main_menu()

