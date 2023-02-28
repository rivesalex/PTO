# PTO
A project aiming at figuring out what are the best days to take PTO provided specific inputs.

Motivation: Sometimes we are given days off, and often times we try to maximize the number of consecutive days we have off. For example: It is preferable for many people, given just one day off, they would likely take that day off on Monday or Friday. 

Given an amount of days, in integers, how can we maximize the amount of consecutive days we can take off in a year. 

Inputs:
  pto_days (required) : the number of pto days that will be taken off. Program will work without it.
  start_date: the start date in 'YYYY-MM-DD format', it is optional and will be bypassed by pressing enter. In this case, the current day will be used,
    and the end date will be a year later.
  end_date: end date of the program, if a start_date in placed, an end date is required. 

Required modules:
datetime and numpy.
