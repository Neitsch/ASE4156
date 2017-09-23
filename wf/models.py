"""
All the models to represent a row in the respective CSV file
"""
from django.db import models


class DailyInteractions(models.Model):
    """
    Daily interactions with WF
    """
    # Customer Identifier
    masked_id = models.IntegerField()
    # Date (month|day|year)
    Date = models.DateField()
    # General category of interaction
    Des1 = models.CharField(max_length=255)
    # More detailed category of interaction
    Des2 = models.CharField(max_length=255)
    # Most detailed description of interaction
    Des3 = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}".format(self.id,
                                               self.masked_id,
                                               self.Date,
                                               self.Des1,
                                               self.Des2,
                                               self.Des3)


class DailyCreditCard(models.Model):
    """
    Daily use of WF credit card
    """
    # Customer Identifier
    masked_id = models.IntegerField()
    # Date (month|day|year)
    Date = models.DateField()
    # General category of credit card purchase
    Des1 = models.CharField(max_length=255)
    # More detailed category of credit card purchase
    Des2 = models.CharField(max_length=255)
    # Most detailed description of credit card purchase
    Des3 = models.CharField(max_length=255)
    # Dollar amount of purchase
    Payment = models.IntegerField()  # Base data only has ints

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.id,
                                                   self.masked_id,
                                                   self.Date,
                                                   self.Des1,
                                                   self.Des2,
                                                   self.Des3,
                                                   self.Payment)


class DailyWebsiteTraffic(models.Model):
    """
    Daily WellsFargo.com traffic
    """
    # Customer Identifier
    masked_id = models.IntegerField()
    # Date (month|day|year)
    Date = models.DateField()
    # wellsfargo.com URL
    wf_page = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}, {}".format(self.id,
                                   self.masked_id,
                                   self.wf_page)


class MonthEndBalances(models.Model):
    """
    Month end balances
    """
    # Customer Identifier
    masked_id = models.IntegerField()
    # Date (year and month)
    asof_yyyymm = models.DateField()
    # customer age
    age = models.IntegerField()
    # customer tenure with WF
    tenure_altered = models.DecimalField(max_digits=16, decimal_places=2)
    # number of checking accounts with WF
    checking_acct_ct = models.IntegerField()
    # number of savings accounts with WF
    savings_acct_ct = models.IntegerField()
    # customer has mortgage with WF
    mortgage_flag = models.BooleanField()
    # customer has HELOC with WF
    heloc_flag = models.BooleanField()
    # customer has personal loan with WF
    personal_loan_flag = models.BooleanField()
    # customer has a credit card with WF
    cc_flag = models.BooleanField()
    # customer has a property or auto insurance with WF
    prot_acct_flag = models.BooleanField()
    # month end balance in checking accounts
    check_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    # month end balance in saving accounts
    sav_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    # month end balance remaining on mortgage
    mortgage_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    # month end balance outstanding in HELOC
    heloc_bal_altered = models.DecimalField(max_digits=16, decimal_places=2)
    # month end balance outstanding in personal loan
    personal_loan_bal_altered = models.DecimalField(
        max_digits=16,
        decimal_places=2
    )
    # number of ATM withdrawals over the month
    atm_withdrawls_cnt = models.IntegerField()
    # number of ATM deposits over the month
    atm_deposits_cnt = models.IntegerField()
    # number of visits to a branch over the month
    branch_visit_cnt = models.IntegerField()
    # number of phone calls into WF over the month
    phone_banker_cnt = models.IntegerField()
    # number of mobile bank transactions over the month
    mobile_bank_cnt = models.IntegerField()
    # number of online bank transactions over the month
    online_bank_cnt = models.IntegerField()
    # number of pieces of direct mail  sent from WF
    # to the customer over the month
    direct_mail_cnt = models.IntegerField()
    # number of pieces of email  sent from WF to the customer  over the month
    direct_email_cnt = models.IntegerField()
    # number of times the customer called WF over the month
    direct_phone_cnt = models.IntegerField()

    class Meta(object):
        unique_together = ('masked_id', 'asof_yyyymm',)

    def __str__(self):
        return "{}, {}, {}".format(self.id,
                                   self.masked_id,
                                   self.asof_yyyymm)
