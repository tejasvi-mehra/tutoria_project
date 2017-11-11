from tutoria.models import Tutor, Student, Session, Transaction, AdminWallet
import datetime

def moneyTransfer(amount, username):
    admin = AdminWallet.objects.get(username = "admin")
    admin.amount = float(admin.amount) - float(amount)
    admin.save()
    tutor = Tutor.objects.get(username=username)
    tutor.balance= float(tutor.balance) + float(amount)
    tutor.save()

def start():
    tdy = datetime.datetime.today()
    transactions = Transaction.objects.filter(completed=False,end_time__lte=tdy)
    for transaction in transactions:
         transaction.completed=True
         transaction.save()
         moneyTransfer(transaction.amount, transaction.tutor.username)

def clear_history():
    thirty_days = datetime.datetime.today()-datetime.timedelta(days=30)
    Transaction.objects.filter(end_time__lte=thirty_days).delete()
    Session.objects.filter(end_time__lte=thirty_days).delete()
# get_all_transactions()
