# DroneSimulator

auto robots course second assignment
## ex1
<h6>submitters</h6>
<p>name:liav levi ID:206603193</p>
<p>name:oria tzadok ID:315500157</p>
<p>name:sagi yosef azulai ID:207544230</p>

## HOW TO RUN
<p> first thing to do for this assignment running and checking: </p>


~~~
pip install -r requirements.txt 
~~~

<p> if you are using windows you may need to install with --user flag like this:</p>

~~~
pip install -r requirements.txt --user
~~~

<p> to run the assignment</p>

~~~
python main.py <map_image_path>
~~~

<p> to run the tests(we disable warning as we use old version of pandas and numpy)</p>

~~~
pytest --disable-warnings
python -m Tests.TestDroneSimulatorTest


~~~