from tutoria.models import Tutor, Student, Session, Transaction, MyTutorsWallet, Wallet, Notification
import datetime
import time as ttime

def moneyTransfer(amount, username):
    admin = MyTutorsWallet.objects.get(username = "mytutors")
    admin.amount = float(admin.amount) - float(amount)
    admin.save()
    tutor = Tutor.objects.get(username=username)
    # tutor.balance= float(tutor.balance) + float(amount)
    # tutor.save()
    wallet = Wallet.objects.get(username=username)
    wallet.balance = float(wallet.balance) + float(amount)
    wallet.save()

def start():
    tdy = datetime.datetime.today()
    transactions = Transaction.objects.filter(completed=False,end_time__lte=tdy)
    for transaction in transactions:
         transaction.completed=True
         transaction.save()
         moneyTransfer(transaction.amount, transaction.tutor.username)
         notif=Notification(
                     title="Click to write a review for your session with {}".format(transaction.tutor),
                     forSession=False,
                     student=transaction.student,
                     now=int(ttime.time()),
                     date="{}/{}/{}".format(tdy.day,tdy.month,tdy.year),
                     time="{}:{}".format(tdy.hour,tdy.minute)
                     )
         notif.save()
         notif=Notification(
                     title="{} was paid by {} to you.".format(transaction.amount,transaction.student),
                     forSession=False,
                     tutor=transaction.tutor,
                     now=int(ttime.time()),
                     date="{}/{}/{}".format(tdy.day,tdy.month,tdy.year),
                     time="{}:{}".format(tdy.hour,tdy.minute)
                     )



def clear_history():
    thirty_days = datetime.datetime.today()-datetime.timedelta(days=30)
    Transaction.objects.filter(end_time__lte=thirty_days).delete()
    Session.objects.filter(end_time__lte=thirty_days).delete()
# get_all_transactions()
