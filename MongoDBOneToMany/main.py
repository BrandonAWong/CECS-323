from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Utilities import Utilities
from Order import Order
from Product import Product
from PriceHistory import PriceHistory
from OrderItem import OrderItem
from StatusChange import StatusChange
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from mongoengine.errors import OperationError
from Menu import Menu
from Option import Option
from menu_definitions import menu_main
from decimal import Decimal, InvalidOperation

"""
This protects Order from deletions in OrderItem of any of the objects reference by Order
in its order_items list.  We could not include this in Order itself since that would 
make a cyclic delete_rule between Order and OrderItem.  I've commented this out because
it makes it impossible to remove OrderItem instances.  But you get the idea how it works."""
# OrderItem.register_delete_rule(Order, 'orderItems', mongoengine.DENY)

def select_order() -> Order:
    return select_general(Order)


def select_order_item() -> OrderItem:
    return select_general(OrderItem)


def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')


def add_order():
    """
    Create a new Order instance.
    :return: None
    """
    success: bool = False
    new_order = None
    while not success:
        order_date = prompt_for_date('Date and time of the order: ')
        """This is sort of a hack.  The customer really should come from a Customer class, and the 
        clerk who made the sale, but I'm trying to keep this simple to concentrate on relationships."""
        new_order = Order(input('Customer name --> '),
                          order_date,
                          input('Clerk who made the sale --> '))
        violated_constraints = unique_general(new_order)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            success = True
            # The first "stats change" is placing the order itself.
            new_order.change_status(StatusChange(
                prompt_for_enum('Select the status:', StatusChange, 'status'),
                order_date))
    new_order.save()


def add_order_item():
    """
    Add an item to an existing order.
    :return: None
    """
    success: bool = False
    new_order_item: OrderItem
    order: Order
    while not success:
        order = select_order()
        new_order_item = OrderItem(order,
                                   select_product(),
                                   int(input('Quantity --> ')))
        # Make sure that this adheres to the existing uniqueness constraints.
        violated_constraints = unique_general(new_order_item)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            success = True
    # we cannot add the OrderItem to the Order until it's been stored in the database.
    new_order_item.save()
    order.add_item(new_order_item)  # Add this OrderItem to the Order's MongoDB list of items.
    order.save()  # Update the order in the database.


def update_order():
    """
    Change the status of an existing order by adding another element to the status vector of the order.
    :return: None
    """
    success: bool = False
    # "Declare" the order variable, more for cosmetics than anything else.
    order: Order
    while not success:
        order = select_order()  # Find an order to modify.
        status_change_date = prompt_for_date('Date and time of the price change: ')
        new_status = prompt_for_enum('Select the status:', StatusChange, 'status')
        try:
            order.change_status(StatusChange(new_status, status_change_date))
            order.save()
            success = True
        except ValueError as VE:
            print('Attempted price change failed because:')
            print(VE)


def delete_order():
    """
    Delete an existing order from the database.
    :return: None
    """
    order = select_order()  # prompt the user for an order to delete
    items = order.orderItems  # retrieve the list of items in this order
    for item in items:
        """The reference from OrderItem back up to Order has a reverse_delete_rule of DENY, which 
        is similar to the RESTRICT option on a relational foreign key constraint.  Which means that
        if I try to delete the order and there are still any OrderItems depending on that order,
        MongoEngine (not MongoDB) will throw an exception."""
        item.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    try:
        order.delete()
    except OperationError:
        print("Unable to delete order. Order items are still related to order.")


def delete_order_item():
    """
    Remove just one item from an existing order.
    :return: None
    """
    order = select_order()  # prompt the user for an order to update
    items = order.orderItems  # retrieve the list of items in this order
    menu_items: list[Option] = []  # list of order items to choose from
    # Create an ad hoc menu of all of the items presently on the order.  Use __str__ to make a text version of each item
    for item in items:
        menu_items.append(Option(item.__str__(), item))
    # prompt the user for which one of those order items to remove, and remove it.
    item = (Menu('Item Menu',
                 'Choose which order item to remove', menu_items).menu_prompt())
    item.delete()
    order.remove_item(item)
    # Update the order to no longer include that order item in its MongoDB list of order items.
    order.save()


def list_order():
    print(select_order())


def add_product():
    while True:
        try:
            product = Product(
                input("Product Code --> "),
                input("Product Name --> "),
                input("Product Description --> "),
                int(input("Quantity In Stock --> ")),
                round(Decimal(input("Buy Price --> ")), 2),
                round(Decimal(input("MSRP --> ")), 2)
            )
        except (ValueError, InvalidOperation):
            print("Invalid input.  Try again.")
            continue

        violated_constraints = unique_general(product)
        if violated_constraints:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
            continue
        break
    product.save()


def delete_product():
    try:
        select_product().delete()
    except OperationError:
        print("Product cannot be deleted, is present in order(s). Delete them first.")


def select_product():
    return select_general(Product)


def update_product():
    while True:
        product = select_product()
        try:
            product.change_price(PriceHistory(round(Decimal(input("New Price --> ")), 2),
                                               prompt_for_date("Date and time of the status change: ")))
            product.save()
            break
        except (ValueError, InvalidOperation) as e:
            print(f'Attempted status change failed because:\n{e}')


if __name__ == "__main__":
    print("Starting in main.")
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    menu: Menu = menu_main.menu_prompt()
    action: str = ""
    while action != "pass":
        action = menu.menu_prompt()
        if action == "back":
            menu = menu_main.menu_prompt()
            continue
        print(f"next action: {action}")
        exec(action)
    log.info("All done for now.")
