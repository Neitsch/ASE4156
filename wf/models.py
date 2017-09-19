from django.db import models


class DailyInteractions(models.Model):
    masked_id = models.IntegerField()
    Date = models.DateField()
    Des1 = models.CharField(max_length=255)
    Des2 = models.CharField(max_length=255)
    Des3 = models.CharField(max_length=255)


class DailyCreditCard(models.Model):
    masked_id = models.IntegerField()
    Date = models.DateField()
    Des1 = models.CharField(max_length=255)
    Des2 = models.CharField(max_length=255)
    Des3 = models.CharField(max_length=255)
    Payment = models.IntegerField()  # Base data only has ints


class DailyWebsiteTraffic(models.Model):
    masked_id = models.IntegerField()
    Date = models.DateField()
    wf_page = models.CharField(max_length=255)


class MonthEndBalances(models.Model):
    masked_id = models.IntegerField()
    asof_yyyymm = models.DateField()
    age = models.IntegerField()
    tenure_altered = models.DecimalField(max_digits=16, decimal_places=2)
    checking_acct_ct = models.IntegerField()
    savings_acct_ct = models.IntegerField()
    mortgage_flag = models.BooleanField()
    heloc_flag = models.BooleanField()
    personal_loan_flag = models.BooleanField()
    cc_flag = models.BooleanField()
    prot_acct_flag = models.BooleanField()
    check_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    sav_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    mortgage_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    heloc_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    personal_loan_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    atm_withdrawls_cnt = models.IntegerField()
    atm_deposits_cnt = models.IntegerField()
    branch_visit_cnt = models.IntegerField()
    phone_banker_cnt = models.IntegerField()
    mobile_bank_cnt = models.IntegerField()
    online_bank_cnt = models.IntegerField()
    direct_mail_cnt = models.IntegerField()
    direct_email_cnt = models.IntegerField()
    direct_phone_cnt = models.IntegerField()
