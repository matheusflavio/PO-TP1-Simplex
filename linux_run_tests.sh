mkdir outputs
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15
do
    time python3 main.py tests/$i > outputs/$i && diff outputs/$i expected_outputs/$i
done
rm -rf outputs