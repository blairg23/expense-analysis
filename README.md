#Expensive API 
#### Your Personal Expense Analysis Django RESTful API

###Accounting Notes
Different providers may choose to use positive or negative values to symbolize debits or credits. There is very little rhyme or reason to what may be chosen at times. For example, Chase credit card statements show a negative value for debits (charges) and a positive value for credits (payments).

In addition to the idiosyncrasies of the financial providers, there is the normal confusing nomenclature of the accounting world, which is considered "well known" by those that deal with finances on a daily basis.

For example, different types of transaction statements have different semantics surrounding debits and credits:   
 
####Credit Cards
    debit = expense, causes balance to increase
    credit = payment, causes balance to decrease 

####Debit Cards / Bank Statements
    debit = income, causes balance to increase
    credit = charge, causes balance to decrease