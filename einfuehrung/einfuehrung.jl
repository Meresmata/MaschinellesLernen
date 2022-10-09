using Pluto
using Dates: now, second

print("High Five")

rightNow = now()
if mod(second(rightNow), 2) == 1
    return 1
else
    return 0
end

integer_vector = [i for i in 0:100]
float_vector = float.(integer_vector)

my_dict = Dict('a'=> 5,
               4 => [1, 2, 4, 5]
              )
              
my_dict['a']
my_dict[4]

square_vector = [i^2 for i in 0:20]

counter = 0
while(second(now()) != 0)
    counter = counter + 1
    sleep(1)
end
print(counter)

function fib(i:: Integer)
    if i == 0
        return 0
    elseif  i == 1
        return 1
    else
        return fib(i - 1) + fib(i - 2)
    end
end

fib(6)

