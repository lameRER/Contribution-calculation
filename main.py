from calc import Calc

start_date = '01.01.23'
end_date = '31.08.23'

cl = Calc(start_date, end_date)
tax_type = cl.get_contribution()
res = {key: cl.calculation(value) for key, value in tax_type.items()}
res1 = [cl.get_to_quarter(key, value) for key, value in res.items()]
[print(*i, sep='\n') for i in res1]
print(*res.items(), sep='\n')
print('Итог:', sum(res.values()))