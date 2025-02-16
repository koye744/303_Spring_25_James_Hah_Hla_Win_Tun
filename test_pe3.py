# this file contains tests for a file named "pe3.py" that must be located in the same dir as this test file
# run in terminal: pytest -v test_pe3.py
# 25 tests should pass, 2 should fail with "XFAIL"

import pytest, datetime
from pe3 import *

#parametrized tests for encode function
@pytest.mark.parametrize("in_text, shift, out_text",[("", 3, ""), 
	("a", 3, "d"),
	(''' I stand before you all today to speak on my assassination, without resentment or bitterness. Although what has occurred is so tragic, the reasoning behind these bold actions are valid. I, like many of you, am so appalled by what has happened, and it deeply saddens me to know the men that I once called my dearest friends have deceived me. They rushed me to the Capitol to be crowned, just to watch my wounds pour out blood. I feel betrayed. I feel hurt. I feel powerless.''', 3,''' l vwdqg ehiruh brx doo wrgdb wr vshdn rq pb dvvdvvlqdwlrq, zlwkrxw uhvhqwphqw ru elwwhuqhvv. dowkrxjk zkdw kdv rffxuuhg lv vr wudjlf, wkh uhdvrqlqj ehklqg wkhvh erog dfwlrqv duh ydolg. l, olnh pdqb ri brx, dp vr dssdoohg eb zkdw kdv kdsshqhg, dqg lw ghhsob vdgghqv ph wr nqrz wkh phq wkdw l rqfh fdoohg pb ghduhvw iulhqgv kdyh ghfhlyhg ph. wkhb uxvkhg ph wr wkh fdslwro wr eh furzqhg, mxvw wr zdwfk pb zrxqgv srxu rxw eorrg. l ihho ehwudbhg. l ihho kxuw. l ihho srzhuohvv.'''),
	("A", 3, "d"), ("XyZ", 3, "abc"), ("X!y.Z&", 3, "a!b.c&"),
	("Calmly we walk on this April day", 10, "mkvwvi go gkvu yx drsc kzbsv nki")])
def test_encode(in_text, shift, out_text):
	assert encode(in_text, shift)[1] == out_text

#parametrized tests for decode function
@pytest.mark.parametrize("in_text, shift, out_text",[("", 3, ""), 
	("d", 3, "a"),
	(''' l vwdqg ehiruh brx doo wrgdb wr vshdn rq pb dvvdvvlqdwlrq, zlwkrxw uhvhqwphqw ru elwwhuqhvv. dowkrxjk zkdw kdv rffxuuhg lv vr wudjlf, wkh uhdvrqlqj ehklqg wkhvh erog dfwlrqv duh ydolg. l, olnh pdqb ri brx, dp vr dssdoohg eb zkdw kdv kdsshqhg, dqg lw ghhsob vdgghqv ph wr nqrz wkh phq wkdw l rqfh fdoohg pb ghduhvw iulhqgv kdyh ghfhlyhg ph. wkhb uxvkhg ph wr wkh fdslwro wr eh furzqhg, mxvw wr zdwfk pb zrxqgv srxu rxw eorrg. l ihho ehwudbhg. l ihho kxuw. l ihho srzhuohvv.''', 3,
		''' i stand before you all today to speak on my assassination, without resentment or bitterness. although what has occurred is so tragic, the reasoning behind these bold actions are valid. i, like many of you, am so appalled by what has happened, and it deeply saddens me to know the men that i once called my dearest friends have deceived me. they rushed me to the capitol to be crowned, just to watch my wounds pour out blood. i feel betrayed. i feel hurt. i feel powerless.'''),
	("d", 3, "a"), ("abc", 3, "xyz"), ("a!b.c&", 3, "x!y.z&"),
	("mkvwvi go gkvu yx drsc kzbsv nki", 10, "calmly we walk on this april day")])
def test_decode(in_text, shift, out_text):
	assert decode(in_text, shift) == out_text

#run encode on empty string; must return tuple where first item is lowercase alphabet
def test_alphabet():
    assert encode("", 1)[0] == list(string.ascii_lowercase)

##
##  END ENCODE/DECODE TESTS : BEGIN BANKACCOUNT CLASS TESTS
##

#input output values for account with balance $500
input_output = (
    (20, 520),
    (30, 530),
    (-35, 500),
    (12, 512)
)

#parametrized fixture
@pytest.fixture(params=input_output)
def input_output_tuples(request):
    a = BankAccount()
    a.balance = 500
    return (a, request.param)

#test function utilizing parametrized fixture
@pytest.mark.bankaccount
def test_deposit_advanced(input_output_tuples):
    input_output_tuples[0].deposit(input_output_tuples[1][0])
    assert input_output_tuples[0].balance == input_output_tuples[1][1]


#fixture for creating Account objects
# creates a 3-item list that contains: [0]BankAccount instance, [1]CheckingAccount instance, and [2]SavingsAccount instance
@pytest.fixture()
def create_objects():
    a = BankAccount("X Abc", 1234, datetime.date.today(), 500)
    b = CheckingAccount("X Abc", 1234, datetime.date.today(), 500)
    c = SavingsAccount("X Abc", 1234, datetime.date.today(), 500)
    return [a, b, c]

#test savings overdraft; create_objects[2] is a savings account instance
@pytest.mark.savingsaccount
def test_savings_overdraft(create_objects):
    create_objects[2].balance = 750
    create_objects[2].withdraw(751)
    create_objects[2].creation_date = (1980, 1, 1)
    assert create_objects[2].balance == 750

#must have had savings account for 180 days to withdraw; create_objects[2] is a savings account instance
@pytest.mark.savingsaccount
def test_savings_withdraw_six_months(create_objects):
    create_objects[2].balance = 750
    create_objects[2].creation_date = datetime.date.today() - datetime.timedelta(days=178)
    create_objects[2].withdraw(200)
    assert create_objects[2].balance == 750

#parametrized tests for checking account withdrawal
@pytest.mark.parametrize("withdraw_amt, updated_balance",
                         [ (600, -130), 
                          (500, 0) ])
def test_checking_withdraw_p(withdraw_amt, updated_balance):
    c = CheckingAccount("X Abc", 1234, datetime.date.today(), balance=500)
    c.withdraw(withdraw_amt)
    assert c.balance == updated_balance

#parametrized tests for checking deposit
@pytest.mark.checkingaccount
@pytest.mark.parametrize("deposited_amount, updated_balance",
                            [
                            (20, 520),
                            pytest.param(-35, 465, marks=pytest.mark.xfail(reason="Negative $35 deposit must not succeed and yield balance of $465")),
                            pytest.param(10, 512, marks=pytest.mark.xfail(reason="Deposit of $10 on $500 balance must not give a balance of $512"))
                            ]
)
def test_deposit(deposited_amount, updated_balance):
    c = CheckingAccount("X Abc", 1234, datetime.date.today(), 500)
    c.deposit(deposited_amount)
    assert c.balance == updated_balance

@pytest.mark.bankaccount
def test_future_date(create_objects):
    with pytest.raises(Exception):
        a = BankAccount("X Abc", 1234, datetime.date.today() + datetime.timedelta(days=2), 500)
